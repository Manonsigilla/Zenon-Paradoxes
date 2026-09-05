import pygame

import config
import sons
from scene import SceneParadoxe
from ui import bouton, texte, theme

ETAPES = [
    ("Le temps est composé d'instants.", "t₁, t₂, t₃, …"),
    ("À chaque instant, la flèche occupe un lieu déterminé.", "x(t)"),
    ("Occuper un lieu déterminé, c'est y être au repos.", "repos"),
    ("Donc à chaque instant, la flèche est immobile.", "∀t : v = 0 ?"),
    ("Somme d'immobilités ⇒ pas de mouvement réel.", "mouvement impossible"),
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

    def reveler(self):
        if self.visibles < len(ETAPES):
            self.visibles += 1
            sons.jouer("etape")
            self.bouton_suivant.actif = self.visibles < len(ETAPES)

    def rejouer(self, avec_son=True):
        self.visibles = 0
        self.bouton_suivant.actif = True
        if avec_son:
            sons.jouer("rejouer")

    def gerer_evenement(self, event):
        super().gerer_evenement(event)
        for b in self.boutons:
            if b.gerer_evenement(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.reveler()

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2
        panneau = pygame.Rect(centre_x - 430, Y_PANNEAU, 860, HAUTEUR_PANNEAU)
        pygame.draw.rect(ecran, theme.SURFACE, panneau, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, panneau, width=2, border_radius=14)

        for i in range(self.visibles):
            y = Y_PREMIERE_LIGNE + i * HAUTEUR_LIGNE
            texte.dessiner_texte(ecran, NUMERAUX[i], centre_x - 394, y,
                                theme.police(20, "gras"), theme.OR)
            texte.dessiner_texte(ecran, ETAPES[i][0], centre_x - 350, y + 2,
                                theme.police(19), theme.CREME, largeur_max=560)
            formule = ETAPES[i][1]
            police_formule = theme.police(20, "gras")
            largeur = police_formule.size(formule)[0]
            texte.dessiner_texte(ecran, formule, centre_x + 394 - largeur, y,
                                police_formule, theme.OR_CLAIR)

        if self.visibles == len(ETAPES):
            texte.dessiner_texte_centre(
                ecran,
                "Conclusion de Zénon : la flèche est immobile à chaque instant, "
                "donc le mouvement semblerait impossible.",
                centre_x, 576, theme.police(20, "italique"), theme.OR_CLAIR,
                largeur_max=1000)

        for b in self.boutons:
            b.dessiner(ecran)