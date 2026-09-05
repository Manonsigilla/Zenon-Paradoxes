"""Étape « Conclusion » : le paradoxe d'Achille et la tortue est levé
par la sommation d'une série infinie en temps fini.

Zénon confond "une infinité d'étapes" et "un temps infini". Le calcul
montre qu'une somme infinie de durées de plus en plus courtes peut
converger vers un total fini : Achille rattrape bel et bien la tortue.
"""

import pygame

import config
from scene import SceneParadoxe
from ui import texte, theme

from .achille_et_tortue import cible, temps_rattrapage


class EtapeConclusion(SceneParadoxe):
    TITRE = "Conclusion"

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2

        plaque_zenon = pygame.Rect(centre_x - 430, 200, 860, 150)
        pygame.draw.rect(ecran, theme.SURFACE, plaque_zenon, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque_zenon, width=2, border_radius=14)

        citation = ("« Le plus lent ne sera jamais rattrapé dans sa course "
                    "par le plus rapide, car le poursuivant doit d'abord "
                    "parvenir au point d'où est parti le fuyard. »")
        police_citation = theme.police(22, "italique")
        police_signature = theme.police(16)
        h_citation = (len(texte.decouper_texte(citation, police_citation, 780))
                      * (police_citation.get_height() + 6) - 6)
        ecart = 4
        hauteur_bloc = h_citation + ecart + police_signature.get_height()
        y_citation = (plaque_zenon.top
                      + (plaque_zenon.height - hauteur_bloc) // 2)

        hauteur = texte.dessiner_texte_centre(
            ecran, citation, centre_x, y_citation,
            police_citation, theme.CREME, largeur_max=780)
        texte.dessiner_texte_centre(
            ecran, "— Zénon d'Élée", centre_x, y_citation + hauteur + ecart,
            police_signature, theme.ENCRE_DOUCE)

        plaque_moderne = pygame.Rect(centre_x - 430, 375, 860, 160)
        pygame.draw.rect(ecran, theme.SURFACE, plaque_moderne, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque_moderne, width=2, border_radius=14)

        texte.dessiner_texte_centre(
            ecran,
            "Chaque étape de Zénon prend un temps réel, de plus en plus court.",
            centre_x, 404, theme.police(20), theme.CREME, largeur_max=800)
        texte.dessiner_texte_centre(
            ecran,
            f"Somme infinie, temps fini : Achille rattrape la tortue à "
            f"{float(cible()):.0f} m, en t = {temps_rattrapage():.0f} s.",
            centre_x, 440, theme.police(26, "gras"), theme.OR_CLAIR)
        texte.dessiner_texte_centre(
            ecran,
            "Une infinité de pas ne signifie pas une durée infinie.",
            centre_x, 480, theme.police(20), theme.CREME, largeur_max=780)

        texte.dessiner_texte_centre(
            ecran,
            "CQFD — Achille n'est pas condamné à l'infini : la série "
            "géométrique D0×(1+r+r²+…) converge, et le rattrapage a bien lieu.",
            centre_x, 560, theme.police(20, "italique"), theme.OR_CLAIR,
            largeur_max=1020)
