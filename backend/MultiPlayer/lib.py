from django.utils import timezone


class ChessGame:
    def __init__(self, room_id):
        self.room_id = room_id
        self.white_id = ""
        self.black_id = ""
        self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.white_time = 600
        self.black_time = 600
        self.turn = "white"
        self.start_time = timezone.now()

    def get_players_num(self):
        ans = 0
        if self.white_id != "":
            ans += 1
        if self.black_id != "":
            ans += 1
        return ans

    def set_player_color(self, player_id):
        if self.white_id == "":
            self.white_id = player_id
        elif self.black_id == "":
            self.black_id = player_id

    def get_game_info(self, player_id):
        return {
            "game_fen": self.FEN,
            "turn": self.turn,
            "white_time": self.white_time,
            "black_time": self.black_time,
            "personal_color": "white" if self.white_id == player_id else "black",
            "size": self.get_players_num(),
        }


class ChessGameCreator:
    games = {}

    @staticmethod
    def create(room_id) -> ChessGame:
        if room_id not in ChessGameCreator.games:
            ChessGameCreator.games[room_id] = ChessGame(room_id)
        return ChessGameCreator.games[room_id]

    def delete(room_id):
        del ChessGameCreator.games[room_id]
