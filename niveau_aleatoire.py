import random
from module_piece import charger_toutes_pieces, ecrire_piece


def choisir_piece(liste):
    #choix hasard chiffre entre 0 et 2
    pièce_hasard = random.randint(0, len(liste) - 1) 
    return liste[pièce_hasard] #en fonction du chiffre donné au hasard

def trouver_limites(liste):
    # trouver la position des premiere et dernière lignes ayant un mur
    debut = -1
    for index, ligne in enumerate(liste):
        if ligne[-1] == '1':
            fin = index
            if debut == -1:
                debut = index
    return (debut, fin)

def generer(piece_debut, couloir_liste):
    # première pièce
    # quelques variables
    longueur_premiere_piece = len(piece_debut[0])
    longueur_couloir = len(couloir_liste[0])
    largeur_couloir = len(couloir_liste)
    debut, fin = trouver_limites(piece_debut)
    debut_couloir = random.randint(debut, fin - largeur_couloir)
    fin_couloir = debut_couloir + len(couloir_liste) - 1
    # on copie la piece de debut comme point de depart de la piece complete
    piece_complete = piece_debut[:]

    for ligne in range(0, len(piece_complete)):
        if ligne == debut_couloir or ligne == fin_couloir:
            piece_complete[ligne] = piece_complete[ligne] + couloir_liste[ligne - debut_couloir]
        elif ligne < debut_couloir or ligne > fin_couloir:
            piece_complete[ligne] = piece_complete[ligne] + '.' * longueur_couloir
        else:
            piece_complete[ligne] = piece_complete[ligne][:-1] + '.' + couloir_liste[ligne - debut_couloir]

    # deuxième pièce
    # quelques variables
    seconde_piece = choisir_piece(generation)
    # position supérieure du couloir par rapport au debut de la seconde piece
    # on la determine de manière aléatoire mais sans que la deuxième pièce soit plus haute que la première
    # afin de simplifier l'algorithme et éviter d'ajouter des lignes au début du tableau
    jonction_couloir = random.randint(0, min(debut_couloir, len(seconde_piece)-1 - largeur_couloir))
    position_initiale = debut_couloir - jonction_couloir
    largeur_complete = max(len(piece_complete), len(piece_complete) - position_initiale + len(seconde_piece) - 1)
    longeur_seconde_piece = len(seconde_piece[0])
    largeur_seconde_piece = len(seconde_piece)

    for ligne in range(0, largeur_complete):
        if ligne < position_initiale or ligne > position_initiale + largeur_seconde_piece - 1:
            # on est dessus la seconde pièce ou dessous la seconde piece, on ajoute des espaces
            if ligne < len(piece_complete):
                piece_complete[ligne] += '.' * longeur_seconde_piece
        else:
            # on est au niveau de la seconde piece, on ajoute la piece
            if ligne > debut_couloir and ligne < (debut_couloir + largeur_couloir - 1):
                # on est dans le couloir, on enlève les murs
                piece_complete[ligne] += '.' + seconde_piece[ligne - position_initiale][1:]
            elif ligne >= len(piece_complete):
                # on est plus bas que la première pièce, on ajoute des espaces
                piece_complete.append('.' * (longueur_premiere_piece + longueur_couloir) + seconde_piece[ligne - position_initiale])
            else:
                # dans les autres cas, on concatène tout simplement
                piece_complete[ligne] += seconde_piece[ligne - position_initiale]

    return piece_complete

nombre_pieces = 10
piece_debut, couloir_liste, generation = charger_toutes_pieces()
piece_initiale = piece_debut
for piece in range(nombre_pieces - 1):
    piece_finale = generer(piece_initiale, couloir_liste)
    piece_initiale = piece_finale

ecrire_piece(piece_finale, 'map.txt')
