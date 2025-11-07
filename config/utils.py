from model.model import Node
from config.constans import *
import pygame

# Hàm tiện ích
def h(p1, p2):
    # Manhattan
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# helper
def is_ancestor(node, maybe_ancestor, came_from) -> bool:
    cur = node
    seen = set()
    while True:
        parent = came_from.get(cur, None)
        if parent is None:
            return False
        if parent == maybe_ancestor:
            return True
        # cycle guard
        if parent in seen:
            return False
        seen.add(parent)
        cur = parent




def reconstruct_path(came_from, current, draw):
    visited = set()
    node = current

    while True:
        parent = came_from.get(node, None)
        if parent is None:
            break

        if parent in visited:
            break
        visited.add(parent)

        if parent.is_start():
            break

        if parent.is_flag():
            try:
                parent.reset()
            except Exception:
                try:
                    parent.wall_filename = None
                except Exception:
                    pass

        try:
            parent.make_path()
        except Exception:
            try:
                parent.color = PURPLE
                if hasattr(parent, "wall_filename"):
                    parent.wall_filename = None
            except Exception:
                pass

        draw()

        node = parent


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows + 1):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
    pygame.draw.rect(win, GREY, (0, 0, width, width), 2)

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col

pygame.font.init()
FONT = pygame.font.SysFont(None, 24)
def draw_button(win, rect, text, color):
    pygame.draw.rect(win, color, rect, border_radius=6)
    text_surf = FONT.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    win.blit(text_surf, text_rect)


#xóa path / flag
def ClearOldPath(grid):
    for row in grid:
        for node in row:
            if node.is_path() or node.is_flag() or node.is_open() or node.is_closed():
                node.reset()