import tkinter as tk
couleurs=['red','blue','green','yellow']
code_secret=[]
current_guess=[]
guess_labels = []
taille_code=4
def chosir_code(couleur):
    if len(code_secret)<taille_code:
        code_secret.append(couleur)
        actualise_code()
def choisir_couleur(couleur):
    if len(current_guess)<taille_code:
        current_guess.append(couleur)
        actualise_code()
        
def test_mastermind():
    while True: #devine jusqu'a ce que les 4 soient a la bonne place
        current_guess=[] # reinitialisé a chaque fois que le joueur 2 devine
        bonne_place=0
        bonne_couleur=0
        chosir_couleur()
        for elem in code_secret:
            if elem in current_guess:
                bonne_couleur+=1
        for i in range (len(code_secret)):
            if current_guess[i]==code_secret[i]:
                bonne_place+=1
        print(f"Vous avez {bonne_couleur} couleurs trouvés, dont {bonne_place} qu sont a la bonne place")
        if bonne_place==4:
            print("Bravo8 Vous avez trouvé le code secret!")
            break
    #il faut integrer ca dans les boutons 
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