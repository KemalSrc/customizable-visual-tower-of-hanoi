import tkinter as tk
from time import time
from collections import deque

def tower_of_hanoi_recursive(n, source, target, auxiliary):

    if n > 0:
        tower_of_hanoi_recursive(n - 1, source, auxiliary, target)
        moves.append(f"Move disc {n} from {source} to {target}")
        tower_of_hanoi_recursive(n - 1, auxiliary, target, source)

def tower_of_hanoi_iterative(n: int, source: str, auxiliary: str, destination: str) -> tuple:
    if n <= 0:
        raise ValueError("Number of discs must be a positive integer.")

    source_stack = deque()
    auxiliary_stack = deque()
    destination_stack = deque()

    for i in range(n, 0, -1):
        source_stack.append(i)

    total_moves = 2**n - 1

    for move_num in range(1, total_moves + 1):
        if move_num % 3 == 1:
            move_disc(source_stack, destination_stack, source, destination, move_num)
        elif move_num % 3 == 2:
            move_disc(source_stack, auxiliary_stack, source, auxiliary, move_num)
        elif move_num % 3 == 0:
            move_disc(auxiliary_stack, destination_stack, auxiliary, destination, move_num)

    return tuple(destination_stack)


def move_disc(source_stack, destination_stack, source, destination, move_num):
    if not source_stack:
        source_stack.append(destination_stack.pop())
        moves.append(f"Move disc {source_stack[-1]} from {destination} to {source}")
        print(f"{move_num} --> Move disc {source_stack[-1]} from {destination} to {source}")
    elif not destination_stack:
        destination_stack.append(source_stack.pop())
        moves.append(f"Move disc {destination_stack[-1]} from {source} to {destination}")
        print(f"{move_num} --> Move disc {destination_stack[-1]} from {source} to {destination}")
    elif source_stack[-1] > destination_stack[-1]:
        source_stack.append(destination_stack.pop())
        moves.append(f"Move disc {source_stack[-1]} from {destination} to {source}")
        print(f"{move_num} --> Move disc {source_stack[-1]} from {destination} to {source}")
    else:
        destination_stack.append(source_stack.pop())
        moves.append(f"Move disc {destination_stack[-1]} from {source} to {destination}")
        print(f"{move_num} --> Move disc {destination_stack[-1]} from {source} to {destination}")

def solve_tower_of_hanoi(num_discs, algorithm):
    global moves
    moves = []

    start_time = time()
    if algorithm == "Recursive":
        tower_of_hanoi_recursive(num_discs, 'A', 'C', 'B')
    elif algorithm == "Iterative":
        temp = tower_of_hanoi_iterative(num_discs, "A","B","C")
    end_time = time()
    return end_time - start_time, moves

def display_moves(moves):
    moves_list.delete(0, tk.END)
    move_counter = 1
    for move in moves:
        moves_list.insert(tk.END, f"{move_counter} --> {move}")
        print(f"{move_counter} --> {move}")
        move_counter += 1

def solve():
    num_discs = int(discs_entry.get())
    selected_algorithm = algorithm_var.get()
    time_taken, moves = solve_tower_of_hanoi(num_discs, selected_algorithm)
    display_moves(moves)

    time_label.config(text=f"Time taken: {time_taken:.6f} seconds")

#--------------------------------------------------------------
# -------------------------------------------------------------

import pygame
import sys

# Hanoi Kulesi problemini çözen fonksiyon
def hanoi(n, source, target, auxiliary, moves):
    if n > 0:
        hanoi(n - 1, source, auxiliary, target, moves)
        moves.append((source, target))
        hanoi(n - 1, auxiliary, target, source, moves)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
root = tk.Tk()
root.title("Tower of Hanoi Solver")

discs_label = tk.Label(root, text="Enter the number of discs:")
discs_label.pack()

discs_entry = tk.Entry(root)


discs_entry.pack()

algorithm_var = tk.StringVar()
algorithm_var.set("Recursive")
algorithm_label = tk.Label(root, text="Choose Algorithm:")
algorithm_label.pack()

recursive_radio = tk.Radiobutton(root, text="Recursive", variable=algorithm_var, value="Recursive")
recursive_radio.pack()

iterative_radio = tk.Radiobutton(root, text="Iterative", variable=algorithm_var, value="Iterative")
iterative_radio.pack()

solve_button = tk.Button(root, text="Solve", command=solve)
solve_button.pack()

time_label = tk.Label(root, text="Time taken: ")
time_label.pack()

moves_list = tk.Listbox(root, width=50, height=15)
moves_list.pack()

root.mainloop()

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Pygame penceresini başlatma
pygame.init()
win_size = (800, 600)
win = pygame.display.set_mode(win_size)

# Disklerin ve direklerin boyutları ve konumları
disk_height = 20
disk_max_width = win_size[0] // 3
disk_min_width = disk_max_width // 4
peg_height = win_size[1] // 2
peg_width = 10
peg_gap = win_size[0] // 3
font = pygame.font.Font(None, 36)

# Hanoi Kulesi problemini çöz ve hareketleri al
num_disks = 4
moves = []
hanoi(num_disks, 0, 2, 1, moves)

# Diskleri oluştur
disks = []
for i in range(num_disks):
    width = disk_min_width + (i * (disk_max_width - disk_min_width)) // (num_disks - 1)
    disks.append(pygame.Rect(0, 0, width, disk_height))

# Diskleri başlangıç direğine yerleştir
pegs = [[] for _ in range(3)]
for i in range(num_disks - 1, -1, -1):
    disks[i].centerx = peg_gap // 2
    disks[i].bottom = win_size[1] - (disk_height * (num_disks - i - 1))
    pegs[0].append(disks[i])

# Oyun döngüsü
move_num = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and move_num < len(moves):
            disk = pegs[moves[move_num][0]].pop()
            disk.centerx = peg_gap // 2 + moves[move_num][1] * peg_gap
            disk.bottom = win_size[1] - disk_height * len(pegs[moves[move_num][1]])
            pegs[moves[move_num][1]].append(disk)
            move_num += 1

    win.fill((255, 255, 255))

    # Direkleri çiz
    for i in range(3):
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(peg_gap // 2 + i * peg_gap - peg_width // 2, win_size[1] - peg_height, peg_width, peg_height))

    # Diskleri çiz
    for peg in pegs:
        for disk in peg:
            pygame.draw.rect(win, (255, 0, 0), disk)

    # Durum metnini çiz
    if move_num < len(moves):
        text = font.render("Next Move", True, (0, 128, 0))
    else:
        text = font.render("Finished", True, (0, 128, 0))
    win.blit(text, (win_size[0] - text.get_width() - 10, 10))

    # Hamle sayısını çiz
    move_text = font.render(f"Movement: {move_num}", True, (0, 0, 128))
    win.blit(move_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
