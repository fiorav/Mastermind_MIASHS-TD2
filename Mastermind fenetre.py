import tkinter as tk #biliotheque
couleurs=["red","blue","green","yellow"]
window=tk.Tk()#cree la fenetre
window.title("mastermind")#titre de la fenetre (pas tres important)
window.geometry("1280x720")#taille de la fenetre (meme chose que au dessus)
couleur_frame=tk.Frame(window)#Frame en gros c'est une boite et dedans on peut peut mettre des texte ou des boutton
couleur_frame.pack(pady=10)
for couleur in couleurs:#cree les boutton
    bouton=tk.Button(couleur_frame,bg=couleur,width=5,height=2)#width c'est la largeur et height c'est la hauteur
    bouton.pack(side=tk.LEFT, padx=5)
window.mainloop()#START GAME!

#Le jouer 1 choisi son code secret
def choix_code():
    codes=[]
    print("Joueur 1, Choisir un code secret a 4 couleurs:")
    for i in range (4):
        code=input(f"Couleur {i+1}:")
        codes.append(code)
    return codes
    print("Code secret choisi")

#le joueur 2 devine le code du joueur 1
def deviner_code(codes):
    bonne_place=0 
    while True: #devine jusqu'a ce que les 4 soient a la bonne place
        guess=[] # reinitialisé a chaque fois que le joueur 2 devine
        bonne_place=0
        bonne_couleur=0
        print("Jouer 2, Devinez le code")
        #deviner
        for i in range(4):
            devine=input(f"Couleur {i+1}:")
            guess.append(devine)
        #verifier combien sont a la bonne place
        for i in range(4):
            if guess[i]==codes[i]:
                bonne_place+=1
        #verifier combien de couleurs sont bonnes mais mal placés
        for color in guess:
            if color in codes:
                bonne_couleur+=1
        #resultats du guess
        print(f"Vous avez {bonne_couleur} couleurs trouvés, dont {bonne_place} qu sont a la bonne place")
        if bonne_place==4:
            print("Bravo!Vous avez trouve le code secret")
            break
       
#execution du code       
code_secret = choix_code()
deviner_code(code_secret)   

#JUSTE PROBLÈME SI IL Y A DES DOUBLES DANS LE GUESS ET PAS DANS LE CODE BONNE_COULEUR PREND 1 EN PLUS QUAND MEME  


