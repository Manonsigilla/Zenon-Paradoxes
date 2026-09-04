"""Étape « Démonstration de Zénon » : son raisonnement, pas à pas.

Les cinq temps du raisonnement de Zénon apparaissent un par un
(Espace ou bouton), comme s'il les énonçait lui-même. La fraction à
droite de chaque ligne suit la progression : 1/2, 1/4, 1/8, 1/2ᵏ,
puis l'infinité d'étapes.
"""

import pygame

import config
import sons
from scene import SceneParadoxe
from ui import bouton, texte, theme

# Les cinq temps du raisonnement (texte, fraction affichée à droite).
# Les numéraux grecs Α Β Γ Δ Ε rappellent qu'il s'agit d'une suite.
ETAPES = [
    ("Pour toucher la cible, le javelot doit d'abord parcourir "
     "la moitié de la distance.", "1/2"),
    ("Puis la moitié du chemin restant.", "1/4"),
    ("Puis encore la moitié du nouveau reste.", "1/8"),
    ("Et ainsi de suite : chaque moitié franchie laisse "
     "une nouvelle moitié à franchir.", "1/2ᵏ"),
    ("Il reste donc TOUJOURS une étape : le javelot "
     "n'atteint jamais la cible.", "∞"),
]
NUMERAUX = ["Α", "Β", "Γ", "Δ", "Ε"]

Y_PANNEAU = 190
HAUTEUR_PANNEAU = 370
Y_PREMIERE_LIGNE = 212
HAUTEUR_LIGNE = 72


class EtapeDemoZenon(SceneParadoxe):
    TITRE = "Démonstration de Zénon"

    def __init__(self, manager):
        super().__init__(manager)
        y = 600
        self.bouton_suivant = bouton.Bouton(
            150, y, 230, 44, "Étape suivante (Espace)",
            on_clic=self.reveler, taille_texte=18)
        self.bouton_rejouer = bouton.Bouton(
            400, y, 150, 44, "Rejouer",
            on_clic=self.rejouer, taille_texte=18)
        self.boutons = [self.bouton_suivant, self.bouton_rejouer]
        self.visibles = 0

    def on_entrer(self):
        super().on_entrer()
        self.rejouer(avec_son=False)

    # ------------------------------------------------------------------
    # Logique : une seule variable d'état, le nombre de lignes révélées
    # ------------------------------------------------------------------
    def reveler(self):
        """Révèle la ligne suivante du raisonnement."""
        if self.visibles < len(ETAPES):
            self.visibles += 1
            sons.jouer("etape")
            self.bouton_suivant.actif = self.visibles < len(ETAPES)

    def rejouer(self, avec_son=True):
        """Cache à nouveau toutes les lignes."""
        self.visibles = 0
        self.bouton_suivant.actif = True
        if avec_son:
            sons.jouer("rejouer")

    # ------------------------------------------------------------------
    # Contrat de scène
    # ------------------------------------------------------------------
    def gerer_evenement(self, event):
        super().gerer_evenement(event)
        for b in self.boutons:
            if b.gerer_evenement(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.reveler()

    # ------------------------------------------------------------------
    # Dessin
    # ------------------------------------------------------------------
    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2

        # Plaque : le raisonnement est gravé sur un panneau sombre
        panneau = pygame.Rect(centre_x - 430, Y_PANNEAU, 860,
                              HAUTEUR_PANNEAU)
        pygame.draw.rect(ecran, theme.SURFACE, panneau, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, panneau, width=2, border_radius=14)

        # Les lignes déjà révélées, numérotées à la grecque
        for i in range(self.visibles):
            y = Y_PREMIERE_LIGNE + i * HAUTEUR_LIGNE
            texte.dessiner_texte(ecran, NUMERAUX[i],
                                 centre_x - 394, y,
                                 theme.police(20, "gras"), theme.OR)
            texte.dessiner_texte(ecran, ETAPES[i][0],
                                 centre_x - 350, y + 2,
                                 theme.police(19), theme.CREME,
                                 largeur_max=560)
            # La fraction, alignée à droite de la plaque
            fraction = ETAPES[i][1]
            police_fraction = theme.police(22, "gras")
            largeur = police_fraction.size(fraction)[0]
            texte.dessiner_texte(ecran, fraction,
                                 centre_x + 394 - largeur, y,
                                 police_fraction, theme.OR_CLAIR)

        # Quand tout est révélé : la conclusion de Zénon
        if self.visibles == len(ETAPES):
            texte.dessiner_texte_centre(
                ecran,
                "Conclusion de Zénon : le javelot n'atteint jamais la "
                "cible — le mouvement serait impossible.",
                centre_x, 576, theme.police(20, "italique"), theme.OR_CLAIR,
                largeur_max=1000)

        for b in self.boutons:
            b.dessiner(ecran)
