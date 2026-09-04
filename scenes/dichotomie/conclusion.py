"""Étape « Conclusion » : la morale mathématique de la dichotomie.

Zénon affirme « jamais » ; la limite répond. Une infinité d'étapes
peut tenir dans une distance finie : une somme infinie de nombres
positifs n'est pas forcément infinie.
"""

import pygame

import config
from scene import SceneParadoxe
from ui import texte, theme


class EtapeConclusion(SceneParadoxe):
    TITRE = "Conclusion"

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2

        # Plaque 1 : la thèse de Zénon
        plaque_zenon = pygame.Rect(centre_x - 430, 200, 860, 150)
        pygame.draw.rect(ecran, theme.SURFACE, plaque_zenon,
                         border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque_zenon, width=2,
                         border_radius=14)
        # Le bloc (citation + signature) est centré verticalement dans
        # la plaque : on compte d'abord les lignes réelles de la
        # citation, on en déduit la hauteur du bloc, puis le départ.
        citation = ("« Il reste toujours une moitié à parcourir : le "
                    "javelot n'atteint jamais la cible. »")
        police_citation = theme.police(22, "italique")
        police_signature = theme.police(16)
        h_citation = (len(texte.decouper_texte(citation, police_citation, 780))
                      * (police_citation.get_height() + 6) - 6)
        ecart = 4
        hauteur_bloc = h_citation + ecart + police_signature.get_height()
        y_citation = (plaque_zenon.top
                      + (plaque_zenon.height - hauteur_bloc) // 2)

        # dessiner_texte_centre renvoie la hauteur réellement utilisée :
        # la signature se place juste dessous, sans jamais chevaucher,
        # même si la citation tient sur une ou deux lignes.
        hauteur = texte.dessiner_texte_centre(
            ecran, citation, centre_x, y_citation,
            police_citation, theme.CREME, largeur_max=780)
        texte.dessiner_texte_centre(
            ecran, "— Zénon", centre_x, y_citation + hauteur + ecart,
            police_signature, theme.ENCRE_DOUCE)

        # Plaque 2 : la réponse moderne
        plaque_moderne = pygame.Rect(centre_x - 430, 375, 860, 160)
        pygame.draw.rect(ecran, theme.SURFACE, plaque_moderne,
                         border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque_moderne, width=2,
                         border_radius=14)
        texte.dessiner_texte_centre(
            ecran,
            "Une infinité d'étapes peut tenir dans une distance finie :",
            centre_x, 398, theme.police(20), theme.CREME, largeur_max=780)
        texte.dessiner_texte_centre(
            ecran, "1/2 + 1/4 + 1/8 + … = 1",
            centre_x, 438, theme.police(26, "gras"), theme.OR_CLAIR)
        texte.dessiner_texte_centre(
            ecran,
            "Le javelot atteint la cible — mais seulement « à la limite ».",
            centre_x, 482, theme.police(20), theme.CREME, largeur_max=780)

        # La morale, en une ligne
        texte.dessiner_texte_centre(
            ecran,
            "CQFD — Zénon s'est trompé : une somme infinie de nombres "
            "positifs n'est pas forcément infinie.",
            centre_x, 560, theme.police(20, "italique"), theme.OR_CLAIR,
            largeur_max=1000)
