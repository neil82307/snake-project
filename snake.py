import pygame
import random
import sys

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 20
FPS = 7
SLOW_FPS = 2

BG = (240, 240, 240)
SNAKE = (20, 120, 20)
FOOD = (200, 30, 30)
TXT = (0, 0, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    hx = (SCREEN_WIDTH // 2) // CELL_SIZE * CELL_SIZE
    hy = (SCREEN_HEIGHT // 2) // CELL_SIZE * CELL_SIZE
    snake = [[hx, hy], [hx - CELL_SIZE, hy], [hx - 2 * CELL_SIZE, hy]]
    dx, dy = CELL_SIZE, 0

    food_x = random.randrange(SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE
    food_y = random.randrange(SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE
    score = 0
    alive = True
    powerup = False
    powerup_start = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL_SIZE, 0
                elif e.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL_SIZE, 0
                elif e.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL_SIZE
                elif e.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL_SIZE

        if alive:
            head = snake[0]
            new = [head[0] + dx, head[1] + dy]
            if new[0] < 0 or new[0] >= SCREEN_WIDTH or new[1] < 0 or new[1] >= SCREEN_HEIGHT:
                alive = False
            elif new in snake:
                alive = False
            else:
                snake.insert(0, new)
                if new[0] == food_x and new[1] == food_y:
                    score += 1
                    if score == 10 and not powerup:
                        powerup = True
                        powerup_start = pygame.time.get_ticks()
                    food_x = random.randrange(SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE
                    food_y = random.randrange(SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE
                else:
                    snake.pop()

        screen.fill(BG)
        pygame.draw.rect(screen, FOOD, (food_x, food_y, CELL_SIZE, CELL_SIZE))
        for s in snake:
            pygame.draw.rect(screen, SNAKE, (s[0], s[1], CELL_SIZE, CELL_SIZE))
        screen.blit(font.render('Score: ' + str(score), True, TXT), (6, 6))

        if powerup:
            sec = (pygame.time.get_ticks() - powerup_start) // 1000
            if sec >= 10:
                powerup = False
            else:
                screen.blit(font.render('Slow: ' + str(10 - sec) + 's', True, (255, 200, 0)), (6, 30))

        if not alive:
            msg = font.render('You lost. Close window to exit.', True, TXT)
            r = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(msg, r)

        pygame.display.flip()
        cur = SLOW_FPS if powerup else FPS
        clock.tick(cur)


if __name__ == '__main__':
    main()
