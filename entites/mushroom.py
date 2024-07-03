from .entite import Entite
from utilities.vect2D import Vect2D, randomVect2D
from random import randint
from utilities.image import size, ratio


class Mushroom(Entite):
    mushroom_list = []
    white = False

    def __init__(self, width, height, dim):
        super().__init__(width, height, self.place(width, height, dim), dim)
        self.__life = 4
        self.__white = Mushroom.white
        self.setImage()

        Mushroom.mushroom_list.append(self)  # Ajout du mushroom à la liste des mushrooms

    def setLife(self, lifePoints):
        white = "white" if self.__white else "notWhite"
        self.__life += lifePoints
        limit = 4
        level = limit if not Entite.level % limit else Entite.level % limit

        if self.__life > 0:
            self.setDim(
                Vect2D(
                    self.getDimX(),
                    self.getDimX()
                    * ratio(
                        size(
                            "assets/images/mushroom/"
                            + white
                            + "/life"
                            + str(self.getLife())
                            + "_niv"
                            + str(level)
                            + ".png"
                        )
                    ),
                )
            )
            self.setImage()
            self.resize(self.getDimX(), self.getDimY())
        else:
            self.dead()

    def dead(self):
        """
        Tue le mushroom et l'enlève de la liste
        """
        Mushroom.mushroom_list.remove(self)

    def getLife(self):
        return self.__life

    # Pour le self.empoisonne

    def getwhite(self):
        return self.__white

    # pour images de mushroom

    def setImage(self):
        """
        Créer le chemin d'accès à l'image en fonction du niveau et de sa vie
        Appel ensuite setImage() de sa classe parent pour charger l'image
        """
        limit = 4
        level = limit if not Entite.level % limit else Entite.level % limit  # 0 == False -> True
        white = "white" if self.__white else "notWhite"
        path_image = (
            "assets/images/mushroom/"
            + white
            + "/life"
            + str(self.getLife())
            + "_niv"
            + str(level)
            + ".png"
        )
        super().setImage(path_image)

    def place(self, width, height, dim):
        """
        Place le champignon dans sa bonne zone

        Args :
            - width (int) : largeur (zone)
            - height (int) : hauteur (zone)
            - dim (int) : dimension d'un champignon

        Return :
            - Vect2D : position aléatoire respectant les consignes
        """
        maxX = int(width / dim.getVect2DX() - 1)
        maxY = int(height / dim.getVect2DY() - 1)
        return Vect2D(randint(0, maxX) * dim.getVect2DX(), randint(0, maxY) * dim.getVect2DY())

    def base_copy(self):
        """
        Retourne une copie des caractéristique de base d'un champignon pour en créer un autre facilement
        """
        return (
            self.getWidth(),
            self.getHeight(),
            Vect2D(
                self.getDimX(), self.getDimX()
            ),  # DimX pour le Y car risque qu'il est deja perdu de la vie
        )

    def changeStyle(self):
        self.__white = not self.__white
        self.setImage()
        self.resize(self.getDimX(), self.getDimY())


def changeStyleAll():
    Mushroom.white = not Mushroom.white
    for k in range(len(Mushroom.mushroom_list)):
        Mushroom.mushroom_list[k].changeStyle()


def lifeMinus(mushroom_list_touch, point, dwarf):
    """
    Args :
        - list_mushroom : liste des champignons qui ont été touché
        - point : point quand on fait mourir un champi
        - dwarf le nain

    Return :
            (Vect2D, points) : position et points
    """
    score = 0
    pos = Vect2D(-100, -100)
    for k in range(len(mushroom_list_touch)):
        if Mushroom.mushroom_list[mushroom_list_touch[k]].getLife() == 1:
            mushroom = Mushroom.mushroom_list[mushroom_list_touch[k]]
            correction = 4
            pos = Vect2D(
                mushroom.getPosX() + mushroom.getDimX() / 2,
                mushroom.getPosY() + correction + mushroom.getDimY() / 2,
            )
            score = point

            dwarf.setScore(score)

        Mushroom.mushroom_list[mushroom_list_touch[k]].setLife(-1)
    return (pos, score)


def respawn():
    """
    Remet à tout les champignons avec 4 vie
    """
    max_life = 4
    for k in range(len(Mushroom.mushroom_list)):
        if Mushroom.mushroom_list[k].getLife() != max_life:
            Mushroom.mushroom_list[k].setLife(max_life - Mushroom.mushroom_list[k].getLife())
            Mushroom.mushroom_list[k].resize(
                Mushroom.mushroom_list[k].getDimX(), Mushroom.mushroom_list[k].getDimY()
            )


def killAlll():
    """
    Tue tous les champignons
    """
    Mushroom.mushroom_list = list()


def changeLevel():
    life_max = 4
    for k in range(len(Mushroom.mushroom_list)):
        Mushroom.mushroom_list[k].setLife(life_max - Mushroom.mushroom_list[k].getLife())


def exist(pos):
    """
    Determine si un champignon est deja à une position donné

    Return :
     - boolean
    """
    for k in range(len(Mushroom.mushroom_list)):
        if pos.equals(Vect2D(Mushroom.mushroom_list[k].getPosX(), Mushroom.mushroom_list[k].getPosY())):
            return True
    return False
