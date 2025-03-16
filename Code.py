from tkinter import *

root=tk.Tk()
root.title("MASTERMIND")

frame=tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

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






