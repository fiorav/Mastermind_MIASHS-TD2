
import tkinter as tk
from tkinter import ttk, messagebox
import random

COLORS = ['red', 'blue', 'green', 'yellow']
CODE_LENGTH = 4
MAX_ATTEMPTS = 10

def main_menu():
    global menu_window
    menu_window = tk.Tk()
    menu_window.title("Mastermind")
    menu_window.geometry("400x300")
    menu_window.configure(bg="#f0f0f0")

    title = ttk.Label(menu_window, text="Jeu Mastermind", font=("Helvetica", 20))
    title.pack(pady=20)

    btn_1_joueur = ttk.Button(menu_window, text="Mode 1 Joueur", command=mode_1_joueur)
    btn_1_joueur.pack(pady=10)

    btn_2_joueurs = ttk.Button(menu_window, text="Mode 2 Joueurs", command=mode_2_joueurs)
    btn_2_joueurs.pack(pady=10)

    btn_quit = ttk.Button(menu_window, text="Quitter", command=menu_window.destroy)
    btn_quit.pack(pady=20)

    menu_window.mainloop()

def mode_1_joueur():
    global current_guess, attempts_left, window, secret_code
    menu_window.destroy()

    secret_code = [random.choice(COLORS) for _ in range(CODE_LENGTH)]
    current_guess = []
    attempts_left = MAX_ATTEMPTS

    window = tk.Tk()
    window.title("Mastermind - 1 Joueur")
    window.geometry("500x400")

    ttk.Label(window, text="Choisissez une combinaison de couleurs", font=("Helvetica", 14)).pack(pady=10)

    color_frame = ttk.Frame(window)
    color_frame.pack()

    for color in COLORS:
        btn = ttk.Button(color_frame, text=color, command=lambda c=color: add_color(c))
        btn.pack(side=tk.LEFT, padx=5)

    global guess_frame, attempts_label
    guess_frame = ttk.Frame(window)
    guess_frame.pack(pady=10)

    attempts_label = ttk.Label(window, text=f"Tentatives restantes: {attempts_left}")
    attempts_label.pack()

    submit_btn = ttk.Button(window, text="Confirmer", command=submit_guess)
    submit_btn.pack(pady=10)

def mode_2_joueurs():
    global entry_code, window_code
    menu_window.destroy()

    window_code = tk.Tk()
    window_code.title("Mastermind - 2 Joueurs")
    window_code.geometry("400x200")

    ttk.Label(window_code, text="Joueur 1: Entrez le code secret (ex: red blue green yellow)").pack(pady=10)

    entry_code = ttk.Entry(window_code, width=50)
    entry_code.pack(pady=10)

    ttk.Button(window_code, text="Valider", command=start_2_joueur_mode).pack(pady=10)

def start_2_joueur_mode():
    global secret_code, current_guess, attempts_left, window
    code_input = entry_code.get().strip().lower().split()

    if len(code_input) != CODE_LENGTH or any(c not in COLORS for c in code_input):
        messagebox.showerror("Erreur", f"Veuillez entrer {CODE_LENGTH} couleurs valides (séparées par des espaces).")
        return

    secret_code = code_input
    window_code.destroy()

    current_guess = []
    attempts_left = MAX_ATTEMPTS

    window = tk.Tk()
    window.title("Mastermind - Joueur 2")
    window.geometry("500x400")

    ttk.Label(window, text="Joueur 2: Devinez la combinaison", font=("Helvetica", 14)).pack(pady=10)

    color_frame = ttk.Frame(window)
    color_frame.pack()

    for color in COLORS:
        btn = ttk.Button(color_frame, text=color, command=lambda c=color: add_color(c))
        btn.pack(side=tk.LEFT, padx=5)

    global guess_frame, attempts_label
    guess_frame = ttk.Frame(window)
    guess_frame.pack(pady=10)

    attempts_label = ttk.Label(window, text=f"Tentatives restantes: {attempts_left}")
    attempts_label.pack()

    submit_btn = ttk.Button(window, text="Confirmer", command=submit_guess)
    submit_btn.pack(pady=10)

def add_color(color):
    global current_guess
    if len(current_guess) < CODE_LENGTH:
        current_guess.append(color)
        display_guess()

def display_guess():
    for widget in guess_frame.winfo_children():
        widget.destroy()

    for color in current_guess:
        lbl = tk.Label(guess_frame, text=color, bg=color, width=10)
        lbl.pack(side=tk.LEFT, padx=2)

def get_feedback(secret, guess):
    black = sum(s == g for s, g in zip(secret, guess))
    white = sum(min(secret.count(c), guess.count(c)) for c in set(guess)) - black
    return black, white

def submit_guess():
    global current_guess, attempts_left

    if len(current_guess) < CODE_LENGTH:
        messagebox.showwarning("Avertissement", f"Choisissez {CODE_LENGTH} couleurs.")
        return

    black, white = get_feedback(secret_code, current_guess)

    if black == CODE_LENGTH:
        messagebox.showinfo("Gagné", f"Bravo ! Le code était bien {secret_code}")
        window.destroy()
        return
    else:
        attempts_left -= 1
        attempts_label.config(text=f"Tentatives restantes: {attempts_left}")
        messagebox.showinfo("Résultat", f"{black} bien placés, {white} mal placés.")

        if attempts_left == 0:
            messagebox.showinfo("Perdu", f"Code secret: {secret_code}")
            window.destroy()

    current_guess = []
    display_guess()

if __name__ == "__main__":
    main_menu()
