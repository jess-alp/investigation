import pygame
import random
import heapq
import time

pygame.init()
size = 300
tile_size = size // 3
screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("8 Puzzle - A*")

font = pygame.font.SysFont(None, 60)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (180, 180, 180)

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVES = {
    0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
    3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
    6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
}

def draw_board(state):
    screen.fill(white)
    for i, tile in enumerate(state):
        x = (i % 3) * tile_size
        y = (i // 3) * tile_size
        rect = pygame.Rect(x, y, tile_size, tile_size)
        pygame.draw.rect(screen, gray, rect, 2)
        if tile != 0:
            text = font.render(str(tile), True, black)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    pygame.display.flip()

def is_solvable(state):
    inv = 0
    nums = [x for x in state if x != 0]
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                inv += 1
    return inv % 2 == 0

def generate_random_state():
    while True:
        state = list(GOAL_STATE)
        random.shuffle(state)
        if is_solvable(state):
            return tuple(state)

def manhattan_distance(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_index = GOAL_STATE.index(tile)
        x1, y1 = i % 3, i // 3
        x2, y2 = goal_index % 3, goal_index // 3
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def get_neighbors(state):
    zero_index = state.index(0)
    neighbors = []
    for move in MOVES[zero_index]:
        new_state = list(state)
        new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
        neighbors.append(tuple(new_state))
    return neighbors

def a_star(start):
    open_set = []
    heapq.heappush(open_set, (0 + manhattan_distance(start), 0, start, []))
    visited = set()
    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        if current == GOAL_STATE:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                heapq.heappush(open_set, (g + 1 + manhattan_distance(neighbor), g + 1, neighbor, path + [current]))
    return None

initial_state = generate_random_state()
solution_path = a_star(initial_state)

for state in solution_path:
    draw_board(state)
    pygame.time.delay(500)

time.sleep(2)
pygame.quit()

