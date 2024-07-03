import pygame
from math import sqrt


def ratio(dim, dim_2=None):  # Permet de marcher 1 où plusieurs paramètres
    """
    Calcule le ratio de deux dimensions. Si une seule dimension est fournie, 
    elle est traitée comme un tuple (largeur, hauteur).

    Args:
        - dim: Tuple de deux entiers (int, int) représentant la largeur et la hauteur,
             ou un seul entier représentant la largeur si dim_2 est fourni.
        - dim_2: (Optionnel) Entier (int) représentant la hauteur.

    Returns:
        - float: Le ratio hauteur/largeur
    """
    if dim_2 is None:
        return dim[1] / dim[0]
    else:
        return dim_2 / dim


def size(path_image):
    """
    Obtient les dimensions (largeur, hauteur) d'une image.

    Args:
        - path_image: Chemin du fichier image (str).

    Returns:
        - tuple: Tuple de deux entiers (int, int) représentant la largeur et la hauteur de l'image.
    """
    return pygame.image.load(path_image).get_size()


def resize(image, x, y):
    """
    Redimensionne une image à une nouvelle largeur et hauteur.

    Args:
        - image: Surface Pygame représentant l'image à redimensionner.
        - x: Nouvelle largeur (int).
        - y: Nouvelle hauteur (int).

    Returns:
        - Surface: Nouvelle surface Pygame représentant l'image redimensionnée
    """
    return pygame.transform.scale(image, (x, y))


def load(path_image):
    """
    Charge une image à partir d'un fichier.

    Args:
        - path_image: Chemin du fichier image (str).

    Returns:
        - Surface: Surface Pygame représentant l'image chargée.
    """

    return pygame.image.load(path_image)


def rotate(image, degree):
    """
    Fait pivoter une image d'un certain nombre de degrés.

    Args:
        - image: Surface Pygame représentant l'image à faire pivoter.
        - degree: Angle de rotation en degrés (float ou int).

    Returns:
        - Surface: Nouvelle surface Pygame représentant l'image pivotée.
    """
    return pygame.transform.rotate(image, degree)
