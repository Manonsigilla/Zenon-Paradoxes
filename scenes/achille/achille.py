"""Le paradoxe d'Achille et la tortue, en deux phases.

PHASE 1 — « Paradoxe » : on rejoue fidèlement le raisonnement de
Zénon. À l'étape k, Achille a comblé une fraction du chemin et la
tortue a, entre-temps, avancé un peu plus loin. La distance qui les
sépare vaut D0 × r^k (D0 = l'avance initiale, r = vitesse_tortue /
vitesse_achille, toujours < 1). Comme pour le javelot de la
dichotomie, cette distance est calculée par une formule qui ne peut
STRUCTURELLEMENT jamais tomber à zéro pour un k fini : dans cette
phase, Achille n'atteint donc jamais visiblement la tortue — une
loupe apparaît même pour continuer à montrer l'écart quand il devient
trop petit pour l'œil nu, exactement comme la loupe de la
dichotomie sur sa cible.

PHASE 2 — « Résolution » : on quitte le raisonnement de Zénon pour
la physique réelle. Les deux coureurs avancent en continu à leur
vraie vitesse ; comme Achille est plus rapide, il rattrape belle et
bien la tortue, à un instant fini (t = D0 / (v_achille − v_tortue)).
C'est la réponse mathématique au paradoxe : une infinité d'étapes de
plus en plus petites peut très bien se dérouler dans un temps fini.
"""

from decimal import Decimal, getcontext

import pygame

import config
from scene import SceneParadoxe
from ui import barre_navigation, theme, texte
import sons

# 50 chiffres significatifs : largement de quoi représenter D0 × r^k
# exactement (r = 3/8 est une fraction décimale exacte) jusqu'à des
# valeurs de k bien au-delà de ce qu'un utilisateur cliquera jamais.
getcontext().prec = 50


# ======================================================================
# CONSTANTES
# ======================================================================

# --- Couleurs (même esprit « antique » que le reste du projet) ---
COULEUR_OR = (198, 156, 71)
COULEUR_OR_CLAIR = (230, 196, 120)
COULEUR_CREME = (238, 230, 210)
COULEUR_ENCRE = (25, 22, 18)
COULEUR_ENCRE_DOUCE = (150, 150, 160)
COULEUR_ACHILLE = (198, 156, 71)      # doré : le héros
COULEUR_TORTUE = (94, 140, 92)        # vert sourd : la tortue
COULEUR_INACTIF = (70, 76, 92)

# --- Géométrie de la piste ---
Y_PISTE = 280
X_DEPART = config.MARGE
X_FIN_PISTE = config.LARGEUR - config.MARGE
LARGEUR_PISTE_PIXELS = X_FIN_PISTE - X_DEPART

# --- Données du paradoxe (unités abstraites, disons des mètres) ---
VITESSE_ACHILLE = 8.0     # m/s
VITESSE_TORTUE = 3.0      # m/s : plus lente, mais elle a une avance
AVANCE_INITIALE = 50.0    # m

# --- Rythme de l'avancée automatique des étapes (phase Paradoxe) ---
DELAI_AUTO_ETAPE = 0.6     # secondes entre deux étapes en mode auto
K_MAXIMUM = 300             # sécurité : au-delà, l'écart est de toute
                            # façon bien en dessous de la précision d'un
                            # écran ; inutile de continuer à calculer

# --- Loupe (phase Paradoxe) : montre que l'écart ne s'annule jamais ---
SEUIL_LOUPE = 70            # px : en dessous, la loupe apparaît
SEUIL_GAP_LOUPE = 4         # écart minimal que la loupe doit montrer
ECHELLE_LOUPE_BASE = 10
LARGEUR_LOUPE = 320
HAUTEUR_LOUPE = 170
LOUPE_X = config.LARGEUR - 400
LOUPE_Y = 180
MAX_ZOOMS = 60


# ======================================================================
# MATHÉMATIQUES DU PARADOXE
# ======================================================================

def raison():
    """r = vitesse_tortue / vitesse_achille (toujours < 1 ici)."""
    return Decimal(str(VITESSE_TORTUE)) / Decimal(str(VITESSE_ACHILLE))


