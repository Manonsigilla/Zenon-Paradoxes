"""Étape « Présentation » du paradoxe de la dichotomie.

Pose le paradoxe en une phrase, gravée sur une plaque sombre cerclée
d'or comme une inscription antique.
"""

import pygame

import config
from scene import SceneParadoxe
from ui import texte, theme


class EtapePresentation(SceneParadoxe):
    TITRE = "Présentation"

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2

        # Plaque : un panneau outremer bordé d'or
        plaque = pygame.Rect(centre_x - 420, 230, 840, 210)
        pygame.draw.rect(ecran, theme.SURFACE, plaque, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque, width=2, border_radius=14)

        # La citation du paradoxe, en pierre sur la plaque
        citation = ("« Le javelot n'atteint jamais la cible : "
                    "il reste toujours la moitié de la moitié du chemin. »")
        texte.dessiner_texte_centre(
            ecran, citation, centre_x, 258,
            theme.police(26, "italique"), theme.CREME, largeur_max=760)

        # Le contexte, en deux lignes
        texte.dessiner_texte_centre(
            ecran,
            "Pour toucher la cible, il faut d'abord couvrir la moitié de la "
            "distance, puis la moitié du reste, puis encore la moitié…\n"
            "Une infinité d'étapes semble nécessaire : le mouvement serait "
            "impossible.",
            centre_x, 355, theme.police(20), theme.ENCRE,
            largeur_max=860)
