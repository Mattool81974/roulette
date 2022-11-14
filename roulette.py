#Importation des bibliothèques nécessaires (pygame pour le fenêtre et sys pour le contrôle de l'application)
from math import *
from pygame import *
from rouletteModule import *
from sys import *
from time import time_ns
import pygame
pygame.init() #Lancer pygame

#Transformer un string en tableau de char
def strEnArray(s):
    return [c for c in s]
#Une fonction mathématique qui a comme représentation graphique un demi cercle parfait
def f(x, y = 1, z = 1):
    multipliant = 1 #Variable permettant d'opposer la valeur finale
    while True: #Transformer la variable pour correspondre à l'intervalle de définition de la fonction
        if x < -y:
            x *= -1
            multipliant *= -1
            x -= y
        elif x > y:
            x *= -1
            multipliant *= -1
            x += y
        else:
            break
    return sqrt(y**2-z*(x**2)) #Retourner l'image de la fonction

#Variable constante de type tuple contenant la taille de l'écran
TAILLE=(700, 600)

#Variable de type nombre contenant le numéro de la page actuel:
#-1.0 -> page de paramètre
#0.0 -> page d'accueil
#1.0 -> page où rentrer ses sous
#2.0 -> page où le jouer choisis son numéro et ou la roulette n'est pas encore lancé
#2.3 -> page où le jouer choisis son numéro et ou la roulette est lancé
#2.6 -> page où les résultats sont données au joueur et ou l'argent est actualisé
#2.65 -> page juste après la 2.6 pour éviter que l'argent se fasse actualier à l'infini
#3.0 -> page d'au revoir
page=0

#Création de la fenêtre dans une instance "screen"
fenetre = display.set_mode(TAILLE)

