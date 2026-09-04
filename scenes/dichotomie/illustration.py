"""Étape « Illustration » : le javelot qui n'atteint jamais la cible.

Le javelot avance par moitiés successives : à l'étape k il a couvert
1 − (1/2)^k de la distance et il reste (1/2)^k. La position n'est
JAMAIS calculée autrement que par cette formule : le paradoxe vit
dans le code, le javelot ne peut structurellement pas dépasser la
cible.

La pointe du javelot EST sa position : elle converge vers le centre
de la cible sans jamais l'atteindre mathématiquement. Quand le reste
devient minuscule, une loupe ×10 centrée sur le centre de la cible
apparaît : on voit la pointe s'approcher puis se fondre dans le
point doré central.

On ne borne pas le nombre d'étapes : mathématiquement (1/2)^k ne
s'annule jamais, et l'affichage reste honnête quel que soit k —
décimales exactes jusqu'à k = 12 (1/2^k possède exactement k
décimales), puis notation scientifique (« 1 − 4,77 × 10⁻⁷ ») qui
n'affiche jamais un « 1 » arrondi. À l'écran la pointe finit par
se figer dans la cible, mais les chiffres, eux, continuent.
"""

from decimal import Decimal, getcontext

import pygame

import config
import sons
from scene import SceneParadoxe
from ui import bouton, texte, theme

# 20 chiffres significatifs suffisent largement : les décimales
# exactes n'excèdent jamais 12 chiffres ici (k ≤ SEUIL_DECIMALES) et
# la notation scientifique n'en montre que 4. La précision reste donc
# minuscule quel que soit k : calcul instantané, aucun risque de
# lenteur ni de crash, même pour des k énormes.
getcontext().prec = 20

# --- Géométrie de la piste (tout est dérivé de ces constantes) ---
X_DEPART = 150
X_CIBLE = 1130
Y_PISTE = 380
LARGEUR_PISTE = X_CIBLE - X_DEPART

# --- Affichage des valeurs ---
SEUIL_DECIMALES = 12   # au-delà : notation scientifique (ligne trop longue)
SEUIL_PIXEL = 15       # au-delà : plus rien ne bouge à l'écran, message

# --- Loupe ---
ECHELLE = 10               # grossissement de la loupe
LARGEUR_LOUPE = 320        # taille du panneau à l'écran
HAUTEUR_LOUPE = 160
LOUPE_X = 900              # coin haut-gauche du panneau
LOUPE_Y = 185
SEUIL_LOUPE = 80           # la loupe apparaît quand il reste < 80 pixels

# --- Rythme du mode automatique ---
DELAI_AUTO = 0.5           # une étape toutes les 0,5 seconde

# Chiffres en exposant pour écrire joliment 1/2⁴, 1/2¹⁰…
_EXPOSANTS = {str(i): c for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}


def en_exposant(k):
    """Convertit 4 en "⁴", 12 en "¹²" (exposants Unicode)."""
    return "".join(_EXPOSANTS[d] for d in str(k))


def format_scientifique(nombre):
    """Met un nombre au format « 4,77 × 10⁻⁷ » (notation française)."""
    mantisse, exposant = f"{nombre:.4e}".split("e")
    mantisse = mantisse.replace(".", ",")
    exposant = int(exposant)
    signe = "⁻" if exposant < 0 else ""
    return f"{mantisse} × 10{signe}{en_exposant(abs(exposant))}"


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
        on peut continuer indéfiniment. Au-delà de SEUIL_DECIMALES,
        l'affichage passe en notation scientifique pour rester
        honnête (« 1 − 4,77 × 10⁻⁷ »), jamais un « 1 » arrondi.
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

    def _reste_exact(self):
        """1/2^k en calcul exact (module decimal) : jamais arrondi.

        L'affichage utilise cette valeur : aucun arrondi à « 0 » ni
        à « 1 », quelle que soit la taille de k.
        """
        return Decimal(1) / (Decimal(2) ** self.k)

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
        """Loupe ×10 centrée sur le centre de la cible.

        Le centre de la cible est au MILIEU du panneau : on voit la
        pointe du javelot converger vers le point doré central et,
        à la saturation, se fondre dedans — le javelot « atteint »
        visuellement le cœur de la cible.
        """
        reste_pixels = LARGEUR_PISTE * 0.5 ** self.k
        if reste_pixels >= SEUIL_LOUPE:
            return

        x = self.x_du_javelot()
        cx = LARGEUR_LOUPE // 2    # le centre de la cible,
        cy = HAUTEUR_LOUPE // 2    # au milieu du panneau

        surface = self.loupe
        surface.fill(theme.FOND)

        def vers_loupe(x_reel):
            """Conversion réel → loupe : une simple multiplication."""
            return cx + (x_reel - X_CIBLE) * ECHELLE

        # La même scène que _dessiner_piste, à l'échelle 10, épurée :
        # la ligne de vol, le chemin restant, le bord de la cible (en
        # arc), puis le centre doré — dessiné AVANT le javelot : la
        # pointe cerclée de sombre reste visible une fois posée sur
        # le centre, comme en taille réelle.
        pygame.draw.line(surface, theme.ENCRE_DOUCE,
                         (0, cy), (LARGEUR_LOUPE, cy), 2)
        pygame.draw.line(surface, theme.OR,
                         (vers_loupe(x), cy), (cx, cy), 5)
        pygame.draw.circle(surface, theme.SURFACE, (cx, cy), 38 * ECHELLE)
        pygame.draw.circle(surface, theme.OR, (cx, cy), 8 * ECHELLE)

        fut = pygame.Rect(vers_loupe(x - 64), cy - 2 * ECHELLE,
                          48 * ECHELLE, 4 * ECHELLE)
        pygame.draw.rect(surface, theme.CREME, fut)
        pygame.draw.rect(surface, theme.SURFACE, fut, width=2)
        # Pointe cerclée de sombre, comme en taille réelle
        pygame.draw.polygon(surface, theme.SURFACE,
                            [(vers_loupe(x - 16), cy - 6 * ECHELLE - 2),
                             (vers_loupe(x) + 2, cy),
                             (vers_loupe(x - 16), cy + 6 * ECHELLE + 2)])
        pygame.draw.polygon(surface, theme.OR,
                            [(vers_loupe(x - 16), cy - 6 * ECHELLE),
                             (vers_loupe(x), cy),
                             (vers_loupe(x - 16), cy + 6 * ECHELLE)])

        texte.dessiner_texte(surface, "× 10", 10, 8,
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
        # Les valeurs exactes, sans arrondi : jusqu'à k = 12, écriture
        # décimale exacte (1/2^k possède exactement k décimales) ;
        # au-delà, notation scientifique — jamais un « 1 » ni un « 0 »
        # arrondis, aussi loin qu'on aille.
        reste = self._reste_exact()
        if self.k <= SEUIL_DECIMALES:
            texte_parcouru = str(Decimal(1) - reste).replace(".", ",")
            texte_reste = str(reste).replace(".", ",")
        else:
            valeur = format_scientifique(reste)
            texte_parcouru = f"1 − {valeur}"
            texte_reste = f"≈ {valeur}"
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
