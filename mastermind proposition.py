import tkinter as tk
from tkinter import messagebox
import random

COLORS = ['red', 'blue', 'green', 'yellow']
CODE_LENGTH = 4
MAX_ATTEMPTS = 10
secret_code = []
proposition=[]
def mode_1_joueur():
    global current_guess,attempts_left
    window_mode_jeu.destroy()
    def generate_secret_code():
        return [random.choice(COLORS) for _ in range(CODE_LENGTH)]

    def get_feedback(secret_code, guess):
        black_pegs = sum(s == g for s, g in zip(secret_code, guess))
        white_pegs = sum(min(secret_code.count(c), guess.count(c)) for c in set(guess)) - black_pegs
        return black_pegs, white_pegs

    def submit_guess():
        global attempts_left, current_guess
        proposition+=current_guess
        afficher_proposition()
        if len(current_guess) < CODE_LENGTH:
            messagebox.showwarning("information", f"choisissez {CODE_LENGTH} couleurs!")
            return

        black_pegs, white_pegs = get_feedback(secret_code, current_guess)
        if black_pegs == CODE_LENGTH:
            messagebox.showinfo("information", f"bravo! le code est bien: {secret_code}")
            window.destroy()
            
        else:
            attempts_left -= 1
            attempts_label.config(text=f"Tentatives restante: {attempts_left}")
            messagebox.showinfo("information",f"info: {black_pegs} noir (position est couleur sont correcte){white_pegs} blanc (mauvaise position mais les couleur sont les bonne)")
            if attempts_left == 0:
                messagebox.showinfo("fin du jeu", f"domage le code est : {secret_code}")
                window.destroy()
            else:
                current_guess = []
                update_guess_display()

    def select_color(color):
        global current_guess
        proposition+=current_guess
        afficher_proposition()
        if len(current_guess) < CODE_LENGTH:
            current_guess.append(color)
            update_guess_display()
       


    def update_guess_display():
        for i, label in enumerate(guess_labels):
            if i < len(current_guess):
                label.config(bg=current_guess[i])
            else:
                label.config(bg="gray")
    def afficher_proposition():
        global proposition
        canvas.delete("all")
        for i, color in enumerate(proposition):
            x = i * 50 + 20
            canvas.create_rectangle(x, 10, x + 40, 50, fill=color, outline="black")
    # afficher le jeu
    window = tk.Tk()
    window.title("Mastermind")
    window.geometry("1280x720")
    # code secret
    secret_code = generate_secret_code()
    attempts_left = MAX_ATTEMPTS
    current_guess = []

    attempts_label = tk.Label(window, text=f"Tentatives restante: {attempts_left}", font=("Arial", 14))
    attempts_label.pack(pady=10)

    # bouton couleurs
    color_frame = tk.Frame(window)
    color_frame.pack(pady=10)
    for color in COLORS:
        btn = tk.Button(color_frame, bg=color, width=5, height=2, command=lambda c=color: select_color(c))
        btn.pack(side=tk.LEFT, padx=5)

    # afficher les couleurs
    guess_frame = tk.Frame(window)
    guess_frame.pack(pady=10)
    guess_labels = []
    for _ in range(CODE_LENGTH):
        label = tk.Label(guess_frame, bg="gray", width=5, height=2)
        label.pack(side=tk.LEFT, padx=5)
        guess_labels.append(label)

    # bouton confirmer
    submit_button = tk.Button(window, text="confirmer", font=("Arial", 14), command=submit_guess)
    submit_button.pack(pady=10)

    window.mainloop()

