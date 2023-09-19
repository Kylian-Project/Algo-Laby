import tkdraw.basic as graph
import Labyrinthe


# ---------------------------------------------------------------------------------

def trouvee_depart(lst):
    soluce = []
    compteur_x = 0
    for y in range(len(lst)):
        for x in lst[y]:
            if x==2:
                soluce.append([y,compteur_x])
            compteur_x+=1
        compteur_x=0
    return soluce

# ---------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------

def nb_lignes(liste):
    return len(liste)

# ---------------------------------------------------------------------------------

def nb_colones(liste):
    return len(liste[0])

# ---------------------------------------------------------------------------------

def voisins_laby(lgn,col,liste):
    voisin = []
    # Voisin gauche
    if col>0:
        voisin.append([lgn,col-1])
    # Voisin droite
    if col<nb_colones(liste)-1:
        voisin.append([lgn,col+1])
    # Voisin haut
    if lgn>0:
        voisin.append([lgn-1,col])
    # Voisin bas
    if lgn<nb_lignes(liste)-1:
        voisin.append([lgn+1,col])

# ---------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------

def resolve_laby(liste):
    global chem_incomplet, derniers_chem, chemin, sous_chemin_final, chemin_plus_rapide
    chemin_final =[]

    chemin = trouvee_depart(liste)

    chem_incomplet = []

    vois_parcouru = []

    vois_pas_parcouru = []

    sous_chemin_final = []

    chemin_plus_rapide = []

    depart = True
    derniers_chem = False
    no_return = False

    def exploreVoie():
        global chem_incomplet, derniers_chem, chemin, sous_chemin_final, chemin_plus_rapide
        test = 0
        runing = True
        if len(chemin) == 0:
            runing = False
        elif len(chemin) > 1 and len(vois_pas_parcouru) == 0 and derniers_chem == False:
            runing = False
        while runing and liste[chemin[-1][-2]][chemin[-1][-1]]!=3:
            temp_vois = voisins_laby_acc(chemin[-1],laby)
            for i in temp_vois: # Gérer si la solution est dans les voisins (ne pas aller en dessous si elle est à droite)
                if liste[i[0]][i[1]]==3:
                    chemin.append(i)
                    runing = False
            if runing:
                for x in range(len(chemin_final)):
                    for y in chemin_final[x]:
                        sous_chemin_final += y

                for i in temp_vois:
                    if i not in chemin and test == 0 and i not in vois_parcouru and (depart or i not in sous_chemin_final):
                        if i in vois_pas_parcouru:
                            chem_incomplet.pop(vois_pas_parcouru.index(i))
                            vois_pas_parcouru.remove(i)
                        chemin.append(i)
                        temp_vois.pop(0)
                        if len(temp_vois)>=1:
                            for x in temp_vois:
                                if x not in chemin and x not in vois_pas_parcouru:
                                    if derniers_chem == True:
                                        derniers_chem = False
                                    if x not in vois_parcouru:
                                        vois_pas_parcouru.append(x)
                                        chem_incomplet += [chemin[:-1]]
                        test = 1
                if test == 0:
                    if len(chemin_final) > 0 or no_return:
                        chemin = []
                        runing = False
                                
                    else:
                        vois_parcouru.append(chemin[-1])
                        chemin.pop()
                        if len(chemin) == 0:
                            runing = False
                test = 0
        if len(chemin) > 0:
            chemin_final.append(chemin)
        sous_chemin_final = []
    
    exploreVoie()

    chemin_plus_rapide = min(chemin_final, key=len)
    if len(chemin_final) > 1:
        chemin_final.remove(min(chemin_final, key=len))

# --------------------------------------------------------------------------------- #

def nb_lignes2(liste,cote_carre):
    return len(liste)*cote_carre

# ------------------------------------------------------------------------

def nb_colones2(liste,cote_carre):
    return len(liste[0])*cote_carre

# ------------------------------------------------------------------------

def dessine_labyrinthe(liste,cote_carre):
    global taille_win, chemin_plus_rapide
    nb_bande=0
    liste_x=[-cote_carre,0]
    liste_y=[-cote_carre,0]
    taille_win = [nb_lignes2(liste, cote_carre),nb_colones2(liste, cote_carre),cote_carre]
    graph.open_win(taille_win[0],taille_win[1])
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
                                graph.plot(y,x,"blue")
                            elif l==3:
                                graph.plot(y,x,"red")
                            else:
                                graph.plot(y,x)
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

    resolve_laby(laby)
    dessin_soluce(laby,chemin_plus_rapide,"yellow")
    graph.wait()

# ------------------------------------------------------------------------

def dessin_soluce(liste,solu,color):
    for y in range(taille_win[0]):
        for x in range(taille_win[1]):
            for i in solu[1:-1]:
                if x>=i[1]*taille_win[2] and x<i[1]*taille_win[2]+taille_win[2] and y>=i[0]*taille_win[2] and y<i[0]*taille_win[2]+taille_win[2]:
                    graph.plot(y,x,color)


# ------------------------------------------------------------------------

# Taille doit être de nombres impaires
# 3ème chiffre = difficulté de 1 à 3
laby = Labyrinthe.creer(105,105,3)

# taille carré du labyrinthe
dessine_labyrinthe(laby, 5)