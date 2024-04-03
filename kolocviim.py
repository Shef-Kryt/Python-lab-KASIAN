from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from abc import ABC, abstractmethod
import sqlite3

conn = sqlite3.connect('results.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS matches
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   player1 TEXT,
                   player2 TEXT,
                   winner TEXT,
                   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

def save_match_result(player1, player2, winner):
    cursor.execute('''INSERT INTO matches (гравець1, гравець2, переможець) VALUES (?, ?, ?)''', (player1, player2, winner))
    conn.commit()

def close_db_connection():
    conn.close()

app = FastAPI()
game = None

class Piece(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def validate_move(self, start, end):
        pass

    @abstractmethod
    def make_move(self, start, end):
        pass

class Pawn(Piece):
    def validate_move(self, start, end):
        if start[0] == end[0] and start[1] == end[1]:
            return False
        return True

    def make_move(self, start, end):
        pass

class Rook(Piece):
    def validate_move(self, start, end):
        return True

    def make_move(self, start, end):
        pass

class Knight(Piece):
    def validate_move(self, start, end):
        return True

    def make_move(self, start, end):
        pass

class Bishop(Piece):
    def validate_move(self, start, end):
        return True

    def make_move(self, start, end):
        pass

class Queen(Piece):
    def validate_move(self, start, end):
        return True

    def make_move(self, start, end):
        pass

class King(Piece):
    def validate_move(self, start, end):
        return True

    def make_move(self, start, end):
        pass

class Board:
    def __init__(self):
        self.board = [
            ["Rook(чорний)", "Knight(чорний)", "Bishop(чорний)", "Queen(чорний)", "King(чорний)", "Bishop(чорний)",
             "Knight(чорний)", "Rook(чорний)"],
            ["Pawn(чорний)", "Pawn(чорний)", "Pawn(чорний)", "Pawn(чорний)", "Pawn(чорний)", "Pawn(чорний)",
             "Pawn(чорний)", "Pawn(чорний)"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["Pawn(білий)", "Pawn(білий)", "Pawn(білий)", "Pawn(білий)", "Pawn(білий)", "Pawn(білий)", "Pawn(білий)",
             "Pawn(білий)"],
            ["Rook(білий)", "Knight(білий)", "Bishop(білий)", "Queen(білий)", "King(білий)", "Bishop(білий)",
             "Knight(білий)", "Rook(білий)"]
        ]

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.board[0] = [
            Rook("чорний"), Knight("чорний"), Bishop("чорний"), Queen("чорний"), King("чорний"),
            Bishop("чорний"), Knight("чорний"), Rook("чорний")
        ]
        self.board[1] = [Pawn("чорний") for _ in range(8)]
        self.board[6] = [Pawn("білий") for _ in range(8)]
        self.board[7] = [
            Rook("білий"), Knight("білий"), Bishop("білий"), Queen("білий"), King("білий"),
            Bishop("білий"), Knight("білий"), Rook("білий")
        ]

        self.coordinates = []
        for row_num in range(8):
            for col_num in range(8):
                col_letter = chr(col_num + ord('a'))
                self.coordinates.append(f"{col_letter}{row_num}")

board = Board()
print(board.coordinates)

class Game:
    def __init__(self):
        self.board = Board()
        self.history = []
        self.current_player = "Гравець1"

    def move(self, player, piece, start, end):
        if not self.validate_move(player, piece, start, end):
            raise HTTPException(status_code=400, detail="Невірний хід")

        start_index = self.board.coordinates.index(start)
        end_index = self.board.coordinates.index(end)

        if self.board.board[end_index // 8][end_index % 8] is not None:
            raise HTTPException(status_code=400, detail="Клітинка вже зайнята")

        piece.make_move(start, end)
        self.history.append((player, piece, start, end))
        self.switch_player()

    def switch_player(self):
        self.current_player = "Гравець2" if self.current_player == "Гравець1" else "Гравець1"

    def validate_move(self, player, piece, start, end):
        end_index = self.board.coordinates.index(end)
        if self.board.board[end_index // 8][end_index % 8] is not None:
            return False
        return piece.validate_move(start, end)

    def end_game(self):
        pass

@app.post("/Початок гри")
async def start_game(гравець1: str, гравець2: str, номер_гравця_1: str, номер_гравця_2: str):
    global game
    game = Game()
    game.current_player = гравець1

    if номер_гравця_1 == "білий":
        game.board.board[1] = [Pawn("білий") for _ in range(8)]
    else:
        game.board.board[6] = [Pawn("чорний") for _ in range(8)]

    if номер_гравця_2 == "чорний":
        game.board.board[0] = [
            Rook("чорний"), Knight("чорний"), Bishop("чорний"), Queen("чорний"), King("чорний"),
            Bishop("чорний"), Knight("чорний"), Rook("чорний")
        ]
    else:
        game.board.board[7] = [
            Rook("білий"), Knight("білий"), Bishop("білий"), Queen("білий"), King("білий"),
            Bishop("білий"), Knight("білий"), Rook("білий")
        ]

    return {"message": "Гра почалася!", "гравець_1": гравець1, "гравець_2": гравець2}

@app.post("/Рух пішок", response_class=HTMLResponse)
async def move(player: str, start: str, end: str):
    if game is None:
        raise HTTPException(status_code=400, detail="Гра не розпочата")

    start_index = game.board.coordinates.index(start)
    piece = game.board.board[start_index // 8][start_index % 8]

    if piece is None:
        raise HTTPException(status_code=400, detail="На цій клітинці немає фігури")

    if (game.current_player == "Гравець1" and "білий" not in piece) or (game.current_player == "Гравець2" and "чорний" not in piece):
        raise HTTPException(status_code=400, detail="Це не ваша фігура")

    piece_instance = None
    if "пішачок" in piece.lower():
        piece_instance = Pawn(piece)
    elif "тура" in piece.lower():
        piece_instance = Rook(piece)
    elif "король" in piece.lower():
        piece_instance = Knight(piece)

    if piece_instance is None:
        raise HTTPException(status_code=400, detail="Невірний хід")
    game.move(player, piece_instance, start, end)
    end_index = game.board.coordinates.index(end)
    if "пішачок" in piece.lower() and game.board.board[end_index // 8][end_index % 8] is not None:
        game.board.board[end_index // 8][end_index % 8] = None

    return HTMLResponse(content=f"Хід зроблено! Хід гравця: {game.current_player}")

@app.get("/result", response_class=HTMLResponse)
async def get_match_results():
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches")
    results = cursor.fetchall()
    conn.close()

    table_content = "<h2>Результати матчів</h2><table border='1'><tr><th>ID</th><th>Гравець 1</th><th>Гравець 2</th><th>Переможець</th><th>Час</th></tr>"
    for row in results:
        table_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
    table_content += "</table>"
    return HTMLResponse(content=table_content)


@app.post("/test", response_class=HTMLResponse)
async def test_win(winner: int):
    if game is None:
        raise HTTPException(status_code=400, detail="Гра не розпочата")

    if winner not in [1, 2]:
        raise HTTPException(status_code=400, detail="Невірний переможець")

    save_match_result(game.current_player, "Opponent", f"Гравець{winner}")
    return HTMLResponse(content=f"Виграш! Переможець: Гравець{winner}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
