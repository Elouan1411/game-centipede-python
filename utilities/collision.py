from math import sqrt


def collisionList(listEntite, entite):
    """
    Vérifie s'il y a une collision entre une entité et une liste d'entité

    Args:
    - listeEntite (list): une liste d'entités
    - entite(Entite)

    Returns:
    - tuple: Un tuple contenant un booléen indiquant s'il y a une collision et une list d'indices des rectangles noirs en collision, sinon une list vide ou la distance entre les deux si c'est pas une list
    """
    list_collision = list()
    for k in range(len(listEntite)):
        if (
            not (entite.getPosX() > listEntite[k].getPosX() + listEntite[k].getDimX() - 1)
            and not (entite.getPosX() + entite.getDimX() < listEntite[k].getPosX() + 1)
            and not (entite.getPosY() > listEntite[k].getPosY() + listEntite[k].getDimY() - 1)
            and not (entite.getPosY() + entite.getDimY() < listEntite[k].getPosY() + 1)
        ):
            list_collision.append(k)

    if len(list_collision) != 0:
        return (True, list_collision)
    return (False, list())


def firstCollision(entite, XorY, list_collision, list_obstacle):
    """
    Trouve où replacer le rectangle, même si deux collisions sont faites en même temps

    Args:
    - entite : entite qui est en collision qu'on veut remplacer
    - XorY (bool): True si la direction concerne l'axe X, False pour l'axe Y.
    - listCollision (list): Une list d'indices des obstacles en collision.
    - listObstacle (list): Une list de tuples contenant les coordonnées et les dimensions des obstacles.

    Returns:
    - int: Coordonnée d'où replacer le rectangle
    """
    desired_coordinate = list()
    if XorY:  # X
        for k in range(len(list_collision)):
            if entite.getDirX() == RIGHT:
                desired_coordinate.append(list_obstacle[list_collision[k]].getPosX() - entite.getDimX())
            if entite.getDirX() == LEFT:
                desired_coordinate.append(
                    list_obstacle[list_collision[k]].getPosX()
                    + list_obstacle[list_collision[k]].getDimX()
                )

    else:  # Y
        for k in range(len(list_collision)):
            if entite.getDirY() == UP:
                desired_coordinate.append(
                    list_obstacle[list_collision[k]].getPosY()
                    + list_obstacle[list_collision[k]].getDimY()
                )
            if entite.getDirY() == DOWN:
                desired_coordinate.append(list_obstacle[list_collision[k]].getPosY() - entite.getDimY())

    if len(desired_coordinate) == 1:
        return desired_coordinate[0]
    elif len(desired_coordinate) == 0:
        # raise ValueError(
        #     "L'entité donnée ne possède pas la direction requise pour cette demande."
        # )

        # Renvoie la position actuelle de l'entite comme si il n'avait pas eu de collision
        return None
        # return entite.getPosX() if XorY else entite.getPosY()
    else:
        if entite.getDirX() == RIGHT or entite.getDirY() == DOWN:
            return min(desired_coordinate)
        elif entite.getDirX() == LEFT or entite.getDirY() == UP:
            return max(desired_coordinate)


def collisionEntite(entite1, entite2):
    """
        Vérifie si deux entités se chevauchent (collision).

        Args:
            entite1: Une instance d'une classe représentant une entité avec les méthodes suivantes :
                - getPosX(): renvoie la position X de l'entité (int).
                - getPosY(): renvoie la position Y de l'entité (int).
                - getDimX(): renvoie la largeur de l'entité (int).
                - getDimY(): renvoie la hauteur de l'entité (int).
            entite2: Une autre instance d'une classe représentant une entité avec les mêmes méthodes.

        Returns:
            boolean : True si les deux entités se chevauchent, False sinon.
    """
    return (
        not (entite2.getPosX() > entite1.getPosX() + entite1.getDimX() - 1)
        and not (entite2.getPosX() + entite2.getDimX() < entite1.getPosX() + 1)
        and not (entite2.getPosY() > entite1.getPosY() + entite1.getDimY() - 1)
        and not (entite2.getPosY() + entite2.getDimY() < entite1.getPosY() + 1)
    )


# Fonction pour vérifier si un point est dans un cercle
def is_point_in_circle(point, circle_center, radius):
    """
    Vérifie si un point se trouve à l'intérieur d'un cercle.

    Args:
        - point(tuple) : représentant les coordonnées du point (x, y).
        - circle_center(tuple) :  représentant les coordonnées du centre du cercle (x, y).
        - radius(float) : Rayon du cercle

    Returns:
        - boolean: True si le point se trouve à l'intérieur du cercle, False sinon.
    """
    distance = sqrt((point[0] - circle_center[0]) ** 2 + (point[1] - circle_center[1]) ** 2)
    return distance < radius


RIGHT = 1  # Pour direction
LEFT = -1  # Pour direction
UP = -1  # Pour direction
DOWN = 1  # Pour direction
STOP = 0  # Pour direction
