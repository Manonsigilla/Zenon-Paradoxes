# Les paradoxes de Zénon

Application Pygame illustrant trois paradoxes de Zénon d'Élée :
la flèche en vol, la dichotomie, et Achille et la tortue. Chaque
paradoxe présente ses deux démonstrations : celle de Zénon et la
réfutation moderne.

## Lancer l'application

```
pip install pygame
python main.py
```

- **F11** : basculer en plein écran
- **← / →** : étape précédente / suivante
- **Espace** : action principale de la scène — dans la dichotomie et la
  flèche, avancer d'une étape (rester appuyé pour défiler) ; dans Achille,
  lancer/mettre en pause (le mode auto s'active via le bouton ou la barre)
- **Échap** : retour à l'accueil
- **Quitter** : fermer la fenêtre

## Structure

- `main.py` — point d'entrée (boucle pygame, plein écran F11, répétition des touches maintenues)
- `config.py` — constantes (fenêtre 1280×720, FPS, chemins)
- `scene.py` — contrat commun des scènes + base des étapes de paradoxe
- `scene_manager.py` — navigation entre les scènes
- `sons.py` — déclaration et lecture des sons (volume réglable : constante `VOLUME`)
- `scenes/accueil.py` — page d'accueil (3 boutons)
- `scenes/dichotomie/` — **terminée** (Manon) : 5 étapes (`presentation`, `illustration`, `demo_zenon`, `demo_moderne`, `conclusion`) + `maths.py` (calculs décimaux exacts)
- `scenes/fleche/` — **terminé** (Angie) : 5 étapes, même structure que la dichotomie
- `scenes/achille/` — **intégré** (Rayene) : 2 phases dans `achille.py` — le raisonnement de Zénon, puis la course réelle en temps continu (l'écart D₀·rᵏ ne s'annule jamais dans la 1ʳᵉ ; Achille rattrape dans la 2ᵉ)
- `scenes/squelette/` — modèle d'origine ; encore chargé dans `main.py` mais plus relié à l'accueil
- `ui/` — boutons, texte, palette (« temple grec »), motifs (colonnade), barre de navigation
- `assets/fonts/` — polices DejaVu Sans et Cardo (voir les licences)
- `assets/images/` — images du style « mixte » (PNG à fond transparent)
- `assets/sons/` — `etape.ogg`, `limite.ogg`, `rejouer.ogg` (.wav ou .ogg — pygame 2 ne lit pas les .mp3)

## Répartition

| Paradoxe | Qui | État |
|---|---|---|
| La flèche en vol | Angie | **terminé** (5 étapes) |
| La dichotomie | Manon | **terminée** (5 étapes) |
| Achille et la tortue | Rayene | **intégré** (2 phases) |
| Socle commun + accueil | ensemble | terminé |

## Créer un paradoxe

Le nombre d'étapes est libre : chaque dossier déclare son propre
parcours dans `__init__.py` (`NOM` et `etapes`). Les trois paradoxes
montrent deux options possibles :

- **5 étapes** (dichotomie, flèche) : `presentation.py`,
  `illustration.py`, `demo_zenon.py`, `demo_moderne.py`,
  `conclusion.py` ;
- **2 phases** (Achille) : tout le déroulé dans `achille.py`, le
  raisonnement puis la résolution.

Pour un nouveau paradoxe :

1. S'inspirer de `scenes/dichotomie/` (exemple complet) ou de
   `scenes/achille/` (variante en phases)
2. Déclarer l'ordre du parcours dans `__init__.py` (`NOM` et `etapes`)
3. Enregistrer le paradoxe dans `main.py` :
   `manager.ajouter_parcours("nom", module)`
4. Pointer le bouton de l'accueil vers `"nom-0"`

Chaque étape d'un paradoxe respecte le contrat de `Scene` :
`on_entrer`, `gerer_evenement`, `mettre_a_jour`, `dessiner`.
