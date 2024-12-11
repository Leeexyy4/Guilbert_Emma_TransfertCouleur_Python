import cv2
import numpy as np
import screeninfo

class Display:
    def __init__(self, image):
        self.largeur_ecran = screeninfo.get_monitors()[0].width
        self.hauteur_ecran = screeninfo.get_monitors()[0].height
        self.fenetre = np.zeros((self.hauteur_ecran, self.largeur_ecran, 3), dtype=np.uint8)
        self.boutons = self.displayBouton()
        self.image = image

    def displayIcon(self, chemin, taille=(40, 40)):
        """ Charge et redimensionne une icône, retourne l'icône redimensionnée ou None si erreur """
        icone = cv2.imread(chemin)
        if icone is None:
            print(f"Erreur: L'icône {chemin} est introuvable.")
            return None
        return cv2.resize(icone, taille)

    def displayBouton(self):
        """ Affiche les boutons dans la fenêtre """
        boutons = {
            'Source': (0, 0, 150, 50, (255, 20, 0)),
            'Cible': (150, 0, 150, 50, (255, 40, 0)),
            'Palette': (300, 0, 150, 50, (255, 60, 0)),
            'Reconstruction': (500, 0, 300, 50, (255, 80, 0)),
            'Transfert global': (800, 0, 300, 50, (255, 100, 0)),
            'Transfert reduit': (1100, 0, 300, 50, (255, 120, 0)),
            'Transfert palette': (1400, 0, 300, 50, (255, 140, 0)),
            'Historique': (1730, 0, 50, 50, (0, 0, 0)),
            'Telecharger': (1790, 0, 50, 50, (0, 0, 0)),
            'Quitter': (1850, 0, 50, 50, (0, 0, 0))
        }

        # Dessiner les boutons
        for label, (x, y, w, h, c) in boutons.items():
            if label == 'Historique':
                historiquesized = self.displayIcon('./assets/images/icons/historique.png', taille=(50,50))
                if historiquesized is not None:
                    self.fenetre[y+5:y+55, x+5:x+55] = historiquesized
            elif label == 'Telecharger':
                downloadResized = self.displayIcon('./assets/images/icons/telecharger.png', taille=(50,50))
                if downloadResized is not None:
                    self.fenetre[y+5:y+55, x+5:x+55] = downloadResized
            elif label == 'Quitter':
                quitResized = self.displayIcon('./assets/images/icons/quitter.png', taille=(50,50))
                if quitResized is not None:
                    self.fenetre[y+5:y+55, x+5:x+55] = quitResized
            else:
                # Dessiner le bouton et la bordure
                cv2.rectangle(self.fenetre, (x, y), (x+w, y+h), c, -1) 
                cv2.rectangle(self.fenetre, (x-2, y-2), (x+w+2, y+h+2), (255, 255, 255), 3) 
                
                # Dessiner le texte centré
                (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                text_x = x + (w - text_width) // 2
                text_y = y + (h + text_height) // 2
                cv2.putText(self.fenetre, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 
        return boutons

    def displayImage(self):
        """ Affiche l'image dans la fenêtre, centrée et sans déformation """
        hauteur_max = self.hauteur_ecran - 50  # Espace pour les boutons
        largeur_max = self.largeur_ecran

        # Charger l'image
        image = cv2.imread(self.image.actual)

        if image is not None:
            # Obtenir les dimensions de l'image
            hauteur_image, largeur_image = image.shape[:2]

            # Calculer le facteur de mise à l'échelle pour respecter les proportions
            ratio_largeur = largeur_max / largeur_image
            ratio_hauteur = hauteur_max / hauteur_image

            # Choisir le plus petit ratio pour éviter la déformation
            ratio = min(ratio_largeur, ratio_hauteur)

            # Calculer les nouvelles dimensions de l'image
            nouvelle_largeur = int(largeur_image * ratio)
            nouvelle_hauteur = int(hauteur_image * ratio)

            # Redimensionner l'image
            image_redimensionnee = cv2.resize(image, (nouvelle_largeur, nouvelle_hauteur))

            # Calculer la position pour centrer l'image dans la fenêtre
            x_offset = (largeur_max - nouvelle_largeur) // 2
            y_offset = (hauteur_max - nouvelle_hauteur) // 2

            # Créer une fenêtre vide (blanche ou noire)
            fenetre_image = np.zeros((hauteur_max, largeur_max, 3), dtype=np.uint8)

            # Copier l'image redimensionnée dans la fenêtre à la position calculée
            fenetre_image[y_offset:y_offset+nouvelle_hauteur, x_offset:x_offset+nouvelle_largeur] = image_redimensionnee

            # Afficher l'image dans la fenêtre (ou l'interface graphique)
            self.fenetre[50:, :] = fenetre_image  # Afficher l'image sous les boutons
        else:
            message = "Cliquez sur le bouton d'importation pour charger l'image de base et l'image cible."
            cv2.putText(self.fenetre, message, (50, self.hauteur_ecran // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Texte en rouge
