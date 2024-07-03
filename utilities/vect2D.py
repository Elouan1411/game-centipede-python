from random import random


class Vect2D:
    """
    Représente un vecteur 2D avec des coordonnées x et y.

    Args:
        - x (float): La coordonnée x du vecteur.
        - y (float): La coordonnée y du vecteur.
    """
    def __init__(self, x, y):
        
        self.__x = x
        self.__y = y

    def getVect2D(self):
        """
        Obtient les coordonnées x et y du vecteur.

        Returns:
            - tuple: Un tuple contenant les coordonnées (x, y) du vecteur.
        """
        return (self.__x, self.__y)

    def getVect2DX(self):
        """
        Obtient la coordonnée x du vecteur.

        Returns:
            - float: La coordonnée x du vecteur.
        """
        return self.__x

    def getVect2DY(self):
        """
        Obtient la coordonnée x du vecteur.

        Returns:
            - float: La coordonnée x du vecteur.
        """
        return self.__y

    def equals(self, vect2D):
        """
        Vérifie si deux vecteurs 2D sont égaux en comparant leurs coordonnées.

        Args:
            - vect2D (Vect2D): Le vecteur à comparer.

        Returns:
            - bool: True si les vecteurs sont égaux, False sinon.
        """
        return self.getVect2DX() == vect2D.getVect2DX() and self.getVect2DY() == vect2D.getVect2DY()


def randomVect2D(widthMin, widthMax, heightMin, heightMax):
    """
    Génère un vecteur 2D avec des coordonnées aléatoires dans les limites spécifiées.

    Args:
        - widthMin (float): La valeur minimale pour la coordonnée x.
        - widthMax (float): La valeur maximale pour la coordonnée x.
        - heightMin (float): La valeur minimale pour la coordonnée y.
        - heightMax (float): La valeur maximale pour la coordonnée y.

    Returns:
        - Vect2D: Un objet Vect2D avec des coordonnées aléatoires.
    """
    return Vect2D(
        ((widthMax - widthMin) * random() + widthMin),
        ((heightMax - heightMin) * random() + heightMin),
    )
