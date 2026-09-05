"""Le paradoxe d'Achille et la tortue.

Chaque dossier de paradoxe expose :
- NOM : le titre du paradoxe, affiché dans l'entête des étapes ;
- etapes : la liste des classes d'étapes, dans l'ordre du parcours.

Parcours : phase Paradoxe (raisonnement de Zénon) → phase Résolution
(course réelle en temps continu).
"""

from .achille import ScenePhaseParadoxe, ScenePhaseResolution

NOM = "Achille et la tortue"
etapes = [ScenePhaseParadoxe, ScenePhaseResolution]