def cible():
    """La limite mathématique : D0 / (1 − r).

    C'est à la fois la « cible » vers laquelle les deux coureurs
    convergent sans jamais l'atteindre dans le raisonnement de Zénon
    (phase Paradoxe), et la distance à laquelle Achille rattrape
    réellement la tortue (phase Résolution) — les deux notions
    désignent le même nombre.
    """
    return Decimal(str(AVANCE_INITIALE)) / (1 - raison())


def temps_rattrapage():
    """Instant réel (en secondes) du rattrapage, calcul indépendant."""
    return AVANCE_INITIALE / (VITESSE_ACHILLE - VITESSE_TORTUE)


def gap_exact(k):
    """Écart D0 × r^k après k étapes : structurellement jamais nul."""
    return Decimal(str(AVANCE_INITIALE)) * raison() ** k


def position_achille_exact(k):
    """Distance parcourue par Achille après k étapes (somme géométrique)."""
    if k == 0:
        return Decimal(0)
    r = raison()
    return Decimal(str(AVANCE_INITIALE)) * (1 - r ** k) / (1 - r)


def position_tortue_exact(k):
    """La tortue est toujours exactement l'écart devant Achille."""
    return position_achille_exact(k) + gap_exact(k)


_EXPOSANTS = {str(i): c for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}


def en_exposant(k):
    """Écrit 4 en "⁴" (utilisé pour l'affichage de r^k et du zoom)."""
    return "".join(_EXPOSANTS[d] for d in str(k))


def format_scientifique(valeur):
    """« 4,77 × 10⁻⁷ » en notation française, pour les écarts minuscules."""
    mantisse, exposant = f"{float(valeur):.3e}".split("e")
    mantisse = mantisse.replace(".", ",")
    exposant = int(exposant)
    signe = "⁻" if exposant < 0 else ""
    return f"{mantisse} × 10{signe}{en_exposant(abs(exposant))}"


def texte_valeur(valeur_decimale):
    """Affiche un nombre sans jamais l'arrondir silencieusement à 0.

    Au-dessus d'un dix-millième : décimales normales. En dessous
    (l'écart devient minuscule mais n'est mathématiquement jamais
    nul) : notation scientifique, pour ne jamais afficher un « 0 »
    trompeur.
    """
    valeur = float(valeur_decimale)
    if valeur == 0:
        return "0"
    if abs(valeur) >= 0.0001:
        return f"{valeur:.4f}".replace(".", ",")
    return format_scientifique(valeur_decimale)


def x_ecran(position_reelle):
    """Convertit une distance réelle (m) en abscisse écran.

    La cible mathématique est toujours placée au même endroit
    (X_FIN_PISTE), qu'on soit dans la phase Paradoxe ou Résolution :
    les deux phases partagent donc exactement la même piste.
    """
    fraction = float(position_reelle) / float(cible())
    return X_DEPART + fraction * LARGEUR_PISTE_PIXELS


# ======================================================================
# ÉTAT DE LA SIMULATION
# ======================================================================

class EtatSimulation:
    """Regroupe toutes les variables qui évoluent pendant l'exécution."""

    def __init__(self):
        self.reinitialiser_complet()

    def reinitialiser_complet(self):
        self.mode = "paradoxe"          # ou "resolution"
        self.k = 0
        self.auto = False
        self.temps_auto = 0.0
        self._reinitialiser_resolution()

    def _reinitialiser_resolution(self):
        self.position_achille_reel = 0.0
        self.position_tortue_reel = AVANCE_INITIALE
        self.objectif_etape_reel = AVANCE_INITIALE
        self.numero_etape_reel = 0
        self.temps_ecoule_reel = 0.0
        self.en_cours_reel = False
        self.termine_reel = False
        self.marques_etapes_reel = [AVANCE_INITIALE]

    # ------------------------------------------------------------------
    # Actions — phase Paradoxe
    # ------------------------------------------------------------------
    def avancer_etape(self):
        if self.k < K_MAXIMUM:
            self.k += 1

    def basculer_auto(self):
        self.auto = not self.auto
        self.temps_auto = 0.0

    def passer_a_resolution(self):
        self.mode = "resolution"
        self._reinitialiser_resolution()

    # ------------------------------------------------------------------
    # Actions — phase Résolution
    # ------------------------------------------------------------------
    def revenir_au_paradoxe(self):
        self.mode = "paradoxe"

    def basculer_course_reelle(self):
        if not self.termine_reel:
            self.en_cours_reel = not self.en_cours_reel

    # ------------------------------------------------------------------
    # Rejouer / recommencer (R) — ne concerne que la phase affichée
    # ------------------------------------------------------------------
    def rejouer(self):
        if self.mode == "paradoxe":
            self.k = 0
            self.auto = False
            self.temps_auto = 0.0
        else:
            self._reinitialiser_resolution()


