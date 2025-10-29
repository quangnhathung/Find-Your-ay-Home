from .Algorithm.SteepestAscent import *
from config.utils import *
import pygame
from .Algorithm.Simple import *
from .Algorithm.Stochastic import *
from .Algorithm.SidewaysMoves import *
from config.config import *

conf = Config()
WIDTH = conf.SCREEN_WIDTH  # kích thước vùng lưới (vuông)
TOP_UI_HEIGHT = 50
BOTTOM_UI_HEIGHT = 50
TOTAL_RIGHT_PANEL = 300   # panel bên phải (không vẽ lưới vào đây)
WIN_HEIGHT = WIDTH + TOP_UI_HEIGHT + BOTTOM_UI_HEIGHT
TOTAL_WIDTH = WIDTH + TOTAL_RIGHT_PANEL

WIN = pygame.display.set_mode((TOTAL_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tim Duong Ve Nha - Hill Climbing")



def root(win=WIN, width=WIDTH):
    ROWS = conf.ROW
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    started = False
    message = ""

    # Lưới vuông riêng biệt
    grid_surf = pygame.Surface((WIDTH, WIDTH))

    # Các nút điều khiển
    button_width = WIDTH // 4
    button_height = 40
    button_y = TOP_UI_HEIGHT + WIDTH + (BOTTOM_UI_HEIGHT - button_height) // 2
    buttons = [
        pygame.Rect(0 * button_width, button_y, button_width, button_height),
        pygame.Rect(1 * button_width, button_y, button_width, button_height),
        pygame.Rect(2 * button_width, button_y, button_width, button_height),
        pygame.Rect(3 * button_width, button_y, button_width, button_height)
    ]
    button_texts = ["Stochastic", "Sideways", "Simple", "Steepest Ascent"]
    button_colors = [LIGHT_BLUE] * 4

    def update_grid_surf():
        grid_surf.fill(WHITE)
        for row in grid:
            for node in row:
                node.draw(grid_surf)
        draw_grid_lines(grid_surf, ROWS, width)

    def redraw_all():
        win.fill(WHITE)
        # --- Vẽ message phía trên ---
        if message:
            text_surf = FONT.render(message, True, BLACK)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, TOP_UI_HEIGHT // 2))
            win.blit(text_surf, text_rect)
        # --- Lưới vuông chính ---
        win.blit(grid_surf, (0, TOP_UI_HEIGHT))
        # --- Các nút phía dưới ---
        for i, rect in enumerate(buttons):
            draw_button(win, rect, button_texts[i], button_colors[i])
        pygame.display.update()

    def algo_draw():
        update_grid_surf()
        win.blit(grid_surf, (0, TOP_UI_HEIGHT))
        pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if TOP_UI_HEIGHT <= pos[1] < TOP_UI_HEIGHT + WIDTH:
                    adjusted_pos = (pos[0], pos[1] - TOP_UI_HEIGHT)
                    row, col = get_clicked_pos(adjusted_pos, ROWS, width)
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
                elif pos[1] >= TOP_UI_HEIGHT + WIDTH:
                    for i, rect in enumerate(buttons):
                        if rect.collidepoint(pos) and start and end:
                            started = True
                            message = ""
                            redraw_all()
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            algo_name = button_texts[i]
                            if algo_name == "Stochastic":
                                found = Stochastic(algo_draw, grid, start, end)
                            elif algo_name == "Sideways":
                                found = Sideways(algo_draw, grid, start, end)
                            elif algo_name == "Simple":
                                found = Simple(algo_draw, grid, start, end)
                            elif algo_name == "Steepest Ascent":
                                found = Steepest_Ascent(algo_draw, grid, start, end)
                            if not found:
                                message = f"BI MAC KET! Khong the tim thay duong voi {algo_name}."
                            else:
                                message = f"Da tim thay nha voi {algo_name}!"
                            started = False
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if TOP_UI_HEIGHT <= pos[1] < TOP_UI_HEIGHT + WIDTH:
                    adjusted_pos = (pos[0], pos[1] - TOP_UI_HEIGHT)
                    row, col = get_clicked_pos(adjusted_pos, ROWS, width)
                    if 0 <= row < ROWS and 0 <= col < ROWS:
                        node = grid[row][col]
                        node.reset()
                        if node == start:
                            start = None
                        elif node == end:
                            end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    message = "Da reset ban do."

        update_grid_surf()
        redraw_all()

    pygame.quit()
