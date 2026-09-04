"""Le paradoxe de la dichotomie.

Chaque dossier de paradoxe expose :
- NOM : le titre du paradoxe, affiché dans l'entête des étapes ;
- etapes : la liste des classes d'étapes, dans l'ordre du parcours.

Les étapes demo_zenon, demo_moderne et conclusion viendront
s'insérer ici au fur et à mesure.
"""

from .illustration import EtapeIllustration
from .presentation import EtapePresentation

NOM = "La dichotomie"
etapes = [EtapePresentation, EtapeIllustration]