def mettre_a_jour_simulation(etat, dt):
    if etat.mode == "paradoxe":
        _mettre_a_jour_paradoxe(etat, dt)
    else:
        _mettre_a_jour_resolution(etat, dt)


def _mettre_a_jour_paradoxe(etat, dt):
    """Avance automatiquement d'une étape toutes les DELAI_AUTO_ETAPE s."""
    if not etat.auto:
        return
    etat.temps_auto += dt
    if etat.temps_auto >= DELAI_AUTO_ETAPE:
        etat.temps_auto = 0.0
        etat.avancer_etape()


def _mettre_a_jour_resolution(etat, dt):
    """Fait courir réellement les deux coureurs, à vitesse constante.

    Contrairement à la phase Paradoxe (positions recalculées d'un
    coup à chaque étape), ici le mouvement est continu : on avance
    juste position += vitesse * dt, comme dans la réalité. Les
    « étapes » de Zénon ne sont plus programmées : elles sont
    simplement détectées, chaque fois qu'Achille atteint le point où
    se trouvait la tortue au début de l'étape en cours.
    """
    if not etat.en_cours_reel or etat.termine_reel:
        return

    etat.temps_ecoule_reel += dt
    etat.position_achille_reel += VITESSE_ACHILLE * dt
    etat.position_tortue_reel += VITESSE_TORTUE * dt

    compte = 0
    while (not etat.termine_reel
           and etat.position_achille_reel >= etat.objectif_etape_reel
           and compte < 500):
        ecart_px = ((etat.position_tortue_reel - etat.position_achille_reel)
                    / float(cible()) * LARGEUR_PISTE_PIXELS)
        if ecart_px <= 2:
            # Écart devenu invisible à l'écran : on annonce directement
            # le rattrapage plutôt que de compter des étapes de plus
            # en plus petites indéfiniment.
            etat.termine_reel = True
            etat.en_cours_reel = False
            etat.position_achille_reel = etat.position_tortue_reel
            break
        etat.numero_etape_reel += 1
        etat.objectif_etape_reel = etat.position_tortue_reel
        etat.marques_etapes_reel.append(etat.position_tortue_reel)
        compte += 1

    if not etat.termine_reel and etat.position_achille_reel >= etat.position_tortue_reel:
        etat.position_achille_reel = etat.position_tortue_reel
        etat.termine_reel = True
        etat.en_cours_reel = False


# ======================================================================
# DESSIN
# ======================================================================

def _dessiner_marqueur_tortue(ecran, x, y):
    carapace = pygame.Rect(0, 0, 40, 24)
    carapace.midbottom = (x, y + 12)
    pygame.draw.ellipse(ecran, COULEUR_TORTUE, carapace)
    pygame.draw.ellipse(ecran, COULEUR_ENCRE, carapace, width=2)
    tete = pygame.Rect(0, 0, 12, 10)
    tete.midleft = (carapace.right - 4, carapace.centery)
    pygame.draw.ellipse(ecran, COULEUR_TORTUE, tete)


def _dessiner_marqueur_achille(ecran, x, y):
    corps = pygame.Rect(0, 0, 14, 30)
    corps.midbottom = (x, y + 2)
    pygame.draw.ellipse(ecran, COULEUR_ACHILLE, corps)
    pygame.draw.circle(ecran, COULEUR_ACHILLE, (x, corps.top - 7), 7)
    pygame.draw.line(ecran, COULEUR_OR_CLAIR,
                      (x - 4, corps.top), (x + 22, corps.top - 26), 3)


