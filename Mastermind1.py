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

#Sauvegarde et chargement
def save_game():
    filename = filedialog.asksaveasfilename(defaultextension=".json", initialdir=SAVE_DIR,
                                            filetypes=[("JSON Files", "*.json")],
                                            title="Sauvegarder la partie")
    if not filename:
        return
    game_data = {
        'game_mode': game_mode,
        'secret_code': secret_code,
        'attempts_left': attempts_left,
        'current_guess': current_guess,
        'guess_history': guess_history,
        'max_attempts': MAX_ATTEMPTS,
        'code_length': CODE_LENGTH,
        'colors': COLORS
    }
    try:
        with open(filename, 'w') as f:
            json.dump(game_data, f)
        messagebox.showinfo("Sauvegarde", "Le jeu a été sauvegardé !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de sauvegarde: {e}")

def load_game():
    global game_mode, secret_code, attempts_left, current_guess, guess_history
    filename = filedialog.askopenfilename(initialdir=SAVE_DIR, title="Charger la partie",
                                          filetypes=[("JSON Files", "*.json")])
    if not filename:
        return
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        game_mode = data['game_mode']
        secret_code = data['secret_code']
        attempts_left = data['attempts_left']
        current_guess = data['current_guess']
        guess_history = data.get('guess_history',[])

        if game_mode == 'single':
            mode_1_joueur(load=True)
        elif game_mode == 'multi':
            mode_2_joueurs(load=True)
        else:
            raise ValueError("Mode de jeu invalide")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de chargement: {e}")

#Interface menu principal
def show_main_menu():
    global window_mode_jeu
    window_mode_jeu = tk.Tk()
    window_mode_jeu.title("Mastermind")
    window_mode_jeu.geometry("900x500")
    menu = tk.Menu(window_mode_jeu)
    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Regle du jeu", command=regle_du_jeu)
    file_menu.add_separator()
    file_menu.add_command(label="Quitter", command=window_mode_jeu.quit)
    menu.add_cascade(label="Fichier", menu=file_menu)
    window_mode_jeu.config(menu=menu)

    frame = tk.Frame(window_mode_jeu)
    frame.pack(pady=50)

    btn_Mode_solo = tk.Button(frame, text="Mode 1 joueur", font=("Arial", 20), command=mode_1_joueur)
    btn_Mode_solo.pack(pady=10)
    btn_Mode_multi = tk.Button(frame, text="Mode 2 joueurs", font=("Arial", 20), command=mode_2_joueurs)
    btn_Mode_multi.pack(pady=10)
    btn_continuer = tk.Button(frame, text="Continuer", font=("Arial", 20), command=load_game)
    btn_continuer.pack(pady=10)
    button_difficulty = tk.Button(frame, text="choisir difficulté", font=("Arial", 20), command=show_difficulty_menu)
    button_difficulty.pack(pady=10)
    btn_quit = tk.Button(frame, text="Quitter", font=("Arial", 20), command=quit)
    btn_quit.pack(pady=10)

    window_mode_jeu.mainloop()

#Interface de jeu
def create_game_ui(load=False):
    global window, attempts_label, guess_labels ,historique_label ,historique_text,guess_history

    window = tk.Tk()
    window.title("Mastermind")
    window.geometry("1280x720")
    create_menu(window)

    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True)



    historique_label = tk.Label(window, text="Historique des essais:", font=("Arial", 12))
    historique_label.pack(pady=5)
    historique_text = tk.Text(window, height=10, width=60, state='disabled')
    historique_text.pack(pady=5,expand=True)


    game_frame = tk.Frame(main_frame)
    game_frame.pack(side=tk.RIGHT, expand=True)

    attempts_label = tk.Label(game_frame, text=f"Tentatives restantes: {attempts_left}", font=("Arial", 14))
    attempts_label.pack(pady=10)

    color_frame = tk.Frame(game_frame)
    color_frame.pack()
    for color in COLORS:
        btn = tk.Button(color_frame, bg=color, width=5, height=2, command=lambda c=color: select_color(c))
        btn.pack(side=tk.LEFT, padx=5)

    guess_frame = tk.Frame(game_frame)
    guess_frame.pack(pady=10)
    guess_labels = []
    for _ in range(CODE_LENGTH):
        label = tk.Label(guess_frame, bg="gray", width=5, height=2)
        label.pack(side=tk.LEFT, padx=5)
        guess_labels.append(label)

    btn_Retour = tk.Button(game_frame, text="Retour", command=Undo)
    btn_Retour.pack(pady=5)
    btn_Confirmer = tk.Button(game_frame, text="Confirmer", command=submit_guess)
    btn_Confirmer.pack(pady=5)



    if load:
        historique_text.config(state='normal')
        historique_text.delete('1.0', tk.END)
        for guess, black, white in guess_history:
            historique_text.insert(tk.END, f"{guess}, avec {black} noir et {white} blanc\n")
        historique_text.config(state='disabled')
   window.mainloop()


#Jeu solo 
def mode_1_joueur(load=False):
    global game_mode, secret_code, attempts_left, current_guess, guess_history
    game_mode= 'single'
    window_mode_jeu.destroy()
    if not load:
        secret_code = []
        for _ in range (CODE_LENGTH):
            secret_code.append(random.choice(COLORS))
        attempts_left = MAX_ATTEMPTS
        current_guess = []
        guess_history = []
    create_game_ui(load)
    
        
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

def select_color(color):
    global current_guess
    if len(current_guess)< CODE_LENGTH:
        current_guess.append(color)
        update_guess_display()

def update_guess_display():
    for i in range (CODE_LENGTH):
        guess_labels[i].config(bg=current_guess[i] if i < len(current_guess) else "gray")


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

#bar de menu 
def create_menu(win):
    menu=tk.Menu(win)
    file_menu=tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Retour au menu principal", command=back_menu)
    file_menu.add_command(label="Sauvegarder", command=save_game)
    file_menu.add_command(label="Regle du jeu", command=regle_du_jeu)
    file_menu.add separator()
    file_menu.add_command(label="Quitter", command=quit)
    menu.add_cascade(label="Fichier", menu=file_menu)
    win.config(menu=menu)
#                ↑     ↑
#                |     L'objet de menu que vous avez créé
#           Nom du paramètre requis par Tkinter

#Lancer le jeu
show_main_menu()