#Angle de la roulette (en radians) calibré pour afficher "1"
angleRoulette=0
#Angle pour la rotation de la roulette (en radians)
angleRotationRoulette=0
#Angle limite pour la rotation de la roulette (en radians), ici à 15 tours
angleRotationRouletteLimite=(pi*2)*15
#Angle limite pour la rotation de la roulette calibrer selon le chiffre choisis
angleRotationRouletteLimiteVrai=angleRotationRouletteLimite
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
    "titrePage0": image.load("assets/titrePage0.png"),
    "boutonValider1": image.load("assets/boutons/boutonValider1.png"),
    "boutonValider2": image.load("assets/boutons/boutonValider2.png"),
    "boutonLancer1": image.load("assets/boutons/boutonLancer1.png"),
    "boutonLancer2": image.load("assets/boutons/boutonLancer2.png"),
    "boutonRejouer1": image.load("assets/boutons/boutonRejouer1.png"),
    "boutonRejouer2": image.load("assets/boutons/boutonRejouer2.png"),
    "boutonArreter1": image.load("assets/boutons/boutonArreter1.png"),
    "boutonArreter2": image.load("assets/boutons/boutonArreter2.png"),
    "boutonQuitter1": image.load("assets/boutons/boutonQuitter1.png"),
    "boutonQuitter2": image.load("assets/boutons/boutonQuitter2.png")
}
#Savoir si il y a un focus sur les interfaces d'entrées
focusInterfaceDEntreeArgent = False
focusInterfaceDEntreeCase = False
focusInterfaceDEntreeMise = False
#Largeur des traits de la roulette
largeurTraitsRoulette=1
#Statue de rotation pour l'animation du bouton chargement
parametreRotationChargement = 0
#Vitesse de rotation pour l'animation du bouton chargement
PARAMETREROTATIONCHARGEMENTVITESSE = 0.5
#Police des chiffres sur la roulette
policeChiffreRoulette=8
#Définir le rect des interfaces d'entrées
rectInterfaceDEntreeArgent = (150, 420, 400, 100)
rectInterfaceDEntreeCase = (80, 530, 150, 70)
rectInterfaceDEntreeMise= (5, 420, 300, 70)
#Taille max de cacractère des interfaces d'entrées
TAILLEMAXTEXTEINTERFACEDENTREEARGENT = 14
TAILLEMAXTEXTEINTERFACEDENTREEMISE = 14
TAILLEMAXTEXTEINTERFACEDENTREECASE = 2
#Temps écoulé entre certaines pages (purement esthétique)
tempsEcoulePage26A265=0
#Temps limite pour le changement d'état du trait d'écriture des interfaces d'entrées (en secondes)
tempsLimiteTraitEcritureVisibleInterfaceDEntreeArgent = 0.4
tempsLimiteTraitEcritureVisibleInterfaceDEntreeMise = 0.4
tempsLimiteTraitEcritureVisibleInterfaceDEntreeCase = 0.4
#Temps depuis lequelle le trait d'écriture des interfaces d'entrée sont dans leurs état (en secondes)
tempsTraitEcritureVisibleInterfaceDEntreeArgent = 0
tempsTraitEcritureVisibleInterfaceDEntreeMise = 0
tempsTraitEcritureVisibleInterfaceDEntreeCase = 0
#Texte contenu dans les interfaces d'entrées
texteInterfaceDEntreeArgent = ""
texteInterfaceDEntreeMise = ""
texteInterfaceDEntreeCase = ""
#Savoir si le trait d'écriture des interfaces d'entrées lors du focus est visible
traitEcritureVisibleInterfaceDEntreeArgent = True
traitEcritureVisibleInterfaceDEntreeMise = True
traitEcritureVisibleInterfaceDEntreeCase = True
#Vitesse de rotation de la roulette
vitesseRotationRoulette=1
#y du bouton valdier de la page 1
yBoutonValiderPage1 = 525

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
            focusInterfaceDEntreeCase = False #Remettre le focus sur l'interface d'entrée case à faux pour tout click
            focusInterfaceDEntreeMise = False #Remettre le focus sur l'interface d'entrée mise à faux pour tout click
            if page == 0:
                if souris[0] >= 200 and souris[0] <= 500 and souris[1] >= 400 and souris[1] <= 642: #Bouton jouer clické
                    page = 1
                elif souris[0] >= 10 and souris[0] <= 76 and souris[1] >= 10 and souris[1] <= 76:
                    page =-1
            elif page == 1:
                if souris[0] >= rectInterfaceDEntreeArgent[0] and souris[0] <= rectInterfaceDEntreeArgent[0] + rectInterfaceDEntreeArgent[2] and souris[1] >= rectInterfaceDEntreeArgent[1] and souris[1] <= rectInterfaceDEntreeArgent[1] + rectInterfaceDEntreeArgent[3]:
                    focusInterfaceDEntreeArgent = True #Remettre le focus sur l'interface d'entrée argent à vrai si clicker sur l'interface
                elif texteInterfaceDEntreeArgent != "" and float(texteInterfaceDEntreeArgent) > 0 and souris[0] >= 550/2 and souris[1] >= yBoutonValiderPage1 and souris[0] <= 550/2 + 150 and souris[1] <= yBoutonValiderPage1 + 71: #Valider la quantité d'argent totale
                    argent = float(texteInterfaceDEntreeArgent)
                    argentDebut = float(texteInterfaceDEntreeArgent)
                    page = 2
            elif page == 2:
                if souris[0] >= rectInterfaceDEntreeMise[0] and souris[0] <= rectInterfaceDEntreeMise[0] + rectInterfaceDEntreeMise[2] and souris[1] >= rectInterfaceDEntreeMise[1] and souris[1] <= rectInterfaceDEntreeMise[1] + rectInterfaceDEntreeMise[3]:
                    focusInterfaceDEntreeMise = True #Remettre le focus sur l'interface d'entrée argent à vrai si clicker sur l'interface
                elif souris[0] >= rectInterfaceDEntreeCase[0] and souris[0] <= rectInterfaceDEntreeCase[0] + rectInterfaceDEntreeCase[2] and souris[1] >= rectInterfaceDEntreeCase[1] and souris[1] <= rectInterfaceDEntreeCase[1] + rectInterfaceDEntreeCase[3]:
                    focusInterfaceDEntreeCase = True #Remettre le focus sur l'interface d'entrée argent à vrai si clicker sur l'interface
                if texteInterfaceDEntreeCase != "" and texteInterfaceDEntreeMise != "" and float(texteInterfaceDEntreeMise) > 0 and souris[0] >= 500/2 and souris[1] >= yBoutonLancerPage2 and souris[0] <= 500/2 + 200 and souris[1] <= yBoutonLancerPage2 + 94: #Lancer la roue
                    page = 2.3
                    argent-=float(texteInterfaceDEntreeMise)
                    angleRotationRoulette=0 #Réinitialisation des données de la roulette
                    angleRoulette=0
                    vitesseRotationRoulette=1
                    hasard=randint(1, nombreCase)
                    angleRotationRouletteLimiteVrai=angleRotationRouletteLimite+((360/nombreCase)*(pi/180)*(ceil(nombreCase/2)-hasard)) #Calcul de l'angle de rotation réel
            elif page - 2.0 > 0.5 and page - 2 < 0.7:
                if argent > 0:
                    if souris[0] >= xMilieu+10 and souris[1] >= 533 and souris[0] <= xMilieu+110 and souris[1] <= 580:
                        page=3
                    if souris[0] >= xMilieu-110 and souris[1] >= 533 and souris[0] <= xMilieu-10 and souris[1] <= 580:
                        page=2
                        texteInterfaceDEntreeMise=""
                        texteInterfaceDEntreeCase=""
                else:
                    if souris[0] >= xMilieu-50 and souris[1] >= 533 and souris[0] <= xMilieu+50 and souris[1] <= 580:
                        page=3
            elif page == 3:
                if souris[0] >= 200 and souris[0] <= 500 and souris[1] >= 450 and souris[1] <= 692:
                    exit()

        elif ev.type == KEYDOWN: #Si une touche du clavier est préssé
            if page == 1:
                if focusInterfaceDEntreeArgent: #Si le focus est sur l'entrée d'argent (tout les nombres)
                    if ev.key == K_KP_ENTER or ev.key == 13 and texteInterfaceDEntreeArgent != "" and float(texteInterfaceDEntreeArgent) > 0: #Valider la quantité d'argent totale
                        argent = float(texteInterfaceDEntreeArgent)
                        argentDebut = float(texteInterfaceDEntreeArgent)
                        page = 2
                    elif ev.key == K_BACKSPACE and len(texteInterfaceDEntreeArgent) > 0: #Supprimer un caractère
                        temp = strEnArray(texteInterfaceDEntreeArgent)
                        temp.__delitem__(len(temp) - 1)
                        texteInterfaceDEntreeArgent = "".join(temp)
                    elif len(texteInterfaceDEntreeArgent) < TAILLEMAXTEXTEINTERFACEDENTREEARGENT: #Si il y a encore de la place dans l'itnerface
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
                        elif (ev.key == K_PERIOD or ev.key == K_KP_PERIOD or ev.key == K_COMMA) and texteInterfaceDEntreeArgent.count(".") <= 0 and len(texteInterfaceDEntreeArgent) > 0:
                            texteInterfaceDEntreeArgent += "." 
            elif page == 2:
                if focusInterfaceDEntreeMise: #Si le focus est sur l'entrée mise (tout les nombres)
                    if ev.key == K_KP_ENTER or ev.key == 13 and texteInterfaceDEntreeArgent != "": #Valider la quantité d'argent totale
                        focusInterfaceDEntreeMise = False
                    elif ev.key == K_BACKSPACE and len(texteInterfaceDEntreeMise) > 0: #Supprimer un caractère
                        temp = strEnArray(texteInterfaceDEntreeMise)
                        temp.__delitem__(len(temp) - 1)
                        texteInterfaceDEntreeMise = "".join(temp)
                    elif len(texteInterfaceDEntreeMise) < TAILLEMAXTEXTEINTERFACEDENTREEMISE: #Si il y a encore de la place dans l'itnerface
                        if ev.key == K_0 or ev.key == K_KP_0 or ev.key == K_KP0:
                            texteInterfaceDEntreeMise += "0"
                        elif ev.key == K_1 or ev.key == K_KP_1 or ev.key == K_KP1:
                            texteInterfaceDEntreeMise += "1"
                        elif ev.key == K_2 or ev.key == K_KP_2 or ev.key == K_KP2:
                            texteInterfaceDEntreeMise += "2"
                        elif ev.key == K_3 or ev.key == K_KP_3 or ev.key == K_KP3:
                            texteInterfaceDEntreeMise += "3"
                        elif ev.key == K_4 or ev.key == K_KP_4 or ev.key == K_KP4:
                            texteInterfaceDEntreeMise += "4"
                        elif ev.key == K_5 or ev.key == K_KP_5 or ev.key == K_KP5:
                            texteInterfaceDEntreeMise += "5"
                        elif ev.key == K_6 or ev.key == K_KP_6 or ev.key == K_KP6:
                            texteInterfaceDEntreeMise += "6"
                        elif ev.key == K_7 or ev.key == K_KP_7 or ev.key == K_KP7:
                            texteInterfaceDEntreeMise += "7"
                        elif ev.key == K_8 or ev.key == K_KP_8 or ev.key == K_KP8:
                            texteInterfaceDEntreeMise += "8"
                        elif ev.key == K_9 or ev.key == K_KP_9 or ev.key == K_KP9:
                            texteInterfaceDEntreeMise += "9" 
                        elif (ev.key == K_PERIOD or ev.key == K_KP_PERIOD or ev.key == K_COMMA) and texteInterfaceDEntreeMise.count(".") <= 0 and len(texteInterfaceDEntreeMise) > 0:
                            texteInterfaceDEntreeMise += "." 
                    if texteInterfaceDEntreeMise != "" and float(texteInterfaceDEntreeMise) > float(texteInterfaceDEntreeArgent):
                        texteInterfaceDEntreeMise = str(float(texteInterfaceDEntreeArgent))
                elif focusInterfaceDEntreeCase: #Si le focus est sur l'entrée mise (tout les nombres)
                    if ev.key == K_KP_ENTER or ev.key == 13 and texteInterfaceDEntreeCase != "": #Valider la quantité d'argent totale
                        focusInterfaceDEntreeCase = False
                    elif ev.key == K_BACKSPACE and len(texteInterfaceDEntreeCase) > 0: #Supprimer un caractère
                        temp = strEnArray(texteInterfaceDEntreeCase)
                        temp.__delitem__(len(temp) - 1)
                        texteInterfaceDEntreeCase = "".join(temp)
                    elif len(texteInterfaceDEntreeCase) < TAILLEMAXTEXTEINTERFACEDENTREECASE: #Si il y a encore de la place dans l'itnerface
                        if ev.key == K_0 or ev.key == K_KP_0 or ev.key == K_KP0:
                            texteInterfaceDEntreeCase += "0"
                        elif ev.key == K_1 or ev.key == K_KP_1 or ev.key == K_KP1:
                            texteInterfaceDEntreeCase += "1"
                        elif ev.key == K_2 or ev.key == K_KP_2 or ev.key == K_KP2:
                            texteInterfaceDEntreeCase += "2"
                        elif ev.key == K_3 or ev.key == K_KP_3 or ev.key == K_KP3:
                            texteInterfaceDEntreeCase += "3"
                        elif ev.key == K_4 or ev.key == K_KP_4 or ev.key == K_KP4:
                            texteInterfaceDEntreeCase += "4"
                        elif ev.key == K_5 or ev.key == K_KP_5 or ev.key == K_KP5:
                            texteInterfaceDEntreeCase += "5"
                        elif ev.key == K_6 or ev.key == K_KP_6 or ev.key == K_KP6:
                            texteInterfaceDEntreeCase += "6"
                        elif ev.key == K_7 or ev.key == K_KP_7 or ev.key == K_KP7:
                            texteInterfaceDEntreeCase += "7"
                        elif ev.key == K_8 or ev.key == K_KP_8 or ev.key == K_KP8:
                            texteInterfaceDEntreeCase += "8"
                        elif ev.key == K_9 or ev.key == K_KP_9 or ev.key == K_KP9:
                            texteInterfaceDEntreeCase += "9"
                    if texteInterfaceDEntreeCase != "" and float(texteInterfaceDEntreeCase) > nombreCase:
                        texteInterfaceDEntreeCase = str(nombreCase)
                    if texteInterfaceDEntreeCase != "" and float(texteInterfaceDEntreeCase) <= 0:
                        texteInterfaceDEntreeCase = str(1)


    fenetre.blit(arrierePlan, (0, 0, TAILLE[0], TAILLE[1])) #Afficher l'image d'arrière plan (visible sur toutes las pages)
    fenetre.blit(elementsGUI["titrePage0"], (50, 0, 600, 300)) #Affichage du titre (visible sur toutes les pages)
    police = font.SysFont("arial", 20) #Augmenter la police à taille 30
    texte=police.render("Par Mattéo Menou, 1er 05, dédicace au grand Léo.", True, (0, 0, 0))
    fenetre.blit(texte, ( 695-texte.get_width(), 5, texte.get_width(), texte.get_height()))
    #Afficher des choses différentes selon la page
    if page == 0 :
        if souris[0] >= 200 and souris[0] <= 500 and souris[1] >= 400 and souris[1] <= 642: #Savoir si le curseur survole le bouton "jouer" ou non
            fenetre.blit(elementsGUI["boutonJouer2"], (200, 400, 300, 142)) #Mettre un bouton focus
            curseur = SYSTEM_CURSOR_HAND #Changer le curseur
        else:
            fenetre.blit(elementsGUI["boutonJouer1"], (200, 400, 300, 142)) #Mettre un bouton non-focus
        boutonParametre = elementsGUI["boutonParametre"]
        boutonParametre = transform.rotate(boutonParametre, parametreRotationChargement)
        if souris[0] >= 10 and souris[0] <= 76 and souris[1] >= 10 and souris[1] <= 76: #Savoir si le curseur survole le bouton "paramètre" ou non
            boutonParametre = transform.rotate(boutonParametre, 360*deltaTimeConcret*PARAMETREROTATIONCHARGEMENTVITESSE) #Tourner le bouton (animation)
            parametreRotationChargement += 360*deltaTimeConcret*PARAMETREROTATIONCHARGEMENTVITESSE #Enregistrer la rotation du bouton
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
        
        if souris[0] >= 550/2 and souris[1] >= yBoutonValiderPage1 and souris[0] <= 550/2 + 150 and souris[1] <= yBoutonValiderPage1 + 71:
            fenetre.blit(elementsGUI["boutonValider2"], (550/2, yBoutonValiderPage1, 150, 71))
            curseur = SYSTEM_CURSOR_HAND #Changer le curseur
        else:
            fenetre.blit(elementsGUI["boutonValider1"], (550/2, yBoutonValiderPage1, 150, 71))

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
    elif floor(page) == 2:
        police = font.SysFont("arial", 30) #Mettre la police à 30
        titreArgent = police.render("Vous avez " + str(round(argent, 2)) + " euros.", True, (0, 0, 0)) #Créer une image avec le texte indiquant la quantité d'argent dedans
        fenetre.blit(titreArgent, (700/2.0-titreArgent.get_width()/2.0, 300, titreArgent.get_width(), titreArgent.get_height())) #Afficher l'image dans la fenêtre
        
        titreMise = police.render("Mise:", True, (0, 0, 0)) #Créer une image avec le titre de la mise dedans
        fenetre.blit(titreMise, (rectInterfaceDEntreeMise[0]+rectInterfaceDEntreeMise[2]/2-titreMise.get_width()/2, rectInterfaceDEntreeMise[1] - titreArgent.get_height(), titreArgent.get_width(), titreArgent.get_height())) #Afficher l'image dans la fenêtre

        draw.rect(fenetre, (0, 0, 0), rectInterfaceDEntreeMise, 0, 10) #Dessiner le cadre de l'interface d'entrée d'argent
        draw.rect(fenetre, (255, 255, 255), (rectInterfaceDEntreeMise[0]+5, rectInterfaceDEntreeMise[1]+5, rectInterfaceDEntreeMise[2]-10, rectInterfaceDEntreeMise[3]-10), 0, 10) #Dessiner l'intérieur de l'interface d'entrée d'argent
        texte = police.render(str(texteInterfaceDEntreeMise), True, (0, 0, 0)) #Générer un texte dans l'interface
        fenetre.blit(texte, ((rectInterfaceDEntreeMise[0] + (rectInterfaceDEntreeMise[2] / 2.0)) - texte.get_width() / 2.0, (rectInterfaceDEntreeMise[1] + rectInterfaceDEntreeMise[3]/2.0) - texte.get_height()/2.0, texte.get_width(), texte.get_height())) #Afficher le texte dans la fenêtre

        if focusInterfaceDEntreeMise: #Savoir si l'interface est focus
            if traitEcritureVisibleInterfaceDEntreeMise: #Savoir si le trait peut être afficher
                draw.rect(fenetre, (0, 0, 0), ((rectInterfaceDEntreeMise[0] + (rectInterfaceDEntreeMise[2] / 2.0)) + texte.get_width()/2.0, (rectInterfaceDEntreeMise[1] + rectInterfaceDEntreeMise[3]/2.0) - texte.get_height()/2.0, 2, texte.get_height())) #Placer un trait d'écriture
            tempsTraitEcritureVisibleInterfaceDEntreeMise += deltaTimeConcret
            if tempsTraitEcritureVisibleInterfaceDEntreeMise >= tempsLimiteTraitEcritureVisibleInterfaceDEntreeMise:
                traitEcritureVisibleInterfaceDEntreeMise = not traitEcritureVisibleInterfaceDEntreeMise #Inversion de la visibilité du trait de l'interface (uniquement esthétique)
                tempsTraitEcritureVisibleInterfaceDEntreeMise = 0 #Remise à zéro du temps d'état du trait de l'interface (uniquement esthétique)   
        else:
            tempsTraitEcritureVisibleInterfaceDEntreeMise = 0 #Remettre le temps d'écriture du trait de l'interface à 0 pour prochain focus (uniquement esthétique)
            traitEcritureVisibleInterfaceDEntreeMise = True #Remettre la visibilité du trait de l'interface à vrai pour prochain focus (uniquement esthétique)

        titreCase = police.render("Case:", True, (0, 0, 0)) #Créer une image avec le titre de la case dedans
        fenetre.blit(titreCase, (rectInterfaceDEntreeCase[0]+rectInterfaceDEntreeCase[2]/2-titreMise.get_width()/2, rectInterfaceDEntreeCase[1] - titreArgent.get_height(), titreArgent.get_width(), titreArgent.get_height())) #Afficher l'image dans la fenêtre

        draw.rect(fenetre, (0, 0, 0), rectInterfaceDEntreeCase, 0, 10) #Dessiner le cadre de l'interface d'entrée d'argent
        draw.rect(fenetre, (255, 255, 255), (rectInterfaceDEntreeCase[0]+5, rectInterfaceDEntreeCase[1]+5, rectInterfaceDEntreeCase[2]-10, rectInterfaceDEntreeCase[3]-10), 0, 10) #Dessiner l'intérieur de l'interface d'entrée d'argent
        texte = police.render(str(texteInterfaceDEntreeCase), True, (0, 0, 0)) #Générer un texte dans l'interface
        fenetre.blit(texte, ((rectInterfaceDEntreeCase[0] + (rectInterfaceDEntreeCase[2] / 2.0)) - texte.get_width() / 2.0, (rectInterfaceDEntreeCase[1] + rectInterfaceDEntreeCase[3]/2.0) - texte.get_height()/2.0, texte.get_width(), texte.get_height())) #Afficher le texte dans la fenêtre

        if focusInterfaceDEntreeCase: #Savoir si l'interface est focus
            if traitEcritureVisibleInterfaceDEntreeCase: #Savoir si le trait peut être afficher
                draw.rect(fenetre, (0, 0, 0), ((rectInterfaceDEntreeCase[0] + (rectInterfaceDEntreeCase[2] / 2.0)) + texte.get_width()/2.0, (rectInterfaceDEntreeCase[1] + rectInterfaceDEntreeCase[3]/2.0) - texte.get_height()/2.0, 2, texte.get_height())) #Placer un trait d'écriture
            tempsTraitEcritureVisibleInterfaceDEntreeCase += deltaTimeConcret
            if tempsTraitEcritureVisibleInterfaceDEntreeCase >= tempsLimiteTraitEcritureVisibleInterfaceDEntreeCase:
                traitEcritureVisibleInterfaceDEntreeCase = not traitEcritureVisibleInterfaceDEntreeCase #Inversion de la visibilité du trait de l'interface (uniquement esthétique)
                tempsTraitEcritureVisibleInterfaceDEntreeCase = 0 #Remise à zéro du temps d'état du trait de l'interface (uniquement esthétique)   
        else:
            tempsTraitEcritureVisibleInterfaceDEntreeCase = 0 #Remettre le temps d'écriture du trait de l'interface à 0 pour prochain focus (uniquement esthétique)
            traitEcritureVisibleInterfaceDEntreeCase = True #Remettre la visibilité du trait de l'interface à vrai pour prochain focus (uniquement esthétique)

        if page-2<=0.4: #Si la page actuel est la page de demande de la mise et de la case ou la page de lancement de la roulette
            largeurRoulette = 125 #Définir la largeur de la roulette
            img=Surface((largeurRoulette * 2, largeurRoulette * 2)).convert_alpha() #Créer une surface roulette compatible alpha
            img.fill((0, 0, 0, 0)) #Rendre le fond de la surface de la roulette transparent
            draw.circle(img, (0, 0, 0), (largeurRoulette, largeurRoulette), largeurRoulette) #Dessiner l'arrière de la roulette
            draw.circle(img, (50, 50, 50), (largeurRoulette, largeurRoulette), largeurRoulette - 25) #Dessine devant l'arrière de la roulette
            draw.circle(img, (139, 0, 0), (largeurRoulette, largeurRoulette), largeurRoulette - 30) #Dessiner le plateau de la roulette
            police = font.SysFont("arial", policeChiffreRoulette) #Mettre la police à la police de la roulette
        
            if page-2>=0.2 and page-2<=0.4: #Si la roulette est lancé
                if page-2>=0.2 and page-2<=0.31 and angleRotationRoulette >= angleRotationRouletteLimiteVrai-0.05: #Vérification du temps restant pour la roulette
                    page=2.35
                    tempsEcoulePage26A265=0
                angleRotationFrame=cos(angleRotationRoulette/angleRotationRouletteLimiteVrai/4*(pi*2))*((pi*2)*12)*deltaTimeConcret #Calcul de la valeur d'angle a changé lors de cette frame
                angleRotationRoulette+=angleRotationFrame
                if angleRotationRoulette > angleRotationRouletteLimiteVrai: #Si l'angle maximale est atteint
                    angleRotationRoulette = angleRotationRouletteLimiteVrai
                    angleRotationFrame = cos(angleRotationRoulette/angleRotationRouletteLimiteVrai/4*(pi*2))*((pi*2)*12)*deltaTimeConcret #Recalculer l'angle après calibrage
                angleRoulette+=angleRotationFrame #Calcul de l'angle de la roulette
                tempsEcoulePage26A265 += deltaTimeConcret #Actualisation du temps entre la page 2.6 et 2.65
                if page-2>=0.31 and page-2<=0.4 and tempsEcoulePage26A265 >= 2: #Quand 2 secondes ont été passées sur la page 2.6
                    page=2.6
            
            for i in range(nombreCase): #Dessiner chaque ligne et nombres
                positionFin=((largeurRoulette-30)*cos(i/nombreCase*(pi*2)+angleRoulette), (largeurRoulette-30)*sin(i/nombreCase*(pi*2)+angleRoulette)) #Calcul de la position de fin de la ligne grâce à la trigonométrie
                draw.line(img, (50, 50, 50), (largeurRoulette, largeurRoulette), ((largeurRoulette) + positionFin[0], (largeurRoulette) + positionFin[1]), largeurTraitsRoulette) #Dessiner la ligne
                texteLettre = i + ceil(nombreCase/4) #Calcul du chiffre présent dans le texte
                if int(texteLettre) > nombreCase: #Calibrage du chiffre
                    texteLettre = str(int(texteLettre) - nombreCase)
                lettre = police.render(str(texteLettre) + " "*(len(str(nombreCase+1))-len(str(i))), True, (0, 0, 0)) #Dessiner la lettre
                lettre = transform.rotate(lettre, -((float(texteLettre) - 1)*(360)/(nombreCase-1)+(angleRoulette*(180/pi)))) #Tourner la lettre
                offsetLettre=policeChiffreRoulette/2 #Variable contenant la distance entre les points de fin des traits et le texte
                positionFin=((largeurRoulette-(30+offsetLettre))*cos(i/nombreCase*(pi*2)+(pi/nombreCase)+angleRoulette), (largeurRoulette-(30+offsetLettre))*sin(i/nombreCase*(pi*2)+(pi/nombreCase)+angleRoulette)) #Calcul de la position du texte grâce à la trigonométrie
                positionFinTrait=(lettre.get_width()*cos(i*2/nombreCase), lettre.get_height()*sin((-i)*2/nombreCase)) #Calcul de la position du texte par rapport au point (sur un cercle)
                img.blit(lettre, ((largeurRoulette) + positionFin[0] - lettre.get_width()/2, (largeurRoulette) + positionFin[1] - lettre.get_height()/2, lettre.get_width(), lettre.get_height())) #Afficher le texte
            draw.circle(img, (0, 0, 0), (largeurRoulette, largeurRoulette), largeurRoulette - 100) #Dessiner la partie centrale de la roulette
            draw.circle(img, (218,165,32), (largeurRoulette, largeurRoulette), largeurRoulette - 102) #Dessine la partie centrale de la roulette
            draw.polygon(img, (30, 30, 30), ((largeurRoulette-20, largeurRoulette*2+10), (largeurRoulette+20, largeurRoulette*2+10), (largeurRoulette, largeurRoulette*2-40))) #Dessine un triangle en bas de la roulette
            fenetre.blit(img, (690 - img.get_width(), 590 - img.get_height(), img.get_width(), img.get_height()))

        if page - 2.0 < 0.2: #Si la page actuel est la page de demande de la mise et de la case
            yBoutonLancerPage2=500
            if souris[0] >= 500/2 and souris[1] >= yBoutonLancerPage2 and souris[0] <= 500/2 + 200 and souris[1] <= yBoutonLancerPage2 + 94:
                fenetre.blit(elementsGUI["boutonLancer2"], (500/2, yBoutonLancerPage2, 200, 94))
                curseur = SYSTEM_CURSOR_HAND #Changer le curseur
            else:
                fenetre.blit(elementsGUI["boutonLancer1"], (500/2, yBoutonLancerPage2, 200, 94))
        
        if page - 2.0 > 0.5 and page - 2 < 0.7: #Si la roulette a été lancé
            police = font.SysFont("arial", 24) #Mettre la police à la police du texte
            texte1=police.render("Le nombre tiré est " + str(hasard) + ".", True, (0, 0, 0)) #Création du texte d'affichage du nombre au hasard
            texte2=police.render("Vous avez choisis le nombre " + texteInterfaceDEntreeCase + ".", True, (0, 0, 0)) #Création du texte d'affichage du nombre au hasard
            if hasard == int(texteInterfaceDEntreeCase):
                texte3=police.render("Les 2 nombres sont similaires.", True, (0, 0, 0)) #Création du texte disant que les 2 nombres sont égaux
                texte4=police.render("La mise est triplé. Elle est de " + str(round(float(texteInterfaceDEntreeMise)*3, 2)) + " euros.", True, (0, 0, 0)) #Création du texte disant le triplage de la mise
                if page - 2.0 > 0.5 and page - 2 < 0.61: #Si l'actualisation n'a pas eu lieu
                    argent+=float(texteInterfaceDEntreeMise)*3 #Actualiser l'argent
            elif hasard%2 == int(texteInterfaceDEntreeCase)%2:
                if hasard%2 == 1: pairOuImpair="impair" #Savoir si les 2 nombres sont soit pairs soit impairs
                else: pairOuImpair="pair"
                texte3=police.render("Les 2 nombres sont " + pairOuImpair + ".", True, (0, 0, 0)) #Création du texte disant que les 2 nombres sont soit pairs soit impairs
                texte4=police.render("La mise est augmenté de sa demi. Elle est de " + str(round(float(texteInterfaceDEntreeMise)*1.5, 2)) + " euros.", True, (0, 0, 0)) #Création du texte disant la multiplication par 1.5 de la mise
                if page - 2.0 > 0.5 and page - 2 < 0.61: #Si l'actualisation n'a pas eu lieu
                    argent+=float(texteInterfaceDEntreeMise)*1.5 #Actualiser l'argent
            else:
                if hasard%2 == 0: pairOuImpair="pair" #Savoir si le nombre tiré sont soit pairs soit impairs
                else: pairOuImpair="impair"
                texte3=police.render("Le nombre tiré est " + pairOuImpair + " et pas celui choisi", True, (0, 0, 0)) #Création du texte disant que les 2 nombres ne sont pas tout les 2 pairs ou impairs
                texte4=police.render("La mise est perdue. Elle est de 0 euros.", True, (0, 0, 0)) #Création du texte disant l'annulation de la mise
            
            if argent > 0:
                texte5=police.render("Il vous reste " + str(round(argent, 2)) + " euros.", True, (0, 0, 0)) #Création du texte disant la quantité d'argent disponible
            else:
                texte5=police.render("Il vous reste 0 euro. Vous êtes ruiné", True, (0, 0, 0)) #Création du texte disant la quantité d'argent disponible et que le joueur est ruiné
            xDroiteInterface=rectInterfaceDEntreeMise[0]+rectInterfaceDEntreeMise[2] #Obtention des coordonnées de la droite de l'interface de la mise pour alignage (purement estéthique)
            xMilieu=xDroiteInterface+((700-xDroiteInterface)/2) #Milieu de l'endroit ou les résultats sont affichés
            fenetre.blit(texte1, ((xMilieu-texte1.get_width()/2), 533-(texte1.get_height()+texte2.get_height()+texte3.get_height()+texte4.get_height()+texte5.get_height()), texte1.get_width(), texte1.get_height())) #Placer le texte 1
            fenetre.blit(texte2, ((xMilieu-texte2.get_width()/2), 533-(texte2.get_height()+texte3.get_height()+texte4.get_height()+texte5.get_height()), texte2.get_width(), texte2.get_height())) #Placer le texte 2
            fenetre.blit(texte3, ((xMilieu-texte3.get_width()/2), 533-(texte3.get_height()+texte4.get_height()+texte5.get_height()), texte3.get_width(), texte3.get_height())) #Placer le texte 3
            fenetre.blit(texte4, ((xMilieu-texte4.get_width()/2), 533-(texte4.get_height()+texte5.get_height()), texte4.get_width(), texte4.get_height())) #Placer le texte 4
            fenetre.blit(texte5, ((xMilieu-texte5.get_width()/2), 533-(texte5.get_height()), texte5.get_width(), texte5.get_height())) #Placer le texte 5

            if argent > 0:
                if souris[0] >= xMilieu+10 and souris[1] >= 533 and souris[0] <= xMilieu+110 and souris[1] <= 580:
                    fenetre.blit(elementsGUI["boutonArreter2"], (xMilieu+10, 533, 100, 47))
                    curseur = SYSTEM_CURSOR_HAND #Changer le curseur
                else:
                    fenetre.blit(elementsGUI["boutonArreter1"], (xMilieu+10, 533, 100, 47))
            
                if souris[0] >= xMilieu-110 and souris[1] >= 533 and souris[0] <= xMilieu-10 and souris[1] <= 580:
                    fenetre.blit(elementsGUI["boutonRejouer2"], (xMilieu-110, 533, 100, 47))
                    curseur = SYSTEM_CURSOR_HAND #Changer le curseur
                else:
                    fenetre.blit(elementsGUI["boutonRejouer1"], (xMilieu-110, 533, 100, 47))
            else:
                if souris[0] >= xMilieu-50 and souris[1] >= 533 and souris[0] <= xMilieu+50 and souris[1] <= 580:
                    fenetre.blit(elementsGUI["boutonArreter2"], (xMilieu-50, 533, 100, 47))
                    curseur = SYSTEM_CURSOR_HAND #Changer le curseur
                else:
                    fenetre.blit(elementsGUI["boutonArreter1"], (xMilieu-50, 533, 100, 47))

            page=2.65 #Actualiser la page pour dire que l'actualisation de l'argent a eu lieu
    elif floor(page) == 3:
        police = font.SysFont("arial", 30) #Mettre la police à 30
        titreArgent = police.render("Vous repartez avec " + str(round(argent, 2)) + " euros.", True, (0, 0, 0)) #Créer une image avec le texte indiquant la quantité d'argent dedans (similaire à celui de la page 2)
        fenetre.blit(titreArgent, (700/2.0-titreArgent.get_width()/2.0, 300, titreArgent.get_width(), titreArgent.get_height())) #Afficher l'image dans la fenêtre
        if argentDebut > argent:
            titreResultat = police.render("Vous avez perdue " + str(round(argentDebut - argent, 2)) + " euros.", True, (0, 0, 0)) #Créer une image avec le texte indiquant le résultat du joueur
            fenetre.blit(titreResultat, (700/2.0-titreResultat.get_width()/2.0, 300 + titreArgent.get_height()+10, titreResultat.get_width(), titreResultat.get_height())) #Afficher l'image dans la fenêtre
            titreCommentaire = police.render("Pas terrible...", True, (0, 0, 0)) #Créer une image avec le texte pour ce moquer du joueur (° ͜ʖ°)
            fenetre.blit(titreCommentaire, (700/2.0-titreCommentaire.get_width()/2.0, 300 + titreArgent.get_height()+titreResultat.get_height()+20, titreCommentaire.get_width(), titreCommentaire.get_height())) #Afficher l'image dans la fenêtre
        elif argentDebut == argent:
            titreResultat = police.render("Vous avez " + str(round(argentDebut - argent, 2)) + " euros, comme au début.", True, (0, 0, 0)) #Créer une image avec le texte indiquant le résultat du joueur
            fenetre.blit(titreResultat, (700/2.0-titreResultat.get_width()/2.0, 300 + titreArgent.get_height()+10, titreResultat.get_width(), titreResultat.get_height())) #Afficher l'image dans la fenêtre
            titreCommentaire = police.render("Pourquoi pas...", True, (0, 0, 0)) #Créer une image avec le texte pour ce moquer du joueur (° ͜ʖ°)
            fenetre.blit(titreCommentaire, (700/2.0-titreCommentaire.get_width()/2.0, 300 + titreArgent.get_height()+titreResultat.get_height()+20, titreCommentaire.get_width(), titreCommentaire.get_height())) #Afficher l'image dans la fenêtre
        else:
            titreResultat = police.render("Vous avez gagné " + str(round(argent - argentDebut, 2)) + " euros.", True, (0, 0, 0)) #Créer une image avec le texte indiquant le résultat du joueur
            fenetre.blit(titreResultat, (700/2.0-titreResultat.get_width()/2.0, 300 + titreArgent.get_height()+10, titreResultat.get_width(), titreResultat.get_height())) #Afficher l'image dans la fenêtre
            titreCommentaire = police.render("Futur millionaire (non) ?", True, (0, 0, 0)) #Créer une image avec le texte pour ce moquer du joueur (° ͜ʖ°)
            fenetre.blit(titreCommentaire, (700/2.0-titreCommentaire.get_width()/2.0, 300 + titreArgent.get_height()+titreResultat.get_height()+20, titreCommentaire.get_width(), titreCommentaire.get_height())) #Afficher l'image dans la fenêtre
        
        if souris[0] >= 200 and souris[0] <= 500 and souris[1] >= 450 and souris[1] <= 692: #Savoir si le curseur survole le bouton "quitter" ou non
            fenetre.blit(elementsGUI["boutonQuitter2"], (200, 450, 300, 142)) #Mettre un bouton focus
            curseur = SYSTEM_CURSOR_HAND #Changer le curseur
        else:
            fenetre.blit(elementsGUI["boutonQuitter1"], (200, 450, 300, 142)) #Mettre un bouton non-focus

        police = font.SysFont("arial", 22) #Mettre la police à 18
        texte=police.render("Merci d'avoir joué !", True, (0, 0, 0)) #Remercier le joueur d'avoir jouer
        fenetre.blit(texte, (10, 590-(texte.get_height()+10), texte.get_width(), texte.get_height()))

    #Actualiser le curseur
    mouse.set_cursor(curseur)
    
    #Actualiser l'écran
    display.flip()
    #Actualisation de deltaTime pour être ensuite calculé
    deltaTime=time_ns()-deltaTime
    deltaTimeConcret = deltaTime * 0.000000001