def _dessiner_loupe_paradoxe(ecran, k, x_achille, x_tortue):
    """Loupe centrée sur la cible mathématique : montre que l'écart ne
    s'annule jamais, en zoomant davantage à mesure qu'il rétrécit —
    exactement le même principe que la loupe de la dichotomie.
    """
    surface = pygame.Surface((LARGEUR_LOUPE, HAUTEUR_LOUPE))
    surface.fill((10, 12, 20))
    cx, cy = LARGEUR_LOUPE // 2, HAUTEUR_LOUPE // 2

    reste_tortue_px = X_FIN_PISTE - x_tortue
    echelle = ECHELLE_LOUPE_BASE
    n_zooms = 0
    while reste_tortue_px * echelle < SEUIL_GAP_LOUPE and n_zooms < MAX_ZOOMS:
        echelle *= 2
        n_zooms += 1

    def vers_loupe(x_reel):
        valeur = cx + (x_reel - X_FIN_PISTE) * echelle
        return max(-5000, min(LARGEUR_LOUPE + 5000, valeur))

    pygame.draw.line(surface, COULEUR_ENCRE_DOUCE,
                      (0, cy), (LARGEUR_LOUPE, cy), 1)
    pygame.draw.line(surface, COULEUR_CREME, (cx, 0), (cx, HAUTEUR_LOUPE), 1)

    x_t = int(vers_loupe(x_tortue))
    x_a = int(vers_loupe(x_achille))
    _dessiner_marqueur_tortue(surface, x_t, cy)
    _dessiner_marqueur_achille(surface, x_a, cy)

    legende = (f"× {ECHELLE_LOUPE_BASE}" if n_zooms == 0
               else f"× {ECHELLE_LOUPE_BASE} · 2{en_exposant(n_zooms)}")
    texte.dessiner_texte(surface, legende, 10, 8,
                         theme.police(15, "gras"), COULEUR_OR_CLAIR)
    texte.dessiner_texte(surface, "la tortue reste toujours devant", 10,
                         HAUTEUR_LOUPE - 26, theme.police(13, "italique"),
                         COULEUR_ENCRE_DOUCE)

    ecran.blit(surface, (LOUPE_X, LOUPE_Y))
    pygame.draw.rect(ecran, COULEUR_OR,
                      (LOUPE_X, LOUPE_Y, LARGEUR_LOUPE, HAUTEUR_LOUPE),
                      width=2, border_radius=8)


# ======================================================================
# SCÈNES
# ======================================================================

