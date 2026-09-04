"""Étape « Illustration » : le javelot qui n'atteint jamais la cible.

Le javelot avance par moitiés successives : à l'étape k il a couvert
1 − (1/2)^k de la distance et il reste (1/2)^k. La position n'est
JAMAIS calculée autrement que par cette formule : le paradoxe vit
dans le code, le javelot ne peut structurellement pas dépasser la
cible.

La pointe du javelot EST sa position : elle converge vers le centre
de la cible sans jamais l'atteindre mathématiquement. Quand le reste
devient minuscule, une loupe centrée sur le centre exact de la cible
(marqué d'une croix) apparaît ; dès que l'écart devient trop petit
pour être vu, son grossissement double — le zoom « poursuit » la
limite, et l'avancée de la pointe reste visible indéfiniment.

On ne borne pas le nombre d'étapes : mathématiquement (1/2)^k ne
s'annule jamais, et l'affichage reste honnête quel que soit k —
décimales exactes jusqu'à k = 12 (1/2^k possède exactement k
décimales), puis notation scientifique (« 1 − 4,77 × 10⁻⁷ ») qui
n'affiche jamais un « 1 » arrondi. À l'écran la pointe finit par
se figer dans la cible, mais les chiffres, eux, continuent.
"""

import pygame

import config
import sons
from scene import SceneParadoxe
from ui import bouton, texte, theme

from .maths import en_exposant, texte_valeur_parcourue, texte_valeur_reste

# --- Géométrie de la piste (tout est dérivé de ces constantes) ---
X_DEPART = 150
X_CIBLE = 1130
Y_PISTE = 380
LARGEUR_PISTE = X_CIBLE - X_DEPART

SEUIL_PIXEL = 15       # au-delà : plus rien ne bouge à l'écran, message

# --- Loupe ---
ECHELLE_BASE = 10          # grossissement de départ de la loupe
LARGEUR_LOUPE = 320        # taille du panneau à l'écran
HAUTEUR_LOUPE = 160
LOUPE_X = 900              # coin haut-gauche du panneau
LOUPE_Y = 185
SEUIL_LOUPE = 80           # la loupe apparaît quand il reste < 80 pixels
SEUIL_GAP_LOUPE = 4        # écart minimal visible : en dessous, le zoom double

# --- Rythme du mode automatique ---
DELAI_AUTO = 0.5           # une étape toutes les 0,5 seconde

