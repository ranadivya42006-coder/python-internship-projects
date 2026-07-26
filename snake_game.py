import tkinter as tk
import random

# -------------------- CONSTANTS --------------------
WIDTH = 500
HEIGHT = 500
SPACE_SIZE = 20
SPEED = 100
BODY_PARTS = 3

SNAKE_COLOR = "white"
FOOD_COLOR = "yellow"
BACKGROUND_COLOR = "black"

# -------------------- GAME VARIABLES --------------------
score = 0
direction = "down"

# -------------------- WINDOW --------------------
window = tk.Tk()
window.title("Snake Game")

score_label = tk.Label(window, text="Score: 0", font=("Arial", 16))
score_label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, width=WIDTH, height=HEIGHT)
canvas.pack()

# -------------------- CREATE FOOD --------------------
def create_food():
    while True:
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        if [x, y] not in snake["body"]:
            canvas.delete("food")
            canvas.create_oval(
                x, y,
                x + SPACE_SIZE, y + SPACE_SIZE,
                fill=FOOD_COLOR,
                tag="food"
            )
            return [x, y]

# -------------------- CHANGE DIRECTION --------------------
def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

# -------------------- NEXT TURN --------------------
def next_turn():
    global food, score

    x, y = snake["body"][0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake["body"].insert(0, [x, y])

    square = canvas.create_rectangle(
        x, y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR,
        outline="white"
    )

    snake["squares"].insert(0, square)

    if [x, y] == food:
        score += 1
        score_label.config(text=f"Score: {score}")
        food = create_food()
    else:
        del snake["body"][-1]
        canvas.delete(snake["squares"][-1])
        del snake["squares"][-1]

    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn)

# -------------------- COLLISION --------------------
def check_collisions():
    x, y = snake["body"][0]

    if x < 0 or x >= WIDTH:
        return True

    if y < 0 or y >= HEIGHT:
        return True

    for part in snake["body"][1:]:
        if x == part[0] and y == part[1]:
            return True

    return False

# -------------------- RESTART --------------------
def restart_game():
    global snake, food, score, direction

    canvas.delete("all")

    score = 0
    direction = "down"

    score_label.config(text="Score: 0")

    snake = {
        "body": [],
        "squares": []
    }

    for i in range(BODY_PARTS):
        snake["body"].append([100 - (i * SPACE_SIZE), 100])

    for x, y in snake["body"]:
        square = canvas.create_rectangle(
            x, y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill=SNAKE_COLOR,
            outline="white"
        )
        snake["squares"].append(square)

    food = create_food()

    next_turn()

# -------------------- GAME OVER --------------------
def game_over():
    canvas.delete("all")

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2 - 50,
        text="GAME OVER",
        fill="red",
        font=("Arial", 28, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2,
        text=f"Final Score: {score}",
        fill="white",
        font=("Arial", 18)
    )

    restart_btn = tk.Button(
        window,
        text="Restart",
        font=("Arial", 14),
        bg="green",
        fg="white",
        command=lambda: [restart_btn.destroy(), restart_game()]
    )

    canvas.create_window(
        WIDTH / 2,
        HEIGHT / 2 + 60,
        window=restart_btn
    )

# -------------------- START GAME --------------------
snake = {
    "body": [],
    "squares": []
}

for i in range(BODY_PARTS):
    snake["body"].append([100 - (i * SPACE_SIZE), 100])

for x, y in snake["body"]:
    square = canvas.create_rectangle(
        x, y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR,
        outline="white"
    )
    snake["squares"].append(square)

food = create_food()

# -------------------- CONTROLS --------------------
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

next_turn()

window.mainloop()