class ScenePhaseParadoxe(SceneParadoxe):
    """Phase 1 : Le raisonnement de Zénon."""

    TITRE = "Le raisonnement de Zénon"

    def __init__(self, manager):
        super().__init__(manager)
        self.etat = EtatSimulation()
        self.etat.mode = "paradoxe"
        # Boutons de cette phase : avancer une étape, passer à la résolution
        self.rect_bouton_avancer = pygame.Rect(X_DEPART, 580, 240, 44)
        self.rect_bouton_resolution = pygame.Rect(X_DEPART + 260, 580,
                                                  280, 44)

    def on_entrer(self):
        super().on_entrer()
        self.etat.k = 0
        self.etat.auto = False
        self.etat.temps_auto = 0.0

    def gerer_evenement(self, event):
        super().gerer_evenement(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.etat.basculer_auto()
                sons.jouer("etape")
            elif event.key == pygame.K_r:
                self.etat.rejouer()
                sons.jouer("rejouer")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_bouton_avancer.collidepoint(event.pos):
                self.etat.avancer_etape()
                sons.jouer("etape")
            elif self.rect_bouton_resolution.collidepoint(event.pos):
                self.etat.passer_a_resolution()
                self.manager.suivant()
                sons.jouer("etape")

    def mettre_a_jour(self, dt):
        mettre_a_jour_simulation(self.etat, dt)

    def dessiner_contenu(self, ecran):
        # Piste et cible mathématique
        pygame.draw.line(ecran, COULEUR_ENCRE_DOUCE,
                          (X_DEPART, Y_PISTE), (X_FIN_PISTE, Y_PISTE), 2)
        pygame.draw.line(ecran, COULEUR_ENCRE_DOUCE,
                          (X_DEPART, Y_PISTE - 14), (X_DEPART, Y_PISTE + 14), 2)
        pygame.draw.circle(ecran, theme.SURFACE, (X_FIN_PISTE, Y_PISTE), 22)
        pygame.draw.circle(ecran, COULEUR_OR, (X_FIN_PISTE, Y_PISTE), 22, width=2)
        pygame.draw.line(ecran, COULEUR_CREME,
                          (X_FIN_PISTE, Y_PISTE - 10), (X_FIN_PISTE, Y_PISTE + 10), 2)
        pygame.draw.line(ecran, COULEUR_CREME,
                          (X_FIN_PISTE - 10, Y_PISTE), (X_FIN_PISTE + 10, Y_PISTE), 2)

        for marque in range(1, self.etat.k):
            x_m = x_ecran(position_tortue_exact(marque))
            pygame.draw.line(ecran, COULEUR_ENCRE_DOUCE,
                              (x_m, Y_PISTE - 6), (x_m, Y_PISTE + 6), 1)

        x_achille = x_ecran(position_achille_exact(self.etat.k))
        x_tortue = x_ecran(position_tortue_exact(self.etat.k))
        _dessiner_marqueur_tortue(ecran, x_tortue, Y_PISTE)
        _dessiner_marqueur_achille(ecran, x_achille, Y_PISTE)

        reste_px_declencheur = X_FIN_PISTE - x_tortue
        if reste_px_declencheur < SEUIL_LOUPE:
            _dessiner_loupe_paradoxe(ecran, self.etat.k, x_achille, x_tortue)

        # Panneau d'information
        panneau = pygame.Rect(X_DEPART - 20, 350,
                              LARGEUR_PISTE_PIXELS + 40, 210)
        pygame.draw.rect(ecran, theme.SURFACE, panneau, border_radius=14)
        pygame.draw.rect(ecran, COULEUR_OR, panneau, width=2, border_radius=14)

        x, y = panneau.left + 24, panneau.top + 16
        texte.dessiner_texte(ecran, f"Étape {self.etat.k}", x, y,
                             theme.police(26, "gras"), COULEUR_OR_CLAIR)
        y += 38
        texte.dessiner_texte(
            ecran,
            f"Position d'Achille : {texte_valeur(position_achille_exact(self.etat.k))} m",
            x, y, theme.police(19), COULEUR_CREME)
        y += 26
        texte.dessiner_texte(
            ecran,
            f"Position de la tortue : {texte_valeur(position_tortue_exact(self.etat.k))} m",
            x, y, theme.police(19), COULEUR_CREME)
        y += 26
        texte.dessiner_texte(
            ecran,
            f"Écart = D0 × r{en_exposant(self.etat.k)} = {texte_valeur(gap_exact(self.etat.k))} m",
            x, y, theme.police(19), COULEUR_CREME)
        y += 32

        if self.etat.k == 0:
            explication = ("Espace : lancer le défilement automatique des "
                            "étapes du raisonnement de Zénon.")
        else:
            explication = (
                "Achille atteint le point où était la tortue ; entre-temps "
                "elle a avancé un peu plus loin — un nouvel écart, plus "
                "petit d'un facteur r, apparaît aussitôt.")
        texte.dessiner_texte(ecran, explication, x, y,
                             theme.police(16, "italique"), COULEUR_OR_CLAIR)

        # Boutons : Avancer une étape / Passer à la résolution
        for rect, label in ((self.rect_bouton_avancer, "Avancer une étape"),
                            (self.rect_bouton_resolution,
                             "Passer à la résolution →")):
            pygame.draw.rect(ecran, theme.SURFACE, rect, border_radius=10)
            pygame.draw.rect(ecran, COULEUR_OR, rect, width=2,
                             border_radius=10)
            texte.dessiner_texte_centre(ecran, label, rect.centerx,
                                        rect.centery - 11,
                                        theme.police(16, "gras"),
                                        COULEUR_CREME)


class ScenePhaseResolution(SceneParadoxe):
    """Phase 2 : La résolution en temps continu."""

    TITRE = "La résolution : la course réelle"

    def __init__(self, manager):
        super().__init__(manager)
        self.etat = EtatSimulation()
        self.etat.mode = "resolution"

    def on_entrer(self):
        super().on_entrer()
        self.etat._reinitialiser_resolution()

    def gerer_evenement(self, event):
        super().gerer_evenement(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.etat.basculer_course_reelle()
                sons.jouer("etape")
            elif event.key == pygame.K_r:
                self.etat.rejouer()
                sons.jouer("rejouer")

    def mettre_a_jour(self, dt):
        mettre_a_jour_simulation(self.etat, dt)

    def dessiner_contenu(self, ecran):
        pygame.draw.line(ecran, COULEUR_ENCRE_DOUCE,
                          (X_DEPART, Y_PISTE), (X_FIN_PISTE, Y_PISTE), 2)
        pygame.draw.line(ecran, COULEUR_ENCRE_DOUCE,
                          (X_DEPART, Y_PISTE - 14), (X_DEPART, Y_PISTE + 14), 2)
        pygame.draw.line(ecran, COULEUR_OR,
                          (X_FIN_PISTE, Y_PISTE - 20), (X_FIN_PISTE, Y_PISTE + 20), 3)
        texte.dessiner_texte(ecran, "Rattrapage réel", X_FIN_PISTE - 46, Y_PISTE - 42,
                             theme.police(14, "italique"), COULEUR_OR_CLAIR)

        for marque in self.etat.marques_etapes_reel:
            x_m = x_ecran(marque)
            pygame.draw.line(ecran, COULEUR_ENCRE_DOUCE,
                              (x_m, Y_PISTE - 6), (x_m, Y_PISTE + 6), 1)

        x_tortue = x_ecran(self.etat.position_tortue_reel)
        x_achille = x_ecran(self.etat.position_achille_reel)
        _dessiner_marqueur_tortue(ecran, x_tortue, Y_PISTE)
        _dessiner_marqueur_achille(ecran, x_achille, Y_PISTE)

        # Panneau d'information
        panneau = pygame.Rect(X_DEPART - 20, 350,
                              LARGEUR_PISTE_PIXELS + 40, 210)
        pygame.draw.rect(ecran, theme.SURFACE, panneau, border_radius=14)
        pygame.draw.rect(ecran, COULEUR_OR, panneau, width=2, border_radius=14)

        x, y = panneau.left + 24, panneau.top + 16
        ecart = self.etat.position_tortue_reel - self.etat.position_achille_reel

        texte.dessiner_texte(ecran, f"Étape {self.etat.numero_etape_reel}   —   "
                                    f"t = {self.etat.temps_ecoule_reel:.2f} s",
                             x, y, theme.police(24, "gras"), COULEUR_OR_CLAIR)
        y += 36
        texte.dessiner_texte(
            ecran, f"Position d'Achille : {self.etat.position_achille_reel:6.2f} m",
            x, y, theme.police(19), COULEUR_CREME)
        y += 26
        texte.dessiner_texte(
            ecran, f"Position de la tortue : {self.etat.position_tortue_reel:6.2f} m",
            x, y, theme.police(19), COULEUR_CREME)
        y += 26
        texte.dessiner_texte(
            ecran, f"Distance qui les sépare : {max(ecart, 0):6.2f} m",
            x, y, theme.police(19), COULEUR_CREME)
        y += 32

        if self.etat.termine_reel:
            explication = (
                f"Achille rattrape la tortue à t = {temps_rattrapage():.2f} s. "
                "Contrairement à ce que suggérait le raisonnement de Zénon, "
                "une infinité d'étapes de plus en plus petites tient bien "
                "dans un temps fini : le paradoxe n'empêchait pas la réalité.")
        elif not self.etat.en_cours_reel and self.etat.numero_etape_reel == 0:
            explication = "Espace : lancer la course réelle."
        else:
            explication = (
                "Cette fois, les deux coureurs avancent en continu, à leur "
                "vraie vitesse : les étapes de Zénon se produisent d'elles-"
                "mêmes, de plus en plus vite, à l'approche du rattrapage.")
        texte.dessiner_texte(ecran, explication, x, y,
                             theme.police(16, "italique"), COULEUR_OR_CLAIR)
