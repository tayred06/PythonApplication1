
#!/usr/bin/python

import mysql.connector
import random
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window = tk.Tk()

mot = ""


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="pendu"
)

print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM users")

users = mycursor.fetchall()

#for x in users:
#  print(x[1])

print("newGame")
mycursor.execute("SELECT COUNT(id) FROM `mots`")
nbMots = mycursor.fetchone()
print(nbMots[0])
print(random.randint(0, nbMots[0]))
mycursor.execute("SELECT `mot` FROM `mots` WHERE id = " + str(random.randint(0, nbMots[0])))
mot = mycursor.fetchone()
mot = mot[0]

nbErreur = 0

motATrouver = []
for x in list(mot):
    motATrouver = motATrouver + ["."]

print(motATrouver)

def insertUser(val):
    print(val)
    mycursor.execute('INSERT INTO users (prenom) VALUES ("' + val + '");')
    mydb.commit()
    print(val)

def newGame():
    print("newGame")
    mycursor.execute("SELECT COUNT(id) FROM `mots`")
    nbMots = mycursor.fetchone()
    print(nbMots[0])
    print(random.randint(0, nbMots[0]))
    mycursor.execute("SELECT `mot` FROM `mots` WHERE id = " + str(random.randint(0, nbMots[0])))
    mot = mycursor.fetchone()
    print(mot[0])


def partie(lettre):
    if (mot == ""):
        print("perdu")
    else:
        print(lettre)
        input_Lettre.delete(0,"end")
        print(mot)
        nbLettre = 0
        for x in list(mot):
            nbLettre = nbLettre + 1
            if (x == lettre):
                print("trouver")
                motATrouver[nbLettre - 1] = lettre
                var_lettreTrouver.set(str( motATrouver))
                #ajouter le if si le mot est trouver
                if (list(mot) == motATrouver):
                    print("GG")
            else:
                #nbErreur = nbErreur + 1
                print("nop")



print(random.randint(1, 100))

#personnalisation de ma fenêtre
window.title("Jeu du pendu")
window.geometry("500x500")
window.minsize(400,400)

#créer une div
divAccueil = Frame(window)

#composant joueur
varList = StringVar(divAccueil)
varList.set("Joueur")
om = OptionMenu(divAccueil, varList, "Mathieu", "Thomas", "Jul", "Max", "Anais", "Greg")
om.pack()
input_nomJoueur = Entry(divAccueil)
input_nomJoueur.pack()
w = Button (divAccueil, text ="Ajouter un joueur", command=lambda: insertUser(input_nomJoueur.get()))
w.pack()

#composant partie
#nP = Button (divAccueil, text ="Nouvelle partie", command=newGame)
#nP.pack()

input_Lettre = Entry(divAccueil)
input_Lettre.pack()

vL = Button (divAccueil, text ="Valider la lettre", command=lambda: partie(input_Lettre.get()))
vL.pack()

var_nbEssais = StringVar()
label_nbEssais = Label(divAccueil, textvariable=var_nbEssais)

var_nbEssais.set("nombre d'essais restant: 10")
label_nbEssais.pack()

var_lettreTrouver = StringVar()
label_lettreTrouver = Label(divAccueil, textvariable=var_lettreTrouver)

var_lettreTrouver.set(str(motATrouver))
label_lettreTrouver.pack()

#composant historique
Lb1 = Listbox(divAccueil)
Lb1.insert(1, "Python")
Lb1.insert(2, "Perl")
Lb1.insert(3, "C")
Lb1.insert(4, "PHP")
Lb1.insert(5, "JSP")
Lb1.insert(6, "Ruby")

Lb1.pack()

#afficher la page Accueil
divAccueil.pack(expand=YES, side=TOP)

#affiche ma fenêtre
window.mainloop()