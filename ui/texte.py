"""Affichage de texte : retour à la ligne, centrage, contour doré.

Utilise les polices DejaVu Sans de ui/theme.py, qui couvrent les
symboles mathématiques (∑, ∞, ½, Δ, →…) nécessaires aux
démonstrations.

Le contour est un vrai contour : le texte est rendu dans la couleur
du contour, décalé dans toutes les directions, puis la couleur du
texte est posée par-dessus — l'écriture apparaît cerclée d'or.
"""

import pygame

_cache_rendus = {}


def rendre_texte(texte, police, couleur, contour=None, epaisseur=1):
    """Surface contenant le texte, cerclé de `contour` si demandé.

    epaisseur : épaisseur du contour en pixels (1 = fin, 2 = gravé).
    """
    cle = (texte, id(police), couleur, contour, epaisseur)
    if cle not in _cache_rendus:
        surface = police.render(texte, True, couleur)
        if contour is not None:
            decalages = [
                (dx, dy)
                for dx in range(-epaisseur, epaisseur + 1)
                for dy in range(-epaisseur, epaisseur + 1)
                if 0 < dx * dx + dy * dy <= epaisseur * epaisseur
            ]
            bord = police.render(texte, True, contour)
            resultat = pygame.Surface(
                (surface.get_width() + 2 * epaisseur,
                 surface.get_height() + 2 * epaisseur),
                pygame.SRCALPHA)
            for dx, dy in decalages:
                resultat.blit(bord, (epaisseur + dx, epaisseur + dy))
            resultat.blit(surface, (epaisseur, epaisseur))
            surface = resultat
        _cache_rendus[cle] = surface
    return _cache_rendus[cle]


def decouper_texte(texte, police, largeur_max):
    """Découpe un texte en lignes tenant dans largeur_max (en pixels).

    Les retours à la ligne explicites ("\n") sont respectés.
    """
    lignes = []
    for paragraphe in texte.split("\n"):
        mots = paragraphe.split()
        ligne = ""
        for mot in mots:
            essai = (ligne + " " + mot).strip()
            if not ligne or police.size(essai)[0] <= largeur_max:
                ligne = essai
            else:
                lignes.append(ligne)
                ligne = mot
        lignes.append(ligne)
    return lignes


def dessiner_texte(ecran, texte, x, y, police, couleur,
                   largeur_max=None, interligne=6, contour=None, epaisseur=1):
    """Dessine un texte (multi-lignes) en haut à gauche de (x, y).

    Renvoie la hauteur totale utilisée, pratique pour enchaîner
    plusieurs blocs de texte les uns sous les autres.
    """
    lignes = (decouper_texte(texte, police, largeur_max)
              if largeur_max else texte.split("\n"))
    pas = police.get_height() + interligne
    for i, ligne in enumerate(lignes):
        surface = rendre_texte(ligne, police, couleur, contour, epaisseur)
        ecran.blit(surface, (x, y + i * pas))
    return len(lignes) * pas - interligne


def dessiner_texte_centre(ecran, texte, centre_x, y, police, couleur,
                          largeur_max=None, interligne=6,
                          contour=None, epaisseur=1):
    """Comme dessiner_texte, mais chaque ligne est centrée sur centre_x."""
    lignes = (decouper_texte(texte, police, largeur_max)
              if largeur_max else texte.split("\n"))
    pas = police.get_height() + interligne
    for i, ligne in enumerate(lignes):
        surface = rendre_texte(ligne, police, couleur, contour, epaisseur)
        ecran.blit(surface, (centre_x - surface.get_width() // 2, y + i * pas))
    return len(lignes) * pas - interligne
