import tkinter as tk
import random
import copy

MAX_BLOCKS = 

disk = [-1] * MAX_BLOCKS
files = []
backup = []
selected_blocks = []

class File:
    def __init__(self, name, blocks):
        self.name = name
        self.blocks = blocks

# ---------------- FUNCTIONS ---------------

def log(msg):
    output.insert(tk.END, msg + "\n")
    output.see(tk.END)

def update_grid():
    for i in range(MAX_BLOCKS):
        if disk[i] == -1:
            if i in selected_blocks:
                blocks[i].config(bg="yellow", text=str(i))
            else:
                blocks[i].config(bg="lightgray", text=str(i))
        else:
            blocks[i].config(bg="lightgreen", text=f"F{disk[i]}")

def toggle_block(i):
    if disk[i] != -1:
        return

    if i in selected_blocks:
        selected_blocks.remove(i)
    else:
        selected_blocks.append(i)

    update_grid()

def create_file():
    name = entry.get()

    if not name:
        log("Enter file name!")
        return

    for f in files:
        if f.name == name:
            log("File already exists!")
            return

    if not selected_blocks:
        log("Select blocks manually!")
        return

    for b in selected_blocks:
        disk[b] = len(files)

    files.append(File(name, selected_blocks.copy()))
    log(f"{name} created → {selected_blocks}")

    selected_blocks.clear()
    update_grid()

def delete_file():
    name = entry.get()

    for i, f in enumerate(files):
        if f.name == name:
            for b in f.blocks:
                disk[b] = -1
            files.pop(i)
            log(f"{name} deleted")
            update_grid()
            return

    log("File not found!")

def show_directory():
    for f in files:
        log(f"{f.name} → {f.blocks}")

def crash():
    global backup
    backup = copy.deepcopy(files)

    for _ in range(5):
        b = random.randint(0, MAX_BLOCKS - 1)
        disk[b] = -1

    log("⚠ Crash simulated!")
    update_grid()

def recover():
    global files

    if not backup:
        log("No backup available")
        return

    files = copy.deepcopy(backup)

    for i in range(MAX_BLOCKS):
        disk[i] = -1

    for i, f in enumerate(files):
        for b in f.blocks:
            disk[b] = i

    log("Recovery complete")
    update_grid()

def optimize():
    new_disk = [-1] * MAX_BLOCKS
    index = 0

    for i, f in enumerate(files):
        new_blocks = []
        for _ in f.blocks:
            new_disk[index] = i
            new_blocks.append(index)
            index += 1
        f.blocks = new_blocks

    for i in range(MAX_BLOCKS):
        disk[i] = new_disk[i]

    log("Disk optimized")
    update_grid()

def fragmentation():
    used = sum(1 for b in disk if b != -1)
    free = MAX_BLOCKS - used
    frag = (free / MAX_BLOCKS) * 100
    log(f"Fragmentation: {frag:.2f}%")

def search_file():
    name = entry.get()
    for f in files:
        if f.name == name:
            log(f"{name} found at {f.blocks}")
            return
    log("File not found")

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Advanced File System Simulator")
root.geometry("650x600")

title = tk.Label(root, text="File System Recovery & Optimization Tool",
                 font=("Arial", 16, "bold"), fg="blue")
title.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Create", bg="lightgreen", command=create_file).grid(row=0, column=0)
tk.Button(btn_frame, text="Delete", bg="salmon", command=delete_file).grid(row=0, column=1)
tk.Button(btn_frame, text="Directory", command=show_directory).grid(row=1, column=0)
tk.Button(btn_frame, text="Search", command=search_file).grid(row=1, column=1)
tk.Button(btn_frame, text="Crash", bg="orange", command=crash).grid(row=2, column=0)
tk.Button(btn_frame, text="Recover", command=recover).grid(row=2, column=1)
tk.Button(btn_frame, text="Optimize", bg="lightblue", command=optimize).grid(row=3, column=0)
tk.Button(btn_frame, text="Fragmentation", command=fragmentation).grid(row=3, column=1)

# Disk Grid
grid_frame = tk.Frame(root)
grid_frame.pack(pady=10)

blocks = []

for i in range(MAX_BLOCKS):
    lbl = tk.Label(grid_frame, text=str(i), width=4, height=2,
                   bg="lightgray", relief="ridge")
    lbl.grid(row=i//10, column=i%10, padx=2, pady=2)

    lbl.bind("<Button-1>", lambda e, idx=i: toggle_block(idx))

    blocks.append(lbl)

# Output box
output = tk.Text(root, height=10, width=70)
output.pack(pady=10)

root.mainloop()
