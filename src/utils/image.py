import shutil, cv2, os, numpy as np
from tkinter import Tk, filedialog
from utils.function import Function

class Image:
    def __init__(self):
        self.dossier : str = None
        self.actual : str = None
        self.base : str = None
        self.cible : str = None
        self.palette : str = None
        self.recontruct : str = None
        self.transfertGlobal : str = None
        self.transfertReduitPalette : str = None
        self.transfertPalette : str = None
        self.function = Function()

    # Méthode pour obtenir le dossier des images
    def getDossier(self):
        return self.dossier

    # Méthode pour définir le dossier des images
    def setDossier(self, dossier):
        self.dossier = dossier

    # Méthode pour obtenir l'image affichée
    def getImage(self):
        if self.base is None or self.cible is None or self.palette is None or self.recontruct is None or self.clusterGlobal is None or self.clustePalette is None :
            print("Erreur : Aucune image n'a été chargée.")
        return self.actual

    # Méthode pour définir l'image de base
    def setImage(self, imageActual):
        self.actual = imageActual

    # Méthode pour obtenir l'image de base
    def getBase(self):
        if self.base is None:
            print("Erreur : Aucune image n'a été chargée.")
        return self.base

    # Méthode pour définir l'image de base
    def setBase(self, imageBase):
        self.base = imageBase
        
    # Méthode pour obtenir l'image cible
    def getCible(self):
        if self.cible is None:
            print("Erreur : Aucune image n'a été chargée.")
        return self.cible

    # Méthode pour définir l'image cible
    def setCible(self, imageCible):
        self.cible = imageCible
        
    # Méthode pour obtenir l'image de la palette
    def getPalette(self):
        if self.palette is None:
            print("Erreur : Aucune image n'a été chargée.")
        return self.palette

    # Méthode pour définir l'image de la palette
    def setPalette(self, imagePalette):
        self.palette = imagePalette
        
    # Méthode pour obtenir l'image regénérée
    def getReconstruct(self):
        if self.recontruct is None:
            print("Erreur : Aucune image n'a été chargée.")
        return self.recontruct

    # Méthode pour définir l'image regénérée
    def setReconstruct(self, imageRecontruct):
        self.recontruct = imageRecontruct
        
    # Méthode pour obtenir l'image par transfert global
    def getTransfertGlobal(self):
        if self.transfertGlobal is None:
            print("Erreur : Aucune image n'a été chargée.")
        return self.transfertGlobal

    # Méthode pour définir l'image par transfert global
    def setTransfertGlobal(self, imageTransfertGlobal):
        self.transfertGlobal = imageTransfertGlobal
        
    # Méthode pour obtenir l'image par transfert reduit de palette
    def getTransfertReduitPalette(self):
        if self.transfertReduitPalette is None:
            print("Erreur : Aucune image n'a été chargée.")
        return self.transfertReduitPalette

    # Méthode pour définir l'image par transfert reduit de palette
    def setTransfertReduitPalette(self, imageTransfertReduitPalette):
        self.transfertReduitPalette = imageTransfertReduitPalette

    # Méthode pour obtenir l'image par transfert de palette
    def getTransfertPalette(self):
        if self.transfertPalette is None:
            print("Erreur : Aucune image n'a été chargée.")
        return self.transfertPalette

    # Méthode pour définir l'image par transfert de palette
    def setTransfertPalette(self, imageTransfertPalette):
        self.transfertPalette = imageTransfertPalette
        
    # Méthode pour vérifier et créer le dossier
    def createDossier(self):
        # Demander à l'utilisateur de sélectionner l'image de base
        root = Tk()
        root.withdraw()  # Masquer la fenêtre Tkinter
        base_image_path = filedialog.askopenfilename(title="Sélectionner l'image de base", filetypes=[("Image Files", "*.jpg")])

        # Demander à l'utilisateur de sélectionner l'image cible
        cible_image_path = filedialog.askopenfilename(title="Sélectionner l'image cible", filetypes=[("Image Files", "*.jpg")])

        # Vérifier si les deux images ont été sélectionnées
        if not base_image_path or not cible_image_path:
            print("Erreur : Les deux images (base et cible) doivent être sélectionnées.")
            return
        
        # Créer un dossier basé sur le nom de l'image de base (par exemple: ./assets/images/nomdelimage)
        base_image_name = os.path.basename(base_image_path)
        base_image_name_without_ext = os.path.splitext(base_image_name)[0]
        folder_path = os.path.join('./assets/images', base_image_name_without_ext)
        
        # Créer le dossier si il n'existe pas
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Enregistrer le chemin du dossier
        self.setDossier(folder_path)

        # Définir les chemins pour les images dans ce dossier
        self.base = os.path.join(folder_path, base_image_name_without_ext + "Base.jpg")
        self.cible = os.path.join(folder_path, base_image_name_without_ext + "Cible.jpg")
        self.palette = os.path.join(folder_path, base_image_name_without_ext + "Palette.jpg")
        self.recontruct = os.path.join(folder_path, base_image_name_without_ext + "Reconstruction.jpg")
        self.transfertGlobal = os.path.join(folder_path, base_image_name_without_ext + "TransfertGlobal.jpg")
        self.transfertReduitPalette = os.path.join(folder_path, base_image_name_without_ext + "TransfertReduitPalette.jpg")
        self.transfertPalette = os.path.join(folder_path, base_image_name_without_ext + "TransfertPalette.jpg")
        
        # Copier les images sélectionnées dans le dossier
        shutil.copy(base_image_path, self.base)
        shutil.copy(cible_image_path, self.cible)

    def createPalette(self):
        """
        Fonction:
            Crée la palette de couleurs à partir de l'image cible en utilisant l'algorithme de clustering K-Means.
            La palette contiendra les n couleurs dominantes de l'image cible.

        Démarche:
            - Charger l'image cible.
            - Appliquer un clustering (K-Means) sur les pixels de l'image pour identifier les couleurs dominantes.
            - Enregistrer la palette dans le dossier spécifié.

        Arguments:
            Aucun, la fonction utilise l'image cible déjà chargée.

        Exemple d'utilisation:
            createPalette()
        """
        # Lire l'image cible en tant qu'image float
        target_image_float = self.function.read_image_as_float(self.base)

        # Appliquer le clustering (par exemple, K-Means) sur l'image cible pour identifier les couleurs dominantes
        clusters, labels = self.function.cluster_image(target_image_float)

        # Générer les images représentant chaque couleur de la palette
        images_uniformes = self.function.generate_uniform_images(clusters, 128)

        # Créer une image représentant la palette en concaténant les images de couleurs
        palette_image = self.function.create_horizontal_image(images_uniformes)

        # Sauvegarder l'image de la palette
        cv2.imwrite(self.palette, (palette_image * 255).astype(np.uint8))


    def createReconstruct(self):
        """
        Fonction:
            Reconstruit l'image cible en utilisant la palette de l'image source et les clusters de l'image cible.
            Cette reconstruction applique un transfert de couleurs basé sur les clusters des images.

        Démarche:
            - Charger l'image source et l'image cible.
            - Effectuer un clustering K-Means sur l'image cible pour obtenir les clusters de couleurs.
            - Appliquer les clusters de l'image source sur l'image cible en utilisant les clusters correspondants.

        Arguments:
            Aucun, la fonction utilise les images source et cible déjà chargées.

        Exemple d'utilisation:
            createReconstruct()
        """
        # Lire l'image source et l'image cible
        source_image_float = self.function.read_image_as_float(self.base)
        target_image_float = self.function.read_image_as_float(self.cible)

        # Appliquer un clustering K-Means sur l'image source et l'image cible
        source_clusters, _ = self.function.cluster_image(source_image_float)
        target_clusters, target_labels = self.function.cluster_image(target_image_float)

        # Reconstructer l'image cible en utilisant les clusters de l'image source
        reconstructed_image = self.function.reconstruct_image_from_clusters(
            self.base, self.cible, n_colors=len(source_clusters)
        )

        # Sauvegarder l'image reconstruite
        cv2.imwrite(self.recontruct, (reconstructed_image * 255).astype(np.uint8))

    def createTransfertGlobal(self):
        """
        Fonction:
            Effectue un transfert global de couleur entre l'image source et l'image cible.
            Cette fonction ajuste les couleurs globales de l'image cible pour correspondre à celles de l'image source.

        Démarche:
            - Lire les images source et cible.
            - Calculer la moyenne des couleurs pour chaque image.
            - Effectuer un transfert global des couleurs en ajustant les couleurs de l'image cible pour correspondre à celles de l'image source.

        Arguments:
            Aucun, la fonction utilise les images source et cible déjà chargées.

        Exemple d'utilisation:
            createTransfertGlobal()
        """
        # Lire les images source et cible
        source_image_float = self.function.read_image_as_float(self.base)
        target_image_float = self.function.read_image_as_float(self.cible)

        # Calculer les statistiques globales des images (par exemple, la moyenne des couleurs)
        source_mean = np.mean(source_image_float, axis=(0, 1))
        target_mean = np.mean(target_image_float, axis=(0, 1))

        # Appliquer le transfert global de couleur (ajuster les couleurs de l'image cible pour correspondre à l'image source)
        transferred_image = (target_image_float - target_mean) + source_mean

        # Sauvegarder l'image transférée globalement
        cv2.imwrite(self.transfertGlobal, (transferred_image * 255).astype(np.uint8))


    def createTransfertReduitPalette(self):
        """
        Fonction:
            Effectue un transfert de couleur réduit aux palettes entre l'image source et l'image cible.
            Cette fonction applique uniquement les couleurs dominantes (clusters) de l'image source
            aux pixels de l'image cible en respectant les clusters de l'image cible.

        Démarche:
            - Lire l'image source et l'image cible.
            - Appliquer un clustering K-Means sur les deux images pour identifier les couleurs dominantes.
            - Réattribuer les couleurs dominantes de l'image source aux régions correspondant aux clusters de l'image cible.

        Arguments:
            Aucun, la fonction utilise les images source et cible déjà chargées.

        Exemple d'utilisation:
            createTransfertReduitPalette()
        """
        # Lire les images source et cible
        source_image_float = self.function.read_image_as_float(self.base)
        target_image_float = self.function.read_image_as_float(self.cible)

        # Appliquer un clustering K-Means sur les deux images
        source_clusters, _ = self.function.cluster_image(source_image_float)
        target_clusters, target_labels = self.function.cluster_image(target_image_float)

        # Initialiser l'image résultat avec les dimensions de l'image cible
        transferred_image_palette = np.zeros_like(target_image_float)

        # Parcourir chaque cluster de l'image cible
        for cluster_idx in range(len(target_clusters)):
            # Trouver les pixels appartenant au cluster actuel dans l'image cible
            cluster_mask = (target_labels == cluster_idx)

            # Récupérer la couleur dominante correspondante dans l'image source
            source_color = source_clusters[cluster_idx % len(source_clusters)]  # Répartition circulaire des clusters

            # Appliquer cette couleur aux pixels correspondants dans l'image cible
            transferred_image_palette[cluster_mask] = source_color

        # Sauvegarder l'image transférée réduite aux palettes
        cv2.imwrite(self.transfertReduitPalette, (transferred_image_palette * 255).astype(np.uint8))


    def createTransfertPalette(self):
        """
        Fonction:
            Effectue un transfert de couleur basé sur la palette de couleurs entre l'image source et l'image cible.
            Cette fonction applique les couleurs dominantes de l'image source sur l'image cible en utilisant le clustering.

        Démarche:
            - Lire les images source et cible.
            - Effectuer un clustering K-Means sur les deux images pour extraire les couleurs dominantes.
            - Mapper les clusters de l'image source sur l'image cible en utilisant la correspondance des clusters.

        Arguments:
            Aucun, la fonction utilise les images source et cible déjà chargées.

        Exemple d'utilisation:
            createTransfertPalette()
        """
        # Lire les images source et cible
        source_image_float = self.function.read_image_as_float(self.base)
        target_image_float = self.function.read_image_as_float(self.cible)

        # Appliquer un clustering K-Means sur l'image source et l'image cible
        source_clusters, _ = self.function.cluster_image(source_image_float)
        target_clusters, target_labels = self.function.cluster_image(target_image_float)

        # Mapper les clusters de l'image source sur l'image cible
        cluster_mapping = self.function.map_clusters(source_clusters, target_clusters)

        # Appliquer les couleurs de l'image source sur l'image cible
        transferred_image = self.function.reconstruct_image_from_clusters(
            self.base, self.cible, n_colors=len(source_clusters)
        )

        # Sauvegarder l'image transférée par palette
        cv2.imwrite(self.transfertPalette, (transferred_image * 255).astype(np.uint8))