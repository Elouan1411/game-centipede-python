from .image import resize, load, size, ratio
from random import randint


def mushroom(window, dwarf, Vect2D, Centipede, settings, collisionList, collisionEntite, Mushroom):
    """
    Crée et positionne des champignons sur la fenêtre de jeu sans qu'ils se chevauchent avec d'autres entités.

    Args:
        - window(Window): Une instance représentant la fenêtre de jeu.
        - dwarf(Dwarf): Une instance représentant le nain.
        - Vect2D(list): Une classe pour représenter un vecteur 2D.
        - Centipede(Centipede): Une classe représentant le centipede.
        - settings: Dictionnaire contenant les paramètres du jeu.
        - collisionList(list): Fonction pour vérifier les collisions avec une liste d'entités.
        - collisionEntite(boolean): Fonction pour vérifier la collision entre deux entités.
        - Mushroom(Mushroom): Classe représentant un champignon.
    """
    # Position start du centipede
    start_centipede = Vect2D(
        Centipede.list_centipede[0].getList(0), Centipede.list_centipede[0].getList(0)
    )
    # Création des mushroomgno   s
    for k in range(settings["mushroom"]["nbMax"]):
        while True:  # do while pour ne pas qu'il se superpose
            mushroom = Mushroom(
                window.get_width(),
                window.get_height(),
                Vect2D(
                    settings["mushroom"]["size"],
                    settings["mushroom"]["size"],
                ),  # Dimmension du mushroom
            )
            mushroom.resize(settings["mushroom"]["size"], settings["mushroom"]["size"])

            if (
                collisionList(Mushroom.mushroom_list[:-1], mushroom)[0]
                or collisionEntite(mushroom, dwarf)
                or (
                    mushroom.getPosX()
                    > start_centipede.getVect2DX().getPosX() - start_centipede.getVect2DX().getDimX()
                    and mushroom.getPosX()
                    < start_centipede.getVect2DX().getPosX() + start_centipede.getVect2DX().getDimX()
                    and mushroom.getPosY() == 0
                )
            ):
                del Mushroom.mushroom_list[-1]
            else:
                break


def creaDwarf(Dwarf, settings, Vect2D, Animation, pygame):
    """
    Crée et initialise le personnage nain dans le jeu.

    Args:
        - Dwarf: Classe représentant le nain.
        - settings: Dictionnaire contenant les paramètres du jeu.
        - Vect2D: Une classe pour représenter un vecteur 2D.
        - Animation: Classe pour gérer les animations.
        - pygame: Module Pygame pour les opérations liées au temps.

    Returns:
        - dwarf(Dwarf)
    """
    # Création du dwarf
    dwarf = Dwarf(
        [
            settings["dwarf"]["width"],
            settings["window"]["DIM_SCENE"][0] - settings["dwarf"]["width"],
        ],  # Largeur de déplacement
        [
            settings["dwarf"]["PERSCENTAGE_HEIGHT"] * settings["window"]["DIM_SCENE"][1],
            settings["window"]["DIM_SCENE"][1] - settings["dwarf"]["height"],
        ],  # Hauteur de déplacement
        Vect2D(
            (settings["window"]["DIM_SCENE"][0] / 2)
            - settings["dwarf"]["size"] / 2,  # Position du dwarf (au centre de sa zone de jeu)
            (
                (
                    settings["dwarf"]["PERSCENTAGE_HEIGHT"] * settings["window"]["DIM_SCENE"][1]
                    + (settings["window"]["DIM_SCENE"][1] - settings["dwarf"]["height"])
                )
                / 2
            )  # Trouver le centre de la zone de jeu du dwarf
            - settings["dwarf"]["size"]
            * (ratio(size("assets/images/dwarf.png")))
            / 2,  # Ajuster pour que le milieu du dwarf soit au milieu (dwarf.dim.y/2)
        ),
        Vect2D(
            settings["dwarf"]["size"],
            settings["dwarf"]["size"] * (ratio(size("assets/images/dwarf.png"))),
        ),  # Dimmension du dwarf
        settings["dwarf"]["speed_dwarf"],  # Vitesse du dwarf
        Animation(
            settings["animation"]["explosion"]["size"],
            "assets/images/animation/explosion",
            ".jpg",
            settings["animation"]["explosion"]["FRAME_RATE"],
            pygame.time.get_ticks(),
        ),
    )
    # Redimensionnement de la souris
    dwarf.resize(dwarf.getDimX(), dwarf.getDimY())
    return dwarf


