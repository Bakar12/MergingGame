import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
GRID_SIZE = 6
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
PADDING = 5

# Colors
COLORS = {
    1: (85, 239, 196),
    2: (255, 234, 167),
    3: (129, 236, 236),
    4: (255, 118, 117),
    5: (162, 155, 254),
    6: (223, 230, 233),
    7: (250, 177, 160),
    8: (232, 67, 147),
    9: (255, 234, 167),
    10: (0, 184, 148),
    11: (9, 132, 227),
    12: (108, 92, 231),
    13: (253, 203, 110),
    14: (184, 233, 148),
    15: (250, 130, 49)
}

# Fonts
FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Merge Madness')

# Grid initialization
grid = [[random.randint(1, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Scores
score = 0
high_score = 0


def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            value = grid[x][y]
            color = COLORS.get(value, (255, 255, 255))
            rect = pygame.Rect(x * TILE_SIZE + PADDING, y * TILE_SIZE + PADDING, TILE_SIZE - PADDING * 2,
                               TILE_SIZE - PADDING * 2)
            pygame.draw.rect(screen, color, rect)
            text = FONT.render(str(value), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


def merge_tiles(x, y, value):
    global score
    queue = [(x, y)]
    to_merge = []
    while queue:
        cx, cy = queue.pop(0)
        if 0 <= cx < GRID_SIZE and 0 <= cy < GRID_SIZE and grid[cx][cy] == value and (cx, cy) not in to_merge:
            to_merge.append((cx, cy))
            queue.extend([(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)])
    if len(to_merge) > 1:
        for cx, cy in to_merge:
            grid[cx][cy] = 0
        grid[x][y] = value + 1
        score += value
        return True
    return False


def spawn_new_tiles():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == 0:
                grid[x][y] = random.randint(1, 3)
                animate_new_tile((x, y))


def animate_new_tile(pos):
    x, y = pos
    for size in range(10, TILE_SIZE, 5):
        screen.fill((255, 255, 255))
        draw_grid()
        value = grid[x][y]
        color = COLORS.get(value, (255, 255, 255))
        rect = pygame.Rect(x * TILE_SIZE + PADDING, y * TILE_SIZE + PADDING, size - PADDING * 2, size - PADDING * 2)
        pygame.draw.rect(screen, color, rect)
        text = FONT.render(str(value), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(30)


def main():
    global score, high_score
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_grid()

        score_text = FONT.render(f'Score: {score}', True, (0, 0, 0))
        high_score_text = FONT.render(f'High Score: {high_score}', True, (0, 0, 0))
        screen.blit(score_text, (10, SCREEN_HEIGHT - 60))
        screen.blit(high_score_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // TILE_SIZE
                grid_y = mouse_y // TILE_SIZE
                if merge_tiles(grid_x, grid_y, grid[grid_x][grid_y]):
                    spawn_new_tiles()
                    if score > high_score:
                        high_score = score

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
