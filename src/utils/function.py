import cv2, numpy as np
from sklearn.cluster._kmeans import KMeans

class Function:
    def __init__(self):
        pass
    
    def read_image_as_float(self, image: str) -> np.ndarray:
        """
        Fonction:
            Lit une image à partir d'un fichier et la convertit en un tableau `NumPy` de type `float64` avec des valeurs comprises entre 0 et 1.
        Arguments:
            image_path: Le lien de l'image a lire.
        Return:
            Le tableau NumPy représentant l'image.
        Exemple d'utilisation: 
            image = read_image_as_float('mon_image.jpg')
        """
        img = cv2.imread(image)
        img_float = img.astype(np.float64) / 255.0
        return img_float

    def cluster_image(self, image: np.ndarray, n_colors: int = 5) -> tuple[np.ndarray, np.ndarray]:
        """
        Focntion:
            Clusterise une image en utilisant l'algorithme K-Means.
        Arguments:
            - image: Le tableau NumPy représentant l'image.
            - n_colors: Le nombre de clusters (couleurs) à utiliser.
        Return:
            Un tuple contenant les centroïdes des clusters et les labels de chaque pixel.
        Exemple d'utilisation:
            clusters, labels = cluster_image(image, n_colors=10)
        """
        # Formatation de l'image en une liste de pixels RGB
        pixels = image.reshape(-1, 3) 
        
        # Appliquer KMeans
        kmeans = KMeans(n_clusters=n_colors)
        kmeans.fit(pixels)
        
        # Retourner les centroïdes des clusters et les labels des pixels
        return kmeans.cluster_centers_, kmeans.labels_

    def recreate_image(self, codebook: np.ndarray, labels: np.ndarray, w: int, h: int) -> np.ndarray:
        """
        Fonction:
            Reconstruit l'image compressée à partir des centroïdes des clusters et des labels des pixels.
        Arguments:
            codebook: Les centroïdes des clusters.
            labels: Les labels des pixels.
            w: La largeur de l'image.
            h: La hauteur de l'image.
        Return:
            Le tableau NumPy représentant l'image reconstruite.
        Exemple d'utilisation:
            image_reconstruite = recreate_image(clusters, labels, image.shape[0], image.shape[1])
        """
        # Assigner les centroïdes aux pixels en fonction des labels
        clustered_pixels = codebook[labels]
        
        # Reconstruire l'image
        return clustered_pixels.reshape(h, w, 3)

    def generate_uniform_images(self, colors: list[tuple[float, float, float]], size: int) -> list[np.ndarray]:
        """
        Fonction:
            Génère une liste d'images uniformes de la taille spécifiée, chacune avec une couleur de la liste colors.
            Enregistre une image JPG représentant les couleurs uniformes si un chemin est fourni.
        Arguments:
            - colors: Liste de tuples RGB représentant les couleurs des clusters.
            - size: Taille de chaque image (size x size).
            - output_path: Chemin pour enregistrer l'image concaténée (optionnel).
        Retourne:
            - Une liste de tableaux NumPy, chaque tableau représentant une image carrée uniforme.
        """
        images = []
        for color in colors:
            # Créer une image uniforme avec la couleur spécifiée
            image = np.full((size, size, 3), color, dtype=np.float64)
            images.append(image)
        return images

    def create_horizontal_image(self, images: list[np.ndarray], output_path: str = None) -> np.ndarray:
        """
        Fonction:
            Crée une image en concaténant horizontalement les images de la liste images.  Cette fonctiuon permet d'afficher la palette calculer à partir de la fonction `cluster_image`.
        Arguments:
            - images: Liste de tableaux NumPy représentant les images à concaténer.
        Retourne:
            - Un tableau NumPy représentant une image où toutes les images sont placées côte à côte.
        Exemple d'utilisation:
            palette = create_horizontal_image(images_uniformes)
        """
        # Concaténer les images horizontalement
        return np.concatenate(images, axis=1)

    def map_clusters(self, clusters1, clusters2) -> list[tuple[float, float]]:
        """
        Fonction:
            Calcule une correspondance entre les clusters de deux images en fonction de leur distance euclidienne.
        Arguments:
            clusters1: Les centroïdes des clusters de la première image.
            clusters2: Les centroïdes des clusters de la deuxième image.
        Return:
            Une liste de tuples, où chaque tuple contient les indices des clusters correspondants dans clusters1 et clusters2.
        Exemple d'utilisation:
            mapping = map_clusters(clusters1, clusters2)
        """
        mapping = []
        
        for i, cluster1 in enumerate(clusters1):
            distances = np.linalg.norm(clusters2 - cluster1, axis=1)
            best_match = np.argmin(distances)
            mapping.append((i, best_match))
        
        return mapping

    def reconstruct_image_from_clusters(self, image_path1: str, image_path2: str, n_colors: int = 6) -> np.ndarray:
        """
        Fonction:
            Reconstruit une image en utilisant les clusters d'une autre image.
        Arguments:
            image_path1: Chemin vers la première image (source des couleurs).
            image_path2: Chemin vers la deuxième image (à reconstruire).
            n_colors: Nombre de couleurs à utiliser pour le clustering.
        Return: 
            L'image recontruite en fonction de la palette de couleurs de la deuxième image.
        Exemple d'utilisation:
            image_reconstruite = reconstruct_image_from_clusters('image1.jpg', 'image2.jpg', 6)
        """
        # Charger les deux images
        image1 = self.read_image_as_float(image_path1)
        image2 = self.read_image_as_float(image_path2)
        
        # Appliquer le clustering sur les deux images
        clusters1, labels1 = self.cluster_image(image1, n_colors)
        clusters2, labels2 = self.cluster_image(image2, n_colors)
        
        # Mapper les clusters de l'image source vers ceux de l'image cible
        mapping = self.map_clusters(clusters1, clusters2)
        
        # Reconstruire l'image cible avec les clusters mappés
        new_labels2 = np.copy(labels2)
        for i, j in mapping:
            new_labels2[labels2 == i] = j
        
        return self.recreate_image(clusters1, new_labels2, image2.shape[1], image2.shape[0])

    def transfer_colors_by_cluster(self, source_image: np.ndarray, target_image: np.ndarray, n_colors: int = 5) -> np.ndarray:
        """
        Fonction:
            Effectue un transfert de couleurs entre une image source et une image cible en utilisant le clustering K-Means.
            Les couleurs de l'image cible sont remplacées par celles de l'image source basées sur les clusters de couleurs.
            
        Arguments:
            source_image: L'image source à partir de laquelle les couleurs seront extraites (tableau NumPy).
            target_image: L'image cible à laquelle les couleurs seront transférées (tableau NumPy).
            n_colors: Le nombre de clusters (couleurs) à utiliser pour le clustering. Par défaut, 5.
            
        Retourne:
            Le tableau NumPy représentant l'image cible après transfert de couleurs.
            
        Exemple d'utilisation:
            image_transferred = transfer_colors_by_cluster(source_image, target_image, n_colors=6)
        """ 
        # Appliquer le clustering sur les deux images
        clusters1, labels1 = self.cluster_image(source_image, n_colors)
        clusters2, labels2 = self.cluster_image(target_image, n_colors)
        
        # Mapper les clusters de l'image source vers ceux de l'image cible
        mapping = self.map_clusters(clusters1, clusters2)
        
        # Remplacer les couleurs de l'image cible par celles de l'image source
        new_labels2 = np.copy(labels2)
        for i, j in mapping:
            new_labels2[labels2 == i] = j
        
        return self.recreate_image(clusters1, new_labels2, target_image.shape[1], target_image.shape[0])