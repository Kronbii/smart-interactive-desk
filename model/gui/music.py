import tkinter as tk
from tkinter import filedialog
from pygame import mixer
from box import Box
import yaml
from gui import CONFIG_PATH

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def create_music_content(parent):
    def play_music():
        song = filedialog.askopenfilename(title="Choose a song", filetypes=[("Audio Files", "*.mp3 *.wav")])
        if song:
            mixer.music.load(song)
            mixer.music.play()
            label_song.config(text=f"Now Playing: {song.split('/')[-1]}")  # Display song name

    def pause_music():
        mixer.music.pause()
        label_song.config(text="Music Paused... 😴")

    def unpause_music():
        mixer.music.unpause()
        label_song.config(text="Resumed 🎶")

    def stop_music():
        mixer.music.stop()
        label_song.config(text="Music Stopped... 🎵")

    def set_volume(val):
        mixer.music.set_volume(float(val) / 100)
    parent.configure(bg=config.theme.background_color)

    # Header
    tk.Label(
        parent,
        text="🎶Music Player",
        font=(config.theme.font_family, 18),
        bg=config.theme.background_color,
        fg=config.theme.font_color
    ).pack(pady=20)

    # Song Info Label
    global label_song
    label_song = tk.Label(
        parent,
        text="No song playing",
        font=(config.theme.font_family, 12, "italic"),
        bg=config.theme.background_color,
        fg=config.theme.font_color
    )
    label_song.pack(pady=10)

    # Buttons: Play, Pause, Stop
    button_frame = tk.Frame(parent, bg=config.theme.background_color)
    button_frame.pack(pady=20)

    # Play Button
    play_button = tk.Button(
        button_frame,
        text="Play 🎧",
        command=play_music,
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        font=(config.theme.font_family, 14, "bold"),
        padx=15,
        pady=5
    )
    play_button.grid(row=0, column=0, padx=10)

    # Pause Button
    pause_button = tk.Button(
        button_frame,
        text="Pause ⏸️",
        command=pause_music,
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        font=(config.theme.font_family, 14, "bold"),
        padx=15,
        pady=5
    )
    pause_button.grid(row=0, column=1, padx=10)

    # Unpause Button
    unpause_button = tk.Button(
        button_frame,
        text="Unpause ▶️",
        command=unpause_music,
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        font=(config.theme.font_family, 14, "bold"),
        padx=15,
        pady=5
    )
    unpause_button.grid(row=0, column=2, padx=10)

    # Stop Button
    stop_button = tk.Button(
        button_frame,
        text="Stop 🛑",
        command=stop_music,
        bg=config.theme.button_color,
        fg=config.theme.button_text_color,
        font=(config.theme.font_family, 14, "bold"),
        padx=15,
        pady=5
    )
    stop_button.grid(row=0, column=3, padx=10)

    # Volume Control Label
    volume_label = tk.Label(
        parent,
        text="Volume 🎚️",
        font=(config.theme.font_family, 14),
        bg=config.theme.background_color,
        fg=config.theme.font_color
    )
    volume_label.pack(pady=10)

    # Volume Control Slider
    volume_slider = tk.Scale(
        parent,
        from_=0,
        to=100,
        orient="horizontal",
        command=set_volume,
        bg=config.theme.background_color,
        fg=config.theme.font_color,
        sliderlength=20,
        length=300  # Wider slider here
    )
    volume_slider.set(50)  # Set default volume to 50%
    volume_slider.pack(pady=10)