def mode_2_joueurs():
    global secret_code,secret_window
    window_mode_jeu.destroy()
    def start_game():
        global secret_code, attempts_left, current_guess
    
        if len(secret_code) < CODE_LENGTH:
            messagebox.showwarning("information",f"choisissez {CODE_LENGTH} couleurs!")
            return

        setup_main_game()  # main menu
    
    def select_secret_color(color):
        global secret_code
        if len(secret_code) < CODE_LENGTH:
            secret_code.append(color)
            update_secret_display()

    def update_secret_display():
        for i, label in enumerate(secret_labels):
            if i < len(secret_code):
                label.config(bg=secret_code[i])
            else:
                label.config(bg="gray")
    # fonction pour que le joueur 1 choisie les couleurs
    def setup_main_game():
        global attempts_left, current_guess, attempts_label, guess_labels, secret_window

        secret_window.destroy()  # fermer la fenetre secret code

        global window
        window = tk.Tk()
        window.title("Mastermind")
        window.geometry("1280x720")

        attempts_left = MAX_ATTEMPTS
        current_guess = []

        #tentatives maximales
        attempts_label = tk.Label(window, text=f"Tentatives restantes: {attempts_left}", font=("Arial", 14))
        attempts_label.pack(pady=10)

        # bouton couleur
        color_frame = tk.Frame(window)
        color_frame.pack(pady=10)
        for color in COLORS:
            btn = tk.Button(color_frame, bg=color, width=5, height=2, command=lambda c=color: select_color(c))
            btn.pack(side=tk.LEFT, padx=5)

        # afficher les couleurs choisie
        global guess_labels
        guess_frame = tk.Frame(window)
        guess_frame.pack(pady=10)
        guess_labels = []
        for _ in range(CODE_LENGTH):
            label = tk.Label(guess_frame, bg="gray", width=5, height=2)
            label.pack(side=tk.LEFT, padx=5)
            guess_labels.append(label)

        # bouton confirmer
        submit_button = tk.Button(window, text="confirmer", font=("Arial", 14), command=submit_guess)
        submit_button.pack(pady=10)

        window.mainloop()

    # fonction pour tester si la position et la couleur sont correcte
    def get_feedback(secret_code, guess):
        black_pegs = sum(s == g for s, g in zip(secret_code, guess))
        white_pegs = sum(min(secret_code.count(c), guess.count(c)) for c in set(guess)) - black_pegs
        return black_pegs, white_pegs

    def submit_guess():
        global attempts_left, current_guess
        proposition+=current_guess
        afficher_proposition()

        if len(current_guess) < CODE_LENGTH:
            messagebox.showwarning("information",f"choisissez {CODE_LENGTH} coleur!")
            return

        black_pegs, white_pegs = get_feedback(secret_code, current_guess)
        if black_pegs == CODE_LENGTH:
            messagebox.showinfo("information",f"bravo le code est bien: {secret_code}")
            window.destroy()
        else:
            attempts_left -= 1
            attempts_label.config(text=f"Tentatives restantes: {attempts_left}")
            messagebox.showinfo("information",f"info: {black_pegs} noir (position est couleur sont correcte){white_pegs} blanc (mauvaise position mais les couleur sont les bonne)")
            if attempts_left == 0:
                messagebox.showinfo(f"domage le code est: {secret_code}")
                window.destroy()
            else:
                current_guess = []
                update_guess_display()

    def select_color(color):
        global current_guess
        proposition+=current_guess
        afficher_proposition()
        if len(current_guess) < CODE_LENGTH:
            current_guess.append(color)
            update_guess_display()

    def update_guess_display():
        for i, label in enumerate(guess_labels):
            if i < len(current_guess):
                label.config(bg=current_guess[i])
            else:
                label.config(bg="gray")
    def afficher_proposition():
        global proposition
        canvas.delete("all")
        for i, color in enumerate(proposition):
            x = i * 50 + 20
            canvas.create_rectangle(x, 10, x + 40, 50, fill=color, outline="black")
    # fenetre code secret
    secret_window = tk.Tk()
    secret_window.title("choisir code secret")
    tk.Label(secret_window, text="choisissez 4 couleurs:", font=("Arial", 14)).pack(pady=10)

    # choisir couleur
    color_frame = tk.Frame(secret_window)
    color_frame.pack(pady=10)
    for color in COLORS:
        btn = tk.Button(color_frame, bg=color, width=5, height=2, command=lambda c=color: select_secret_color(c))
        btn.pack(side=tk.LEFT, padx=5)

    # secret code 
    secret_frame = tk.Frame(secret_window)
    secret_frame.pack(pady=10)
    secret_labels = []
    for _ in range(CODE_LENGTH):
        label = tk.Label(secret_frame, bg="gray", width=5, height=2)
        label.pack(side=tk.LEFT, padx=5)
        secret_labels.append(label)

    # confirm bouton
    confirm_button = tk.Button(secret_window, text="confirmer", font=("Arial", 14), command=start_game)
    confirm_button.pack(pady=10)

    secret_window.mainloop()
    

#poupées russes :(

window_mode_jeu = tk.Tk()
window_mode_jeu.title("Mastermind")
mode_jeu_frame=tk.Frame(window_mode_jeu)
mode_jeu_frame.pack()
button = tk.Button(mode_jeu_frame,text="Mode 1 joueur", font=("courrier",40), bg="white", fg="black", command=mode_1_joueur)
button.pack()
button = tk.Button(mode_jeu_frame,text="Mode 2 joueur", font=("courrier",40), bg="white", fg="black", command=mode_2_joueurs)
proposition_label=tk.Label(mode_1_joueur, text="Prpositions précédentes :")
proposition_label.grid(row=3, columnspan=proposition)

canvas = tk.Canvas(window, width=250, height=200, bg="white")
canvas.pack(pady=10)
button.pack()
window_mode_jeu.mainloop()