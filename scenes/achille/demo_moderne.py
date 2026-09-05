import pygame

import config
import sons
from scene import SceneParadoxe
from ui import bouton, texte, theme

ETAPES = [
    "1) L'écart après l'étape k vaut D(k) = D0 × r^k, avec r = v_tortue/v_achille < 1.",
    "2) Une suite géométrique de raison r < 1 tend vers 0 : lim D(k) = 0 quand k → ∞.",
    "3) Chaque étape prend un temps réel : Δt(k) = D(k−1) / v_achille.",
    "4) La durée totale est la somme de cette série géométrique : T = Σ Δt(k).",
    "5) Cette somme géométrique de raison r < 1 converge : T = D0 / (v_achille − v_tortue).",
    "6) Donc : une infinité d'étapes tient dans un temps fini — Achille rattrape la tortue.",
]

DELAI_AUTO = 0.7


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

    def ajouter(self):
        if self.k < len(ETAPES):
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

    def gerer_evenement(self, event):
        super().gerer_evenement(event)
        for b in self.boutons:
            if b.gerer_evenement(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.ajouter()

    def mettre_a_jour(self, dt):
        if self.auto and self.k < len(ETAPES):
            self.temps += dt
            if self.temps >= DELAI_AUTO:
                self.temps = 0
                self.ajouter()

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2
        panneau = pygame.Rect(centre_x - 470, 210, 940, 340)
        pygame.draw.rect(ecran, theme.SURFACE, panneau, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, panneau, width=2, border_radius=14)

        y = 240
        for i in range(self.k):
            est_conclusion = (i == 5)
            couleur = theme.OR_CLAIR if est_conclusion else theme.CREME
            taille = 22 if est_conclusion else 20
            style = "gras" if est_conclusion else "normal"

            texte.dessiner_texte(
                ecran,
                ETAPES[i],
                centre_x - 430,
                y + i * 46,
                theme.police(taille, style),
                couleur,
                largeur_max=860
    )
