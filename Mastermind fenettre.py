import tkinter as tk
couleurs=['red','blue','green','yellow']
def couleur_choisie(couleur):
    print(f"choisie la couleur:{couleur}")
window=tk.Tk()
window.title("mastermind")
window.geometry("1280x720")#taille de la fenettre
couleur_frame=tk.Frame(window)
couleur_frame.pack(pady=10)
for couleur in couleurs:
    bouton=tk.Button(couleur_frame,bg=couleur,width=5,height=2)#width c'est la largeur et height c'est la hauteur
    bouton.pack(side=tk.LEFT, padx=5)
window.mainloop()#START GAME!