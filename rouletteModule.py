from random import *

#Variable global
argent = 15000
argentDebut = 15000
nombreCase = 37
hasard=0

#Demander l'argent total à l'utilisateur
def demanderArgent():
    global argent #Pouvoir utiliser argent dans la fonction
    n = int(input("Choisissez une somme d'argent: ")) #Demander l'argent de l'utilisateur
    while n < 0: #Tant que le numéro n'est pas bon, redemander
        n = int(input("Nombre invalide (que des nombres entiers accéptés), réessayez: "))
    argent = n

#Demander la mise à l'utilisateur
def demanderMise():
    global argent #Pouvoir utiliser argent dans la fonction
    n = int(input("Choisissez une mise: ")) #Demander une mise
    while n < 0 or n > argent: #Tant que le numéro n'est pas bon, redemander
        n = int(input("Nombre invalide (plus élevé que votre argent), réessayez: "))
    argent -= n #Soustraire la mise à la somme
    return n #Retourner la mise
#Demander le numero à l'utilisateur
def demanderNumero():
    #Demander un numéro
    n = int(input("Choisissez un chiffre (il doit être entre 0 et 36): "))
    #Tant que le numéro n'est pas bon, redemander
    while n < 0 or n > 36:
        n = int(input("Nombre invalide (il doit être entre 0 et 36), réessayez: "))
    #Retourner le numéro
    return n
def impair(n1, n2): return n1%2==1 and n2%2==1 #Voir si 2 nombres sont pair
def pair(n1, n2): return n1%2==0 and n2%2==0 #Voir si 2 nombres sont impair
#Dire combien d'argent il reste
def printArgent(): print("Il vous reste: " + str(argent) + " euros")

#Lancer la roulette
def roulette():
    global argent #Pouvoir utiliser argent dans la fonction
    global hasard #Pouvoir utiliser hasard dans la fonction
    numero=demanderNumero() #Demander un numero et la mise à l'utilisateur
    mise=demanderMise()
    hasard=randint(0, 36) #Tirer un numéro aléatoire
    print("Le chiffre tiré est: " + str(hasard)) #Dire le chiffre tiré aléatoirement
    if hasard==numero: #Si le numéro tiré et le numéro de l'utilisateur sont pareils
        mise*=4 #Quadruplé la mise
    elif (pair(hasard, numero)) or (impair(hasard, numero)): #Sinon si les 2 sont pairs ou impairs
        mise*=1.5 #Multiplier la mise par 1.5
    else: #Sinon
        mise = 0 #Enlever la mise
    print("Votre mise finale est " + str(mise))
    argent += mise #Ajouter la mise à l'argent total
    printArgent()