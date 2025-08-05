import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeBotGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe (Player vs Bot)")
        
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.moves = 0

        self.player_symbol, self.bot_symbol = random.choice([("X", "O"), ("O", "X")])
        self.current_player = "X"  # X always starts

        self.create_widgets()
        self.update_status()

        if self.current_player == self.bot_symbol:
            self.root.after(500, self.bot_move)

    def create_widgets(self):
        self.role_label = tk.Label(self.root, text=f"You are '{self.player_symbol}'", font=("Arial", 14))
        self.role_label.grid(row=0, column=0, columnspan=3, pady=5)

        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                                command=lambda row=r, col=c: self.player_move(row, col))
                btn.grid(row=r+1, column=c)
                self.buttons[r][c] = btn

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.grid(row=4, column=0, columnspan=3, pady=10)

    def update_status(self):
        if self.current_player == self.player_symbol:
            self.status_label.config(text="Your Turn")
        else:
            self.status_label.config(text="Bot's Turn")

    def player_move(self, row, col):
        if self.board[row][col] == "" and self.current_player == self.player_symbol:
            self.make_move(row, col, self.player_symbol)
            self.after_player_move()

    def after_player_move(self):
        if self.check_endgame(self.player_symbol):
            return
        self.current_player = self.bot_symbol
        self.update_status()
        self.root.after(500, self.bot_move)

    def bot_move(self):
        if self.current_player != self.bot_symbol:
            return

        empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        if empty:
            row, col = random.choice(empty)
            self.make_move(row, col, self.bot_symbol)

        if not self.check_endgame(self.bot_symbol):
            self.current_player = self.player_symbol
            self.update_status()

    def make_move(self, row, col, symbol):
        self.board[row][col] = symbol
        self.buttons[row][col].config(text=symbol, state="disabled")
        self.moves += 1

    def check_endgame(self, symbol):
        if self.check_winner(symbol):
            if symbol == self.player_symbol:
                messagebox.showinfo("Game Over", "🎉 You Win!")
            else:
                messagebox.showinfo("Game Over", "🤖 Bot Wins!")
            self.reset_game()
            return True
        elif self.moves == 9:
            messagebox.showinfo("Game Over", "It's a Tie!")
            self.reset_game()
            return True
        return False

    def check_winner(self, symbol):
        b = self.board
        # Rows, Columns, Diagonals
        return any(all(b[r][c] == symbol for c in range(3)) for r in range(3)) or \
               any(all(b[r][c] == symbol for r in range(3)) for c in range(3)) or \
               all(b[i][i] == symbol for i in range(3)) or \
               all(b[i][2 - i] == symbol for i in range(3))

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.moves = 0

        self.player_symbol, self.bot_symbol = random.choice([("X", "O"), ("O", "X")])
        self.current_player = "X"
        self.role_label.config(text=f"You are '{self.player_symbol}'")

        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", state="normal")

        self.update_status()
        if self.current_player == self.bot_symbol:
            self.root.after(500, self.bot_move)


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeBotGame(root)
    root.mainloop()
