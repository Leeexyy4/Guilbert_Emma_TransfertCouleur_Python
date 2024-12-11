import cv2

# Classe Action pour gérer les actions des boutons
class Logic:
    def __init__(self, image):
        self.image = image
    
    def clickEvent(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for label, (bx, by, bw, bh, _) in param.items():
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    self.boutonAction(label)
                    
    def boutonAction(self, label):
        print(label)
        if label == 'Quitter':
            cv2.destroyAllWindows()
            exit()
        elif label == 'Telecharger':
            self.image.createDossier()
            self.image.createPalette()
            self.image.createReconstruct()
            self.image.createTransfertGlobal()
            self.image.createTransfertReduitPalette()
            self.image.createTransfertPalette()
            self.image.setImage(self.image.getBase())
        elif label == 'Historique':
            self.image.setImage(self.image.getBase())
        elif label == 'Source':
            self.image.setImage(self.image.getBase())
        elif label == 'Cible':
            self.image.setImage(self.image.getCible())
        elif label == 'Palette':
            self.image.setImage(self.image.getPalette())
        elif label == 'Reconstruction':
            self.image.setImage(self.image.getReconstruct())
        elif label == 'Transfert global':
            self.image.setImage(self.image.getTransfertGlobal())
        elif label == 'Transfert reduit':
            self.image.setImage(self.image.getTransfertReduitPalette())
        elif label == 'Transfert palette':
            self.image.setImage(self.image.getTransfertPalette())