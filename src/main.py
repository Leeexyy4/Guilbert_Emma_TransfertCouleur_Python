import cv2
import sys  # Importer sys pour quitter proprement le programme
from display.display import Display
from logic.logic import Logic
from utils.image import Image

# Classe Main pour initialiser et gérer la logique principale de l'application
class Main:
    def __init__(self):
        self.image = Image() 
        self.display = Display(self.image) 
        self.logic = Logic(self.image) 

    def run(self):
        try:
            while True:
                self.display.displayImage() 
                cv2.imshow("Changement de palette de couleurs", self.display.fenetre)
                cv2.setMouseCallback("Changement de palette de couleurs", self.logic.clickEvent, param=self.display.boutons)
                key = cv2.waitKey(1) & 0xFF

                if key == 27: 
                    break
                    
                if cv2.getWindowProperty("Changement de palette de couleurs", cv2.WND_PROP_VISIBLE) < 1:
                    break 

            cv2.destroyAllWindows()
            sys.exit()

        except Exception as e:
            print(f"Erreur : {e}")
            sys.exit(1)  

if __name__ == "__main__":
    main = Main() 
    main.run()
