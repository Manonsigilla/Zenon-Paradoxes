"""Point d'entrée : lance la fenêtre et la boucle principale.

Usage : python main.py
F11 : basculer en plein écran.
"""

import pygame

import config
import sons
from scene_manager import SceneManager
from scenes import accueil, achille, dichotomie, fleche


def basculer_plein_ecran(manager):
    pygame.display.toggle_fullscreen()
    # Le basculement peut recréer la surface d'affichage :
    # le gestionnaire doit récupérer la nouvelle.
    manager.actualiser_ecran()


def main():
    pygame.init()
    sons.initialiser()   # sans carte son, l'application fonctionne quand même
    # Répétition des touches maintenues : un événement après 250 ms,
    # puis toutes les 150 ms. C'est ce qui permet de garder Espace
    # enfoncée pour faire défiler les étapes.
    pygame.key.set_repeat(250, 150)
    ecran = pygame.display.set_mode(config.TAILLE_ECRAN)
    pygame.display.set_caption(config.TITRE)
    horloge = pygame.time.Clock()

    # --- Enregistrement des scènes ---
    manager = SceneManager(ecran)
    manager.enregistrer("accueil", accueil.SceneAccueil(manager))
    manager.ajouter_parcours("dichotomie", dichotomie)
    manager.ajouter_parcours("achille", achille)
    manager.ajouter_parcours("fleche", fleche)
    # puis pointer le bouton de l'accueil vers "fleche-0".
    manager.aller_a("accueil")

    # --- Boucle principale ---
    en_cours = True
    while en_cours:
        dt = horloge.tick(config.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            # F11 est déclenché au RELÂCHEMENT de la touche : sinon,
            # avec la répétition activée, la maintenir ferait clignoter
            # le plein écran plusieurs fois par seconde.
            elif event.type == pygame.KEYUP and event.key == pygame.K_F11:
                basculer_plein_ecran(manager)
            else:
                manager.gerer_evenement(event)

        manager.mettre_a_jour(dt)
        manager.dessiner()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
