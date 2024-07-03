def manageDirection(key_pressed):
    """
    Gère la direction d'un objet en fonction des touches enfoncées.

    Args:
        - key_pressed (dict): Un dictionnaire contenant les états des touches. Les clés doivent inclure:
            - "LEFT": booléen indiquant si la touche gauche est enfoncée.
            - "RIGHT": booléen indiquant si la touche droite est enfoncée.
            - "UP": booléen indiquant si la touche haut est enfoncée.
            - "DOWN": booléen indiquant si la touche bas est enfoncée.
            - "Last_x": dernière direction x (int).
            - "Last_y": dernière direction y (int).

    Returns:
        - list: Une liste contenant les nouveaux vecteurs de direction [x, y] avec les valeurs:
            - LEFT (-1) ou RIGHT (1) ou STOP (0) pour x.
            - UP (-1) ou DOWN (1) ou STOP (0) pour y.
    """
    vect_dir = [0, 0]

    # Gestion des x
    if key_pressed["LEFT"] and key_pressed["RIGHT"]:
        vect_dir[0] = key_pressed["Last_x"]
    elif key_pressed["LEFT"]:
        vect_dir[0] = LEFT
    elif key_pressed["RIGHT"]:
        vect_dir[0] = RIGHT
    else:
        vect_dir[0] = STOP

    # Gestion des y
    if key_pressed["UP"] and key_pressed["DOWN"]:
        vect_dir[1] = key_pressed["Last_y"]
    elif key_pressed["UP"]:
        vect_dir[1] = UP
    elif key_pressed["DOWN"]:
        vect_dir[1] = DOWN
    else:
        vect_dir[1] = STOP

    return vect_dir


def sign(num):
    """
    Renvoie le signe d'un nombre.

    Args:
        num (float ou int): Le nombre dont le signe est à déterminer.

    Returns:
        int: -1 si le nombre est négatif, 1 si le nombre est positif, 0 si le nombre est nul.
    """
    return -1 if num < 0 else 1 if num > 0 else 0


RIGHT = 1
LEFT = -1
UP = -1
DOWN = 1
STOP = 0
