#########################################
####### Copyright Kylian-Project ########
#########################################

# -----> Just a fun BONUS <-----

import pygame
from pygame import *
from pygame import gfxdraw
import Labyrinthe
import time


# ----------------------------------------------------------------

# Nombre impaire obligatoire pour taille, exemple Labyrinthe.creer(101,101,3)
# 3eme chiffre = difficulte de 1 à 3
laby = Labyrinthe.creer(51,51,3)
pos_joueur = [1,1]


# ----------------------------------------------------------------

def nb_lignes2(liste,cote_carre):
    return len(liste)*cote_carre

# ----------------------------------------------------------------

def nb_colones2(liste,cote_carre):
    return len(liste[0])*cote_carre

# ----------------------------------------------------------------


liste = laby
cote_carre = 10
# Limite de temps en secondes
finish_time = 60

taille_win = [nb_lignes2(liste, cote_carre),nb_colones2(liste, cote_carre),cote_carre]

pygame.init()
pygame.display.set_caption("LabyGame BONUS")
taille = largeur, hauteur = taille_win[0], taille_win[1]  # taille de la fenêtre
fenetre = pygame.display.set_mode(taille)  # def la taille avec la ligne juste au dessus

img_mur = pygame.image.load("phantom.png").convert_alpha()
rect_mur = img_mur.get_rect()
img_mur = pygame.transform.scale(img_mur, (10, 10))

pygame.key.set_repeat(100,30)

time_elapsed_since_last_action = 0
clock = pygame.time.Clock()
score = 0

# ----------------------------------------------------------------

def coord(lst,nb):
    soluce = []
    compteur_x = 0
    for y in range(len(lst)):
        for x in lst[y]:
            if x==nb or x==3 or x==2:
                soluce.append([y,compteur_x])
            compteur_x+=1
        compteur_x=0
    return soluce

# ----------------------------------------------------------------

def nb_lignes(liste):
    return len(liste)

# ----------------------------------------------------------------

def nb_colones(liste):
    return len(liste[0])

# ----------------------------------------------------------------

def voisins_laby_acc(couple,liste):
    voisin = []
    chemin_dispo = coord(liste, 1)
    # Voisin bas
    if couple[0]<nb_lignes(liste)-1 and [couple[0]+1,couple[1]] in chemin_dispo:
        voisin.append([couple[0]+1,couple[1]])
    # Voisin droite
    if couple[1]<nb_colones(liste)-1 and [couple[0],couple[1]+1] in chemin_dispo:
        voisin.append([couple[0],couple[1]+1])
    # Voisin haut
    if couple[0]>0 and [couple[0]-1,couple[1]] in chemin_dispo:
        voisin.append([couple[0]-1,couple[1]])
    # Voisin gauche
    if couple[1]>0 and [couple[0],couple[1]-1] in chemin_dispo:
        voisin.append([couple[0],couple[1]-1])
    return voisin

# ----------------------------------------------------------------

def exploreVoie(depart,liste):
    chemin = [depart]
    vois_parcouru = []
    test = 0
    runing = True
    while runing and liste[chemin[-1][-2]][chemin[-1][-1]]!=3:
        temp_vois = voisins_laby_acc(chemin[-1],laby)
        for i in temp_vois:
            if i not in chemin and test == 0 and i not in vois_parcouru:
                chemin.append(i)
                test = 1
        if test == 0:
            
            vois_parcouru.append(chemin[-1])
            chemin.pop()
            if len(chemin) == 0:
                print("Pas de solution")
                runing = False
        test = 0
    return chemin

# ----------------------------------------------------------------

