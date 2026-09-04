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

        # Plaque : un panneau outremer bordé d'or, assez haut pour que
        # le texte respire (la citation et le contexte tiennent
        # confortablement à l'intérieur)
        plaque = pygame.Rect(centre_x - 420, 225, 840, 250)
        pygame.draw.rect(ecran, theme.SURFACE, plaque, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque, width=2, border_radius=14)

        # La citation du paradoxe, en pierre sur la plaque
        citation = ("« Le javelot n'atteint jamais la cible : "
                    "il reste toujours la moitié de la moitié du chemin. »")
        police_citation = theme.police(26, "italique")
        police_contexte = theme.police(20)
        contexte = ("Pour toucher la cible, il faut d'abord couvrir la "
                    "moitié de la distance, puis la moitié du reste, puis "
                    "encore la moitié…\n"
                    "Une infinité d'étapes semble nécessaire : le "
                    "mouvement serait impossible.")

        # Le bloc (citation + contexte) est centré verticalement dans la
        # plaque : on compte d'abord ses lignes réelles, on en déduit sa
        # hauteur, puis on calcule le point de départ.
        h_citation = (len(texte.decouper_texte(citation, police_citation, 760))
                      * (police_citation.get_height() + 6) - 6)
        h_contexte = (len(texte.decouper_texte(contexte, police_contexte, 860))
                      * (police_contexte.get_height() + 6) - 6)
        ecart = 16
        y_bloc = (plaque.top
                  + (plaque.height - (h_citation + ecart + h_contexte)) // 2)

        texte.dessiner_texte_centre(
            ecran, citation, centre_x, y_bloc,
            police_citation, theme.CREME, largeur_max=760)
        texte.dessiner_texte_centre(
            ecran, contexte, centre_x, y_bloc + h_citation + ecart,
            police_contexte, theme.ENCRE, largeur_max=860)
