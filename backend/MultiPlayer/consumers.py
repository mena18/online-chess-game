# chat/consumers.py
import json

# from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .lib import ChessGameCreator


class Event:
    sender_channel_name = None
    body = None

    def __init__(self, d: dict):
        self.sender_channel_name = d["sender_channel_name"]
        self.body = d["body"]


class MultiPlayerGameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]

        self.room_group_name = f"MultiPlayerGame_{self.room_name}"
        self.chessGame = ChessGameCreator.create(self.room_name)
        print("\n\n\n")
        print(self.chessGame.get_game_info(self.player_id)["game_fen"])
        print("\n\n\n")
        self.chessGame.set_player_color(self.player_id)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "player.joined",
                "body": {},
                "sender_channel_name": self.channel_name,
            },
        )

    async def disconnect(self, close_code):
        # Leave room group

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if self.player_id == self.chessGame.white_id:
            self.chessGame.white_id = ""
        elif self.player_id == self.chessGame.black_id:
            self.chessGame.black_id = ""

        if self.chessGame.get_players_num() == 0:
            ChessGameCreator.delete(self.room_name)
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "player.joined",
                "body": {
                    "message": "User Left The Chat",
                    "game_info": self.chessGame.get_game_info(self.player_id),
                },
                "sender_channel_name": self.channel_name,
            },
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        type = text_data_json["type"]

        if type == "multi.game.make.move":
            print("Before make move\n\n\n")
            print(self.chessGame.get_game_info(self.player_id)["game_fen"])
            print("\n\n\n")

            self.chessGame.FEN = body["fen"]
            self.chessGame.turn = body["turn"]
            self.chessGame.white_time = body["white_time"]
            self.chessGame.black_time = body["black_time"]

            body["game_info"] = self.chessGame.get_game_info(self.player_id)

            print("After make move\n\n\n")
            print(self.chessGame.get_game_info(self.player_id)["game_fen"])
            print("\n\n\n")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": type, "sender_channel_name": self.channel_name, "body": body},
        )

    # Receive message from room group

    async def player_joined(self, event):

        event = Event(event)

        await self.send(
            text_data=json.dumps(
                {
                    "body": self.chessGame.get_game_info(self.player_id),
                    "type": "player_joined",
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
