import pygame
from config.utils import *

def hill_climbing_algorithm(draw, grid, start, end, delay=25):
    came_from = {}
    current = start
    path_nodes = {start}
    current_h = h(start.get_pos(), end.get_pos())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        best_neighbor = None
        min_h = current_h

        for neighbor in current.neighbors:
            if neighbor not in path_nodes and not neighbor.is_wall():
                neighbor_h = h(neighbor.get_pos(), end.get_pos())
                if neighbor_h < min_h:
                    min_h = neighbor_h
                    best_neighbor = neighbor

        if best_neighbor is None:
            current.make_closed()
            draw()
            return False

        came_from[best_neighbor] = current
        current = best_neighbor
        path_nodes.add(current)
        current_h = min_h

        if current != end:
            current.make_open()

        draw()
        pygame.time.wait(delay)