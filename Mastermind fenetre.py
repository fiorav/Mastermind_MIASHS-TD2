import tkinter as tk #biliotheque
couleurs=['red','blue','green','yellow']
window=tk.Tk()#cree la fenetre
window.title("mastermind")#titre de la fenetre (pas tres important)
window.geometry("1280x720")#taille de la fenetre (meme chose que au dessus)
couleur_frame=tk.Frame(window)#Frame en gros c'est une boite et dedans on peut peut mettre des texte ou des boutton
couleur_frame.pack(pady=10)
for couleur in couleurs:#cree les boutton
    bouton=tk.Button(couleur_frame,bg=couleur,width=5,height=2)#width c'est la largeur et height c'est la hauteur
    bouton.pack(side=tk.LEFT, padx=5)
window.mainloop()#START GAME!

def choix_code():
    codes=[]
    for i in range (4):
        code=input("Choisir une couleur pour creer un code a quatre couleurs(faire cela 4 fois):")#permet a l'utilisateur qui choisi le code secret de le mmettre dedans 
        codes.append(code) #met les couleurs choisis dans une liste 
    return codes #a enlever plus tard mais la c'est pour tester qu'il renvoie bien le code secret de l'utilisateur
print(choix_code())

def deviner_code():
    guess=[] 
    for i in range (4):
        devine=input("deviner le code du jouer numero 1")
        guess.append(devine)
    return guess
print(deviner_code)
