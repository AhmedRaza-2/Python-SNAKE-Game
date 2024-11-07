import tkinter
import random
ROWS = 25
COLS = 25
TILE_SIZE = 25
WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
# Game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)
# Canvas for drawing
canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
# Center the window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
window_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")
# Initialize game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) # Snake's head
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = [] # Snake's body
game_over = False
score = 0
high_score = 0
def reset_game():
    global snake, food, velocityX, velocityY, snake_body, game_over, score
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = []
    game_over = False
    score = 0
def change_direction(e):
    global velocityX, velocityY, game_over
    if game_over:
        reset_game()
    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0
def move():
    global snake, food, snake_body, game_over, score, high_score
    if game_over:
        return
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        high_score = max(score, high_score)
        return    
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            high_score = max(score, high_score)
            return    
    if snake.x == food.x and snake.y == food.y: 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE
def draw():
    global snake, food, snake_body, game_over, score, high_score
    move()
    canvas.delete("all")
    # Draw background grid
    for row in range(ROWS):
        for col in range(COLS):
            color = "lightgreen" if (row + col) % 2 == 0 else "#98FB98"
            canvas.create_rectangle(col * TILE_SIZE, row * TILE_SIZE, (col + 1) * TILE_SIZE, (row + 1) * TILE_SIZE, fill=color, outline=color)
    # Draw food
    canvas.create_oval(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red', outline="black", width=2)
    # Draw snake
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='blue', outline="black", width=2)
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='blue', outline="black", width=2)
    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20 bold", text=f"Game Over: {score}", fill="black")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30, font="Arial 15 bold", text="Press any key to restart", fill="black")
    else:
        canvas.create_text(50, 20, font="Arial 14 bold", text=f"Score: {score}", fill="black")
        canvas.create_text(150, 20, font="Arial 14 bold", text=f"High Score: {high_score}", fill="black")
    window.after(100, draw)
draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()