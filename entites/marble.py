from utilities.vect2D import Vect2D
from .entite import EntiteMouv, Entite
from .mushroom import Mushroom
from random import randint
from utilities.collision import *
from utilities.manageDirection import sign


class Marble(EntiteMouv):
    def __init__(self, width, height, pos, dim, speed, isHead, next_marble):
        super().__init__(width, height, pos, dim, speed, Vect2D((-1) ** randint(1, 2), 0))
        self.__isHead = isHead
        self.setImage(isHead)
        self.__next_marble = next_marble

        self.__pos_y_before_rotate = self.getPosY()
        self.__dir_x_before_rotate = self.getDirX()

        self.__heading = DOWN  # cap de la marble si elle monte ou descend

    def setImage(self, isHead=None):
        if isHead is None:
            isHead = self.__isHead

        limit = 4
        level = limit if not Entite.level % limit else Entite.level % limit
        path_image = (
            "assets/images/centipede/head" + str(level) + ".png"
            if isHead
            else "assets/images/centipede/marble" + str(level) + ".png"
        )
        super().setImage(path_image)

    def updateDir(self):
        """Met à jour la direction de la marble en fonction de sa position et de la marble devant elle

        Return : void
        """
        self.setDir(
            sign(self.__next_marble.getPosX() - self.getPosX()),
            sign(self.__next_marble.getPosY() - self.getPosY()),
        )

    def updatePos(self, dt, queue, k):
        """
        Met à jour la position d'une marble (tête ou corps)
        Args :
            - average_dt : intervalle de temps d'un tour de boucle de jeu
            - queue : file des positions
            - k : numero de la marble

        Return :
            - queue : file des positions
        """

        if self.__isHead:
            self.setPos(
                self.getPosX() + self.getDirX() * average_dt * self.getSpeed(),
                self.getPosY() + self.getDirY() * average_dt * self.getSpeed(),
            )
            queue.enqueue(Vect2D(*self.getPos()))
        else:
            coef = int(abs(self.getDimX() / (self.getSpeed() * average_dt)))
            # coef = int(abs(self.getDimX() / (self.getSpeed() * dt)))
            self.setPos(*queue.get_item(k * coef).getVect2D())

    def update(self, dt, window, queue, k):
        """
        Méthode principal de déplacement de chaque marble (utilise les méthodes : updatePos et updateDir)
        Elle gère les collisions avec les mushrooms et se déplace en fonction

        Args :
            - average_dt : intervalle de temps d'un tour de boucle du jeu
            - window : fenetre du jeu pour avoir les dimmensions de window
            - queue : file de toutes les positions
            - k : numero de la marble

        return : queue (file des positions)
        """
        if self.__isHead:
            # Sauvegarde de la direction
            dir_before = Vect2D(self.getDirX(), self.getDirY())

            # Gestion du heading
            if self.getPosY() + self.getDimY() > self.getHeight()[1]:
                # Si elle sort par le bas
                self.setHeading(UP)
                self.setDir(self.getDirX(), self.getHeading())
            if self.getPosY() < self.getHeight()[0] and self.getHeading() == UP:
                self.setHeading(DOWN)
                self.setDir(self.getDirX(), self.getHeading())

            # check collision
            mushroom_millipede_collision = collisionList(Mushroom.mushroom_list, self)
            if mushroom_millipede_collision[0]:
                # remplacement pour ne plus etre en collision
                remplacement = firstCollision(
                    self, True, mushroom_millipede_collision[1], Mushroom.mushroom_list
                )
                if remplacement is not None:
                    self.setPos(x=remplacement)

                    # rotation
                    self.setDir(STOP, self.getHeading())
                elif (
                    remplacement is None
                    and self.getDirY() == self.getHeading()
                    and self.getPosY() < self.getPosYBefore() + self.getDimY()
                ):
                    # Si il tape un mushroom par le bas
                    Mushroom.mushroom_list[mushroom_millipede_collision[1][0]].setLife(-1)

            # Collision avec les bords
            elif self.getPosX() + self.getDimX() >= window.get_width() - self.getWidth():

                self.setPos(x=window.get_width() - self.getWidth() - self.getDimX() - 1)
                self.setDir(STOP, self.getHeading())

            elif self.getPosX() < 0 + self.getWidth():
                self.setPos(x=0 + self.getWidth() + 1)
                self.setDir(STOP, self.getHeading())

            if self.getDirY() == DOWN:
                if self.getPosY() > self.getPosYBefore() + self.getDimY():
                    # replacement exact pour bien être sur les cases de la grille (imaginaire)
                    self.setPos(y=self.getPosYBefore() + self.getDimY())
                    self.setDir((-1) * self.getDirXBefore(), STOP)

                    # mise à jour de before
                    self.updateBefore()

            elif self.getDirY() == UP:
                if self.getPosY() < self.getPosYBefore() - self.getDimY():
                    # replacement exact pour bien être sur les cases de la grille (imaginaire)
                    self.setPos(y=self.getPosYBefore() - self.getDimY())
                    self.setDir((-1) * self.getDirXBefore(), STOP)

                    # mise à jour de before
                    self.updateBefore()

            self.manageRotate(dir_before)

        self.updatePos(dt, queue, k)  # Il avance

        return queue

    def manageRotate(self, dir_before):
        # Vérifier si la direction a changé
        if dir_before.getVect2DX() == self.getDirX() and dir_before.getVect2DY() == self.getDirY():
            # Si la direction n'a pas changé, ne faites rien et retournez
            return

        # Calculer le produit vectoriel des directions avant et après le déplacement
        cross_product = (
            dir_before.getVect2DX() * self.getDirY() - dir_before.getVect2DY() * self.getDirX()
        )

        # Si le produit vectoriel est positif, la marble a tourné dans le sens horaire
        if cross_product > 0:
            self.rotate(-90)
        # Si le produit vectoriel est négatif, la marble a tourné dans le sens anti-horaire
        elif cross_product < 0:
            self.rotate(90)

    def isHead(self):
        return self.__isHead

    def becomeHead(self):
        self.__isHead = True
        self.__next_marble = None
        self.setImage(self.__isHead)
        self.resize(self.getDimX(), self.getDimY())
        self.updateBefore()

    def rotate(self, degree):
        super().rotateImage(degree)

    def getPosYBefore(self):
        return self.__pos_y_before_rotate

    def setPosYBefore(self):
        self.__pos_y_before_rotate = self.getPosY()

    def getDirXBefore(self):
        return self.__dir_x_before_rotate

    def setDirXBefore(self):
        self.__dir_x_before_rotate = self.getDirX()

    def updateBefore(self):
        self.setPosYBefore()
        self.setDirXBefore()

    def setHeading(self, heading):
        self.__heading = heading

    def getHeading(self):
        return self.__heading


RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1
STOP = 0
average_dt = 0.16
