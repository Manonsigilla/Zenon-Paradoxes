"""Point d'entrée : lance la fenêtre et la boucle principale.

Usage : python main.py
F11 : basculer en plein écran.
"""

import pygame

import config
from scene_manager import SceneManager
from scenes import accueil, squelette


def basculer_plein_ecran(manager):
    pygame.display.toggle_fullscreen()
    # Le basculement peut recréer la surface d'affichage :
    # le gestionnaire doit récupérer la nouvelle.
    manager.actualiser_ecran()


def main():
    pygame.init()
    ecran = pygame.display.set_mode(config.TAILLE_ECRAN)
    pygame.display.set_caption(config.TITRE)
    horloge = pygame.time.Clock()

    # --- Enregistrement des scènes ---
    manager = SceneManager(ecran)
    manager.enregistrer("accueil", accueil.SceneAccueil(manager))
    manager.ajouter_parcours("squelette", squelette)
    # Dès qu'un paradoxe est prêt, par exemple :
    #     from scenes import fleche
    #     manager.ajouter_parcours("fleche", fleche)
    # puis pointer le bouton de l'accueil vers "fleche-0".
    manager.aller_a("accueil")

    # --- Boucle principale ---
    en_cours = True
    while en_cours:
        dt = horloge.tick(config.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                basculer_plein_ecran(manager)
            else:
                manager.gerer_evenement(event)

        manager.mettre_a_jour(dt)
        manager.dessiner()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
