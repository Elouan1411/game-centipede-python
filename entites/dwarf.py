from .entite import EntiteMouv
from utilities.manageDirection import sign


class Dwarf(EntiteMouv):
    score = 0

    def __init__(self, width, height, pos, dim, speed, explosion_animation):
        super().__init__(width, height, pos, dim, speed)
        self.__life = 3
        self.__explosion_animation = explosion_animation
        self.setImage("assets/images/dwarf.png")

    # Pour life

    def setLife(self, lifePoints):
        self.__life += lifePoints

    def getLife(self):
        return self.__life

    def getExplosionAnimation(self):
        return self.__explosion_animation

    def setExplosionAnimation(self, etat):
        """
        Args :
            - etat : boolean
        """
        return self.getExplosionAnimation().setAnimationActive(etat)

    # Autres méthodes

    def checkEdge(self):
        """
        Replacement si nain hors zone
        """
        self.setPos(
            x=min(
                max(self.getPosX(), self.getWidth()[0]),
                self.getWidth()[1] - self.getDimX(),
            ),
            y=min(
                max(self.getPosY(), self.getHeight()[0]),
                self.getHeight()[1] - self.getDimY(),
            ),
        )

    def manageDirection(self, key_pressed):
        """
        Gère la direction d'un objet en fonction des touches enfoncées.
        (Pour garder en mémoire qu'une touche a été pressé -> car non fonctionnel avec pygame seulement)

        Args:
        - key_pressed (dict): Un dictionnaire contenant les états des touches.

        Returns:
        - list: Une liste contenant les nouveaux vecteurs de direction x et y.
        """

        # Gestion des x
        if key_pressed["LEFT"] and key_pressed["RIGHT"]:
            self.setDir(x=key_pressed["Last_x"])
        elif key_pressed["LEFT"]:
            self.setDir(x=LEFT)
        elif key_pressed["RIGHT"]:
            self.setDir(x=RIGHT)
        else:
            self.setDir(x=STOP)

        # Gestion des y
        if key_pressed["UP"] and key_pressed["DOWN"]:
            self.setDir(y=key_pressed["Last_y"])
        elif key_pressed["UP"]:
            self.setDir(y=UP)
        elif key_pressed["DOWN"]:
            self.setDir(y=DOWN)
        else:
            self.setDir(y=STOP)

    def getScore(self):
        return Dwarf.score

    def setScore(self, point):
        Dwarf.score += point


RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1
STOP = 0
