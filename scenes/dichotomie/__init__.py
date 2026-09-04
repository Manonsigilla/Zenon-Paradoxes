"""Le paradoxe de la dichotomie.

Chaque dossier de paradoxe expose :
- NOM : le titre du paradoxe, affiché dans l'entête des étapes ;
- etapes : la liste des classes d'étapes, dans l'ordre du parcours.

Parcours : présentation → illustration → démonstration de Zénon →
démonstration moderne → conclusion.
"""

from .conclusion import EtapeConclusion
from .demo_moderne import EtapeDemoModerne
from .demo_zenon import EtapeDemoZenon
from .illustration import EtapeIllustration
from .presentation import EtapePresentation

NOM = "La dichotomie"
etapes = [EtapePresentation, EtapeIllustration, EtapeDemoZenon,
          EtapeDemoModerne, EtapeConclusion]
