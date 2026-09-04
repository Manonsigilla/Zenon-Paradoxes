"""Gestion des sons de l'application.

Les fichiers audio vont dans assets/sons/. Formats acceptés :
.wav et .ogg (PAS de .mp3 : pygame 2 ne le lit plus).

Chaque son est déclaré dans SONS (nom logique -> fichier) ; si le
fichier .ogg est absent, l'extension .wav est essayée à la place.
Quand le fichier n'existe pas du tout, jouer() ne fait rien : le
code est prêt à accueillir les sons dès qu'on les dépose dans le
dossier, et l'application fonctionne sans eux en attendant.
"""

import os

import pygame

import config

# ------------------------------------------------------------------------
# Déclaration des sons : pour ajouter un son, déposer le fichier dans
# assets/sons/ avec le bon nom (.ogg ou .wav), puis appeler
# sons.jouer("nom") là où l'événement se produit.
# ------------------------------------------------------------------------
SONS = {
    "etape": "etape.ogg",      # un demi-pas du javelot / une ligne révélée
    "limite": "limite.ogg",    # l'écran sature, le calcul continue
    "rejouer": "rejouer.ogg",  # remise à zéro
}

# Volume de lecture (0.0 = muet, 1.0 = maximum). Les sons trouvés en
# ligne ont des niveaux très variables : ce réglage s'applique à tous.
VOLUME = 0.6

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


def _chemin_existant(nom):
    """Chemin du fichier du son, en essayant .ogg puis .wav."""
    base = os.path.splitext(SONS[nom])[0]
    for extension in (".ogg", ".wav"):
        chemin = os.path.join(config.DOSSIER_SONS, base + extension)
        if os.path.exists(chemin):
            return chemin
    # Fichier introuvable : on renvoie le chemin attendu pour l'avertissement
    return os.path.join(config.DOSSIER_SONS, base + ".ogg")


def _charger(nom):
    """Charge (une fois) le son déclaré, ou None s'il est indisponible."""
    if nom in _sons_charges:
        return _sons_charges[nom]
    if not pygame.mixer.get_init():
        return None
    chemin = _chemin_existant(nom)
    if not os.path.exists(chemin):
        if nom not in _averti:
            print(f"Sons : fichier absent (déposez-le dans assets/sons/) : {chemin}")
            _averti.add(nom)
        return None
    try:
        son = pygame.mixer.Sound(chemin)
        son.set_volume(VOLUME)
    except pygame.error:
        return None
    _sons_charges[nom] = son
    return son


def jouer(nom):
    """Joue le son déclaré. Sans effet si le fichier n'existe pas."""
    son = _charger(nom)
    if son is not None:
        son.play()
