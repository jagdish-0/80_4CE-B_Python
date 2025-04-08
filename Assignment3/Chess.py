import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 8
SQUARE_SIZE = 60

class Piece:
    def __init__(self, color, kind):
        self.color = color
        self.kind = kind

    def __str__(self):
        symbols = {
            'K': '♔' if self.color == 'white' else '♚',
            'Q': '♕' if self.color == 'white' else '♛',
            'R': '♖' if self.color == 'white' else '♜',
            'B': '♗' if self.color == 'white' else '♝',
            'N': '♘' if self.color == 'white' else '♞',
            'P': '♙' if self.color == 'white' else '♟',
        }
        return symbols[self.kind]

class ChessBoard(tk.Canvas):
    def __init__(self, master):
        canvas_size = SQUARE_SIZE * BOARD_SIZE
        super().__init__(master, width=canvas_size, height=canvas_size)
        self.pack()
        self.selected = None
        self.turn = 'white'
        self.board = self.create_board()
        self.bind("<Button-1>", self.on_click)
        self.draw_board()

    def create_board(self):
        # Initialize an 8x8 chessboard with pieces
        board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Place major pieces
        placement = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for i, kind in enumerate(placement):
            board[0][i] = Piece('black', kind)
            board[7][i] = Piece('white', kind)

        # Place pawns
        for i in range(BOARD_SIZE):
            board[1][i] = Piece('black', 'P')
            board[6][i] = Piece('white', 'P')

        return board

    def draw_board(self):
        self.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                self.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.board[row][col]
                if piece:
                    self.create_text(
                        x1 + SQUARE_SIZE / 2,
                        y1 + SQUARE_SIZE / 2,
                        text=str(piece),
                        font=("Arial", 32)
                    )

    def on_click(self, event):
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        if self.selected:
            if (row, col) != self.selected:
                if self.move_piece(self.selected, (row, col)):
                    self.turn = 'black' if self.turn == 'white' else 'white'
            self.selected = None
        else:
            piece = self.board[row][col]
            if piece and piece.color == self.turn:
                self.selected = (row, col)
        self.draw_board()

    def move_piece(self, start, end):
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]
        target = self.board[er][ec]

        if not self.is_legal_move(piece, start, end):
            return False

        if target and target.color == piece.color:
            return False

        self.board[er][ec] = piece
        self.board[sr][sc] = None
        return True

    def is_legal_move(self, piece, start, end):
        sr, sc = start
        er, ec = end
        dr, dc = er - sr, ec - sc

        if piece.kind == 'P':
            direction = -1 if piece.color == 'white' else 1
            start_row = 6 if piece.color == 'white' else 1

            # Normal move
            if dc == 0 and dr == direction and not self.board[er][ec]:
                return True
            # Double move
            if dc == 0 and dr == 2 * direction and sr == start_row and not self.board[sr + direction][sc] and not self.board[er][ec]:
                return True
            # Capture
            if abs(dc) == 1 and dr == direction and self.board[er][ec] and self.board[er][ec].color != piece.color:
                return True
            return False

        if piece.kind == 'R':
            if sr == er or sc == ec:
                return self.clear_path(start, end)
        elif piece.kind == 'B':
            if abs(dr) == abs(dc):
                return self.clear_path(start, end)
        elif piece.kind == 'Q':
            if sr == er or sc == ec or abs(dr) == abs(dc):
                return self.clear_path(start, end)
        elif piece.kind == 'N':
            return (abs(dr), abs(dc)) in [(2, 1), (1, 2)]
        elif piece.kind == 'K':
            return max(abs(dr), abs(dc)) == 1

        return False

    def clear_path(self, start, end):
        sr, sc = start
        er, ec = end
        dr = (er - sr) // max(1, abs(er - sr)) if er != sr else 0
        dc = (ec - sc) // max(1, abs(ec - sc)) if ec != sc else 0
        r, c = sr + dr, sc + dc
        while (r, c) != (er, ec):
            if self.board[r][c]:
                return False
            r += dr
            c += dc
        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Game in Tkinter")
    game = ChessBoard(root)
    root.mainloop()
