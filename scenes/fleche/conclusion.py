"""Étape « Conclusion » : le paradoxe est levé par la notion de vitesse.

Zénon confond "être quelque part à un instant" et "être immobile dans
le temps". Le calcul infinitésimal montre qu'une position instantanée
n'empêche pas une vitesse non nulle.
"""

import pygame

import config
from scene import SceneParadoxe
from ui import texte, theme


class EtapeConclusion(SceneParadoxe):
    TITRE = "Conclusion"

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2

        plaque_zenon = pygame.Rect(centre_x - 430, 200, 860, 150)
        pygame.draw.rect(ecran, theme.SURFACE, plaque_zenon, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque_zenon, width=2, border_radius=14)

        citation = ("« À chaque instant la flèche est au repos ; "
                    "donc le mouvement n'existe pas. »")
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
            ecran, "— Zénon", centre_x, y_citation + hauteur + ecart,
            police_signature, theme.ENCRE_DOUCE)

        plaque_moderne = pygame.Rect(centre_x - 430, 375, 860, 160)
        pygame.draw.rect(ecran, theme.SURFACE, plaque_moderne, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque_moderne, width=2, border_radius=14)

        texte.dessiner_texte_centre(
            ecran,
            "À un instant, la position est fixée ; sur un intervalle, elle varie.",
            centre_x, 404, theme.police(20), theme.CREME, largeur_max=800)
        texte.dessiner_texte_centre(
            ecran,
            "La vitesse instantanée peut être non nulle : v(t)=x'(t).",
            centre_x, 440, theme.police(26, "gras"), theme.OR_CLAIR)
        texte.dessiner_texte_centre(
            ecran,
            "Donc le mouvement est cohérent avec les instants.",
            centre_x, 480, theme.police(20), theme.CREME, largeur_max=780)

        texte.dessiner_texte_centre(
            ecran,
            "CQFD — La flèche n'est pas immobile : elle a une position à chaque instant et une vitesse définie.",
            centre_x, 560, theme.police(20, "italique"), theme.OR_CLAIR,
            largeur_max=1020)