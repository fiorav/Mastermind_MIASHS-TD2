import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json
import os

COLORS = ['red', 'blue', 'green', 'yellow']
CODE_LENGTH = 4
MAX_ATTEMPTS = 10
SAVE_DIR = 'C:/Users/pc/Desktop/mastermind/Mastermind_saves'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

game_mode = None
secret_code = []
current_guess = []
attempts_left = MAX_ATTEMPTS
guess_history = []

# ------------------- Sauvegarde et chargement -------------------
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
        guess_history = data.get('guess_history', [])

        if game_mode == 'single':
            mode_1_joueur(load=True)
        elif game_mode == 'multi':
            mode_2_joueurs(load=True)
        else:
            raise ValueError("Mode de jeu invalide")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de chargement: {e}")

# ------------------- Interface menu principal -------------------
def show_main_menu():
    global window_mode_jeu
    window_mode_jeu = tk.Tk()
    window_mode_jeu.title("Mastermind")
    window_mode_jeu.geometry("640x320")
    menu = tk.Menu(window_mode_jeu)
    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Regle du jeu", command=regle_du_jeu)
    file_menu.add_separator()
    file_menu.add_command(label="Quitter", command=window_mode_jeu.quit)
    menu.add_cascade(label="Fichier", menu=file_menu)
    window_mode_jeu.config(menu=menu)

    frame = tk.Frame(window_mode_jeu)
    frame.pack(pady=50)

    tk.Button(frame, text="Mode 1 joueur", font=("Arial", 20), command=mode_1_joueur).pack(pady=10)
    tk.Button(frame, text="Mode 2 joueurs", font=("Arial", 20), command=mode_2_joueurs).pack(pady=10)
    tk.Button(frame, text="Continuer", font=("Arial", 20), command=load_game).pack(pady=10)

    window_mode_jeu.mainloop()

# ------------------- Interface de jeu -------------------
def create_game_ui(load=False):
    global window, attempts_label, guess_labels, history_listbox

    window = tk.Tk()
    window.title("Mastermind")
    window.geometry("1280x720")
    create_menu(window)

    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    history_frame = tk.Frame(main_frame)
    history_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
    tk.Label(history_frame, text="Historique des essais", font=("Arial", 12)).pack()
    history_listbox = tk.Listbox(history_frame, height=25, width=30)
    history_listbox.pack()
    update_history_display()

    game_frame = tk.Frame(main_frame)
    game_frame.pack(side=tk.RIGHT, expand=True)

    attempts_label = tk.Label(game_frame, text=f"Tentatives restantes: {attempts_left}", font=("Arial", 14))
    attempts_label.pack(pady=10)

    color_frame = tk.Frame(game_frame)
    color_frame.pack()
    for color in COLORS:
        tk.Button(color_frame, bg=color, width=5, height=2, command=lambda c=color: select_color(c)).pack(side=tk.LEFT, padx=5)

    guess_frame = tk.Frame(game_frame)
    guess_frame.pack(pady=10)
    guess_labels = []
    for _ in range(CODE_LENGTH):
        label = tk.Label(guess_frame, bg="gray", width=5, height=2)
        label.pack(side=tk.LEFT, padx=5)
        guess_labels.append(label)

    tk.Button(game_frame, text="Retour", command=back).pack(pady=5)
    tk.Button(game_frame, text="Confirmer", command=submit_guess).pack(pady=5)
    window.mainloop()

# ------------------- Jeu solo -------------------
def mode_1_joueur(load=False):
    global game_mode, secret_code, attempts_left, current_guess, guess_history
    game_mode = 'single'
    window_mode_jeu.destroy()
    if not load:
        secret_code = [random.choice(COLORS) for _ in range(CODE_LENGTH)]
        attempts_left = MAX_ATTEMPTS
        current_guess = []
        guess_history = []
    create_game_ui(load)

# ------------------- Jeu multi -------------------
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

# ------------------- Saisie du code secret -------------------
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
        if secret_code:
            secret_code.pop()
            update_labels()

    global secret_window
    secret_window = tk.Tk()
    secret_window.title("Choix du code secret")

    tk.Label(secret_window, text="Choisissez 4 couleurs :", font=("Arial", 14)).pack(pady=10)

    btn_frame = tk.Frame(secret_window)
    btn_frame.pack()
    for color in COLORS:
        tk.Button(btn_frame, bg=color, width=5, height=2, command=lambda c=color: add_color(c)).pack(side=tk.LEFT, padx=5)

    label_frame = tk.Frame(secret_window)
    label_frame.pack(pady=10)
    labels = [tk.Label(label_frame, bg="gray", width=5, height=2) for _ in range(CODE_LENGTH)]
    for l in labels:
        l.pack(side=tk.LEFT, padx=5)

    tk.Button(secret_window, text="Retour", command=undo).pack(pady=5)
    tk.Button(secret_window, text="Confirmer", command=confirm).pack(pady=5)
    secret_window.mainloop()

