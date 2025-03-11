import tkinter as tk #biliotheque
couleurs=['red','blue','green','yellow']
def couleur_choisie(couleur): #fonction pour choisir une couleur
    print(f"choisie la couleur:{couleur}")
window=tk.Tk()#cree la fenetre
window.title("mastermind")#titre de la fenetre (pas tres important)
window.geometry("1280x720")#taille de la fenetre (meme chose que au dessus)
couleur_frame=tk.Frame(window)#Frame en gros c'est une boite et dedans on peut peut mettre des texte ou des boutton
couleur_frame.pack(pady=10)
for couleur in couleurs:#cree les boutton
    bouton=tk.Button(couleur_frame,bg=couleur,width=5,height=2)#width c'est la largeur et height c'est la hauteur
    bouton.pack(side=tk.LEFT, padx=5)
window.mainloop()#START GAME!
