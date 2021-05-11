
#!/usr/bin/python

import mysql.connector
import random
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window = tk.Tk()

mot = ""
nbErreur = 0



mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="pendu"
        )

print(mydb)
mycursor = mydb.cursor()

mycursor.execute("SELECT COUNT(id) FROM `mots`")
nbMots = mycursor.fetchone()
mycursor.execute("SELECT `mot` FROM `mots` WHERE id = " + str(random.randint(0, nbMots[0])))
mot = mycursor.fetchone()
mot = mot[0]


motATrouver = []
for x in list(mot):
    motATrouver = motATrouver + ["."]


def insertUser(val):
    mycursor.execute('INSERT INTO users (prenom) VALUES ("' + val + '");')
    mydb.commit()

def newGame():
    mycursor.execute("SELECT COUNT(id) FROM `mots`")
    nbMots = mycursor.fetchone()
    mycursor.execute("SELECT `mot` FROM `mots` WHERE id = " + str(random.randint(0, nbMots[0])))
    mot = mycursor.fetchone()


def partie(lettre):
    trouver = 0
    global nbErreur
    if (nbErreur != 10):
        if (mot == ""):
            print("perdu") 
        else:
            input_Lettre.delete(0,"end")
            nbLettre = 0
            for x in list(mot):
                nbLettre = nbLettre + 1
             
                if (x == lettre):
                    motATrouver[nbLettre - 1] = lettre
                    var_lettreTrouver.set(str( motATrouver))
                    #ajouter le if si le mot est trouver
                    if (list(mot) == motATrouver):
                        mycursor.execute('INSERT INTO historique (prenom, mot, etat) VALUES ("' + Lbprenom.get(Lbprenom.curselection()) + '", "' + mot + '", "gagner");')
                        mydb.commit()
                        var_partie.set("Partie Gagner")
                else:
                    trouver = 1
            if(trouver == 1):
                nbErreur = nbErreur + 1
                var_nbEssais.set("nombre d'essais restant: " + str((10 - nbErreur)))
                
    else:
        mycursor.execute('INSERT INTO historique (prenom, mot, etat) VALUES ("' + Lbprenom.get(Lbprenom.curselection()) + '", "' + mot + '", "perdu");')
        mydb.commit()
        var_partie.set("Partie Perdu")



#personnalisation de ma fenêtre
window.title("Jeu du pendu")
window.geometry("500x500")
window.minsize(400,400)

#créer une div
pagePrincipal = Frame(window)

var_partie = StringVar()
label_partie = Label(pagePrincipal, textvariable=var_partie)

var_partie.set("Partie en cours")
label_partie.config(font=("Arial", 25))
label_partie.pack()

#composant joueur
varList = StringVar(pagePrincipal)
varList.set("Joueur")
#om = OptionMenu(pagePrincipal, varList, "Mathieu", "Thomas", "Jul", "Max", "Anais", "Greg")
#om.pack()

Lbprenom = Listbox(pagePrincipal, width = 50)
mycursor.execute("SELECT * FROM users")
joueurs = mycursor.fetchall()
for x in joueurs:
  Lbprenom.insert(END, x[1])

Lbprenom.pack()


input_nomJoueur = Entry(pagePrincipal)
input_nomJoueur.pack()
w = Button (pagePrincipal, text ="Ajouter un joueur", command=lambda: insertUser(input_nomJoueur.get()))
w.pack()

#composant partie
#nP = Button (pagePrincipal, text ="Nouvelle partie", command=newGame)
#nP.pack()

input_Lettre = Entry(pagePrincipal)
input_Lettre.pack()

vL = Button (pagePrincipal, text ="Valider la lettre", command=lambda: partie(input_Lettre.get()))
vL.pack()

var_nbEssais = StringVar()
label_nbEssais = Label(pagePrincipal, textvariable=var_nbEssais)

var_nbEssais.set("nombre d'essais restant: 10")
label_nbEssais.pack()

var_lettreTrouver = StringVar()
label_lettreTrouver = Label(pagePrincipal, textvariable=var_lettreTrouver)

var_lettreTrouver.set(str(motATrouver))
label_lettreTrouver.pack()

#composant historique
Lb1 = Listbox(pagePrincipal, width = 50)
mycursor.execute("SELECT * FROM historique ORDER BY id DESC")
historique = mycursor.fetchall()
for x in historique:
  Lb1.insert(END, x[1] + " - " + x[2] + " - " + x[3])

Lb1.pack()

#afficher la page Accueil
pagePrincipal.pack(expand=YES, side=TOP)

#affiche ma fenêtre
window.mainloop()