"""Motifs décoratifs : la frise grecque et la colonnade.

La colonnade est la signature visuelle de l'application : une
architrave à méandre dorée portée par de petites colonnes — un
temple en miniature, comme sur les frontispices des vieux ouvrages.
"""

import pygame


def dessiner_meandre(ecran, x, y, largeur, hauteur, couleur):
    """Dessine une frise de méandre allant de x à x + largeur.

    La frise est une ligne brisée unique qui alterne : montée sur la
    hauteur de la bande, court chemin le long du haut, descente, long
    chemin le long du bas — le motif de la « grecque » classique.
    """
    points = [(x, y + hauteur)]
    s = hauteur  # largeur d'une dent (carrée, comme sur les vases)
    cx, cy = x, y + hauteur
    while cx < x + largeur:
        cy = y                    # monter
        points.append((cx, cy))
        cx += s                    # filer le long du haut
        points.append((cx, cy))
        cy = y + hauteur           # descendre
        points.append((cx, cy))
        cx += 2 * s                # filer le long du bas
        points.append((cx, cy))
    pygame.draw.lines(ecran, couleur, False, points, max(2, hauteur // 5))


HAUTEUR_ARCHITRAVE = 9


def dessiner_colonnade(ecran, x, y, largeur,
                       couleur_or, couleur_or_clair, couleur_fut):
    """Dessine une mini-colonnade de temple grec.

    De haut en bas : un reflet de lumière, l'architrave (frise de
    méandre), les chapiteaux dorés, les fûts, les bases et le
    stylobate. La hauteur totale est d'environ 40 pixels.
    """
    dessiner_meandre(ecran, x, y, largeur, HAUTEUR_ARCHITRAVE, couleur_or)
    pygame.draw.line(ecran, couleur_or_clair,
                     (x, y - 1), (x + largeur, y - 1), 1)

    y_fut = y + HAUTEUR_ARCHITRAVE + 5
    hauteur_fut = 13
    pygame.draw.line(ecran, couleur_or,
                     (x, y_fut + 5 + hauteur_fut + 4),
                     (x + largeur, y_fut + 5 + hauteur_fut + 4), 2)

    pas = 46
    cx = x + pas // 2
    while cx < x + largeur - 14:
        pygame.draw.rect(ecran, couleur_or,
                         (cx - 7, y_fut, 14, 5))          # chapiteau
        pygame.draw.rect(ecran, couleur_fut,
                         (cx - 4, y_fut + 5, 8, hauteur_fut))  # fût
        pygame.draw.rect(ecran, couleur_or,
                         (cx - 6, y_fut + 5 + hauteur_fut, 12, 3))  # base
        cx += pas
