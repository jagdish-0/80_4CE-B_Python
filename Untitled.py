import tkinter as tk

class ChessBoard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess Board")
        self.square_size = 50
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.selected_piece = None
        self.pieces = {
            (0, 0): "♜", (0, 7): "♜", (0, 1): "♞", (0, 6): "♞", (0, 2): "♝", (0, 5): "♝", (0, 3): "♛", (0, 4): "♚", 
            (7, 0): "♖", (7, 7): "♖", (7, 1): "♘", (7, 6): "♘", (7, 2): "♗", (7, 5): "♗", (7, 3): "♕", (7, 4): "♔"
        }
        for i in range(8):
            self.pieces[(1, i)] = "♟"
            self.pieces[(6, i)] = "♙"
        
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1, y1 = col * self.square_size, row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                if (row, col) in self.pieces:
                    self.canvas.create_text(x1 + self.square_size // 2, y1 + self.square_size // 2, 
                                            text=self.pieces[(row, col)], font=("Arial", 24))

    def on_click(self, event):
        col, row = event.x // self.square_size, event.y // self.square_size
        if self.selected_piece:
            self.pieces[(row, col)] = self.pieces.pop(self.selected_piece)
            self.selected_piece = None
        elif (row, col) in self.pieces:
            self.selected_piece = (row, col)
        self.draw_board()
        print("selected")

ChessBoard()