class EtapeIllustration(SceneParadoxe):
    TITRE = "Illustration"

    def __init__(self, manager):
        super().__init__(manager)
        # Les boutons internes (en plus de la barre de navigation)
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
        # La loupe dessine dans une surface dédiée : on ne zoome pas
        # des pixels, on redessine la zone à une autre échelle.
        self.loupe = pygame.Surface((LARGEUR_LOUPE, HAUTEUR_LOUPE))
        # État initial (réglé proprement par on_entrer)
        self.k = 0
        self.temps = 0
        self.auto = False

    def on_entrer(self):
        # À CHAQUE arrivée sur la scène : on repart de zéro
        # (silencieusement : pas de son quand on arrive).
        super().on_entrer()
        self.rejouer(avec_son=False)
        self.auto = False
        self.bouton_auto.texte = "Auto : non"

    # ------------------------------------------------------------------
    # Logique : l'état tient en trois variables (k, temps, auto)
    # ------------------------------------------------------------------
    def avancer(self):
        """Une étape de plus : le javelot couvre la moitié du reste.

        Aucune limite : mathématiquement (1/2)^k ne s'annule jamais,
        on peut continuer indéfiniment. Au-delà de k = 12, l'affichage
        passe en notation scientifique pour rester honnête
        (« 1 − 4,77 × 10⁻⁷ »), jamais un « 1 » arrondi.
        """
        self.k += 1
        sons.jouer("etape")
        if self.k == SEUIL_PIXEL:
            sons.jouer("limite")   # l'écran sature, le calcul continue

    def rejouer(self, avec_son=True):
        """Remet le javelot au départ."""
        self.k = 0
        self.temps = 0
        self.bouton_avancer.actif = True
        if avec_son:
            sons.jouer("rejouer")

    def basculer_auto(self):
        """Active ou coupe le défilement automatique."""
        self.auto = not self.auto
        self.temps = 0
        self.bouton_auto.texte = "Auto : oui" if self.auto else "Auto : non"

    def fraction_parcourue(self):
        """Fraction de la distance couverte : 1 − (1/2)^k.

        C'est LE cœur mathématique de la scène : mathématiquement,
        cette valeur est strictement inférieure à 1 pour tout k.
        On écrit 0.5 ** k plutôt que 1 / 2 ** k : les deux sont
        identiques, mais 0.5 ** k tend doucement vers 0 pour k énorme,
        alors que 1 / 2 ** k lèverait une erreur au-delà de k = 1074.
        """
        return 1 - 0.5 ** self.k

    def x_du_javelot(self):
        """Position de la POINTE en pixels : conversion fraction → écran."""
        return X_DEPART + self.fraction_parcourue() * LARGEUR_PISTE

    # ------------------------------------------------------------------
    # Contrat de scène
    # ------------------------------------------------------------------
    def gerer_evenement(self, event):
        # La barre de navigation et le clavier ← → Échap d'abord
        super().gerer_evenement(event)
        for b in self.boutons:
            if b.gerer_evenement(event):
                return
        # Espace : une demi-distance de plus
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.avancer()

    def mettre_a_jour(self, dt):
        # Le mode auto ne s'arrête jamais de lui-même : les étapes
        # continuent tant qu'on le laisse tourner. dt est le temps
        # écoulé depuis la dernière image : l'animation a le même
        # rythme quelle que soit la vitesse de la machine.
        if self.auto:
            self.temps += dt
            if self.temps >= DELAI_AUTO:
                self.temps = 0
                self.avancer()

    # ------------------------------------------------------------------
    # Dessin
    # ------------------------------------------------------------------
    def dessiner_contenu(self, ecran):
        self._dessiner_piste(ecran)
        self._dessiner_loupe(ecran)
        self._dessiner_textes(ecran)
        for b in self.boutons:
            b.dessiner(ecran)

    def _dessiner_piste(self, ecran):
        # La ligne de vol et la marque de départ
        pygame.draw.line(ecran, theme.ENCRE_DOUCE,
                         (X_DEPART, Y_PISTE), (X_CIBLE, Y_PISTE), 2)
        pygame.draw.line(ecran, theme.ENCRE_DOUCE,
                         (X_DEPART, Y_PISTE - 14), (X_DEPART, Y_PISTE + 14), 2)

        x = self.x_du_javelot()   # x EST la pointe du javelot

        # Le chemin restant, en or : de la pointe au centre de la cible.
        # Il se réduit de moitié à chaque étape.
        pygame.draw.line(ecran, theme.OR, (x, Y_PISTE), (X_CIBLE, Y_PISTE), 5)

        # La cible : ronds concentriques, comme un bouclier grec
        pygame.draw.circle(ecran, theme.SURFACE, (X_CIBLE, Y_PISTE), 38)
        pygame.draw.circle(ecran, theme.CREME, (X_CIBLE, Y_PISTE), 27)
        pygame.draw.circle(ecran, theme.SURFACE, (X_CIBLE, Y_PISTE), 17)
        pygame.draw.circle(ecran, theme.OR, (X_CIBLE, Y_PISTE), 8)

        # Le centre exact de la cible : une petite croix crème
        pygame.draw.line(ecran, theme.CREME,
                         (X_CIBLE, Y_PISTE - 14), (X_CIBLE, Y_PISTE + 14), 2)
        pygame.draw.line(ecran, theme.CREME,
                         (X_CIBLE - 14, Y_PISTE), (X_CIBLE + 14, Y_PISTE), 2)

        # Le javelot, ancré par sa pointe : fût crème cerclé de sombre
        # pour rester lisible devant la cible, pointe dorée à l'avant.
        fut = pygame.Rect(x - 64, Y_PISTE - 2, 48, 4)
        pygame.draw.rect(ecran, theme.CREME, fut)
        pygame.draw.rect(ecran, theme.SURFACE, fut, width=1)
        # La pointe est dessinée deux fois : un triangle sombre un peu
        # plus grand, puis le triangle doré par-dessus. Le liseré sombre
        # qui en résulte garde la pointe visible même une fois posée
        # sur le point central doré de la cible.
        pygame.draw.polygon(ecran, theme.SURFACE,
                            [(x - 16, Y_PISTE - 8), (x + 2, Y_PISTE),
                             (x - 16, Y_PISTE + 8)])
        pygame.draw.polygon(ecran, theme.OR,
                            [(x - 16, Y_PISTE - 6), (x, Y_PISTE),
                             (x - 16, Y_PISTE + 6)])

    def _dessiner_loupe(self, ecran):
        """Loupe centrée sur le centre exact de la cible, zoom adaptatif.

        Dès que l'écart restant devient trop petit pour être vu, le
        grossissement double : le zoom « poursuit » la limite, et
        l'avancée de la pointe reste visible indéfiniment. Deux
        ambiances : vue extérieure (fond nuit, cible en arcs) tant
        que la pointe est hors du point doré ; vue intérieure (fond
        or) quand elle est dedans — le chemin restant et le centre
        exact y sont dessinés en sombre pour rester lisibles.
        """
        reste_pixels = LARGEUR_PISTE * 0.5 ** self.k
        if reste_pixels >= SEUIL_LOUPE:
            return

        x = self.x_du_javelot()
        cx = LARGEUR_LOUPE // 2    # le centre de la cible,
        cy = HAUTEUR_LOUPE // 2    # au milieu du panneau

        # Zoom adaptatif : tant que l'écart est trop petit pour être
        # vu, on double le grossissement. L'écart dans la loupe reste
        # ainsi toujours entre SEUIL_GAP_LOUPE et 2 × SEUIL_GAP_LOUPE.
        echelle = ECHELLE_BASE
        n_zooms = 0
        while reste_pixels * echelle < SEUIL_GAP_LOUPE:
            echelle *= 2
            n_zooms += 1

        # La pointe est-elle à l'intérieur du point doré central ?
        # (moins de 8 pixels réels du centre)
        dans_le_point = reste_pixels < 8

        surface = self.loupe
        surface.fill(theme.OR if dans_le_point else theme.FOND)

        def vers_loupe(x_reel):
            """Conversion réel → loupe.

            Les coordonnées sont bornées : à très fort grossissement,
            les objets hors champ auraient des coordonnées énormes qui
            feraient déborder les entiers de pygame.
            """
            valeur = cx + (x_reel - X_CIBLE) * echelle
            return max(-5000, min(LARGEUR_LOUPE + 5000, valeur))

        def bornes_y(valeur):
            return max(-5000, min(HAUTEUR_LOUPE + 5000, valeur))

        # La ligne de vol, puis la marque du centre exact (une croix)
        couleur_trait = theme.SURFACE if dans_le_point else theme.ENCRE_DOUCE
        pygame.draw.line(surface, couleur_trait,
                         (0, cy), (LARGEUR_LOUPE, cy), 2)

        # Vue extérieure : le bord de la cible en arc, puis le point
        # doré. Au-delà d'une certaine taille, les cercles rempliraient
        # tout le panneau (et feraient déborder les entiers) : on ne
        # les dessine plus.
        if not dans_le_point and 38 * echelle <= 4 * LARGEUR_LOUPE:
            pygame.draw.circle(surface, theme.SURFACE, (cx, cy),
                               38 * echelle)
        if not dans_le_point and 8 * echelle <= 4 * LARGEUR_LOUPE:
            pygame.draw.circle(surface, theme.OR, (cx, cy), 8 * echelle)
        pygame.draw.line(surface, couleur_trait,
                         (cx, 0), (cx, HAUTEUR_LOUPE), 2)

        # Le chemin restant, de la pointe au centre exact
        couleur_gap = theme.SURFACE if dans_le_point else theme.OR
        pygame.draw.line(surface, couleur_gap,
                         (int(vers_loupe(x)), cy), (cx, cy), 5)

        # Le javelot : fût et pointe cerclés de sombre ; la pointe
        # devient crème quand elle est posée sur l'or, pour rester
        # visible.
        gauche_fut = int(vers_loupe(x - 64))
        droite_fut = int(vers_loupe(x - 16))
        haut_fut = int(bornes_y(cy - 2 * echelle))
        bas_fut = int(bornes_y(cy + 2 * echelle))
        fut = pygame.Rect(gauche_fut, haut_fut,
                          droite_fut - gauche_fut, bas_fut - haut_fut)
        if fut.width > 0 and fut.height > 0:
            pygame.draw.rect(surface, theme.CREME, fut)
            pygame.draw.rect(surface, theme.SURFACE, fut, width=2)
        couleur_pointe = theme.CREME if dans_le_point else theme.OR
        pygame.draw.polygon(surface, theme.SURFACE,
                            [(int(vers_loupe(x - 16)),
                              int(bornes_y(cy - 6 * echelle - 2))),
                             (int(vers_loupe(x)) + 2, cy),
                             (int(vers_loupe(x - 16)),
                              int(bornes_y(cy + 6 * echelle + 2)))])
        pygame.draw.polygon(surface, couleur_pointe,
                            [(int(vers_loupe(x - 16)),
                              int(bornes_y(cy - 6 * echelle))),
                             (int(vers_loupe(x)), cy),
                             (int(vers_loupe(x - 16)),
                              int(bornes_y(cy + 6 * echelle)))])

        # L'échelle affichée raconte le zoom qui poursuit la limite
        if n_zooms == 0:
            legende = f"× {ECHELLE_BASE}"
        else:
            legende = f"× {ECHELLE_BASE} · 2{en_exposant(n_zooms)}"
        texte.dessiner_texte(surface, legende, 10, 8,
                             theme.police(16, "gras"), theme.OR_CLAIR)

        # Affichage du panneau, cerclé d'or
        ecran.blit(surface, (LOUPE_X, LOUPE_Y))
        cadre = pygame.Rect(LOUPE_X, LOUPE_Y, LARGEUR_LOUPE, HAUTEUR_LOUPE)
        pygame.draw.rect(ecran, theme.OR, cadre, width=2, border_radius=8)

    def _dessiner_textes(self, ecran):
        x, y = X_DEPART, 435
        texte.dessiner_texte(ecran, f"Étape {self.k}",
                             x, y, theme.police(32, "titre"), theme.ENCRE,
                             contour=theme.OR, epaisseur=1)
        # Les valeurs exactes, sans arrondi : décimales exactes
        # jusqu'à k = 12, puis notation scientifique — jamais un « 1 »
        # ni un « 0 » arrondis, aussi loin qu'on aille (voir maths.py).
        texte_parcouru = texte_valeur_parcourue(self.k)
        texte_reste = texte_valeur_reste(self.k)
        texte.dessiner_texte(
            ecran, f"Parcouru : 1 − 1/2{en_exposant(self.k)} = {texte_parcouru}",
            x, y + 48, theme.police(22), theme.ENCRE)
        texte.dessiner_texte(
            ecran, f"Reste   : 1/2{en_exposant(self.k)} = {texte_reste}",
            x, y + 80, theme.police(22), theme.ENCRE)
        if self.k >= SEUIL_PIXEL:
            # L'écran sature, mais le calcul continue : le dire.
            texte.dessiner_texte(
                ecran,
                "Plus rien ne bouge à l'écran : il reste moins d'un pixel, même à la loupe ×10.",
                x, y + 112, theme.police(17, "italique"), theme.OR_CLAIR)
            texte.dessiner_texte(
                ecran,
                "Mais 1/2^k ne s'annule jamais — les décimales, elles, continuent. →",
                x, y + 136, theme.police(17, "italique"), theme.OR_CLAIR)
        else:
            texte.dessiner_texte(
                ecran, "Espace : franchir la moitié du chemin restant",
                x, y + 120, theme.police(16, "italique"), theme.ENCRE_DOUCE)
