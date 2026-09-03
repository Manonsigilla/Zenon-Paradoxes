"""Bouton réutilisable : survol, clic, état désactivé, sous-texte.

Deux apparences, dans l'esprit du thème :
- style par défaut : bouton bleu outremer, texte pierre cerclé d'or,
  pour le fond bleu nuit ;
- style inverse (inverse=True) : bouton pierre, texte outremer, pour
  les panneaux sombres (barre de navigation).
Le survol passe à l'or dans les deux cas : l'or = interactif.
"""

import pygame

from ui import texte, theme


class Bouton:
    """Bouton rectangulaire à coins arrondis.

    texte : libellé principal (gras).
    sous_texte : libellé secondaire optionnel, plus petit.
    on_clic : fonction appelée quand le bouton est cliqué.
    actif : False pour afficher le bouton grisé et ignorer les clics.
    inverse : True pour le style clair sur fond sombre.
    """

    def __init__(self, x, y, largeur, hauteur, texte, on_clic=None,
                 actif=True, taille_texte=22, sous_texte=None, inverse=False):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.sous_texte = sous_texte
        self.on_clic = on_clic
        self.actif = actif
        self.inverse = inverse
        self.police = theme.police(taille_texte, "gras")
        self.police_sous_texte = theme.police(16)

    def est_survole(self):
        """True si la souris est au-dessus d'un bouton actif."""
        return self.actif and self.rect.collidepoint(pygame.mouse.get_pos())

    def gerer_evenement(self, event):
        """Renvoie True si le bouton vient d'être cliqué."""
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.actif and self.rect.collidepoint(event.pos)):
            if self.on_clic is not None:
                self.on_clic()
            return True
        return False

    def dessiner(self, ecran):
        if not self.actif:
            fond, couleur, bordure = theme.GRIS, theme.GRIS_TEXTE, None
            contour = None
        elif self.est_survole():
            fond, couleur, bordure = theme.OR, theme.SURFACE, theme.OR_CLAIR
            contour = theme.SURFACE
        elif self.inverse:
            fond, couleur, bordure = theme.CREME, theme.SURFACE, theme.OR
            contour = theme.OR
        else:
            fond, couleur, bordure = theme.SURFACE, theme.CREME, theme.OR
            contour = theme.OR
        pygame.draw.rect(ecran, fond, self.rect, border_radius=10)
        if bordure is not None:
            pygame.draw.rect(ecran, bordure, self.rect, width=2,
                             border_radius=10)

        hauteur_ligne = self.police.get_height()
        sous_hauteur = (self.police_sous_texte.get_height() + 4
                        if self.sous_texte else 0)
        lignes = self.texte.split("\n")
        y = self.rect.centery - (len(lignes) * hauteur_ligne + sous_hauteur) // 2

        for ligne in lignes:
            surface = texte.rendre_texte(ligne, self.police, couleur,
                                         contour=contour, epaisseur=1)
            ecran.blit(surface, surface.get_rect(
                center=(self.rect.centerx, y + hauteur_ligne // 2)))
            y += hauteur_ligne

        if self.sous_texte:
            surface = texte.rendre_texte(self.sous_texte,
                                         self.police_sous_texte, couleur,
                                         contour=contour, epaisseur=1)
            y += 2
            ecran.blit(surface, surface.get_rect(
                center=(self.rect.centerx,
                        y + self.police_sous_texte.get_height() // 2)))
