"""Étape « Démonstration moderne » : la série géométrique.

L'étape k du javelot ajoute 1/2^k à la distance parcourue. La barre
empile ces termes : chaque nouveau segment doré est exactement la
moitié du vide restant. La somme après k étapes vaut
S_k = 1/2 + 1/4 + … + 1/2^k = 1 − (1/2)^k, calculée en précision
exacte (jamais un « 1 » arrondi à l'écran).

Quand k grandit, (1/2)^k tend vers 0 : la somme S_k tend vers 1, et
la somme infinie vaut exactement 1. Une infinité d'étapes tient dans
une distance finie — c'est la réponse moderne à Zénon, affichée dès
que le motif de la série est visible (k ≥ 4).
"""

import pygame

import config
import sons
from scene import SceneParadoxe
from ui import bouton, texte, theme

from .maths import en_exposant, texte_valeur_parcourue, texte_valeur_reste

# --- Géométrie de la barre (même piste que l'illustration) ---
X_DEPART = 150
X_CIBLE = 1130
Y_BARRE = 320
HAUTEUR_BARRE = 44
LARGEUR = X_CIBLE - X_DEPART

# La conclusion apparaît quand le motif de la série est visible
SEUIL_CONCLUSION = 4

# --- Rythme du mode automatique ---
DELAI_AUTO = 0.5           # un terme toutes les 0,5 seconde


class EtapeDemoModerne(SceneParadoxe):
    TITRE = "Démonstration moderne"

    def __init__(self, manager):
        super().__init__(manager)
        y = 600
        self.bouton_ajouter = bouton.Bouton(
            150, y, 190, 44, "Ajouter (Espace)",
            on_clic=self.ajouter, taille_texte=18)
        self.bouton_auto = bouton.Bouton(
            360, y, 150, 44, "Auto : non",
            on_clic=self.basculer_auto, taille_texte=18)
        self.bouton_rejouer = bouton.Bouton(
            530, y, 150, 44, "Rejouer",
            on_clic=self.rejouer, taille_texte=18)
        self.boutons = [self.bouton_ajouter, self.bouton_auto,
                        self.bouton_rejouer]
        self.k = 0
        self.temps = 0
        self.auto = False

    def on_entrer(self):
        super().on_entrer()
        self.rejouer(avec_son=False)
        self.auto = False
        self.bouton_auto.texte = "Auto : non"

    # ------------------------------------------------------------------
    # Logique : k = nombre de termes de la somme S_k
    # ------------------------------------------------------------------
    def ajouter(self):
        """Ajoute le terme suivant 1/2^k à la somme."""
        self.k += 1
        sons.jouer("etape")

    def rejouer(self, avec_son=True):
        self.k = 0
        self.temps = 0
        if avec_son:
            sons.jouer("rejouer")

    def basculer_auto(self):
        self.auto = not self.auto
        self.temps = 0
        self.bouton_auto.texte = "Auto : oui" if self.auto else "Auto : non"

    # ------------------------------------------------------------------
    # Contrat de scène
    # ------------------------------------------------------------------
    def gerer_evenement(self, event):
        super().gerer_evenement(event)
        for b in self.boutons:
            if b.gerer_evenement(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.ajouter()

    def mettre_a_jour(self, dt):
        if self.auto:
            self.temps += dt
            if self.temps >= DELAI_AUTO:
                self.temps = 0
                self.ajouter()

    # ------------------------------------------------------------------
    # Dessin
    # ------------------------------------------------------------------
    def dessiner_contenu(self, ecran):
        self._dessiner_barre(ecran)
        self._dessiner_textes(ecran)
        for b in self.boutons:
            b.dessiner(ecran)

    def _dessiner_barre(self, ecran):
        # Le fond de la barre = la distance totale (le vide restant)
        pygame.draw.rect(ecran, theme.ENCRE_DOUCE,
                         (X_DEPART, Y_BARRE, LARGEUR, HAUTEUR_BARRE))
        pygame.draw.rect(ecran, theme.SURFACE,
                         (X_DEPART, Y_BARRE, LARGEUR, HAUTEUR_BARRE),
                         width=2, border_radius=6)

        # Les termes empilés : le segment i vaut 1/2^i de la distance.
        # Chaque nouveau segment est la moitié du vide restant, en or
        # alterné pour distinguer les termes entre eux.
        for i in range(1, min(self.k, 14) + 1):
            gauche = X_DEPART + (1 - 0.5 ** (i - 1)) * LARGEUR
            droite = X_DEPART + (1 - 0.5 ** i) * LARGEUR
            couleur = theme.OR if i % 2 == 1 else theme.OR_CLAIR
            pygame.draw.rect(ecran, couleur,
                             (gauche, Y_BARRE, droite - gauche,
                              HAUTEUR_BARRE))

        # Repères 0 et 1 sous la barre
        police = theme.police(16)
        texte.dessiner_texte(ecran, "0", X_DEPART, Y_BARRE + 52,
                             police, theme.ENCRE_DOUCE)
        texte.dessiner_texte(ecran, "1", X_CIBLE - 8, Y_BARRE + 52,
                             police, theme.ENCRE_DOUCE)

    def _dessiner_textes(self, ecran):
        x, y = X_DEPART, 405
        # La somme partielle, en valeurs exactes
        texte.dessiner_texte(
            ecran,
            f"Sₖ = 1/2 + 1/4 + 1/8 + … + 1/2{en_exposant(self.k)} "
            f"= 1 − 1/2{en_exposant(self.k)} = "
            f"{texte_valeur_parcourue(self.k)}",
            x, y, theme.police(22), theme.ENCRE)
        # Le dernier terme ajouté (0,5 ; 0,25 ; 0,125… décimales exactes)
        texte.dessiner_texte(
            ecran,
            f"Dernier terme ajouté : 1/2{en_exposant(self.k)} = "
            f"{texte_valeur_reste(self.k)}",
            x, y + 38, theme.police(22), theme.ENCRE)
        # La formule de la somme des termes d'une suite géométrique
        texte.dessiner_texte(
            ecran,
            "Suite géométrique de raison 1/2 :  Sₖ = ½ · "
            f"(1 − (1/2){en_exposant(self.k)}) / (1 − ½) = "
            f"1 − (1/2){en_exposant(self.k)}",
            x, y + 76, theme.police(18), theme.ENCRE_DOUCE)

        # Dès que le motif est visible : la conclusion de la démo.
        # En gras (et non en italique) pour que les exposants ⁴ ⁵ ⁶…
        # restent bien lisibles à cette taille.
        if self.k >= SEUIL_CONCLUSION:
            texte.dessiner_texte(
                ecran,
                f"Quand k → +∞ : (1/2){en_exposant(self.k)} → 0, "
                "donc Sₖ → 1.",
                x, y + 112, theme.police(18, "gras"), theme.OR_CLAIR)
            texte.dessiner_texte(
                ecran,
                "La somme infinie vaut exactement 1 : "
                "1/2 + 1/4 + 1/8 + … = 1. La distance est finie : "
                "le javelot atteint la cible.",
                x, y + 136, theme.police(18, "gras"), theme.OR_CLAIR)
