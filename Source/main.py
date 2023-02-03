import os.path
from PlayOnPress import KeyboardPlayer
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pickle
from functions import *
from style import *

combinations = {}
no_combinations = set()

currently_pressed = set()

chosen_file = ""


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")
        self.title("TypeTheSound")
        self.config(background=bg)
        add_style()

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Datei", menu=self.filemenu)
        self.filemenu.add_command(label="Alle löschen", command=self.delete_all)
        self.filemenu.add_command(label="Öffnen", command=self.load_configuration)
        self.filemenu.add_command(label="Speichern", command=self.save_configuration)
        self.filemenu.add_command(label="Beenden", command=self.quit)

        self.add_frame = Frame(self)
        self.add_frame.columnconfigure(1, weight=2)
        self.combi_frame = Frame(self)
        self.combi_frame.columnconfigure(0, weight=2)
        self.keys_label = Label(self.add_frame)

        self.file_button = Button(self.add_frame, command=self.open_music_file, text="Datei öffnen (MP3, OGG oder WAV)")

        Label(self.add_frame, text="Gedrückte Tasten:").grid(row=0, column=0, pady=10, sticky="we", padx=(0, 10))
        self.keys_label.grid(row=0, column=1, pady=10, sticky="we")

        Label(self.add_frame, text="Datei:").grid(row=1, column=0, pady=10, sticky="we")
        self.file_button.grid(row=1, column=1, pady=10, sticky="we")

        self.add_button = Button(self.add_frame, command=self.add_combi,
                                 text="Tastenkombination gedrückt halten und hier klicken.")
        self.add_button.grid(column=0, columnspan=2, pady=10, sticky="we")

        self.add_frame.pack(fill="x", padx=20, pady=10)
        self.combi_frame.pack(fill="x", padx=20, pady=20)

    def update_combi_frame(self):
        for s in self.combi_frame.grid_slaves():
            s.destroy()

        for i, combi in enumerate(combinations):
            row = i

            name = shorten_path(combinations[combi])
            combination = pretty_combination(combi)
            text = f"{name}: {combination}"
            Button(self.combi_frame, text=text, command=lambda path=combinations[combi]: player.play_sound(path)) \
                .grid(row=row, column=0, pady=10, sticky="we")

            Button(self.combi_frame, text="x", command=lambda combi=combi: self.delete_combi(combi)) \
                .grid(row=row, column=1, sticky="we")

        for i, path in enumerate(no_combinations):
            row = i + len(combinations) + 1

            text = shorten_path(path)
            Button(self.combi_frame, text=text, command=lambda path=path: player.play_sound(path)) \
                .grid(row=row, column=0, pady=10, sticky="we")

            Button(self.combi_frame, text="x", command=lambda path=path: self.delete_no_combi(path)) \
                .grid(row=row, column=1, sticky="we")

    def add_combi(self):
        key = frozenset(currently_pressed)
        if len(key) != 0:
            combinations[key] = chosen_file
        else:
            no_combinations.add(chosen_file)
        self.file_button.config(text="Datei öffnen (MP3, OGG oder WAV)")
        self.update_combi_frame()

    def delete_combi(self, combi):
        if player.currently_playing == combinations[combi]:
            player.stop_playback()
        combinations.pop(combi)
        self.update_combi_frame()

    def delete_no_combi(self, path):
        if player.currently_playing == path:
            player.stop_playback()
        no_combinations.remove(path)
        self.update_combi_frame()

    def delete_all(self):
        player.stop_playback()
        no_combinations.clear()
        combinations.clear()
        self.update_combi_frame()

    def open_music_file(self):
        global chosen_file
        chosen = askopenfilename(filetypes=[("Audiodateien", ".mp3 .ogg .wav")])
        if chosen != "":
            if chosen.endswith(".mp3") or chosen.endswith(".ogg") or chosen.endswith(".wav"):
                chosen_file = chosen
                self.file_button.config(text=chosen_file.split("/")[-1])
            else:
                # TODO: Unsupported Filetype Error
                pass

    def load_configuration(self):
        savefile = askopenfilename(filetypes=(("TypeTheSound Datei", ".tts"),))
        if savefile != "":
            with open(savefile, "rb") as f:
                data = pickle.load(f)
                self.delete_all()
                for combi in data["combinations"].keys():
                    if os.path.isfile(data["combinations"][combi]):
                        combinations[combi] = data["combinations"][combi]
                for path in data["no_combinations"]:
                    if os.path.isfile(path):
                        no_combinations.add(path)
        self.update_combi_frame()

    def save_configuration(self):
        data = {
            "combinations": combinations,
            "no_combinations": no_combinations
        }
        savefile = asksaveasfilename(filetypes=(("TypeTheSound Datei", ".tts"),))
        if savefile != "":
            with open(savefile, "wb") as f:
                pickle.dump(data, f)


root = MainWindow()

player = KeyboardPlayer(combinations, currently_pressed, root.keys_label, True)
player.start()

root.update_combi_frame()

root.mainloop()
