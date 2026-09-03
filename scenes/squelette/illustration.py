"""Étape « Illustration » — SQUELLETTE.

Le modèle d'une étape animée. C'est ici que vivra l'illustration de
votre paradoxe :
- dessiner_contenu  : dessiner les objets (formes géométriques, sprites) ;
- mettre_a_jour(dt) : calculer les positions au fil du temps ;
- gerer_evenement   : gérer les interactions (rejouer, pause, réglages),
  en appelant d'abord super().gerer_evenement(event) pour garder la
  barre de navigation fonctionnelle.
"""

import config
from scene import SceneParadoxe
from ui import theme, texte


class EtapeIllustration(SceneParadoxe):
    TITRE = "Illustration"

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2
        texte.dessiner_texte_centre(
            ecran, "Ici viendra l'illustration animée du paradoxe.",
            centre_x, 330, theme.police(26, "gras"), theme.ENCRE)
        texte.dessiner_texte_centre(
            ecran,
            "Utilisez mettre_a_jour(dt) pour animer et dessiner_contenu\n"
            "pour dessiner. dt est le temps écoulé depuis l'image précédente.",
            centre_x, 400, theme.police(20), theme.ENCRE_DOUCE,
            largeur_max=700)
