#Importation des bibliothèques nécessaires (pygame pour le fenêtre et sys pour le contrôle de l'application)
from time import time_ns
from pygame import *
from sys import *

#Variable constante de type tuple contenant la taille de l'écran
TAILLE=(700, 700)

#Variable de type nombre contenant le numéro de la page actuel:
#0.0 -> page d'accueil
#1.0 -> page où rentrer ses sous
#2.0 -> page où le jouer choisis son numéro
#3.0 -> page de lancement de la roulette avant que le nombre soit affiché
#3.5 -> page de lancement de la roulette après que le nombre soit affiché
page=0

#Création de la fenêtre dans une instance "screen"
fenetre = display.set_mode(TAILLE)

#Chargement de l'image d'arrière plan
arrierePlan = image.load("assets/arrierePlan.png")
#Variable qui stocke le temps de l'itération de boucle actuel en secondes
deltaTime = 0.0
#Variable qui stocke le temps de la dernière itération de boucle en secondes
deltaTimeConcret = 0.0
#Charger tout les éléments de la GUI dans un dictionnaire
elementsGUI = {
    "boutonJouer1": image.load("assets/boutons/boutonJouer1.png"),
    "boutonJouer2": image.load("assets/boutons/boutonJouer2.png"),
    "boutonParametre": image.load("assets/boutons/boutonParametre.png"),
    "titrePage0": image.load("assets/titrePage0.png")
}
#Vitesse de rotation pour l'animation du bouton chargement
PARAMETRE_ROTATION_VITESSE = 0.5

#Boucle qui s'effectuera jusqu'à ce que l'évènement QUIT ne soit enclenché
while True:
    #Actualiser deltaTime
    deltaTime = time_ns()-deltaTime

    #Variable de type tuple contenant la position de la souris
    souris = mouse.get_pos()
    #Variable de type cursor qui contient la texture de curseur qui sera appliqué au curseur au finale
    curseur = SYSTEM_CURSOR_ARROW

    for ev in event.get(): #Gérer les évènements de l'application
        if ev.type == QUIT: exit() #Si évenement pour quitter détecter, quitter l'application
        elif ev.type == MOUSEBUTTONDOWN: #Si évenement clicker détécter
            if page == 0:
                if souris[0] >= 200 and souris[0] <= 500 and souris[1] >= 500 and souris[1] <= 642: #Bouton jouer clické
                    page = 1

    #Afficher l'image d'arrière plan (visible sur toutes las pages)
    fenetre.blit(arrierePlan, (0, 0, TAILLE[0], TAILLE[1]))
    #Afficher des choses différentes selon la page
    if page == 0 :
        fenetre.blit(elementsGUI["titrePage0"], (50, 0, 600, 300)) #Affichage du titre
        if souris[0] >= 200 and souris[0] <= 500 and souris[1] >= 500 and souris[1] <= 642: #Savoir si le curseur survole le bouton "jouer" ou non
            fenetre.blit(elementsGUI["boutonJouer2"], (200, 500, 300, 142)) #Mettre un bouton focus
            curseur = SYSTEM_CURSOR_HAND #Changer le curseur
        else:
            fenetre.blit(elementsGUI["boutonJouer1"], (200, 500, 300, 142)) #Mettre un bouton non-focus
        if souris[0] >= 10 and souris[0] <= 76 and souris[1] >= 10 and souris[1] <= 76: #Savoir si le curseur survole le bouton "paramètre" ou non
            print(deltaTime)
            elementsGUI["boutonParametre"] = transform.rotate(elementsGUI["boutonParametre"], 360*deltaTime*PARAMETRE_ROTATION_VITESSE)
        fenetre.blit(elementsGUI["boutonParametre"], (10, 10, 66, 66)) #Afficher le bouton parametre
    #Actualiser le curseur
    mouse.set_cursor(curseur)
    
    #Actualiser l'écran
    display.flip()
    #Actualisation de deltaTime pour être ensuite calculé
    deltaTime=time_ns()