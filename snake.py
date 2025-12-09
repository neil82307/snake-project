import pygame
import random
import sys

width = 480
height = 480
sqr_size = 10
BG = (255, 255, 255)
BODY_C = (0, 128, 0)
FOOD_C = (255, 0, 0)

class Snake:
    def __init__(self):
        self.step = sqr_size * 2
        max_x = (width - sqr_size) // (sqr_size * 2)
        max_y = (height - sqr_size) // (sqr_size * 2)
        start_x = (max_x // 2) * (sqr_size * 2) + sqr_size
        start_y = (max_y // 2) * (sqr_size * 2) + sqr_size
        self.body = [
            (start_x, start_y),
            (start_x - self.step, start_y),
            (start_x - 2 * self.step, start_y),
        ]
        self._dir = "RIGHT"
        self._initial_len = len(self.body)

    def change_mov(self, key):
        if key == "LEFT" and self._dir != "RIGHT":
            self._dir = "LEFT"
        if key == "RIGHT" and self._dir != "LEFT":
            self._dir = "RIGHT"
        if key == "UP" and self._dir != "DOWN":
            self._dir = "UP"
        if key == "DOWN" and self._dir != "UP":
            self._dir = "DOWN"

    def move(self, eat):
        head = self.body[0]
        x, y = head
        if self._dir == "LEFT":
            x -= self.step
        elif self._dir == "RIGHT":
            x += self.step
        elif self._dir == "UP":
            y -= self.step
        elif self._dir == "DOWN":
            y += self.step
        new_head = (x, y)
        self.body.insert(0, new_head)
        if not eat:
            self.body.pop()

    def score(self):
        return len(self.body) - self._initial_len

class Food:
    def __init__(self):
        self.pos = self._random_pos()

    def _random_pos(self):
        max_x = (width - sqr_size) // (sqr_size * 2)
        max_y = (height - sqr_size) // (sqr_size * 2)
        rx = random.randint(0, max_x) * sqr_size * 2 + sqr_size
        ry = random.randint(0, max_y) * sqr_size * 2 + sqr_size
        return (rx, ry)

def check_food(snake, food):
    hx, hy = snake.body[0]
    fx, fy = food.pos
    dx = hx - fx
    dy = hy - fy
    dist2 = dx * dx + dy * dy
    thresh = sqr_size * sqr_size
    return dist2 <= thresh

def loser(snake, food):
    head = snake.body[0]
    x, y = head
    if x < 0 or x >= width or y < 0 or y >= height:
        return True
    if head in snake.body[1:]:
        return True
    return False

def game_speed(snake):
    return 10 + max(0, snake.score()) * 2
