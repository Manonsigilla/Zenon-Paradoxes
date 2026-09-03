"""Navigation entre les scènes : l'accueil et les étapes des paradoxes.

Les étapes d'un paradoxe forment un parcours linéaire. L'ordre est
déclaré dans le __init__.py du dossier du paradoxe (attributs NOM et
etapes), jamais ici : pour ajouter un paradoxe, voir main.py.
"""

import pygame


class SceneManager:
    def __init__(self, ecran):
        self.ecran = ecran
        self.scenes = {}        # identifiant -> instance de scène
        self.parcours = {}      # nom du paradoxe -> {"nom": str, "ids": [str]}
        self.paradoxe_de = {}   # identifiant d'étape -> nom du paradoxe
        self.id_actuel = None
        self.scene_actuelle = None

    # ------------------------------------------------------------- écran
    def actualiser_ecran(self):
        """À appeler après un basculement plein écran : la surface
        d'affichage peut changer, il faut la récupérer à nouveau."""
        self.ecran = pygame.display.get_surface()

    # ------------------------------------------------------ enregistrement
    def enregistrer(self, identifiant, scene):
        """Enregistre une scène indépendante (ex. l'accueil)."""
        self.scenes[identifiant] = scene

    def ajouter_parcours(self, nom, module):
        """Enregistre toutes les étapes d'un paradoxe.

        `module` doit exposer :
        - NOM : le titre du paradoxe (affiché dans l'entête) ;
        - etapes : la liste des classes d'étapes, dans l'ordre.
        Chaque étape reçoit l'identifiant "nom-0", "nom-1", etc.
        """
        ids = []
        for i, classe in enumerate(module.etapes):
            identifiant = f"{nom}-{i}"
            self.enregistrer(identifiant, classe(self))
            self.paradoxe_de[identifiant] = nom
            ids.append(identifiant)
        self.parcours[nom] = {"nom": module.NOM, "ids": ids}

    # ---------------------------------------------------------- navigation
    def aller_a(self, identifiant):
        """Change de scène et signale à la nouvelle qu'elle est active."""
        if identifiant not in self.scenes:
            raise KeyError(f"Scène inconnue : {identifiant}")
        self.id_actuel = identifiant
        self.scene_actuelle = self.scenes[identifiant]
        self.scene_actuelle.on_entrer()

    def suivant(self):
        """Avance d'une étape dans le parcours courant (sans effet à la fin)."""
        ids = self._ids_du_parcours()
        if ids is not None and self.id_actuel != ids[-1]:
            self.aller_a(ids[ids.index(self.id_actuel) + 1])

    def precedent(self):
        """Recule d'une étape dans le parcours courant (sans effet au début)."""
        ids = self._ids_du_parcours()
        if ids is not None and self.id_actuel != ids[0]:
            self.aller_a(ids[ids.index(self.id_actuel) - 1])

    def _ids_du_parcours(self):
        """Liste des identifiants du parcours courant, ou None."""
        nom = self.paradoxe_de.get(self.id_actuel)
        return self.parcours[nom]["ids"] if nom is not None else None

    # -------------------------------------------------------- informations
    def position_de(self, identifiant):
        """Numéro d'étape (1..N) et total du parcours, ou None hors paradoxe."""
        ids = self._ids_du_parcours()
        if ids is None:
            return None
        return ids.index(identifiant) + 1, len(ids)

    def nom_paradoxe(self, identifiant):
        """Titre du paradoxe auquel appartient la scène ("" hors paradoxe)."""
        nom = self.paradoxe_de.get(identifiant)
        return self.parcours[nom]["nom"] if nom is not None else ""

    # ---------------------------------------------------------- délégation
    def gerer_evenement(self, event):
        self.scene_actuelle.gerer_evenement(event)

    def mettre_a_jour(self, dt):
        self.scene_actuelle.mettre_a_jour(dt)

    def dessiner(self):
        self.scene_actuelle.dessiner(self.ecran)
