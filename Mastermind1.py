import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json

COLORS = ['red', 'blue', 'green', 'yellow']
CODE_LENGTH = 4
MAX_ATTEMPTS = 10
SAVE_DIR = 'C:/Users/pc/Desktop/mastermind/Mastermind_saves'

game_mode = None
secret_code = []
current_guess = []
attempts_left = MAX_ATTEMPTS
guess_history = []



    historique_label = tk.Label(window, text="Historique des essais:", font=("Arial", 12))
    historique_label.pack(pady=5)
    historique_text = tk.Text(window, height=10, width=60, state='disabled')
    historique_text.pack(pady=5,expand=True)




    if load:
        historique_text.config(state='normal')
        historique_text.delete('1.0', tk.END)
        for guess, black, white in guess_history:
            historique_text.insert(tk.END, f"{guess}, avec {black} noir et {white} blanc\n")
        historique_text.config(state='disabled')




#Jeu multi
def mode_2_joueurs(load=False):
    global game_mode, secret_code, attempts_left, current_guess, guess_history
    game_mode = 'multi'
    window_mode_jeu.destroy()
    if not load:
        secret_code = []
        attempts_left = MAX_ATTEMPTS
        current_guess = []
        guess_history = []
        setup_secret_code_selection()
    else:
        create_game_ui(load=True)

#code secret seulement pour multi joueur
def setup_secret_code_selection():
    def confirm():
        if len(secret_code) == CODE_LENGTH:
            secret_window.destroy()
            create_game_ui()
        else:
            messagebox.showwarning("Attention", "Choisissez 4 couleurs.")

    def add_color(color):
        if len(secret_code) < CODE_LENGTH:
            secret_code.append(color)
            update_labels()

    def update_labels():
        for i in range(CODE_LENGTH):
            labels[i].config(bg=secret_code[i] if i < len(secret_code) else "gray")

    def undo():
        secret_code.pop()
        update_labels()





    guess_history.append((current_guess.copy(), black_pegs, white_pegs))
    historique_text.config(state= 'normal')
    historique_text.insert(tk.END, f"{current_guess}, avec {black_pegs} noir et {white_pegs} blanc\n")
    historique_text.config(state='disabled')

    if black_pegs == CODE_LENGTH:
        messagebox.showinfo("information", f"bravo! le code est bien: {secret_code}")
        window.destroy()
        show_main_menu()
    else:
        attempts_left -= 1
        attempts_label.config(text=f"Tentatives restante: {attempts_left}")
        if attempts_left == 0:
            messagebox.showinfo("fin du jeu", f"domage le code est : {secret_code}")
            window.destroy()
            show_main_menu()
        else:
            current_guess = []
            update_guess_display()




def set_difficulty(level):
    global CODE_LENGTH, MAX_ATTEMPTS, COLORS
    if level == 'facile':
        CODE_LENGTH = 4
        MAX_ATTEMPTS = 10
        COLORS = ['red', 'blue', 'green', 'yellow']
    elif level == 'moyen':
        CODE_LENGTH = 5
        MAX_ATTEMPTS = 8
        COLORS = ['red', 'blue', 'green', 'yellow', 'orange']
    elif level == 'difficile':
        CODE_LENGTH = 6
        MAX_ATTEMPTS = 8
        COLORS = ['red', 'blue', 'green', 'yellow', 'orange', 'purple'
    elif level == "test":
        CODE_LENGTH = 8
        MAX_ATTEMPTS = 999
        COLORS = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown']

def show_difficulty_menu():
    difficulty_window = tk.Toplevel()
    difficulty_window.title("Choisir la difficulté")

    label=tk.Label(difficulty_window, text="Sélectionnez une difficulté", font=("Arial", 18))
    label.pack(pady=10)

    btn_facile = tk.Button(difficulty_window, text="Facile", font=("Arial", 14), command=lambda: [set_difficulty('facile'), difficulty_window.destroy()])
    btn_facile.pack(pady=5)
    btn_moyen = tk.Button(difficulty_window, text="Moyen", font=("Arial", 14), command=lambda: [set_difficulty('moyen'), difficulty_window.destroy()])
    btn_moyen.pack(pady=5)
    btn_difficile = tk.Button(difficulty_window, text="Difficile", font=("Arial", 14), command=lambda: [set_difficulty('difficile'), difficulty_window.destroy()])
    btn_difficile.pack(pady=5)
    btn_test = tk.Button(difficulty_window, text="Test", font=("Arial", 14), command=lambda: [set_difficulty('test'), difficulty_window.destroy()])
    btn_test.pack(pady=5)
