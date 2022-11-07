#Importation des bibliothèques nécessaires (pygame pour le fenêtre et sys pour le contrôle de l'application)
from math import *
from pygame import *
from rouletteModule import *
from sys import *
from time import time_ns
import pygame
pygame.init() #Lancer pygame

#Variable constante de type tuple contenant la taille de l'écran
TAILLE=(700, 600)

#Variable de type nombre contenant le numéro de la page actuel:
#-1.0 -> page de paramètre
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
#Savoir si il y a un focus sur l'interface d'entrée d'argent
focusInterfaceDEntreeArgent = False
#Statue de rotation pour l'animation du bouton chargement
parametreRotation = 0
#Vitesse de rotation pour l'animation du bouton chargement
PARAMETRE_ROTATION_VITESSE = 0.5
#Définir le rect de l'interface d'entrée d'argent
rectInterfaceDEntreeArgent = (150, 450, 400, 100)
#Temps depuis lequelle le trait d'écriture de l'interface d'entrée argent est dans son état (en secondes)
tempsTraitEcritureVisibleInterfaceDEntreeArgent = 0
#Temps limite pour le changement d'état du trait d'écriture de l'interface d'entrée argent (en secondes)
tempsLimiteTraitEcritureVisibleInterfaceDEntreeArgent = 0.4
#Texte contenu dans l'interface d'entrée argent
texteInterfaceDEntreeArgent = ""
#Savoir si le trait d'écriture de l'interface d'entrée argent lors du focus est visible
traitEcritureVisibleInterfaceDEntreeArgent = True

police = font.SysFont("arial", 30) #Définir la police arial de taille 30

