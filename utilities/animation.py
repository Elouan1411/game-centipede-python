from os import listdir
from os.path import join
import re

from utilities import load, resize, Vect2D


class Animation:
    """
    Permet d'initialiser les animations que nous utiliserons
    Args :
        - dim (tuple[int, int]): Dimensions de chaque frame de l'animation.
        - frames_path (str): Chemin vers le dossier contenant les frames de l'animation.
        - extension (str): Extension des fichiers d'images (par exemple, '.png').
        - frame_rate (int): Nombre d'images par seconde.
        - frame_timer (int): Temps initial du chronomètre pour l'animation.

    """

    def __init__(self, dim, frames_path, extension, frame_rate, frame_timer):

        self.__pos = Vect2D(None, None)
        self.__dim = dim
        self.__frames_path = frames_path
        self.__extension = extension
        self.__frame_rate = frame_rate
        self.__frame_timer = frame_timer
        self.__current_frame = 0
        self.__animation_frames = self.load_frames()
        self.__animation_active = False

    # Chargement des images
    def load_frames(self):
        """
        Permet de charger les images à afficher.
        
        Returns :
            - animation_frames (list): Liste des images chargées.
        
        """
        animation_frames = []
        filenames = listdir(self.getFramePath())
        # Trier les noms de fichiers comme des nombres entiers
        filenames.sort(key=lambda x: int(re.search(r"\d+", x).group()))
        for filename in filenames:
            if filename.endswith(self.getExtension()):
                image = load(join(self.getFramePath(), filename))
                image = resize(image, self.getDim(), self.getDim())
                animation_frames.append(image)
        return animation_frames

    

    def manageFrame(self, current_time, entite, frame_timer, offset):
        """
        Permet de gerer l'affichage des images
        Args : 
            - current_time (int): Temps actuel en millisecondes.
            - entite (object): Entité associée à l'animation.
            - frame_timer (int): Chronomètre de l'image actuelle.
            - offset (dict): Décalage pour le placement de l'image {'width': int, 'height': int}
    
        """
        if current_time - frame_timer >= 1000 / self.getFrameRate() and self.getCurrentFrame() < len(
            self.getListAnimationFrames()
        ):

            # Passer à la frame suivante
            self.setCurrentFrame(1)

            # Réinitialiser le chronomètre
            self.setFrameTimer(current_time)

            # Si l'animation est finit
            if self.getCurrentFrame() == len(self.getListAnimationFrames()) - 1:
                self.setAnimationActive(False)
                self.setCurrentFrame(-self.getCurrentFrame())  # Remise à 0

            # Placement de la frame
            if self.getCurrentFrame() == 1:  # Pour ne pas qu'elle bouge une fois lancé
                self.setPos(
                    x=-(self.getDim() / 2)
                    + entite.getPosX()
                    + (entite.getDimX() / 2)
                    + entite.getDirX() * offset["width"],
                    y=-(self.getDim() / 2)
                    + entite.getPosY()
                    + (entite.getDimY() / 2)
                    + entite.getDirY() * offset["height"],
                )

    # Position
  

    def getPos(self):
        """
        Permet d'obtenir la position de l'objet
                
        Return : 
            - self.__pos.getVect2D(tuple) : la position du self
        """
        return self.__pos.getVect2D()

    def setPos(self, x=None, y=None):
        """
        Permet de modifier la position.
        
        Args: 
            - x (float, optional): Nouvelle position en X.
            - y (float, optional): Nouvelle position en Y.
        """
        self.__pos = Vect2D(x, y)

    # CurrentFrame

    def getCurrentFrame(self):
        """
        Permet d'obtenir l'image active de l'objet
            
        Returns : 
            - self.__current_frame(int) : l'image active
        """
        return self.__current_frame


    def setCurrentFrame(self, nb):
        """
        Permet de modifier l'image active de l'objet en ajoutant nb
        
        Args : 
            - nb(int) : nombre à ajouter à l'image active
        """
        self.__current_frame += nb

    # Dimension

    def getDim(self):
        """
        Permet d'obtenir la dimension de l'objet
            
        Return : 
            - self.__dim(tuple[int, int]) : la dimension
        """
        return self.__dim

    # AnimationActive

    def getAnimationActive(self):
        """
        Permet d'obtenir l'état de l'animation en cours

        Return :
            - self.__animation_active(bool)
        """
        return self.__animation_active

    def setAnimationActive(self, etat):
        """
        Permet de modifier l'état de l'animation en cours

        Args :
            - etat (boolean)

        """
        self.__animation_active = etat

    def getFrameTimer(self):
        """
        Permet d'obtenir le temps pour lequel les images vont s'écouler

        Args :

        Return :
            - self.__frame_timer(int)
        """
        return self.__frame_timer

    def setFrameTimer(self, current_frame):
        """
        Permet de modifier le timer pour l'écoulement des images

        Args :
            - current_frame(int)

        """
        self.__frame_timer = current_frame

    # Animation frames
    def getAnimationFrames(self):
        """
        Permet d'obtenir l'image active de l'animation active
        
        Returns : 
            - self.__animation_frames[self.getCurrentFrame()](object): l'image active de l'animation
        """
        return self.__animation_frames[self.getCurrentFrame()]

    def getListAnimationFrames(self):
        """
        Permet d'obtenir la liste des animations
        
        Returns : 
            - self.__animation_frames(list) : liste des animations
        """
        return self.__animation_frames

    # Frame Path
    def getFramePath(self):
        """
        Permet d'obtenir le chemin d'obtention de l'image
        
        Returns : 
            - self.__frames_path(str): le chemin d'obtention de l'image active
        """
        return self.__frames_path

    # Extension
    def getExtension(self):
        """
        Permet d'obtenir l'extension
        
        Returns : 
            - self.__extension(str)
        """
        return self.__extension

    # FrameRate
    def getFrameRate(self):
        """
        Permet d'obtenir la fréquence de l'image
         
        Returns : 
            - self.__frame_rate(int) : la fréquence de l'image
        """
        return self.__frame_rate
