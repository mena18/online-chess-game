# chat/consumers.py
import json

# from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer

active_rooms = {}


class Event:
    sender_channel_name = None
    body = None

    def __init__(self, d: dict):
        self.sender_channel_name = d["sender_channel_name"]
        self.body = d["body"]


class MultiPlayerGameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"MultiPlayerGame_{self.room_name}"

        if self.room_group_name not in active_rooms:
            active_rooms[self.room_group_name] = set()

        active_rooms[self.room_group_name].add(self.channel_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        size = len(active_rooms[self.room_group_name])
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "multi.game.connect",
                "body": {
                    "message": "User Entered The Chat",
                    "size": size,
                    "personal_color": "white" if size % 2 == 0 else "black",
                },
                "sender_channel_name": self.channel_name,
            },
        )

    async def disconnect(self, close_code):
        # Leave room group

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Remove the current user's channel from the group's set of active users
        if self.channel_name in active_rooms[self.room_group_name]:
            active_rooms[self.room_group_name].remove(self.channel_name)

        # If the group is empty, remove it from the dictionary
        if not active_rooms[self.room_group_name]:
            del active_rooms[self.room_group_name]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "multi.game.connect",
                "body": {
                    "message": "User Left The Chat",
                    "size": len(active_rooms.get(self.room_group_name, [])),
                    "personal_color": "",
                },
                "sender_channel_name": self.channel_name,
            },
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        type = text_data_json["type"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": type, "sender_channel_name": self.channel_name, "body": body},
        )

    # Receive message from room group

    async def multi_game_connect(self, event):

        event = Event(event)

        await self.send(
            text_data=json.dumps(
                {
                    "body": event.body["message"],
                    "type": "multi_game_connect",
                    "size": event.body["size"],
                    "yourself": event.sender_channel_name == self.channel_name,
                }
            )
        )

    async def multi_game_make_move(self, event):

        event = Event(event)
        if event.sender_channel_name != self.channel_name:
            await self.send(
                text_data=json.dumps(
                    {
                        "body": event.body,
                        "type": "multi_game_make_move",
                        "yourself": event.sender_channel_name == self.channel_name,
                    }
                )
            )

    async def multi_game_chat_message(self, event):
        event = Event(event)

        await self.send(
            text_data=json.dumps(
                {
                    "message": event.body,
                    "type": "multi_game_chat_message",
                    "owner": event.sender_channel_name == self.channel_name,
                }
            )
        )

    async def multi_game_over(self, event):
        event = Event(event)

        await self.send(
            text_data=json.dumps(
                {
                    "body": event.body,
                    "type": "multi_game_over",
                    "owner": event.sender_channel_name == self.channel_name,
                }
            )
        )
        # Send message to WebSocket
