import tkinter as tk 
from tkinter import messagebox

def sauvegarder():
    messagebox.showinfo("Sauvegarder", "Jeu sauvegardé")
    #code pour sauvegarder le jeu

def abandonner():
    if messagebox.askyesno("abandonner", "voulez-vous abandonner?"):
        fenetre.destroy()

fenetre= tk.Tk()
fenetre.title("Menu abandonner et sauvegarder")

bouton_frame=tk.Frame(fenetre)
bouton_frame.pack(pady=20)

bouton_sauvegarder=tk.Button(bouton_frame, text="sauvegarder", command=sauvegarder, width=15)
bouton_sauvegarder.pack(side=tk.LEFT, padx=10)

bouton_abandonner= tk.Button(bouton_frame, text="abandonner", width=15, bg="red", fg="white")
bouton_abandonner.pack(side=tk.LEFT, padx=10)

fenetre.mainloop()
