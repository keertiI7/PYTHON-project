import tkinter as tk
from tkinter import ttk, messagebox
from string import ascii_uppercase
import random
from PIL import Image, ImageTk
import pygame
import json

class ImageGallery(tk.Frame):
    def __init__(self, master, image_paths, transition_callback):
        super().__init__(master)
        self.master = master
        self.image_paths = image_paths
        self.image_index = 0
        self.transition_callback = transition_callback

        self.image_label = tk.Label(self)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        arrow_image_path = r"C:\Users\Keerti\OneDrive\Desktop\wise prog\right arrow.png"
        arrow_image = Image.open(arrow_image_path)
        arrow_image = arrow_image.resize((60, 60), Image.LANCZOS)
        self.arrow_photo = ImageTk.PhotoImage(arrow_image)

        self.next_button = ttk.Button(self, image=self.arrow_photo, command=self.show_next_image)
        self.next_button.place(relx=0.95, rely=0.95, anchor=tk.SE)

        arrow_left_image_path = r"C:\Users\Keerti\OneDrive\Desktop\wise prog\left arrow.png"
        arrow_left_image = Image.open(arrow_left_image_path)
        arrow_left_image = arrow_left_image.resize((60, 60), Image.LANCZOS)
        self.arrow_left_photo = ImageTk.PhotoImage(arrow_left_image)

        self.prev_button = ttk.Button(self, image=self.arrow_left_photo, command=self.show_prev_image)
        self.prev_button.place(relx=0.05, rely=0.95, anchor=tk.SW)

        self.show_image()

        # Initialize and play background music
        pygame.mixer.init()
        pygame.mixer.music.load(r"C:\Users\Keerti\OneDrive\Desktop\wise prog\hangaudio.mp3")
        pygame.mixer.music.play(-1)  # -1 to loop the music

    def show_image(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        image_path = self.image_paths[self.image_index]
        image = Image.open(image_path)
        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

        if self.image_index == 0:
            self.prev_button.place_forget()
        else:
            self.prev_button.place(relx=0.05, rely=0.95, anchor=tk.SW)

    def show_next_image(self):
        self.image_index += 1
        if self.image_index >= len(self.image_paths):
            self.transition_callback()
        else:
            self.show_image()

    def show_prev_image(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()

class AnimatedGIF(tk.Label):
    def __init__(self, master, path, width, height, delay=100):
        super().__init__(master)
        self._master = master
        self._path = path
        self._delay = delay
        self._width = width
        self._height = height

        self._image = Image.open(self._path)
        self._frames = self._prepare_frames(self._image)
        self._frame_index = 0
        self.config(image=self._frames[self._frame_index])

        self._animate()

    def _prepare_frames(self, image):
        frames = []
        try:
            while True:
                frame = image.copy().convert("RGBA")
                frame = frame.resize((self._width, self._height), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
                image.seek(image.tell() + 1)
        except EOFError:
            pass
        return frames

    def _animate(self):
        self._frame_index = (self._frame_index + 1) % len(self._frames)
        self.config(image=self._frames[self._frame_index])
        self._master.after(self._delay, self._animate)

def start_hangman_game(root, player_name):
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="lightblue")
    frame.pack(fill=tk.BOTH, expand=True)

    gif_path = r"C:\Users\Keerti\OneDrive\Desktop\wise prog\resize hang.gif"
    gif = AnimatedGIF(frame, gif_path, root.winfo_screenwidth(), root.winfo_screenheight())
    gif.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text="WELCOME TO HANGMAN", font=("Comic Sans MS", 36, "bold"), fg="green")
    title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    start_button = tk.Button(frame, text="START", font=("Comic Sans MS", 18, "bold"), command=lambda: start_hangman_game_play(root, frame, player_name))
    start_button.place(relx=0.95, rely=0.95, anchor=tk.SE)

def start_hangman_game_play(root, frame, player_name):
    global score
    score = 0
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    word_list = ["anita","ramesh","manojkumar","faithmanjusha","saikrishna","teja","suryanarayana","sowmya","ashokkumar","sundari","harshini", "bhanusri", "akanksha", "snikitha", "akshitha", "anoohya", "jeevana", "satvika", "ananya",
                 "dharanidevi", "priya", "nagaananya", "mounika", "ishanvi", "priyamvada", "likitha", "akshaya", "bhavishya", "sravani",
                 "sumedha", "srividya", "praneetha", "sevitha", "thamkin", "lakshmiyasavi", "lahari", "rasagna", "varsha", "vaishnavi", "sania",
                 "sahasraanjali", "yasavi", "adifasaniya", "lohitha", "qhajistha", "harshitha", "yuvika", "sreshta", "haripriya", "harika",
                 "sharmada", "varshini", "shruthi", "manya", "karuna", "sohana", "pooja", "rishika", "gayathri", "tejasree",
                 "sahasra", "vaidehi", "shreya", "leisha", "akhila", "keerti", "hansini"]

    def load_and_resize_image(image_path, size=(300, 300)):
        img = Image.open(image_path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    photos = [load_and_resize_image(f"{i}.png") for i in range(7)]

    def newGame():
        global the_word_withSpaces
        global numberOfGuesses
        global letters_buttons
        global the_word

        numberOfGuesses = 0
        imgLabel.config(image=photos[0])
        the_word = random.choice(word_list).upper()
        the_word_withSpaces = " ".join(the_word)
        lblWord.set(" ".join("_" * len(the_word)))
        for btn in letters_buttons:
            btn.config(state="normal")
        scoreLabel.config(text=f"Score: {score}")

    def guess(letter):
        global numberOfGuesses
        global letters_buttons
        global score
        if numberOfGuesses < 7:
            txt = list(the_word_withSpaces)
            guessed = list(lblWord.get())
            if the_word_withSpaces.count(letter) > 0:
                for c in range(len(txt)):
                    if txt[c] == letter:
                        guessed[c] = letter
                lblWord.set("".join(guessed))
                if lblWord.get() == the_word_withSpaces:
                    score += 10
                    scoreLabel.config(text=f"Score: {score}")
                    messagebox.showinfo("Hangman", "You Guessed it! You Won!")
                    newGame()
            else:
                numberOfGuesses += 1
                imgLabel.config(image=photos[numberOfGuesses])
                if numberOfGuesses == 6:
                    messagebox.showinfo("Hangman", f"Game Over! The correct word was: {the_word}")
                    newGame()

            for btn in letters_buttons:
                if btn.cget('text') == letter:
                    btn.config(state="disabled")

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    inner_frame = tk.Frame(frame, bg="lightblue")
    inner_frame.grid(row=0, column=0, padx=20, pady=20)

    imgLabel = tk.Label(inner_frame, bg="lightblue")
    imgLabel.grid(row=0, column=0, columnspan=9, padx=10, pady=10)
    imgLabel.config(image=photos[0])

    lblWord = tk.StringVar()
    tk.Label(inner_frame, textvariable=lblWord, font=("Consolas", 24, "bold"), bg="lightblue").grid(row=1, column=0, columnspan=9, padx=10, pady=10)

    player_name_label = tk.Label(inner_frame, text=f"Player: {player_name}", font=("Comic Sans MS", 18, "bold"), bg="lightblue")
    player_name_label.grid(row=2, column=0, columnspan=9, pady=10)

    scoreLabel = tk.Label(inner_frame, text=f"Score: {score}", font=("Helvetica", 18), bg="lightblue")
    scoreLabel.grid(row=3, column=0, columnspan=9, pady=10)

    letters_buttons = []
    n = 0
    for c in ascii_uppercase:
        style = {'font': ('Helvetica', 24, 'bold'), 'background': '#3498db', 'foreground': 'white', 'borderwidth': 2,
                 'relief': 'raised', 'width': 4, 'height': 2}
        btn = tk.Button(inner_frame, text=c, command=lambda c=c: guess(c), **style)
        btn.grid(row=4 + n // 9, column=n % 9, padx=5, pady=5)
        letters_buttons.append(btn)
        n += 1

    exit_button = tk.Button(inner_frame, text="Exit", command=lambda: exit_game(root, player_name, score), font=("Helvetica 18 bold"), bg="#e74c3c", fg="white", bd=2, relief="raised")
    exit_button.grid(row=6, column=8, sticky="NSWE", padx=5, pady=5)

    newGame()

def show_leaderboard():
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.attributes('-fullscreen', True)
    leaderboard_window.configure(bg="lightblue")

    frame = tk.Frame(leaderboard_window, bg="lightblue")
    frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text="LEADERBOARD", font=("Algerian", 40, "bold"), bg="lightblue", fg="green")
    title_label.pack(pady=20)

    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = {}

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    table_frame = tk.Frame(frame, bg="lightblue")
    table_frame.pack(pady=20)

    for i, (player, score) in enumerate(sorted_leaderboard, start=1):
        player_label = tk.Label(table_frame, text=f"{i}. {player}", font=("Comic Sans MS", 24), bg="lightblue", anchor="w")
        player_label.grid(row=i, column=0, padx=20, pady=5, sticky="w")

        score_label = tk.Label(table_frame, text=f"{score}", font=("Comic Sans MS", 24), bg="lightblue", anchor="e")
        score_label.grid(row=i, column=1, padx=20, pady=5, sticky="e")

    exit_button = tk.Button(frame, text="Exit", command=lambda: exit_application(leaderboard_window), font=("Helvetica 18 bold"), bg="#e74c3c", fg="white", bd=2, relief="raised")
    exit_button.pack(pady=20)

def exit_application(leaderboard_window):
    leaderboard_window.destroy()
    root.destroy()

def exit_game(root, player_name, score):
    save_score(player_name, score)
    pygame.mixer.music.stop()
    show_leaderboard()

def save_score(player_name, score):
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = {}

    if player_name in leaderboard:
        if score > leaderboard[player_name]:
            leaderboard[player_name] = score
    else:
        leaderboard[player_name] = score

    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)

def prompt_player_name(root):
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="lightblue")
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text="Enter your name:", font=("Comic Sans MS", 24), bg="lightblue")
    label.pack(pady=20)

    entry = tk.Entry(frame, font=("Comic Sans MS", 24))
    entry.pack(pady=10)

    start_button = tk.Button(frame, text="Start Game", font=("Helvetica 18 bold"), bg="#3498db", fg="white", bd=2, relief="raised",
                             command=lambda: start_hangman_game(root, entry.get()))
    start_button.pack(pady=20)

if __name__ == "__main__":
    def transition_to_hangman():
        app.pack_forget()
        prompt_player_name(root)

    root = tk.Tk()
    root.title("Image Gallery and Hangman Game")
    root.attributes('-fullscreen', True)

    image_paths = [
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\home page final.png",
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\rule 1.png",
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\rule2 .png",
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\rule3.png",
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\rule 4.png",
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\rule 5.png",
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\rule 6.png",
        r"C:\Users\Keerti\OneDrive\Desktop\wise prog\rule 7.png"
    ]

    app = ImageGallery(root, image_paths, transition_to_hangman)
    app.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
