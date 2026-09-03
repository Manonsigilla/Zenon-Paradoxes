"""Contrat commun des scènes et base des étapes de paradoxe.

Chaque écran de l'application (l'accueil comme les étapes des
paradoxes) respecte le même contrat : on_entrer / gerer_evenement /
mettre_a_jour / dessiner. Le gestionnaire (scene_manager.py) ne
connaît rien d'autre d'une scène.
"""

import pygame

import config
from ui import barre_navigation, motifs, texte, theme


class Scene:
    """Contrat commun à toutes les scènes de l'application."""

    def __init__(self, manager):
        self.manager = manager

    def on_entrer(self):
        """Appelée par le gestionnaire quand la scène devient active.

        À surcharger pour réinitialiser l'état d'une scène (par
        exemple remettre une animation à zéro avant de la rejouer).
        """

    def gerer_evenement(self, event):
        """Reçoit les événements pygame (clics, clavier…)."""

    def mettre_a_jour(self, dt):
        """Met à jour l'état de la scène. dt est en secondes.

        C'est ici que vivent les animations : positions calculées
        à partir du temps écoulé depuis la dernière image.
        """

    def dessiner(self, ecran):
        """Dessine la scène sur l'écran."""


class SceneParadoxe(Scene):
    """Base commune aux étapes d'un paradoxe.

    Fournit l'entête (nom du paradoxe + titre de l'étape) et la barre
    de navigation. Chaque étape concrète ne surcharge que
    dessiner_contenu (et éventuellement mettre_a_jour / gerer_evenement
    pour les animations et interactions).
    """

    TITRE = "Étape"
    HAUTEUR_ENTETE = 152  # hauteur réservée à l'entête (titre + colonnade)

    def __init__(self, manager):
        super().__init__(manager)
        self.barre = barre_navigation.BarreNavigation(manager)

    def on_entrer(self):
        self.barre.mettre_a_jour(self.manager.position_de(self.manager.id_actuel))

    def gerer_evenement(self, event):
        # Une étape qui a besoin de ses propres interactions surcharge
        # cette méthode en appelant d'abord super().gerer_evenement(event)
        # pour garder la barre de navigation et le clavier fonctionnels.
        self.barre.gerer_evenement(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.manager.precedent()
            elif event.key == pygame.K_RIGHT:
                self.manager.suivant()
            elif event.key == pygame.K_ESCAPE:
                self.manager.aller_a("accueil")

    def dessiner(self, ecran):
        ecran.fill(theme.FOND)
        self._dessiner_entete(ecran)
        self.dessiner_contenu(ecran)
        self.barre.dessiner(ecran)

    def _dessiner_entete(self, ecran):
        nom = self.manager.nom_paradoxe(self.manager.id_actuel)
        texte.dessiner_texte(ecran, nom.upper(), config.MARGE, 36,
                             theme.police(18, "titre"), theme.ENCRE,
                             contour=theme.OR, epaisseur=1)
        texte.dessiner_texte(ecran, self.TITRE, config.MARGE, 62,
                             theme.police(38, "titre"), theme.ENCRE,
                             contour=theme.OR, epaisseur=2)

        # Aide clavier, discrète, en haut à droite
        aide = "← → naviguer   ·   Échap : accueil"
        police_aide = theme.police(16)
        largeur_aide = police_aide.size(aide)[0]
        texte.dessiner_texte(
            ecran, aide, config.LARGEUR - config.MARGE - largeur_aide, 44,
            police_aide, theme.ENCRE_DOUCE)

        # Colonnade, signature du thème
        motifs.dessiner_colonnade(ecran, config.MARGE, 114,
                                  config.LARGEUR - 2 * config.MARGE,
                                  theme.OR, theme.OR_CLAIR, theme.ROUGE)

    def dessiner_contenu(self, ecran):
        """Contenu propre à l'étape : à surcharger."""
