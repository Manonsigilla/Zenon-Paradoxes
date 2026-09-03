"""Barre de navigation commune à toutes les étapes des paradoxes.

En bas de l'écran : un bandeau vernis (sombre), le bouton Accueil à
gauche, l'indicateur d'étape au centre, Précédent / Suivant à droite.
Les boutons Précédent et Suivant se désactivent automatiquement aux
extrémités du parcours.
"""

import pygame

import config
from ui import theme, texte
from ui.bouton import Bouton

TAILLE_TEXTE = 20
HAUTEUR_BOUTON = 44


class BarreNavigation:
    def __init__(self, manager):
        self.manager = manager
        self.numero, self.total = 1, 1

        y = (config.HAUTEUR - config.HAUTEUR_BARRE
             + (config.HAUTEUR_BARRE - HAUTEUR_BOUTON) // 2)
        largeur = 160
        self.bouton_accueil = Bouton(
            config.MARGE, y, 150, HAUTEUR_BOUTON, "Accueil",
            on_clic=lambda: manager.aller_a("accueil"),
            taille_texte=TAILLE_TEXTE, inverse=True)
        self.bouton_precedent = Bouton(
            config.LARGEUR - config.MARGE - 2 * largeur - 20, y,
            largeur, HAUTEUR_BOUTON, "← Précédent",
            on_clic=manager.precedent, taille_texte=TAILLE_TEXTE, inverse=True)
        self.bouton_suivant = Bouton(
            config.LARGEUR - config.MARGE - largeur, y,
            largeur, HAUTEUR_BOUTON, "Suivant →",
            on_clic=manager.suivant, taille_texte=TAILLE_TEXTE, inverse=True)

    def mettre_a_jour(self, position):
        """position = (numéro de l'étape courante, total d'étapes)."""
        self.numero, self.total = position
        self.bouton_precedent.actif = self.numero > 1
        self.bouton_suivant.actif = self.numero < self.total

    def gerer_evenement(self, event):
        for bouton in (self.bouton_accueil, self.bouton_precedent,
                       self.bouton_suivant):
            if bouton.gerer_evenement(event):
                return

    def dessiner(self, ecran):
        bandeau = pygame.Rect(0, config.HAUTEUR - config.HAUTEUR_BARRE,
                              config.LARGEUR, config.HAUTEUR_BARRE)
        pygame.draw.rect(ecran, theme.SURFACE, bandeau)
        pygame.draw.line(ecran, theme.OR, bandeau.topleft, bandeau.topright, 2)

        self.bouton_accueil.dessiner(ecran)
        self.bouton_precedent.dessiner(ecran)
        self.bouton_suivant.dessiner(ecran)

        police = theme.police(TAILLE_TEXTE)
        texte.dessiner_texte_centre(
            ecran, f"Étape {self.numero} / {self.total}",
            config.LARGEUR // 2, bandeau.centery - police.get_height() // 2,
            police, theme.CREME, contour=theme.OR, epaisseur=1)