# ------------------- Logique de jeu -------------------
def get_feedback(secret, guess):
    black = sum([1 for i in range(CODE_LENGTH) if secret[i] == guess[i]])
    white = sum(min(secret.count(c), guess.count(c)) for c in set(guess)) - black
    return black, white

def submit_guess():#confimer
    global attempts_left, current_guess, guess_history

    if len(current_guess) < CODE_LENGTH:
        messagebox.showwarning("information", f"choisissez {CODE_LENGTH} couleurs!")
        return

    black_pegs, white_pegs = get_feedback(secret_code, current_guess)
    guess_history.append((current_guess.copy(), black_pegs, white_pegs))
    update_history_display()

    if black_pegs == CODE_LENGTH:
        messagebox.showinfo("information", f"bravo! le code est bien: {secret_code}")
        window.destroy()
        show_main_menu()
    else:
        attempts_left -= 1
        attempts_label.config(text=f"Tentatives restante: {attempts_left}")
        messagebox.showinfo("information",f"{black_pegs} pions noir (position est couleur sont correcte)\n{white_pegs} pions blanc (mauvaise position mais les couleur sont les bonne)")
        if attempts_left == 0:
            messagebox.showinfo("fin du jeu", f"domage le code est : {secret_code}")
            window.destroy()
            show_main_menu()
        else:
            current_guess = []
            update_guess_display()

def update_history_display():
    if 'history_listbox' in globals():
        history_listbox.delete(0, tk.END)
        for guess, black, white in guess_history:
            history_listbox.insert(tk.END, f"{' '.join(guess)} => {black} noir, {white} blanc")

def select_color(color):
    global current_guess
    if len(current_guess) < CODE_LENGTH:
        current_guess.append(color)
        update_guess_display()

def update_guess_display():
    for i in range(CODE_LENGTH):
        guess_labels[i].config(bg=current_guess[i] if i < len(current_guess) else "gray")

def back():
    if current_guess:
        current_guess.pop()
        update_guess_display()

def regle_du_jeu():
    rules_window = tk.Toplevel()
    rules_window.title("Règles du Jeu Mastermind")
    rules_window.geometry("600x400")
    
    # Créer un frame de texte et une barre de défilement
    frame = tk.Frame(rules_window)
    frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text.pack(fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=text.yview)
    
    rules_text = """
    Règles du Jeu Mastermind:

    1. Objectif du Jeu:
    - En mode 1 joueur: Deviner le code secret généré par l'ordinateur.
    - En mode 2 joueurs: Le Joueur 1 crée un code secret que le Joueur 2 doit deviner.

    2. Mécanique de Jeu:
    - Le code secret est composé de 4 couleurs.
    - Les couleurs possibles sont: rouge, bleu, vert et jaune.
    - Les couleurs peuvent être répétées dans le code.

    3. Feedback:
    - Pions noirs: Nombre de couleurs correctement placées.
    - Pions blancs: Nombre de couleurs correctes mais mal placées.
    
    4. Nombre d'Essais:
    - Vous avez 10 tentatives pour deviner le code secret.
    
    5. Commandes:
    - Cliquez sur les boutons de couleur pour faire une proposition.
    - Utilisez le bouton "Retour" pour corriger votre sélection.
    - Cliquez sur "Confirmer" pour valider votre proposition.
    """
    
    text.insert(tk.END, rules_text)
    text.config(state=tk.DISABLED) #pour que le text devien non modifiable

def back_menu():
    window.destroy()
    show_main_menu() 

# ------------------- Menu -------------------
def create_menu(win):
    menu = tk.Menu(win)
    file_menu = tk.Menu(menu, tearoff=0)
    file_menu.add_command(label="Retour au menu principal",command=back_menu)
    file_menu.add_command(label="Sauvegarder", command=save_game)
    file_menu.add_command(label="Regle du jeu", command=regle_du_jeu)
    file_menu.add_separator()
    file_menu.add_command(label="Quitter", command=win.quit)
    menu.add_cascade(label="Fichier", menu=file_menu)
    win.config(menu=menu)
    #           ↑     ↑
    #           /     L'objet de menu que vous avez créé
    #           Nom du paramètre requis par Tkinter

# ------------------- Lancer -------------------
show_main_menu()