#Boucle qui s'effectuera jusqu'à ce que l'évènement QUIT ne soit enclenché
while True:
    #Actualiser deltaTime
    deltaTime = time_ns()

    police = font.SysFont("arial", 30) #Redéfinir la police arial de taille 30

    #Variable de type tuple contenant la position de la souris
    souris = mouse.get_pos()
    #Variable de type cursor qui contient la texture de curseur qui sera appliqué au curseur au finale
    curseur = SYSTEM_CURSOR_ARROW

    for ev in event.get(): #Gérer les évènements de l'application
        if ev.type == QUIT: exit() #Si évenement pour quitter détecter, quitter l'application
        elif ev.type == MOUSEBUTTONDOWN: #Si évenement clicker détécter
            focusInterfaceDEntreeArgent = False #Remettre le focus sur l'interface d'entrée argent à faux pour tout click
            if page == 0:
                if souris[0] >= 200 and souris[0] <= 400 and souris[1] >= 400 and souris[1] <= 642: #Bouton jouer clické
                    page = 1
                elif souris[0] >= 10 and souris[0] <= 76 and souris[1] >= 10 and souris[1] <= 76:
                    page =-1
            elif page == 1:
                if souris[0] >= rectInterfaceDEntreeArgent[0] and souris[0] <= rectInterfaceDEntreeArgent[0] + rectInterfaceDEntreeArgent[2] and souris[1] >= rectInterfaceDEntreeArgent[1] and souris[1] <= rectInterfaceDEntreeArgent[1] + rectInterfaceDEntreeArgent[3]:
                    focusInterfaceDEntreeArgent = True #Remettre le focus sur l'interface d'entrée argent à vrai si clicker sur l'interface
        elif ev.type == KEYDOWN: #Si une touche du clavier est préssé
            if page == 1:
                if focusInterfaceDEntreeArgent: #Si le focus est sur l'entrée d'argent (tout les nombres)
                    if ev.key == K_0 or ev.key == K_KP_0 or ev.key == K_KP0:
                        texteInterfaceDEntreeArgent += "0"
                    elif ev.key == K_1 or ev.key == K_KP_1 or ev.key == K_KP1:
                        texteInterfaceDEntreeArgent += "1"
                    elif ev.key == K_2 or ev.key == K_KP_2 or ev.key == K_KP2:
                        texteInterfaceDEntreeArgent += "2"
                    elif ev.key == K_3 or ev.key == K_KP_3 or ev.key == K_KP3:
                        texteInterfaceDEntreeArgent += "3"
                    elif ev.key == K_4 or ev.key == K_KP_4 or ev.key == K_KP4:
                        texteInterfaceDEntreeArgent += "4"
                    elif ev.key == K_5 or ev.key == K_KP_5 or ev.key == K_KP5:
                        texteInterfaceDEntreeArgent += "5"
                    elif ev.key == K_6 or ev.key == K_KP_6 or ev.key == K_KP6:
                        texteInterfaceDEntreeArgent += "6"
                    elif ev.key == K_7 or ev.key == K_KP_7 or ev.key == K_KP7:
                        texteInterfaceDEntreeArgent += "7"
                    elif ev.key == K_8 or ev.key == K_KP_8 or ev.key == K_KP8:
                        texteInterfaceDEntreeArgent += "8"
                    elif ev.key == K_9 or ev.key == K_KP_9 or ev.key == K_KP9:
                        texteInterfaceDEntreeArgent += "9"
                    elif ev.key == K_DELETE: #Supprimer un caractère
                        temp = texteInterfaceDEntreeArgent.split("")
                        print(len(temp))
                        temp.remove(len(temp) - 1, 1)
                        print(len(temp))
                        texteInterfaceDEntreeArgent = "".join(temp)

    fenetre.blit(arrierePlan, (0, 0, TAILLE[0], TAILLE[1])) #Afficher l'image d'arrière plan (visible sur toutes las pages)
    fenetre.blit(elementsGUI["titrePage0"], (50, 0, 600, 300)) #Affichage du titre (visible sur toutes les pages)
    #Afficher des choses différentes selon la page
    if page == 0 :
        if souris[0] >= 200 and souris[0] <= 500 and souris[1] >= 400 and souris[1] <= 642: #Savoir si le curseur survole le bouton "jouer" ou non
            fenetre.blit(elementsGUI["boutonJouer2"], (200, 400, 300, 142)) #Mettre un bouton focus
            curseur = SYSTEM_CURSOR_HAND #Changer le curseur
        else:
            fenetre.blit(elementsGUI["boutonJouer1"], (200, 400, 300, 142)) #Mettre un bouton non-focus
        boutonParametre = elementsGUI["boutonParametre"]
        boutonParametre = transform.rotate(boutonParametre, parametreRotation)
        if souris[0] >= 10 and souris[0] <= 76 and souris[1] >= 10 and souris[1] <= 76: #Savoir si le curseur survole le bouton "paramètre" ou non
            boutonParametre = transform.rotate(boutonParametre, 360*deltaTimeConcret*PARAMETRE_ROTATION_VITESSE) #Tourner le bouton (animation)
            parametreRotation += 360*deltaTimeConcret*PARAMETRE_ROTATION_VITESSE #Enregistrer la rotation du bouton
            curseur = SYSTEM_CURSOR_HAND #Changer le curseur
        fenetre.blit(boutonParametre, (10+(66-boutonParametre.get_size()[0])/2, 10+(66-boutonParametre.get_size()[1])/2, boutonParametre.get_size()[0], boutonParametre.get_size()[1])) #Afficher le bouton parametre
    elif page == 1:
        police = font.SysFont("arial", 48) #Augmenter la police à taille 48
        titreArgent = police.render("Rentrez votre quantité d'argent:", True, (0, 0, 0)) #Créer une image avec le texte dedans
        fenetre.blit(titreArgent, (700/2.0-titreArgent.get_width()/2.0, 350, titreArgent.get_width(), titreArgent.get_height())) #Afficher l'image dans la fenêtre
        draw.rect(fenetre, (0, 0, 0), rectInterfaceDEntreeArgent, 0, 10) #Dessiner le cadre de l'interface d'entrée d'argent
        draw.rect(fenetre, (255, 255, 255), (rectInterfaceDEntreeArgent[0]+5, rectInterfaceDEntreeArgent[1]+5, rectInterfaceDEntreeArgent[2]-10, rectInterfaceDEntreeArgent[3]-10), 0, 10) #Dessiner l'intérieur de l'interface d'entrée d'argent
        texte = police.render(texteInterfaceDEntreeArgent, True, (0, 0, 0))
        fenetre.blit(texte, ((rectInterfaceDEntreeArgent[0] + (rectInterfaceDEntreeArgent[2] / 2.0)) - texte.get_width() / 2.0, (rectInterfaceDEntreeArgent[1] + rectInterfaceDEntreeArgent[3]/2.0) - texte.get_height()/2.0, texte.get_width(), texte.get_height())) #Afficher le texte dans la fenêtre
        if focusInterfaceDEntreeArgent: #Savoir si l'interface est focus
            if traitEcritureVisibleInterfaceDEntreeArgent: #Savoir si le trait peut être afficher
                draw.rect(fenetre, (0, 0, 0), ((rectInterfaceDEntreeArgent[0] + (rectInterfaceDEntreeArgent[2] / 2.0)) + texte.get_width()/2.0, (rectInterfaceDEntreeArgent[1] + rectInterfaceDEntreeArgent[3]/2.0) - texte.get_height()/2.0, 2, texte.get_height())) #Placer un trait d'écriture
            tempsTraitEcritureVisibleInterfaceDEntreeArgent += deltaTimeConcret
            if tempsTraitEcritureVisibleInterfaceDEntreeArgent >= tempsLimiteTraitEcritureVisibleInterfaceDEntreeArgent:
                traitEcritureVisibleInterfaceDEntreeArgent = not traitEcritureVisibleInterfaceDEntreeArgent #Inversion de la visibilité du trait de l'interface (uniquement esthétique)
                tempsTraitEcritureVisibleInterfaceDEntreeArgent = 0 #Remise à zéro du temps d'état du trait de l'interface (uniquement esthétique)
            
        else:
            tempsTraitEcritureVisibleInterfaceDEntreeArgent = 0 #Remettre le temps d'écriture du trait de l'interface à 0 pour prochain focus (uniquement esthétique)
            traitEcritureVisibleInterfaceDEntreeArgent = True #Remettre la visibilité du trait de l'interface à vrai pour prochain focus (uniquement esthétique)

    #Actualiser le curseur
    mouse.set_cursor(curseur)
    
    #Actualiser l'écran
    display.flip()
    #Actualisation de deltaTime pour être ensuite calculé
    deltaTime=time_ns()-deltaTime
    deltaTimeConcret = deltaTime * 0.000000001