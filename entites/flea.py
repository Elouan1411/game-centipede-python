from .entite import EntiteMouv, Entite
from utilities.vect2D import Vect2D
from random import randint, random
from .mushroom import Mushroom, exist
from math import ceil


class Flea(EntiteMouv):
    fleas_list = list()

    def __init__(self, width, height, dim, speed):
        super().__init__(width, height, place(width, dim), dim, speed, Vect2D(0, 1))

        limit = 4
        level = limit if not Entite.level % limit else Entite.level % limit
        self.setImage("assets/images/flea/flea" + str(level) + ".png")
        self.__quantity_mushroom_max = randint(1, 2)
        self.__quantity_mushroom_now = 0

        Flea.fleas_list.append(self)

    def update(self, dt):
        """
        Met à jour la position de la puce et place les champignons si besoin

        Args :
            - dt : intervalle de temps d'un tour de boucle
        """
        self.setPos(
            self.getPosX() + self.getDirX() * dt * self.getSpeed(),
            self.getPosY() + self.getDirY() * dt * self.getSpeed(),
        )

        # On place un champignon
        nb_loop = ceil(self.getHeight() / (dt * self.getSpeed()))
        if (
            self.__quantity_mushroom_now < self.__quantity_mushroom_max
            and random() < self.__quantity_mushroom_max / nb_loop
        ):
            if len(Mushroom.mushroom_list) > 0:
                # On ne le place pas si y'en a deja un à cette place
                new_pos = Vect2D(
                    int(self.getPosX() / self.getDimX()) * self.getDimX(),
                    int(self.getPosY() / self.getDimY()) * self.getDimY(),
                )
                if not exist(new_pos):
                    new_mushroom = Mushroom(*Mushroom.mushroom_list[0].base_copy())
                    new_mushroom.resize(new_mushroom.getDimX(), new_mushroom.getDimY())
                    new_mushroom.setPos(
                        int(self.getPosX() / self.getDimX()) * self.getDimX(),
                        int(self.getPosY() / self.getDimY()) * self.getDimY(),
                    )


def update(dt):
    """
    Met à jour chaque puce en utilisant la méthode update de sa classe
    """
    delete = list()
    for k in range(len(Flea.fleas_list)):
        Flea.fleas_list[k].update(dt)

        # Supression de la liste si il n'est plus sur l'écran
        if Flea.fleas_list[k].getPosY() > Flea.fleas_list[k].getHeight():
            delete.append(k)

    # Suppression des shotes sorties du jeu
    for k in sorted(delete, reverse=True):
        del Flea.fleas_list[k]


def place(width, dim):
    """
    Place la puce dans sa bonne zone

    Args :
        - width (int) : largeur (zone)
        - height (int) : hauteur (zone)
        - dim (int) : dimension de la puce

    Return :
        - Vect2D : position aléatoire respectant les consignes
    """
    maxX = int(width / dim.getVect2DX() - 1)
    return Vect2D(randint(0, maxX) * dim.getVect2DX(), -dim.getVect2DY() - 1)


def manageFleas(dt, nb_max_mushroom, proba_appareance):
    """
    Gère l'avancer des puces, ainsi que leur création et leur suppresion

    Return :
        - Booleen : Ajouter une puce ou non
    """
    update(dt)
    if random() < proba_appareance / 3000 and len(Mushroom.mushroom_list) <= nb_max_mushroom:
        return True


def killAll():
    """
    Tue toutes les puces
    """
    Flea.fleas_list = list()


def dead(list_touch, dwarf, point):
    """
    Args :
        - list_mushroom : liste des champignons qui ont été touché
    """
    score = 0
    pos = Vect2D(-100, -100)
    # Suppression des shotes sorties du jeu
    for k in sorted(list_touch, reverse=True):
        dwarf.setScore(point)
        score = point
        flea = Flea.fleas_list[k]
        correction = 4
        pos = Vect2D(
            flea.getPosX() + flea.getDimX() / 2, flea.getPosY() + correction + flea.getDimY() / 2
        )
        del Flea.fleas_list[k]
    return (pos, score)


RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1
STOP = 0
