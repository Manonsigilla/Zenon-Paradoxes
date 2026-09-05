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
- **Espace** : avancer d'une étape (rester appuyé pour défiler)
- **Échap** : retour à l'accueil
- **Quitter** : fermer la fenêtre

## Structure

- `main.py` — point d'entrée (boucle pygame, plein écran F11, répétition des touches maintenues)
- `config.py` — constantes (fenêtre 1280×720, FPS, chemins)
- `scene.py` — contrat commun des scènes + base des étapes de paradoxe
- `scene_manager.py` — navigation entre les scènes
- `sons.py` — déclaration et lecture des sons (volume réglable : constante `VOLUME`)
- `scenes/accueil.py` — page d'accueil (3 boutons)
- `scenes/dichotomie/` — **terminé** : 5 étapes (`presentation`, `illustration`, `demo_zenon`, `demo_moderne`, `conclusion`) + `maths.py` (calculs décimaux exacts partagés)
- `scenes/fleche/`, `scenes/achille/` — à créer (un paradoxe par personne)
- `scenes/squelette/` — modèle à copier pour créer un paradoxe (à supprimer à la fin)
- `ui/` — boutons, texte, palette (« temple grec »), motifs (colonnade), barre de navigation
- `assets/fonts/` — polices DejaVu Sans et Cardo (voir les licences)
- `assets/images/` — images du style « mixte » (PNG à fond transparent)
- `assets/sons/` — `etape.ogg`, `limite.ogg`, `rejouer.ogg` (.wav ou .ogg — pygame 2 ne lit pas les .mp3)

## Répartition

| Paradoxe | Qui | État |
|---|---|---|
| La flèche en vol | Angie | **terminée**  |
| La dichotomie | Manon | **terminée** |
| Achille et la tortue | Rayene | à faire |
| Socle commun + accueil | ensemble | terminé |

## Créer un paradoxe

1. Copier `scenes/squelette/` vers `scenes/fleche/` (par exemple) — ou
   s'inspirer de `scenes/dichotomie/`, l'exemple le plus complet
2. Créer les étapes (`presentation.py`, `illustration.py`, `demo_zenon.py`,
   `demo_moderne.py`, `conclusion.py`) en s'inspirant du squelette
3. Déclarer l'ordre du parcours dans `__init__.py` (`NOM` et `etapes`)
4. Enregistrer le paradoxe dans `main.py` :
   `manager.ajouter_parcours("fleche", fleche)`
5. Pointer le bouton de l'accueil vers `"fleche-0"`

Chaque étape d'un paradoxe respecte le contrat de `Scene` :
`on_entrer`, `gerer_evenement`, `mettre_a_jour`, `dessiner`.
