import tkinter as tk
import random

# ---------------- Window ----------------
WIDTH = 900
HEIGHT = 500

BG = "#000000"
LEFT = "#C0C0C0"      
RIGHT = "#D4AF37"     
BALL = "#FFFFFF"
TEXT = "#FFD700"

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 110
BALL_SIZE = 20
WIN_SCORE = 5

root = tk.Tk()
root.title("PONG GAME")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG,
    highlightthickness=0
)
canvas.pack()

# Keyboard focus
root.focus_force()
canvas.focus_set()

# ---------------- Scores ----------------
left_score = 0
right_score = 0

score_text = canvas.create_text(
    WIDTH // 2,
    40,
    text="0 : 0",
    fill=TEXT,
    font=("Arial", 24, "bold")
)

winner_text = None
game_over = False

# ---------------- Paddles ----------------
left_paddle = canvas.create_rectangle(
    40,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    40 + PADDLE_WIDTH,
    HEIGHT // 2 + PADDLE_HEIGHT // 2,
    fill=LEFT,
    outline=""
)

right_paddle = canvas.create_rectangle(
    WIDTH - 55,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    WIDTH - 40,
    HEIGHT // 2 + PADDLE_HEIGHT // 2,
    fill=RIGHT,
    outline=""
)

# ---------------- Ball ----------------
ball = canvas.create_oval(
    WIDTH // 2 - BALL_SIZE // 2,
    HEIGHT // 2 - BALL_SIZE // 2,
    WIDTH // 2 + BALL_SIZE // 2,
    HEIGHT // 2 + BALL_SIZE // 2,
    fill=BALL,
    outline=""
)

ball_dx = random.choice([-5, 5])
ball_dy = random.choice([-4, 4])

keys = {}

# ---------------- Paddle Movement ----------------
def move_paddles():
    if keys.get("w") or keys.get("W"):
        canvas.move(left_paddle, 0, -8)

    if keys.get("s") or keys.get("S"):
        canvas.move(left_paddle, 0, 8)

    if keys.get("Up"):
        canvas.move(right_paddle, 0, -8)

    if keys.get("Down"):
        canvas.move(right_paddle, 0, 8)

    keep_inside(left_paddle)
    keep_inside(right_paddle)


def keep_inside(paddle):
    x1, y1, x2, y2 = canvas.coords(paddle)

    if y1 < 0:
        canvas.move(paddle, 0, -y1)

    if y2 > HEIGHT:
        canvas.move(paddle, 0, HEIGHT - y2)

# ---------------- Score ----------------
def update_score():
    canvas.itemconfig(score_text, text=f"{left_score} : {right_score}")

# ---------------- Reset Ball ----------------
def reset_ball():
    global ball_dx, ball_dy

    canvas.coords(
        ball,
        WIDTH // 2 - BALL_SIZE // 2,
        HEIGHT // 2 - BALL_SIZE // 2,
        WIDTH // 2 + BALL_SIZE // 2,
        HEIGHT // 2 + BALL_SIZE // 2
    )

    ball_dx = random.choice([-5, 5])
    ball_dy = random.choice([-4, 4])

# ---------------- Collision ----------------
def overlap(a, b):
    ax1, ay1, ax2, ay2 = canvas.coords(a)
    bx1, by1, bx2, by2 = canvas.coords(b)

    return (
        ax2 >= bx1 and
        ax1 <= bx2 and
        ay2 >= by1 and
        ay1 <= by2
    )

# ---------------- Game Loop ----------------
def game():
    global ball_dx, ball_dy
    global left_score, right_score
    global game_over, winner_text

    if game_over:
        return

    move_paddles()

    canvas.move(ball, ball_dx, ball_dy)

    bx1, by1, bx2, by2 = canvas.coords(ball)

    # Bounce off top and bottom
    if by1 <= 0 or by2 >= HEIGHT:
        ball_dy *= -1

    # Bounce off left paddle
    if overlap(ball, left_paddle) and ball_dx < 0:
        ball_dx *= -1.05

    # Bounce off right paddle
    if overlap(ball, right_paddle) and ball_dx > 0:
        ball_dx *= -1.05

    # Right player scores
    if bx1 <= 0:
        right_score += 1
        update_score()
        reset_ball()

    # Left player scores
    if bx2 >= WIDTH:
        left_score += 1
        update_score()
        reset_ball()

    # Check winner
    if left_score >= WIN_SCORE:
        game_over = True
        winner_text = canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="🏆 SLIVER PLAYER WINS!\n\nPress R to Play Again",
            fill=LEFT,
            font=("Arial", 28, "bold"),
            justify="center"
        )
        return

    if right_score >= WIN_SCORE:
        game_over = True
        winner_text = canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="🏆 GOLD PLAYER WINS!\n\nPress R to Play Again",
            fill=RIGHT,
            font=("Arial", 28, "bold"),
            justify="center"
        )
        return

    root.after(16, game)

# ---------------- Keyboard ----------------
def press(event):
    keys[event.keysym] = True

def release(event):
    keys[event.keysym] = False

# ---------------- Restart ----------------
def restart(event=None):
    global left_score, right_score
    global game_over, winner_text

    left_score = 0
    right_score = 0
    game_over = False

    update_score()

    if winner_text:
        canvas.delete(winner_text)

    # Reset paddle positions
    canvas.coords(
        left_paddle,
        40,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        40 + PADDLE_WIDTH,
        HEIGHT // 2 + PADDLE_HEIGHT // 2
    )

    canvas.coords(
        right_paddle,
        WIDTH - 55,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        WIDTH - 40,
        HEIGHT // 2 + PADDLE_HEIGHT // 2
    )

    reset_ball()
    game()

# ---------------- Key Bindings ----------------
root.bind_all("<KeyPress>", press)
root.bind_all("<KeyRelease>", release)
root.bind_all("<KeyPress-r>", restart)
root.bind_all("<KeyPress-R>", restart)

# ---------------- Start ----------------
game()

root.mainloop()