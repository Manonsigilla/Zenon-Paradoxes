import pygame

import config
from scene import SceneParadoxe
from ui import texte, theme

class EtapePresentation(SceneParadoxe):
    TITRE = "Présentation"

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2

        plaque = pygame.Rect(centre_x - 420, 225, 840, 250)
        pygame.draw.rect(ecran, theme.SURFACE, plaque, border_radius=14)
        pygame.draw.rect(ecran, theme.OR, plaque, width=2, border_radius=14)

        citation = ("« Achille ne rattrapera jamais la tortue : il doit "
                    "d'abord atteindre le point d'où elle est partie. »")
        contexte = ("Achille, très rapide, fait la course contre une tortue "
                "très lente. \n"
                "Mais la tortue part avec une avance. Pour la rattraper, "
                "Achille doit d'abord atteindre le point où elle se "
                "trouvait ; \n"
                "or pendant ce temps, la tortue a déjà avancé un peu plus "
                "loin.")

        police_citation = theme.police(26, "italique")
        police_contexte = theme.police(20)

        h_citation = (len(texte.decouper_texte(citation, police_citation, 760))
                    * (police_citation.get_height() +6) - 6)
        h_contexte = (len(texte.decouper_texte(contexte, police_contexte, 860))
                      * (police_contexte.get_height() + 6) - 6)
        ecart = 16
        y_bloc = (plaque.top
                  + (plaque.height - (h_citation + ecart + h_contexte)) // 2)

        texte.dessiner_texte_centre(
            ecran, citation, centre_x, y_bloc,
            police_citation, theme.CREME, largeur_max=760)
        texte.dessiner_texte_centre(
            ecran, contexte, centre_x, y_bloc + h_citation + ecart,
            police_contexte, theme.ENCRE, largeur_max=860)
