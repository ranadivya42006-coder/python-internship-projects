import tkinter as tk
from tkinter import messagebox

# -------------------- Window --------------------
root = tk.Tk()
root.title("Connect Four")
root.configure(bg="#1E3A5F")
root.resizable(False, False)

ROWS = 6
COLS = 7
CELL = 80

# Colors
BOARD_COLOR = "#F5F5F5"
EMPTY = "white"
PLAYER1 = "#00BFFF"   # Blue
PLAYER2 = "#32CD32"   # Green

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
circles = []
current_player = 1
game_over = False


# -------------------- Functions --------------------

def reset_game():
    global board, current_player, game_over

    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    current_player = 1
    game_over = False

    status.config(text="Blue Player's Turn", fg=PLAYER1)

    for r in range(ROWS):
        for c in range(COLS):
            canvas.itemconfig(circles[r][c], fill=EMPTY)


def check_win(player):

    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    return False


def board_full():
    for c in range(COLS):
        if board[0][c] == 0:
            return False
    return True


def drop_piece(col):
    global current_player, game_over

    if game_over:
        return

    for row in range(ROWS - 1, -1, -1):

        if board[row][col] == 0:

            board[row][col] = current_player

            if current_player == 1:
                canvas.itemconfig(circles[row][col], fill=PLAYER1)
            else:
                canvas.itemconfig(circles[row][col], fill=PLAYER2)

            if check_win(current_player):
                game_over = True

                if current_player == 1:
                    status.config(text="Blue Player Wins!", fg=PLAYER1)
                    messagebox.showinfo("Winner", "Blue Player Wins!")
                else:
                    status.config(text="Green Player Wins!", fg=PLAYER2)
                    messagebox.showinfo("Winner", "Green Player Wins!")

                return

            if board_full():
                game_over = True
                status.config(text="Match Draw!", fg="black")
                messagebox.showinfo("Game Over", "It's a Draw!")
                return

            current_player = 2 if current_player == 1 else 1

            if current_player == 1:
                status.config(text="Blue Player's Turn", fg=PLAYER1)
            else:
                status.config(text="Green Player's Turn", fg=PLAYER2)

            return


# -------------------- UI --------------------

title = tk.Label(
    root,
    text="CONNECT FOUR",
    font=("Arial", 24, "bold"),
    bg="#1E3A5F",
    fg="white"
)
title.pack(pady=10)

status = tk.Label(
    root,
    text="Blue Player's Turn",
    font=("Arial", 16, "bold"),
    bg="#1E3A5F",
    fg=PLAYER1
)
status.pack()

button_frame = tk.Frame(root, bg="#1E3A5F")
button_frame.pack()

for c in range(COLS):
    btn = tk.Button(
        button_frame,
        text=f"↓ {c+1}",
        font=("Arial", 12, "bold"),
        width=8,
        command=lambda col=c: drop_piece(col),
        bg="#FFD54F"
    )
    btn.grid(row=0, column=c, padx=2, pady=5)

canvas = tk.Canvas(
    root,
    width=COLS * CELL,
    height=ROWS * CELL,
    bg=BOARD_COLOR,
    highlightthickness=0
)
canvas.pack(pady=10)

for r in range(ROWS):
    row = []
    for c in range(COLS):

        x1 = c * CELL + 10
        y1 = r * CELL + 10
        x2 = x1 + CELL - 20
        y2 = y1 + CELL - 20

        circle = canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            fill=EMPTY,
            outline="black",
            width=2
        )

        row.append(circle)

    circles.append(row)

restart = tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 14, "bold"),
    command=reset_game,
    bg="#4CAF50",
    fg="white",
    width=20
)
restart.pack(pady=10)

root.mainloop()