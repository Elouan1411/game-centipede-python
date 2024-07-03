from utilities.vect2D import Vect2D
from utilities import image


class Entite:
    """
    Classe parent pour chaque entite
    """

    level = 1

    def __init__(self, width, height, pos, dim):
        self.__width = width
        self.__height = height
        self.__pos = pos
        self.setDim(dim)
        self.__image = None

    # Pour position
    def setPos(self, x=None, y=None):
        if x is not None and y is not None:
            self.__pos = Vect2D(x, y)
        elif x is not None:
            self.__pos = Vect2D(x, self.getPosY())
        elif y is not None:
            self.__pos = Vect2D(self.getPosX(), y)
        else:
            self.__pos = Vect2D(0, 0)

    def getPosX(self):
        return self.__pos.getVect2D()[0]

    def getPosY(self):
        return self.__pos.getVect2D()[1]

    def getPos(self):
        return self.__pos.getVect2D()

    # Pour la dimension
    def getDimX(self):
        return self.__dim.getVect2DX()

    def getDimY(self):
        return self.__dim.getVect2DY()

    def setDim(self, dim):
        if not isinstance(dim, Vect2D):
            raise ValueError("La dimension doit être un objet de type Vect2D")
        if dim.getVect2DX() < 0 or dim.getVect2DY() < 0:
            print("Attention : dimensions non valides. Initialisation avec la valeur par défaut (0, 0).")
            dim = Vect2D(0, 0)  # Utilisation de la valeur par défaut (0, 0)

        self.__dim = dim  # Initialisation de l'attribut dim

    # Pour largeur et hauteur de la zone du dwarf
    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    # Les autres methodes

    def movement(self, x, y):
        self.setPos(x=self.getPosX() + x, y=self.getPosY() + y)

    # Pour l'image
    def getImage(self):
        return self.__image

    def resize(self, x, y):
        self.__image = image.resize(self.getImage(), x, y)

    def setImage(self, path_image):
        self.__image = image.load(path_image)

    def rotateImage(self, degree):
        self.__image = image.rotate(self.__image, degree)


class EntiteMouv(Entite):
    def __init__(self, width, height, pos, dim, speed, direction=None):
        super().__init__(width, height, pos, dim)
        self.setSpeed(speed)
        if direction is None:
            self.__dir = Vect2D(0, 0)
        else:
            self.__dir = direction

    # Pour vitesse

    def setSpeed(self, speed):
        if (not isinstance(speed, int)) and (not isinstance(speed, float)):
            raise ValueError("La vitesse doit être un objet de type int ou float")
        if speed < 0:
            print("Attention : vitesse non valide. Initialisation avec la valeur par défaut 0.")
            speed = 0  # Utilisation de la valeur par défaut (0, 0)

        self.__speed = speed  # Initialisation de l'attribut dim

    def getSpeed(self):
        return self.__speed

    # Pour direction

    def setDir(self, x=None, y=None):
        if x is not None and y is not None:
            self.__dir = Vect2D(x, y)
        elif x is not None:
            self.__dir = Vect2D(x, self.getDirY())
        elif y is not None:
            self.__dir = Vect2D(self.getDirX(), y)
        else:
            self.__dir = Vect2D(0, 0)

    def getDirX(self):
        return self.__dir.getVect2D()[0]

    def getDirY(self):
        return self.__dir.getVect2D()[1]
