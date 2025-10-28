from .SteepestAscent import *
from config.utils import *
import pygame

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Tìm Đường Về Nhà - Hill Climbing")

def root(win=WIN, width=WIDTH):
    ROWS = 20  # đặt >=20 để có nhiều node
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if 0 <= row < ROWS and 0 <= col < ROWS:
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if 0 <= row < ROWS and 0 <= col < ROWS:
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    print("Đang tìm đường bằng LEO ĐỒI (Hill Climbing)...")
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    found = hill_climbing_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    if not found:
                        print("BỊ MẮC KẸT! Không thể tìm thấy đường.")
                    else:
                        print("Đã tìm thấy nhà! (Trường hợp rất may mắn)")
                    started = False

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    print("Đã reset bản đồ.")

    pygame.quit()