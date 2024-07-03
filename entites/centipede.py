from utilities.queue import Queue
from utilities.vect2D import Vect2D
from .mushroom import Mushroom, exist


class Centipede:
    list_centipede = list()

    def __init__(self, dimMarble, listMarble=None):
        """
        Agrs :
            - dimMarble : dimension d'une marble pour les cacher de la fenêtre avant qu'elles apparaissent
            - listMarble : liste de bille qui constitue le centipede (optionnel)
        """
        if listMarble is None:
            self.__listMarble = list()
        else:
            self.__listMarble = listMarble

        self.__queue = Queue()

        nb_max_need = 800
        for i in range(1, nb_max_need + 1):
            self.__queue.enqueue(Vect2D(-dimMarble - 1, 0))  # Cacher les marbles avant le démarrage

        # Ajout du centipede à la liste des centipedes
        if listMarble is None:
            Centipede.list_centipede.append(self)

    def update(self, dt, window):
        for k in range(len(self.__listMarble)):
            self.__queue = self.__listMarble[k].update(dt, window, self.__queue, k)

            if k == len(self.__listMarble) - 1:  # Si c'est la derniere marble
                self.__queue.dequeue()  # On supprime le dernier element

    def append(self, marble):
        self.__listMarble.append(marble)

    def getList(self, k=None):
        if k is None:
            return self.__listMarble
        return self.__listMarble[k]

    def becomeHead(self):
        """
        La première marble devient une tête
        """
        self.__listMarble[0].becomeHead()

    def dead(self, k):
        """
        Créer 2 nouveaux centipedes quand une marble au milieu de centipede est mort
        Args :
            - k (int) : numero de la marble du centipede qui meurt
        """
        dead_marble = self.__listMarble[0]
        if k != len(self.getList()) - 1:  # Si il a pas touché la dernière
            # Contient les marbles de k+1 jusqu'à la fin
            new_centipede2 = Centipede(self.getList(0).getDimX(), self.getList()[k + 1 :])
            new_centipede2.becomeHead()
            nb_max_need = 800
            for i in range(1, nb_max_need + 1):
                new_centipede2.__queue.enqueue(
                    Vect2D(
                        -new_centipede2.getList(0).getDimX() - 1,
                        0,
                    )
                )
            Centipede.list_centipede.append(new_centipede2)

        # Contient les marbles de 0 à k-1
        if k != 0:  # Si il a pas touché la première
            new_centipede1 = Centipede(self.getList(0).getDimX(), self.getList()[:k])
            Centipede.list_centipede.append(new_centipede1)

        if len(Mushroom.mushroom_list) > 0:
            # On ne le place pas si y'en a deja un à cette place
            new_pos = Vect2D(
                int(dead_marble.getPosX() / dead_marble.getDimX()) * dead_marble.getDimX(),
                int(dead_marble.getPosY() / dead_marble.getDimY()) * dead_marble.getDimY(),
            )
            if not exist(new_pos):
                new_mushroom = Mushroom(*Mushroom.mushroom_list[0].base_copy())
                new_mushroom.resize(new_mushroom.getDimX(), new_mushroom.getDimY())
                new_mushroom.setPos(
                    int(dead_marble.getPosX() / dead_marble.getDimX()) * dead_marble.getDimX(),
                    int(dead_marble.getPosY() / dead_marble.getDimY()) * dead_marble.getDimY(),
                )


def updateCentipede(dt, window):
    for k in range(len(Centipede.list_centipede)):
        Centipede.list_centipede[k].update(dt, window)


def killAll():
    """
    Tue tout les centipèdes, pour qu'en le dwarf perd une vie
    """
    Centipede.list_centipede = list()


def touch(list_touch, dwarf, point):
    """
    Supprime la marble touché et sépare le centipede en 2 nouveaux centipede
    Args :
        - touch (list) : sous la forme [[numMarble,numCentipede],[numMarble,numCentipede],...]
        - dwarf le nain
        - point : dico des points

    Return:
        (Vect2D, points) : position et points
    """
    score = 0
    for k in range(len(list_touch)):
        if Centipede.list_centipede[list_touch[k][1]].getList(list_touch[k][0]).isHead():
            score = point["marble"]["head"]
        else:
            score = point["marble"]["body"]

        dwarf.setScore(score)

        marble = Centipede.list_centipede[list_touch[k][1]].getList(list_touch[k][0])
        correction = 4
        pos = Vect2D(
            marble.getPosX() + marble.getDimX() / 2, marble.getPosY() + correction + marble.getDimY() / 2
        )

        Centipede.list_centipede[list_touch[k][1]].dead(list_touch[k][0])
        del Centipede.list_centipede[list_touch[k][1]]

    if score != 0:
        return (pos, score)
    # else : si pas de collision
    return (Vect2D(-100, -100), 0)
