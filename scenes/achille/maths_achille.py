"""Outils mathématiques partagés entre les scènes d'Achille et la tortue.

- les vitesses et l'avance initiale du paradoxe (mètres, secondes) ;
- le contexte decimal en précision 50 : calculs exacts sans arrondi,
  instantanés même pour des k énormes (r = 3/8 est une fraction
  décimale exacte) ;
- raison / cible / temps_rattrapage : les trois nombres-clés du
  paradoxe — r = v_tortue/v_achille, la limite D0/(1−r) vers laquelle
  converge la série de Zénon (et qui est aussi le point réel du
  rattrapage), et l'instant réel de ce rattrapage ;
- gap_exact / position_achille_exact / position_tortue_exact : les
  positions à l'étape k du raisonnement de Zénon, en calcul exact ;
- en_exposant : écrit r⁴ plutôt que r^4 ;
- format_scientifique : « 4,77 × 10⁻⁷ » en notation française ;
- texte_valeur : affichage d'un nombre sans jamais l'arrondir
  silencieusement à 0.
"""

from decimal import Decimal, getcontext

# --- Données du paradoxe (unités abstraites, disons des mètres) ---
VITESSE_ACHILLE = 8.0     # m/s
VITESSE_TORTUE = 3.0      # m/s : plus lente, mais elle a une avance
AVANCE_INITIALE = 50.0    # m

# 50 chiffres significatifs : largement de quoi représenter D0 × r^k
# exactement (r = 3/8 est une fraction décimale exacte) jusqu'à des
# valeurs de k bien au-delà de ce qu'un utilisateur cliquera jamais.
getcontext().prec = 50

# Chiffres en exposant pour écrire joliment r⁴, r¹⁰…
_EXPOSANTS = {str(i): c for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}


def raison():
    """r = vitesse_tortue / vitesse_achille (toujours < 1 ici)."""
    return Decimal(str(VITESSE_TORTUE)) / Decimal(str(VITESSE_ACHILLE))


def cible():
    """La limite mathématique : D0 / (1 − r).

    C'est à la fois la « cible » vers laquelle les deux coureurs
    convergent sans jamais l'atteindre dans le raisonnement de Zénon,
    et la distance à laquelle Achille rattrape réellement la tortue —
    les deux notions désignent le même nombre.
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


def en_exposant(k):
    """Convertit 4 en "⁴" (utilisé pour l'affichage de r^k)."""
    return "".join(_EXPOSANTS[d] for d in str(k))


def format_scientifique(valeur):
    """Met un nombre au format « 4,77 × 10⁻⁷ » (notation française)."""
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
