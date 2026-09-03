"""Identité visuelle : le temple grec dans la nuit.

Palette inspirée d'un temple grec sous le ciel nocturne :
- le fond est un bleu ardoise profond (la nuit) ;
- les panneaux et boutons sont en bleu outremer (l'ombre du temple) ;
- les écritures sont couleur de pierre, cerclées d'un filet d'or ;
- l'or marque l'interactivité (survol) et les éléments nobles
  (architrave, chapiteaux, liserés) ;
- la terre rouge habille les fûts des colonnes.

Les titres utilisent Cardo, police dessinée pour les textes
classiques ; le corps du texte reste en DejaVu Sans, qui couvre les
symboles mathématiques (∑, ∞, ½, Δ, →…).
"""

import os

import pygame

import config

# ------------------------------------------------------------------------
# Palette (à utiliser telle quelle dans toutes les scènes)
# ------------------------------------------------------------------------
FOND = (46, 53, 70)            # NUIT — bleu ardoise, fond général
SURFACE = (40, 61, 112)        # OUTREMER — panneaux et boutons
ENCRE = (224, 221, 213)        # PIERRE — texte principal
ENCRE_DOUCE = (170, 166, 155)  # texte secondaire
CREME = (224, 221, 213)        # texte sur SURFACE (= pierre)
OR = (227, 177, 78)            # OR — contours, chapiteaux, survol
OR_CLAIR = (246, 215, 141)     # reflet doré (liserés de lumière)
ROUGE = (112, 53, 41)          # TERRE ROUGE — fûts des colonnes
GRIS = (74, 80, 100)           # bouton désactivé : fond
GRIS_TEXTE = (148, 152, 168)   # bouton désactivé : texte

# ------------------------------------------------------------------------
# Polices (dans assets/fonts, voir les fichiers de licence)
# ------------------------------------------------------------------------
_FICHIERS = {
    "normal": "DejaVuSans.ttf",
    "gras": "DejaVuSans-Bold.ttf",
    "italique": "DejaVuSans-Oblique.ttf",
    "titre": "Cardo-Bold.ttf",
}
_cache_polices = {}


def police(taille=24, style="normal"):
    """Renvoie une police (mise en cache pour la performance).

    style : "normal", "gras", "italique" (DejaVu) ou "titre" (Cardo).
    """
    cle = (taille, style)
    if cle not in _cache_polices:
        chemin = os.path.join(config.DOSSIER_FONTS, _FICHIERS[style])
        _cache_polices[cle] = pygame.font.Font(chemin, taille)
    return _cache_polices[cle]
