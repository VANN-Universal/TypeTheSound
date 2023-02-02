import pygame
from pygame import mixer
from pynput.keyboard import Listener, Key
from tkinter import *
from threading import Thread
from functions import *


class KeyboardPlayer(Thread):
    def __init__(self, combinations, pressed_keys, label: Label, restart_music=False):
        super().__init__(daemon=True)
        self.currently_playing = ""
        self.combinations = combinations
        self.pressed_keys = pressed_keys
        self.label = label
        self.restart_music = restart_music
        mixer.init()

    def run(self):
        with Listener(on_press=self.key_pressed, on_release=self.key_released) as listener:
            listener.join()

    def play_sound(self, path):
        if path != self.currently_playing or self.restart_music:
            try:
                mixer.music.load(path)
                mixer.music.play()
                self.currently_playing = path
            except pygame.error:
                print("Unsupported Filetype")

    def stop_playback(self):
        mixer.music.stop()

    def key_pressed(self, key):
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            self.label.config(text=pretty_combination(self.pressed_keys))
            for combi in self.combinations:
                if all(k in self.pressed_keys for k in combi):
                    self.play_sound(self.combinations[combi])

    def key_released(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            self.label.config(text=pretty_combination(self.pressed_keys))
