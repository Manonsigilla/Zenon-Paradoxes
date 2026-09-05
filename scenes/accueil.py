"""Page d'accueil : titre, sous-titre et 3 boutons vers les paradoxes.

Les boutons portent les numéraux grecs Α Β Γ, comme une inscription
antique : les trois paradoxes forment une suite.
"""

import pygame

import config
from scene import Scene
from ui import bouton, motifs, texte, theme

# Chaque bouton pointe vers la première étape de son paradoxe ("nom-0").
# Tant qu'un paradoxe n'est pas codé, son bouton pointe vers le squelette :
# remplacez "squelette-0" par "fleche-0", "dichotomie-0" ou "achille-0"
# dès que le paradoxe correspondant existe.
PARADOXES = [
    ("Α", "La flèche en vol",
    "Le mouvement existe-t-il à l'instant ?",
    "fleche-0"),
    ("Β", "La dichotomie",
    "Peut-on parcourir une distance finie ?",
    "dichotomie-0"),
    ("Γ", "Achille et la tortue",
    "Le plus rapide peut-il rattraper le plus lent ?",
    "achille-0"),
]

LARGEUR_BOUTON = 620
HAUTEUR_BOUTON = 82


class SceneAccueil(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        centre_x = config.LARGEUR // 2
        premier_y = 330
        espace = HAUTEUR_BOUTON + 26
        self.boutons = []
        for i, (lettre, nom, sous_titre, cible) in enumerate(PARADOXES):
            self.boutons.append(bouton.Bouton(
                centre_x - LARGEUR_BOUTON // 2, premier_y + i * espace,
                LARGEUR_BOUTON, HAUTEUR_BOUTON,
                f"{lettre}   {nom}", sous_texte=sous_titre,
                # Le paramètre par défaut fige la cible au moment de la
                # création du bouton (sinon tous pointeraient la dernière).
                on_clic=lambda cible=cible: manager.aller_a(cible),
                taille_texte=26))

    def gerer_evenement(self, event):
        for b in self.boutons:
            if b.gerer_evenement(event):
                return

    def dessiner(self, ecran):
        ecran.fill(theme.FOND)
        centre_x = config.LARGEUR // 2

        texte.dessiner_texte_centre(ecran, "ΖΗΝΩΝ Ο ΕΛΕΑΤΗΣ",
                                    centre_x, 84,
                                    theme.police(20, "titre"), theme.ENCRE,
                                    contour=theme.OR, epaisseur=1)
        texte.dessiner_texte_centre(ecran, "Les paradoxes de Zénon",
                                    centre_x, 116,
                                    theme.police(54, "titre"), theme.ENCRE,
                                    contour=theme.OR, epaisseur=2)
        texte.dessiner_texte_centre(
            ecran, "Zénon d'Élée (Ve siècle av. J.-C.) — trois paradoxes du mouvement",
            centre_x, 200, theme.police(22, "italique"), theme.ENCRE_DOUCE)

        # Colonnade sous le titre
        motifs.dessiner_colonnade(ecran, centre_x - 230, 256, 460,
                                theme.OR, theme.OR_CLAIR, theme.ROUGE)

        for b in self.boutons:
            b.dessiner(ecran)

        # Pied de page : complétez avec vos noms si vous le souhaitez.
        texte.dessiner_texte_centre(
            ecran, "Projet de mathématiques",
            centre_x, config.HAUTEUR - 55,
            theme.police(16, "italique"), theme.ENCRE_DOUCE)
