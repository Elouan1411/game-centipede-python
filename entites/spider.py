from utilities.vect2D import randomVect2D, Vect2D
from .entite import EntiteMouv, Entite
from random import random, randint


class Spider(EntiteMouv):
    def __init__(self, dim, speed, size_window, waiting, waiting_hide):
        super().__init__(
            -dim.getVect2DX(),  # width
            -dim.getVect2DY(),
            randomVect2D(*placement(dim, size_window)),
            dim,
            speed,
        )

        self.__heading = [
            0,
            randint(*waiting_hide),
        ]  # Pour la premiere apparition # Pour rester dans une direction un temps [nbDeTourEnCours, capQuiSiDépasserChangementDeDir]
        self.__size_window = size_window
        self.__hide = True
        self.__waiting = waiting
        self.__waiting_hide = waiting_hide
        self.__side = LEFT if self.getPosX() < self.__size_window.getVect2DX() / 2 else RIGHT
        self.setDir(-self.__side, (-1) ** randint(1, 2))
        self.setImage()

    def setImage(self):
        """
        Créer le chemin d'accès à l'image en fonction du niveau et de sa vie
        Appel ensuite setImage() de sa classe parent pour charger l'image
        """
        limit = 4
        level = limit if not Entite.level % limit else Entite.level % limit  # 0 == False -> True
        path_image = "assets/images/spider/spider" + str(level) + ".png"
        super().setImage(path_image)

    def update(self, dt):
        self.__heading[0] += 1
        if not (self.__hide and self.__heading[0] < self.__heading[1]):

            # Repositionnement vertical
            if (
                self.getPosY() < self.__size_window.getVect2DY() / 2
                or self.getPosY() + self.getDimY() > self.__size_window.getVect2DY()
            ):
                self.setDir(self.getDirX(), -self.getDirY())
                self.setPos(
                    self.getPosX() + self.getDirX() * dt * self.getSpeed(),
                    self.getPosY() + self.getDirY() * dt * self.getSpeed(),
                )

            if self.__hide:
                # On avance pour ne plus être caché
                self.setDir(-self.__side, (-1) ** randint(1, 2))
                self.setPos(
                    self.getPosX() + self.getDirX() * dt * self.getSpeed(),
                    self.getPosY() + self.getDirY() * dt * self.getSpeed(),
                )
                self.__side = LEFT if self.getPosX() < self.__size_window.getVect2DX() / 2 else RIGHT
                self.__hide = False
            else:
                if self.__heading[0] < self.__heading[1]:  # On avance dans la même direction
                    self.setPos(
                        self.getPosX() + self.getDirX() * dt * self.getSpeed(),
                        self.getPosY() + self.getDirY() * dt * self.getSpeed(),
                    )
                else:
                    self.__heading = [
                        0,
                        randint(*self.__waiting),
                    ]  # On remet à 0 le nouveau cap
                    self.setDir(
                        (randint(-self.__side, 0) if -self.__side < 0 else randint(0, -self.__side)),
                        (-1) ** randint(1, 2),
                    )

                if (
                    self.getPosX() + self.getDimX() <= 0
                    or self.getPosX() >= self.__size_window.getVect2DX()
                ):
                    self.__hide = True
                    self.setDir(STOP, STOP)
                    self.__heading = [
                        0,
                        randint(*self.__waiting_hide),
                    ]  # temps de pause avant que ca reparte

    def dead(self, dwarf, point, rules_distance):
        """
        Args :
            - dward : le nain
            - point : dico contenant le nombre de point gagné suivant la distance
            - rules_distance : dico contenant les valeurs des distances

        Return :
            (Vect2D, points) : position et points
        """
        distance = dwarf.getPosY() - self.getPosY() + self.getDimY()
        if distance < rules_distance["small_d"]:
            score = point["small"]
        elif distance > rules_distance["long_d"]:
            score = point["long"]
        else:
            score = point["medium"]
        dwarf.setScore(score)

        return (Vect2D(self.getPosX() + self.getDimX(), self.getPosY() + self.getDimY()), score)


def placement(dim, size_window):
    """
    fonction qui donne un espace (à gauche ou à droite) en dehors de l'écran où l'araignée va se placer
    renvoie un tuple avec les bons paramètres pour la fonction randomVect2D() du fichier vect2D.py
    """
    if random() < 0.5:
        return (
            -dim.getVect2DX(),
            -dim.getVect2DX(),
            size_window.getVect2DY() / 2,
            size_window.getVect2DY() - dim.getVect2DY(),
        )  # araignée à gauche de l'écran
    # else
    return (
        size_window.getVect2DX(),
        size_window.getVect2DX(),
        size_window.getVect2DY() / 2,
        size_window.getVect2DY() - dim.getVect2DY(),
    )  # araignée à droite de l'écran


LEFT = -1
RIGHT = 1
STOP = 0
