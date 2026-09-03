"""Étape « Présentation » — SQUELLETTE.

Le modèle d'une étape uniquement textuelle : posez le paradoxe en
une ou deux phrases dans dessiner_contenu.
"""

import config
from scene import SceneParadoxe
from ui import theme, texte


class EtapePresentation(SceneParadoxe):
    TITRE = "Présentation"

    def dessiner_contenu(self, ecran):
        centre_x = config.LARGEUR // 2
        texte.dessiner_texte_centre(
            ecran, "Ceci est une étape squelette.",
            centre_x, 300, theme.police(26, "gras"), theme.ENCRE)
        texte.dessiner_texte_centre(
            ecran,
            "Elle sert à valider la navigation (Précédent / Suivant / Accueil).\n"
            "Copiez ce fichier pour créer vos étapes, puis remplacez son contenu.",
            centre_x, 370, theme.police(20), theme.ENCRE_DOUCE,
            largeur_max=700)
