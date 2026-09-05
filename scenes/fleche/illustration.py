import pygame

import config
import sons
from scene import SceneParadoxe
from ui import bouton, texte, theme

X_DEPART = 170
X_ARRIVEE = 1110
Y_TRAJECTOIRE = 360
NB_INSTANTS = 12

DELAI_AUTO = 0.6

class EtapeIllustration(SceneParadoxe):
    TITRE = "Illustration"

    def __init__(self, manager):
        super().__init__(manager)
        y = 600
        self.bouton_avancer = bouton.Bouton(
            150, y, 190, 44, "Avancer (Espace)",
            on_clic=self.avancer, taille_texte=18)
        self.bouton_auto = bouton.Bouton(
            360, y, 150, 44, "Auto : non",
            on_clic=self.basculer_auto, taille_texte=18)
        self.bouton_rejouer = bouton.Bouton(
            530, y, 150, 44, "Rejouer",
            on_clic=self.rejouer, taille_texte=18)
        self.boutons = [self.bouton_avancer, self.bouton_auto,
                        self.bouton_rejouer]
        self.k = 0
        self.temps = 0
        self.auto = False

    def on_entrer(self):
        super().on_entrer()
        self.rejouer(avec_son=False)
        self.auto = False
        self.bouton_auto.texte = "Auto : non"

    def avancer(self):
        if self.k < NB_INSTANTS:
            self.k += 1
            sons.jouer("etape")
        self.bouton_avancer.actif = self.k < NB_INSTANTS

    def rejouer(self, avec_son=True):
        self.k = 0
        self.temps = 0
        self.bouton_avancer.actif = True
        if avec_son:
            sons.jouer("rejouer")

    def basculer_auto(self):
        self.auto = not self.auto
        self.temps = 0
        self.bouton_auto.texte = "Auto : oui" if self.auto else "Auto : non"

    def x_fleche(self):
        if NB_INSTANTS == 0:
            return X_DEPART
        return X_DEPART + (self.k / NB_INSTANTS) * (X_ARRIVEE - X_DEPART)

    def gerer_evenement(self, event):
        super().gerer_evenement(event)
        for b in self.boutons:
            if b.gerer_evenement(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.avancer()

    def mettre_a_jour(self, dt):
        if self.auto and self.k < NB_INSTANTS:
            self.temps += dt
            if self.temps >= DELAI_AUTO:
                self.temps = 0
                self.avancer()

    def dessiner_contenu(self, ecran):
        self._dessiner_trajectoire(ecran)
        self._dessiner_fleche(ecran)
        self._dessiner_textes(ecran)
        for b in self.boutons:
            b.dessiner(ecran)

    def _dessiner_trajectoire(self, ecran):
        pygame.draw.line(ecran, theme.ENCRE_DOUCE,
                        (X_DEPART, Y_TRAJECTOIRE), (X_ARRIVEE, Y_TRAJECTOIRE), 2)
        pygame.draw.circle(ecran, theme.OR, (X_DEPART, Y_TRAJECTOIRE), 6)
        pygame.draw.circle(ecran, theme.OR, (X_ARRIVEE, Y_TRAJECTOIRE), 6)

        for i in range(NB_INSTANTS + 1):
            x = int(X_DEPART + i * (X_ARRIVEE - X_DEPART) / NB_INSTANTS)
            pygame.draw.line(ecran, theme.SURFACE, (x, Y_TRAJECTOIRE - 8),
                            (x, Y_TRAJECTOIRE + 8), 1)

    def _dessiner_fleche(self, ecran):
        x = int(self.x_fleche())
        fut = pygame.Rect(x - 65, Y_TRAJECTOIRE - 2, 50, 4)
        pygame.draw.rect(ecran, theme.CREME, fut)
        pygame.draw.rect(ecran, theme.SURFACE, fut, width=1)
        pygame.draw.polygon(ecran, theme.SURFACE,
                            [(x - 16, Y_TRAJECTOIRE - 8), (x + 2, Y_TRAJECTOIRE),
                            (x - 16, Y_TRAJECTOIRE + 8)])
        pygame.draw.polygon(ecran, theme.OR,
                            [(x - 16, Y_TRAJECTOIRE - 6), (x, Y_TRAJECTOIRE),
                            (x - 16, Y_TRAJECTOIRE + 6)])

    def _dessiner_textes(self, ecran):
        x, y = 150, 440
        texte.dessiner_texte(
            ecran, f"Instant : {self.k}/{NB_INSTANTS}",
            x, y, theme.police(32, "titre"), theme.ENCRE,
            contour=theme.OR, epaisseur=1)
        texte.dessiner_texte(
            ecran,
            "À cet instant précis, la flèche est immobile (position fixée).",
            x, y + 52, theme.police(22), theme.ENCRE)
        texte.dessiner_texte(
            ecran,
            "Mais en passant à l'instant suivant, sa position change.",
            x, y + 84, theme.police(22), theme.ENCRE)
        if self.k == NB_INSTANTS:
            texte.dessiner_texte(
                ecran,
                "La succession des instants reconstitue le mouvement complet.",
                x, y + 118, theme.police(18, "italique"), theme.OR_CLAIR)