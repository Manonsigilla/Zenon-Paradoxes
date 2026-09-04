"""Outils mathématiques partagés entre les scènes de la dichotomie.

- le contexte decimal en précision 20 : calculs exacts sans arrondi,
  instantanés quel que soit k ;
- en_exposant : écrit 1/2⁴ plutôt que 1/2^4 ;
- format_scientifique : « 4,77 × 10⁻⁷ » en notation française ;
- texte_valeur_parcourue / texte_valeur_reste : les textes
  d'affichage de S_k = 1 − 1/2^k et de 1/2^k, sans arrondi à « 1 »
  ni à « 0 ».
"""

from decimal import Decimal, getcontext

# 20 chiffres significatifs suffisent largement : les décimales
# exactes n'excèdent jamais 12 chiffres ici (k ≤ 12) et la notation
# scientifique n'en montre que 4. La précision reste donc minuscule
# quel que soit k : calcul instantané, aucun risque de lenteur ni de
# crash, même pour des k énormes.
getcontext().prec = 20

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


def reste_exact(k):
    """1/2^k en calcul exact (module decimal) : jamais arrondi."""
    return Decimal(1) / (Decimal(2) ** k)


def texte_valeur_parcourue(k):
    """Texte d'affichage de S_k = 1 − 1/2^k, sans arrondi à « 1 ».

    Jusqu'à k = 12 : décimales exactes ; au-delà : notation
    scientifique (« 1 − 4,77 × 10⁻⁷ »).
    """
    reste = reste_exact(k)
    if k <= 12:
        return str(Decimal(1) - reste).replace(".", ",")
    return "1 − " + format_scientifique(reste)


def texte_valeur_reste(k):
    """Texte d'affichage de 1/2^k, sans arrondi à « 0 »."""
    reste = reste_exact(k)
    if k <= 12:
        return str(reste).replace(".", ",")
    return "≈ " + format_scientifique(reste)
