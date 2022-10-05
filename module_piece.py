SPAWN = 'maps/spawn_point.txt'
COULOIR = 'maps/couloir.txt'
PIECE_PREFIX = "salle_"
DOSSIER = 'maps'

def lister_fichiers(fichier_prefix):
    import os
    liste = []
    for fichier in os.listdir(DOSSIER):
        if fichier.startswith(fichier_prefix):
            liste.append(os.path.join(DOSSIER, fichier))
    return liste

def charger_piece(fichier):
    with open(fichier) as f:
        # le contenu est transformé en liste, chaque ligne étant un objet de la liste
        return f.read().split()

def charger_pieces_aleatoires():
    liste = []
    for fichier in lister_fichiers(PIECE_PREFIX):
        liste.append(charger_piece(fichier))
    return liste

def charger_toutes_pieces():
    return charger_piece(SPAWN), charger_piece(COULOIR), charger_pieces_aleatoires()

def ecrire_piece(contenu, nom_fichier):
    with open(nom_fichier, 'w') as f:
        # assemblage des listes et conversion en texte pour les mettre dans le fichier
        texte = '\n'.join(contenu)
        f.write(texte)
