"""Configuration globale de l'application.

Toutes les constantes partagées entre les scènes vivent ici :
dimensions de la fenêtre, FPS, chemins des ressources.
"""

import os

# --- Fenêtre ---
LARGEUR = 1280
HAUTEUR = 720
TAILLE_ECRAN = (LARGEUR, HAUTEUR)
FPS = 60
TITRE = "Les paradoxes de Zénon"

# --- Chemins des ressources ---
# Chemin absolu de la racine du projet, quel que soit l'endroit
# d'où le programme est lancé.
RACINE = os.path.dirname(os.path.abspath(__file__))
DOSSIER_ASSETS = os.path.join(RACINE, "assets")
DOSSIER_FONTS = os.path.join(DOSSIER_ASSETS, "fonts")
DOSSIER_IMAGES = os.path.join(DOSSIER_ASSETS, "images")
DOSSIER_SONS = os.path.join(DOSSIER_ASSETS, "sons")

# --- Mise en page ---
MARGE = 60          # marge latérale commune à toutes les scènes
HAUTEUR_BARRE = 64  # hauteur de la barre de navigation en bas
