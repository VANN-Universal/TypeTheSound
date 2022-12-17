from PlayOnPress import KeyboardPlayer
from pynput.keyboard import Controller
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from functions import *
from style import *

combinations = {}
currently_pressed = set()
stop_condition = [False]

controller = Controller()

root = tk.Tk()
root.geometry("600x600")
root.title("TypeTheSound")
root.config(background=bg)
add_style()

add_frame = Frame(root)
add_frame.columnconfigure(1, weight=2)
combi_frame = Frame(root)
combi_frame.columnconfigure(1, weight=2)
keys_label = Label(add_frame)

player = KeyboardPlayer(combinations, currently_pressed, keys_label, True)
player.start()

def update_combi_frame():
    for s in combi_frame.grid_slaves():
        s.destroy()
    for i, combi in enumerate(combinations):
        text = pretty_combination(combi)
        Button(combi_frame, text=text, command=lambda path=combinations[combi]: player.play_sound(path)).grid(row=i*2, column=0, pady=10, sticky="we")
        text = shorten_path(combinations[combi])
        Label(combi_frame, text=text).grid(row=i*2, column=1)
        def delete_combi(combi):
            combinations.pop(combi)
            update_combi_frame()
        Button(combi_frame, text="x", command=lambda combi=combi: delete_combi(combi)).grid(row=i*2, column=2, sticky="we")
        if i < len(combinations)-1:
            Separator(combi_frame).grid(row=i*2+1, column=0, columnspan=3, sticky="we")

file = ""
def openfile():
    global file
    chosen = askopenfilename(filetypes=[])
    if chosen != "":
        file = chosen
        file_button.config(text=file.split("/")[-1])

file_button = Button(add_frame, command=openfile, text="Datei öffnen")

def add_combination():
    key = frozenset(currently_pressed)
    combinations[key] = file
    update_combi_frame()
    file_button.config(text="Datei öffnen")

Label(add_frame, text="Gedrückte Tasten:").grid(row=0, column=0, pady=10, sticky="we", padx=(0, 10))
keys_label.grid(row=0, column=1, pady=10, sticky="we")
add_button = Button(add_frame, command=add_combination, text="Tastenkombination gedrückt halten und hier klicken.")
Label(add_frame, text="Datei:").grid(row=1, column=0, pady=10, sticky="we")
file_button.grid(row=1, column=1, pady=10, sticky="we")
add_button.grid(column=0, columnspan=2, pady=10, sticky="we")
add_frame.pack(fill="x", padx=20, pady=10)
combi_frame.pack(fill="x", padx=20, pady=20)
update_combi_frame()

root.mainloop()
