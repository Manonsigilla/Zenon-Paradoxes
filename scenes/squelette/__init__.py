"""Paradoxe squelette : le modèle à copier pour créer un vrai paradoxe.

Chaque dossier de paradoxe expose deux choses :
- NOM : le titre du paradoxe, affiché dans l'entête des étapes ;
- etapes : la liste des classes d'étapes, dans l'ordre du parcours.

Pour créer votre paradoxe :
1. copiez ce dossier (ex. vers scenes/fleche/) ;
2. créez vos étapes en vous inspirant de presentation.py et
   illustration.py (contenu, animation, interactions) ;
3. adaptez NOM et etapes ci-dessous ;
4. enregistrez le paradoxe dans main.py et pointez le bouton de
   l'accueil vers "fleche-0".

Ce dossier disparaîtra quand les 3 vrais paradoxes seront codés.
"""

from .illustration import EtapeIllustration
from .presentation import EtapePresentation

NOM = "Paradoxe squelette"
etapes = [EtapePresentation, EtapeIllustration]
