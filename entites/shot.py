from utilities import collisionList, Vect2D, firstCollision
from .entite import EntiteMouv
from .centipede import Centipede


class Shot(EntiteMouv):
    list_shot = list()  # liste des shots en cours

    def __init__(
        self, pos, max_dim, default_dim, speed
    ):  # max_dim = dim final      /      default_dim = dim du dwarf
        super().__init__(0, 0, pos, default_dim, speed)
        self.__max_dim = max_dim
        self.setImage("assets/images/shot.png")
        self.setDir(STOP, UP)

    def growUp(self, dt):
        """
        Augmente progressivement la taille du shot jusqu'à sa taille maximale.
        Assure que le shot ne dépasse pas la taille initiale du dwarf.

        Args :
            - dt : intervalle de temps d'une boucle pour calculer la distance parcourue par le shot.
        """

        if self.getDimY() < self.getDimYMax():
            self.setDim(
                Vect2D(
                    self.getDimX(),
                    self.getDimY() + dt * self.getSpeed(),
                )
            )
            if self.getDimY() > self.getDimYMax():
                self.setDim(Vect2D(self.getDimX(), self.getDimYMax()))

    def getDimYMax(self):
        return self.__max_dim.getVect2DY()


def update(dt):
    """
    Met à jour tous les missiles
    """
    delete = list()
    for k in range(len(Shot.list_shot)):
        Shot.list_shot[k].growUp(dt)

        if Shot.list_shot[k].getPosY() + Shot.list_shot[k].getDimY() < 0:
            delete.append(k)
        else:
            Shot.list_shot[k].setPos(
                Shot.list_shot[k].getPosX(),
                Shot.list_shot[k].getPosY()
                + Shot.list_shot[k].getDirY() * dt * Shot.list_shot[k].getSpeed(),
            )

    # Suppression des shotes sorties du jeu
    for k in sorted(delete, reverse=True):
        del Shot.list_shot[k]


def collisionChampi(list_mushroom):
    """
    Renvoie une liste d'indice des mushrooms qui ont été touché
    """
    infoColli = [False, list()]  # Pour si il n'y a pas de shot en route
    touch = list()  # liste des mushrooms touché
    delete = list()  # liste des shots qui ont touché un mushroom
    for k in range(len(Shot.list_shot)):
        infoColli = collisionList(list_mushroom, Shot.list_shot[k])

        # Supression du shot si il a touché un mushroom
        if infoColli[0]:
            delete.append(k)

        # Ajout des indices des mushroom dans une liste
        for i in range(len(infoColli[1])):
            touch.append(infoColli[1][i])

    # Suppression des shotes sorties du jeu
    for k in sorted(delete, reverse=True):
        del Shot.list_shot[k]

    return touch


def collisionFleas(fleas_list):
    """
    Renvoie une liste d'indice des puces qui ont été touché
    """
    infoColli = [False, list()]  # Pour si il n'y a pas de shot en route
    touch = list()  # liste des mushrooms touché
    delete = list()  # liste des shots qui ont touché un mushroom
    for k in range(len(Shot.list_shot)):
        infoColli = collisionList(fleas_list, Shot.list_shot[k])

        # Supression du shot si il a touché un mushroom
        if infoColli[0]:
            delete.append(k)

        # Ajout des indices des mushroom dans une liste
        for i in range(len(infoColli[1])):
            touch.append(infoColli[1][i])

    # Suppression des shotes sorties du jeu
    for k in sorted(delete, reverse=True):
        del Shot.list_shot[k]

    return touch


def collisionMarble():
    """
    Return :
        - touch (list) : sous la forme [[numMarble,numCentipede],[numMarble,numCentipede],...]
    """
    infoColli = [False, list()]  # Pour si il n'y a pas de shot en route
    delete = list()  # liste des shots qui ont touché un mushroom
    touch = list()
    for centipede in range(len(Centipede.list_centipede)):
        for shot in range(len(Shot.list_shot)):
            infoColli = collisionList(
                Centipede.list_centipede[centipede].getList(), Shot.list_shot[shot]
            )

            # Supression du shot si il a touché un mushroom
            if infoColli[0]:
                delete.append(shot)

                # Ajout d'une marble (pas plusieurs -> si un shot à touché deux marbles en meme temps)
                touch.append([infoColli[1][0], centipede])

        # Suppression des shotes sorties du jeu
        for k in range(len(delete)):
            try:
                del Shot.list_shot[delete[k]]
            except:
                pass

    return touch


RIGHT = 1  # Pour direction
LEFT = -1  # Pour direction
UP = -1  # Pour direction
DOWN = 1  # Pour direction
STOP = 0  # Pour direction
