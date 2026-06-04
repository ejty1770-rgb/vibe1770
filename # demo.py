# demo.py

import tkinter as tk
import random

WIDTH = 800
HEIGHT = 600
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
BALL_RADIUS = 10

class BlockBreaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter 블럭깨기")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.paddle = self.canvas.create_rectangle(
            (WIDTH - PADDLE_WIDTH) // 2,
            HEIGHT - 60,
            (WIDTH + PADDLE_WIDTH) // 2,
            HEIGHT - 60 + PADDLE_HEIGHT,
            fill="blue",
        )

        self.ball = self.canvas.create_oval(
            WIDTH // 2 - BALL_RADIUS,
            HEIGHT - 80 - BALL_RADIUS,
            WIDTH // 2 + BALL_RADIUS,
            HEIGHT - 80 + BALL_RADIUS,
            fill="red",
        )

        self.bricks = []
        self.create_bricks()

        self.ball_dx = 5
        self.ball_dy = -5
        self.score = 0
        self.lives = 3
        self.game_over = False

        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 18), text="점수: 0")
        self.lives_text = self.canvas.create_text(WIDTH - 10, 10, anchor="ne", fill="white", font=("Arial", 18), text="목숨: 3")
        self.message_text = None

        self.root.bind("<Left>", lambda event: self.move_paddle(-20))
        self.root.bind("<Right>", lambda event: self.move_paddle(20))
        self.root.bind("<a>", lambda event: self.move_paddle(-20))
        self.root.bind("<d>", lambda event: self.move_paddle(20))
        self.root.bind("<r>", lambda event: self.reset_game())

        self.update()

    def create_bricks(self):
        colors = ["#ff4b4b", "#4bff7b", "#ffe54b", "#4bb6ff", "#b14bff", "#ff9a4b"]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x1 = col * BRICK_WIDTH + 1
                y1 = row * BRICK_HEIGHT + 50
                x2 = x1 + BRICK_WIDTH - 2
                y2 = y1 + BRICK_HEIGHT - 2
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row % len(colors)], width=0)
                self.bricks.append(brick)

    def move_paddle(self, dx):
        if self.game_over:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        new_x1 = max(0, x1 + dx)
        new_x2 = min(WIDTH, x2 + dx)
        if new_x1 <= 0:
            new_x1 = 0
            new_x2 = PADDLE_WIDTH
        if new_x2 >= WIDTH:
            new_x2 = WIDTH
            new_x1 = WIDTH - PADDLE_WIDTH
        self.canvas.coords(self.paddle, new_x1, y1, new_x2, y2)

    def update(self):
        if not self.game_over:
            self.move_ball()
        self.root.after(20, self.update)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= WIDTH:
            self.ball_dx *= -1
        if y1 <= 0:
            self.ball_dy *= -1

        if self.check_paddle_collision():
            self.ball_dy *= -1
            paddle_x1, _, paddle_x2, _ = self.canvas.coords(self.paddle)
            ball_center = (x1 + x2) / 2
            offset = (ball_center - (paddle_x1 + paddle_x2) / 2) / (PADDLE_WIDTH / 2)
            self.ball_dx = 5 * offset
            self.ball_dx = max(-7, min(self.ball_dx, 7))

        if self.check_brick_collision():
            self.score += 10
            self.canvas.itemconfigure(self.score_text, text=f"점수: {self.score}")

        if y2 >= HEIGHT:
            self.lives -= 1
            self.canvas.itemconfigure(self.lives_text, text=f"목숨: {self.lives}")
            if self.lives <= 0:
                self.end_game(False)
            else:
                self.reset_ball()

        if not self.bricks:
            self.end_game(True)

    def check_paddle_collision(self):
        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)
        return self.rects_overlap(ball_coords, paddle_coords)

    def check_brick_collision(self):
        ball_coords = self.canvas.coords(self.ball)
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick)
            if self.rects_overlap(ball_coords, brick_coords):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_dy *= -1
                return True
        return False

    @staticmethod
    def rects_overlap(a, b):
        return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])

    def reset_ball(self):
        self.canvas.coords(
            self.ball,
            WIDTH // 2 - BALL_RADIUS,
            HEIGHT - 80 - BALL_RADIUS,
            WIDTH // 2 + BALL_RADIUS,
            HEIGHT - 80 + BALL_RADIUS,
        )
        self.ball_dx = random.choice([-5, 5])
        self.ball_dy = -5

    def reset_game(self):
        if self.message_text:
            self.canvas.delete(self.message_text)
            self.message_text = None
        self.canvas.coords(self.paddle, (WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 60, (WIDTH + PADDLE_WIDTH) // 2, HEIGHT - 45)
        self.reset_ball()
        for brick in self.bricks:
            self.canvas.delete(brick)
        self.bricks.clear()
        self.create_bricks()
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.canvas.itemconfigure(self.score_text, text="점수: 0")
        self.canvas.itemconfigure(self.lives_text, text="목숨: 3")

    def end_game(self, victory):
        self.game_over = True
        message = "승리! 다시 시작하려면 R키를 누르세요." if victory else "게임 오버! 다시 시작하려면 R키를 누르세요."
        color = "yellow" if victory else "white"
        self.message_text = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, fill=color, font=("Arial", 24), text=message)


def main():
    root = tk.Tk()
    app = BlockBreaker(root)
    root.mainloop()


if __name__ == "__main__":
    main()

