import tkinter as tk
couleurs=['red','blue','green','yellow']
current_guess=[]
guess_labels = []
taille_code=4
def choisir_couleur(couleur):
    if len(current_guess)<taille_code:
        current_guess.append(couleur)
        actualise_code()
def actualise_code():
    i=0
    for label in guess_labels:
        if i<len(current_guess):
            label.config(bg=current_guess[i])
        else:
            label.config(bg="gray")
        i+=1
def confirmer():
    print("le code devinee:", current_guess)
    current_guess.clear()
    actualise_code()

window=tk.Tk()
window.title("mastermind")
window.geometry("1280x720")
#bouton pour choisir les couleurs
couleur_frame=tk.Frame(window)
couleur_frame.pack(pady=10)
for couleur in couleurs:
    bouton = tk.Button(couleur_frame, bg=couleur, width=5, height=2, command=lambda c=couleur: choisir_couleur(c))
    bouton.pack(side=tk.LEFT, padx=5)
#bouton pour afficher les couleurs choisie
guess_frame = tk.Frame(window)
guess_frame.pack(pady=10)
for _ in range(taille_code):
    label = tk.Label(guess_frame, bg="gray", width=5, height=2)
    label.pack(side=tk.LEFT, padx=5)
    guess_labels.append(label)
#bouton pour confirmer
submit_button = tk.Button(window, text="confirmer", font=("Arial", 14), command=confirmer)
submit_button.pack(pady=10)
window.mainloop()