def creaSpider(window, settings, Vect2D, Spider):
    """
    Crée et initialise une araignée dans le jeu.

    Args:
        - window: Une instance représentant la fenêtre de jeu.
        - settings: Dictionnaire contenant les paramètres du jeu.
        - Vect2D: Une classe pour représenter un vecteur 2D.
        - Spider: Classe représentant une araignée.

    Returns:
        - Instance de Spider initialisée.
    """
    spider = Spider(
        Vect2D(
            settings["spider"]["size"],
            settings["spider"]["size"] * (ratio(size("assets/images/spider/spider1.png"))),
        ),
        settings["spider"]["speed"],
        Vect2D(window.get_width(), window.get_height()),
        settings["spider"]["waiting"],
        settings["spider"]["waiting_hide"],
    )

    spider.resize(spider.getDimX(), spider.getDimY())
    return spider


def creaFlea(Flea, settings, Vect2D, window):
    """
    Crée et initialise une puce dans le jeu.

    Args:
        - Flea: Classe représentant une puce.
        - settings: Dictionnaire contenant les paramètres du jeu.
        - Vect2D: Une classe pour représenter un vecteur 2D.
        - window: Une instance représentant la fenêtre de jeu.

    """
    flea = Flea(
        window.get_width(),
        window.get_height(),
        Vect2D(
            settings["flea"]["size"],
            settings["flea"]["size"],
        ),
        settings["flea"]["speed"],
    )

    flea.resize(flea.getDimX(), flea.getDimY())


def centipede(Centipede, settings, Marble, Vect2D, window):
    """
    Crée et initialise un centipede dans le jeu.

    Args:
        - Centipede: Classe représentant le centipede.
        - settings: Dictionnaire contenant les paramètres du jeu.
        - Marble: Classe représentant une bille du centipede.
        - Vect2D: Une classe pour représenter un vecteur 2D.
        - window: Une instance représentant la fenêtre de jeu.

    Returns:
        -Instance de Centipede initialisée.
    """
    centipede = Centipede(settings["marble"]["size"])
    for k in range(settings["centipede"]["length"]):
        (
            centipede.append(creaMarble(True, None, k, Marble, settings, Vect2D, window))
            if k == 0
            else centipede.append(
                creaMarble(False, centipede.getList(k - 1), k, Marble, settings, Vect2D, window)
            )
        )
    return centipede


def creaMarble(
    isHead, next_marble, nb, Marble, settings, Vect2D, window
):  # width, height, pos, dim, speed, isHead
    """ 
    Crée et initialise une bille pour le centipede dans le jeu.

    Args:
        - isHead: Booléen indiquant si la bille est la tête du centipede.
        - next_marble: La bille suivante dans le centipede.
        - nb: Numéro de la bille dans le centipede.
        - Marble: Classe représentant une bille.
        - settings: Dictionnaire contenant les paramètres du jeu.
        - Vect2D: Une classe pour représenter un vecteur 2D.
        - window: Une instance représentant la fenêtre de jeu.

    Returns:
        - Instance de Marble initialisée.
    """
    marble = Marble(
        settings["marble"]["width"],
        [
            settings["marble"]["PERSCENTAGE_HEIGHT"] * settings["window"]["DIM_SCENE"][1],
            settings["window"]["DIM_SCENE"][1],
        ],
        Vect2D(
            window.get_width() / 2
            - (settings["marble"]["size"] / 2)
            + nb
            * settings["marble"][
                "size"
            ],  # Pour décaller de la taille d'une boule à chaque boule en plus
            0,
        ),
        Vect2D(
            settings["marble"]["size"],
            settings["marble"]["size"],
        ),
        settings["marble"]["speed"],
        isHead,
        next_marble,  # next_marble -> à faire plus tard
    )
    marble.resize(marble.getDimX(), marble.getDimY())

    if marble.isHead():
        marble.setDir(x=(-1) ** randint(1, 2))
    return marble
