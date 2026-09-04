"""Gestion des sons de l'application.

Les fichiers audio vont dans assets/sons/. Formats acceptés :
.wav et .ogg (PAS de .mp3 : pygame 2 ne le lit plus).

Chaque son est déclaré dans SONS (nom logique -> fichier). Quand le
fichier n'existe pas encore, jouer() ne fait rien : le code est prêt
à accueillir les sons dès qu'on les dépose dans le dossier, et
l'application fonctionne sans eux en attendant.
"""

import os

import pygame

import config

# ------------------------------------------------------------------------
# Déclaration des sons : pour ajouter un son, déposer le fichier dans
# assets/sons/ avec le bon nom, puis appeler sons.jouer("nom") là où
# l'événement se produit.
# ------------------------------------------------------------------------
SONS = {
    "etape": "etape.ogg",      # un demi-pas du javelot
    "limite": "limite.ogg",    # l'écran ne peut plus rien montrer
    "rejouer": "rejouer.ogg",  # remise à zéro
}

_sons_charges = {}
_averti = set()


def initialiser():
    """Initialise le module audio (appelée dans main.py).

    Si l'initialisation échoue (pas de périphérique audio), on ne
    bloque pas l'application : les sons seront simplement ignorés.
    """
    try:
        pygame.mixer.init()
    except pygame.error:
        pass


def _charger(nom):
    """Charge (une fois) le son déclaré, ou None s'il est indisponible."""
    if nom in _sons_charges:
        return _sons_charges[nom]
    if not pygame.mixer.get_init():
        return None
    chemin = os.path.join(config.DOSSIER_SONS, SONS[nom])
    if not os.path.exists(chemin):
        if nom not in _averti:
            print(f"Sons : fichier absent (déposez-le dans assets/sons/) : {chemin}")
            _averti.add(nom)
        return None
    try:
        son = pygame.mixer.Sound(chemin)
    except pygame.error:
        return None
    _sons_charges[nom] = son
    return son


def jouer(nom):
    """Joue le son déclaré. Sans effet si le fichier n'existe pas."""
    son = _charger(nom)
    if son is not None:
        son.play()
