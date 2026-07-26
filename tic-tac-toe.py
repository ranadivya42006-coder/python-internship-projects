import tkinter as tk
from tkinter import messagebox

# Colors
BG_COLOR = "#FFE5B4"
GRID_COLOR = "#FFF8DC"
X_COLOR = "#FF4500"
O_COLOR = "#8A2BE2"
TEXT_COLOR = "#5C4033"

# Main Window
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("350x450")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

current_player = "X"
board = [""] * 9
buttons = []

# Title
title = tk.Label(
    root,
    text="Tic Tac Toe",
    font=("Arial", 22, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title.pack(pady=10)

# Status Label
status = tk.Label(
    root,
    text="Player X's Turn",
    font=("Arial", 14),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
status.pack(pady=5)

# Game Frame
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack()

def check_winner():
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    for pattern in win_patterns:
        a, b, c = pattern
        if board[a] == board[b] == board[c] != "":
            return True

    return False

def reset_game():
    global current_player, board

    current_player = "X"
    board = [""] * 9

    for button in buttons:
        button.config(
            text="",
            state="normal",
            fg=TEXT_COLOR
        )

    status.config(text="Player X's Turn")

def on_click(index):
    global current_player

    if board[index] == "":
        board[index] = current_player

        color = X_COLOR if current_player == "X" else O_COLOR

        buttons[index].config(
            text=current_player,
            fg=color
        )

        # Check winner
        if check_winner():
            messagebox.showinfo(
                "Winner",
                f"🎉 Player {current_player} Wins!"
            )
            reset_game()
            return

        # Check draw
        if "" not in board:
            messagebox.showinfo(
                "Game Over",
                "🤝 Match Draw!\nNo player won the game."
            )
            reset_game()
            return

        # Switch player
        current_player = "O" if current_player == "X" else "X"
        status.config(text=f"Player {current_player}'s Turn")

# Create 3x3 Grid
for i in range(9):
    btn = tk.Button(
        frame,
        text="",
        font=("Arial", 24, "bold"),
        width=5,
        height=2,
        bg=GRID_COLOR,
        fg=TEXT_COLOR,
        command=lambda i=i: on_click(i)
    )

    btn.grid(
        row=i // 3,
        column=i % 3,
        padx=5,
        pady=5
    )

    buttons.append(btn)

# Restart Button
restart_btn = tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 12, "bold"),
    command=reset_game,
    bg="#FFD166"
)
restart_btn.pack(pady=15)

root.mainloop()