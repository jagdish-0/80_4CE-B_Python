import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        self.create_board()

    def create_board(self):
        for i in range(9):
            btn = tk.Button(self.window, text="", font=("Arial", 20), height=3, width=6,
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

    def on_click(self, index):
        if self.board[index] == "" and not self.check_winner():
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a Tie!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),  
                                (0, 4, 8), (2, 4, 6)]  

        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                return True
        return False

    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text="")

    def run(self):
        self.window.mainloop()

# Run the game
if __name__ == "__main__":
    game = TicTacToe()
    game.run()