def jeu():
    global taille_win, chemin_plus_rapide, time_elapsed_since_last_action, score, clock
    running = 1
    fenetre.fill((192,192,192))
    dessiner = True
    fini = False
    font = pygame.font.Font(None, 60)
    while running:
        rect_mur.x, rect_mur.y = pos_joueur[0]*cote_carre, pos_joueur[1]*cote_carre
        for event in pygame.event.get():  # On parcourt la liste de tous les événements reçus
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                running = 0  # On arrête la boucle
            if event.type == KEYDOWN:  # si une touche pressé
                if fini == False:
                    if event.key == K_ESCAPE:  # si touche echap pressé
                        running = 0  # quitte le menu, ferme donc la fenêtre
                    if event.key == K_RIGHT and (laby[pos_joueur[0]+1][pos_joueur[1]] == 1 or laby[pos_joueur[0]+1][pos_joueur[1]] == 2 or laby[pos_joueur[0]+1][pos_joueur[1]] == 3):
                        pos_joueur[0]+=1
                    if event.key == K_LEFT and (laby[pos_joueur[0]-1][pos_joueur[1]] == 1 or laby[pos_joueur[0]-1][pos_joueur[1]] == 2 or laby[pos_joueur[0]-1][pos_joueur[1]] == 3):
                        pos_joueur[0]-=1
                    if event.key == K_UP and (laby[pos_joueur[0]][pos_joueur[1]-1] == 1 or laby[pos_joueur[0]][pos_joueur[1]-1] == 2 or laby[pos_joueur[0]][pos_joueur[1]-1] == 3):
                        pos_joueur[1]-=1
                    if event.key == K_DOWN and (laby[pos_joueur[0]][pos_joueur[1]+1] == 1 or laby[pos_joueur[0]][pos_joueur[1]+1] == 2 or laby[pos_joueur[0]][pos_joueur[1]+1] == 3):
                        pos_joueur[1]+=1

        if laby[pos_joueur[0]][pos_joueur[1]] == 3:
            running = False

        if dessiner:
            nb_bande=0
            liste_x=[-cote_carre,0]
            liste_y=[-cote_carre,0]
            for c in range(nb_lignes2(liste, cote_carre)//cote_carre):
                liste_y[0] += cote_carre
                liste_y[1] += cote_carre
                # Dessine ligne par ligne
                for l in liste[c]:
                    if l==0 or l==2 or l==3:
                        nb_bande += 1
                        liste_x[0] += cote_carre
                        liste_x[1] += cote_carre

                        for x in range(taille_win[0]): # parcourt les colonnes x
                            for y in range(taille_win[1]): # parcourt les lignes y
                                if x>=liste_x[0] and x<liste_x[1] and y>=liste_y[0] and y<liste_y[1]:
                                    if l==2:
                                        # graph.plot(y,x,"blue")
                                        pygame.gfxdraw.pixel(fenetre, y, x, (0,0,255))
                                    elif l==3:
                                        # graph.plot(y,x,"red")
                                        pygame.gfxdraw.pixel(fenetre, y, x, (255,0,0))
                                    else:
                                        # graph.plot(y,x)
                                        pygame.gfxdraw.pixel(fenetre, y, x, (0,0,0))
                        if nb_bande == nb_colones2(liste, cote_carre)//cote_carre:
                            nb_bande = 0
                            liste_x=[-cote_carre,0]
                    else:
                        nb_bande += 1
                        liste_x[0] += cote_carre
                        liste_x[1] += cote_carre
                        if nb_bande == nb_colones2(liste, cote_carre)//cote_carre:
                            nb_bande = 0
                            liste_x=[-cote_carre,0]
            pygame.image.save(fenetre, "laby_fond.png")
            img_fond = pygame.image.load("laby_fond.png").convert_alpha()
            rect_fond = img_fond.get_rect()
            dessiner = False

        dt = clock.tick() 

        time_elapsed_since_last_action += dt

        if time_elapsed_since_last_action > 1000:
            score+=1
            time_elapsed_since_last_action = 0
        
        if score == finish_time and fini == False:
            chem_final = exploreVoie(pos_joueur, liste)
            fini = True
            for j in chem_final:
                pos_joueur[0] = j[0]
                pos_joueur[1] = j[1]
                rect_mur.x, rect_mur.y = pos_joueur[0]*cote_carre, pos_joueur[1]*cote_carre
                fenetre.blit(img_fond, rect_fond)
                fenetre.blit(img_mur, rect_mur)
                pygame.display.flip()
                time.sleep(0.05)
            running = 0
        

        fenetre.blit(img_fond, rect_fond)
        fenetre.blit(img_mur, rect_mur)
        score1 = font.render(str(score), 1, (212, 120, 0))
        fenetre.blit(score1, (0, 0))
        pygame.display.flip()

# ----------------------------------------------------------------

jeu()
pygame.quit()

# ----------------------------------------------------------------

#########################################
####### Copyright Kylian-Project ########
#########################################
