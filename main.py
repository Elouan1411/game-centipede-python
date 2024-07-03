# ================================
#
# Auteur : BOITEUX Elouan, BENALI Samia, 2024fff
#
# ================================

import sys

import os

with open(os.devnull, "w") as f:
    # Désactiver stdout
    oldstdout = sys.stdout
    sys.stdout = f
    from pygame.locals import *
    from pygame import *

    # Réactiver stdout
    sys.stdout = oldstdout

import math
import json
from random import randint

# Import de mes modules
from entites import *
from utilities import *


# Initialisation de pygame
pygame.init()

#####################################################
########      DECLARATION FONCTION        ###########
#####################################################


def restart_program():
    python = sys.executable
    os.execl(python, f'"{python}"', *map(lambda arg: f'"{arg}"', sys.argv))


def modify_value_json(fichier, cles, nouvelle_valeur):
    """
    Modifie la valeur d'une clé précise dans un fichier JSON profond.

    Args:
    - fichier (str): Le chemin vers le fichier JSON.
    - cles (list): Liste des clés pour atteindre la valeur à modifier, dans l'ordre.
    - nouvelle_valeur: La nouvelle valeur de la clé.

    Returns:
    - bool: True si la modification a réussi, False sinon.
    """
    try:
        with open(fichier, "r") as f:
            data = json.load(f)

        # Naviguer vers la valeur spécifiée
        temp = data
        for key in cles[:-1]:
            temp = temp[key]

        # Vérifier l'existence de la clé finale et modifier la valeur
        if cles[-1] in temp:
            temp[cles[-1]] = nouvelle_valeur
            with open(fichier, "w") as f:
                json.dump(data, f, indent=4)
            return True
        else:
            return False
    except:
        return False


def toggle_fullscren():
    modify_value_json(
        "settings.json",
        ["window", "FULL_SCREEN", "boolean"],
        not settings["window"]["FULL_SCREEN"]["boolean"],
    )

    restart_program()


def resizeFullScreen(list_full_screen, settings, DIM_SCENE, DIM_SCENE_FULL_SCREEN):
    val_ratio = ratio(DIM_SCENE[0], DIM_SCENE_FULL_SCREEN[0])
    for key, value in settings.items():
        if isinstance(value, dict):
            # Si la valeur est un autre dictionnaire, on appele récursivement la fonction sur ce sous-dictionnaire
            settings[key] = resizeFullScreen(list_full_screen, value, DIM_SCENE, DIM_SCENE_FULL_SCREEN)

        elif key in list_full_screen:
            # Si la clé est "size", multipliez sa valeur par le facteur spécifié
            settings[key] *= val_ratio
    return settings


def updateAttributLevel(list_update, settings, nb):
    for key, value in settings.items():
        if isinstance(value, dict):
            # Si la valeur est un autre dictionnaire, on appele récursivement la fonction sur ce sous-dictionnaire
            settings[key] = updateAttributLevel(list_update, value, nb)

        elif key in list_update:
            settings[key] += nb
    return settings


def draftTouched():
    dwarf.setLife(-1)
    mushroom.respawn()
    spider = creaElement.creaSpider(window, settings, Vect2D, Spider)
    centipede.killAll()  # centipedes
    flea.killAll()
    creaElement.centipede(Centipede, settings, Marble, Vect2D, window)

    # Création de l'animation
    dwarf.setExplosionAnimation(True)
    dwarf.getExplosionAnimation().manageFrame(
        pygame.time.get_ticks(),
        dwarf,
        dwarf.getExplosionAnimation().getFrameTimer(),
        settings["animation"]["explosion"]["OFF_SET"],
    )

    # Replacement du nain au centre
    dwarf.setPos(
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
    )

    try:
        dead_sound.play()
    except:
        pass
    return spider


def init(new_level=None):
    """
    Initialise toute les variables requis pour le jeu
    Args :
        new_level : si new_level = False -> on créer des champignons sinon on change juste leur couleur
    Return :
        retourne toutes les variables utiles à stocker
    """
    clock = pygame.time.Clock()

    previous_time = pygame.time.get_ticks()  # Temps au début de la boucle

    wall_collision = False  # Pour faire un son quand le dwarf tape un mur

    inBreak = False  # Pour mettre pause
    gameOver = False

    # Création du dwarf
    dwarf = creaElement.creaDwarf(Dwarf, settings, Vect2D, Animation, pygame)

    # Création du mille-patte
    creaElement.centipede(Centipede, settings, Marble, Vect2D, window)

    # Création des mushrooms
    if not new_level:
        creaElement.mushroom(
            window, dwarf, Vect2D, Centipede, settings, collisionList, collisionEntite, Mushroom
        )
    else:
        mushroom.changeLevel()

    spider = creaElement.creaSpider(window, settings, Vect2D, Spider)
    return clock, previous_time, wall_collision, inBreak, gameOver, dwarf, spider


def newLevel():
    Entite.level += 1
    # mushroom.killAlll()
    updateAttributLevel(settings["update_level"]["1"], settings, 5)
    updateAttributLevel(settings["update_level"]["2"], settings, 33)

    return init(True)


def backLevel1():
    updateAttributLevel(settings["update_level"]["1"], settings, -5 * (Entite.level - 1))
    updateAttributLevel(settings["update_level"]["2"], settings, -33 * (Entite.level - 1))
    Entite.level = 1
    Dwarf.score = 0
    mushroom.killAlll()
    centipede.killAll()

    return init(False)


#####################################################
########     CHARGEMENT RESSOURCES        ###########
#####################################################
# Charger les constantes depuis le fichier JSON
with open("settings.json", "r") as f:
    settings = json.load(f)
# Charger les fichiers audios
try:
    pygame.mixer.music.load(settings["audios"]["arcade"]["PATH"])
    pygame.mixer.music.set_volume(settings["audios"]["arcade"]["volume"])
    pygame.mixer.music.play(-1)
    wall_sound = pygame.mixer.Sound(settings["audios"]["wall"]["PATH"])
    wall_sound.set_volume(settings["audios"]["wall"]["volume"])
    new_niv_sound = pygame.mixer.Sound(settings["audios"]["niv"]["PATH"])
    new_niv_sound.set_volume(settings["audios"]["niv"]["volume"])
    shot_sound = pygame.mixer.Sound(settings["audios"]["shot"]["PATH"])
    shot_sound.set_volume(settings["audios"]["shot"]["volume"])
    dead_sound = pygame.mixer.Sound(settings["audios"]["dead"]["PATH"])
    dead_sound.set_volume(settings["audios"]["dead"]["volume"])
    game_over_sound = pygame.mixer.Sound(settings["audios"]["game_over"]["PATH"])
    game_over_sound.set_volume(settings["audios"]["game_over"]["volume"])
    sound_play_game_over = False

except pygame.error:
    # Désintaller puis réinstaller pygame
    # pip uninstall pyagme
    # pip install pygame
    ("Impossible de charger la musique. Le jeu continuera sans musique.")


#####################################################
########    DECLARATION CONSTANTES        ###########
#####################################################


RIGHT = 1  # Pour direction
LEFT = -1  # Pour direction
UP = -1  # Pour direction
DOWN = 1  # Pour direction
STOP = 0  # Pour direction


pygame.display.set_icon(pygame.image.load("assets/images/logo.png"))

# Création de la scène de jeu
pygame.display.set_caption("Centipede")
if settings["window"]["FULL_SCREEN"]["boolean"]:
    window = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    settings = resizeFullScreen(
        settings["window"]["FULL_SCREEN"]["LIST"],
        settings,
        tuple(settings["window"]["DIM_SCENE"]),
        window.get_size(),
    )
    settings["window"]["DIM_SCENE"] = tuple(window.get_size())
else:
    window = pygame.display.set_mode(tuple(settings["window"]["DIM_SCENE"]))


# Création d'une font de text
font = pygame.font.SysFont("Arial", int(settings["font"]["general"]["size"]))
arcade_font = pygame.font.Font(
    settings["font"]["score"]["PATH"], int(settings["font"]["score"]["dim"]["medium_d"])
)
arcade_font_mini = pygame.font.Font(
    settings["font"]["score"]["PATH"], int(settings["font"]["score"]["dim"]["small_d"])
)
arcade_font_big = pygame.font.Font(
    settings["font"]["score"]["PATH"], int(settings["font"]["score"]["dim"]["big_d"])
)
game_font = pygame.font.Font(
    settings["font"]["game"]["PATH"], int(settings["font"]["game"]["dim"]["big_d"])
)


# Fond d'écran = la scene de jeu qui occupe toute la fenêtre
scene = pygame.Surface(window.get_size())
scene.fill(tuple(settings["scene"]["background_color"]))


#####################################################
########      DECLARATION VARIABLES       ###########
#####################################################


key_pressed = {
    "UP": False,
    "DOWN": False,
    "LEFT": False,
    "RIGHT": False,
    "Last_x": None,
    "Last_y": None,
}


inGame = False  # Pour lancer le jeu au debut de la partie
restart = False  # Pour relancer le jeu après avoir été mort
next_level = False  # Pour passer au niveau suivant
display_first_level = True
counter_break = 0


list_score_blit = list()

clock, previous_time, wall_collision, inBreak, gameOver, dwarf, spider = init()

# Boucle de jeu (infinie)

while True:
    for event in pygame.event.get():
        # pygame.key.set_repeat(1, VITESSE[1])

        # Clic sur la croix (fenêtre d'exécution) ==> Fermer la fenêtre
        if event.type == QUIT:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
            pygame.quit()
            sys.exit()

        # Touche ESC ==> Fermer la fenêtre
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            try:
                pygame.mixer.music.stop()
            except:
                pass
            pygame.quit()
            sys.exit()

        # Mettre en grand ecran ou non quand appuie sur f
        if event.type == KEYDOWN and event.key == K_f:
            pygame.quit()
            toggle_fullscren()

        if event.type == KEYDOWN and event.key == K_g:
            pygame.quit()
            restart_program()

        # Premier niveau
        if event.type == KEYDOWN and event.key == K_RETURN and display_first_level and inGame:
            display_first_level = False

        # Entré pour changer de niveau
        if event.type == KEYDOWN and event.key == K_RETURN and next_level:
            next_level = False
            clock, previous_time, wall_collision, inBreak, gameOver, dwarf, spider = newLevel()

        if (  # Appuie sur n'importe quel bouton pour lancer le jeu
            (event.type == KEYDOWN and not event.key == K_ESCAPE and not event.key == K_f)
            or (event.type == MOUSEBUTTONDOWN and event.button == 1)
        ) and not inGame:
            inGame = True
            try:
                new_niv_sound.play()
            except:
                pass

        if not gameOver and event.type == MOUSEBUTTONDOWN and event.button == 1:
            if collision.is_point_in_circle(
                pygame.mouse.get_pos(),
                [
                    settings["button"]["pause"]["margin"] + settings["button"]["pause"]["size"] / 2,
                    settings["button"]["pause"]["margin"] + settings["button"]["pause"]["size"] / 2,
                ],
                settings["button"]["pause"]["size"] / 2,
            ):
                inBreak = not inBreak
                counter_break = 0

            elif collision.is_point_in_circle(
                pygame.mouse.get_pos(),
                [
                    2 * settings["button"]["dark"]["margin"]
                    + 3 * settings["button"]["dark"]["size"] / 2,
                    settings["button"]["dark"]["margin"] + settings["button"]["dark"]["size"] / 2,
                ],
                settings["button"]["dark"]["size"] / 2,
            ):
                settings["scene"]["background_color"] = (
                    settings["color"]["white"]
                    if settings["scene"]["background_color"] == settings["color"]["black"]
                    else settings["color"]["black"]
                )

                mushroom.changeStyleAll()

        # Pour relancer la partie
        if gameOver and event.type == KEYDOWN and event.key == K_RETURN:
            restart = True

        if (
            inGame
            and not display_first_level
            and not gameOver
            and not inBreak
            and ((event.type == KEYDOWN and event.key == K_SPACE))
        ):
            try:
                shot_sound.play()
            except:
                pass
            Shot.list_shot.append(
                Shot(
                    Vect2D(
                        dwarf.getPosX() + dwarf.getDimX() / 2 - settings["shot"]["width"] / 2,
                        dwarf.getPosY(),
                    ),
                    Vect2D(settings["shot"]["width"], settings["shot"]["height"]),
                    Vect2D(
                        settings["shot"]["width"],
                        settings["dwarf"]["size"] * (ratio(size("assets/images/dwarf.png"))),
                    ),
                    settings["shot"]["speed"],
                )
            )
            Shot.list_shot[-1].resize(Shot.list_shot[-1].getDimX(), Shot.list_shot[-1].getDimY())

        # Touche tab pour pause
        if event.type == KEYDOWN and event.key == K_TAB and inGame and not gameOver:
            if inBreak:
                inBreak = False
                counter_break = 0

            else:
                copy_key_pressed = key_pressed
                inBreak = True
                for direction in key_pressed:
                    key_pressed[direction] = False

        #####################################################
        ########        TOUCHES DIRECTION         ###########
        #####################################################

        if inGame and not inBreak and not gameOver and not next_level:

            # Fleche RIGHT ==> déplacement du personnage à RIGHT
            if event.type == KEYDOWN and event.key == K_RIGHT:
                key_pressed["RIGHT"] = True
                key_pressed["Last_x"] = RIGHT

            # Fleche LEFT ==> déplacement du personnage à LEFT
            if event.type == KEYDOWN and event.key == K_LEFT:
                key_pressed["LEFT"] = True
                key_pressed["Last_x"] = LEFT

            # Fleche UP ==> déplacement du personnage en UP
            if event.type == KEYDOWN and event.key == K_UP:
                key_pressed["UP"] = True
                key_pressed["Last_y"] = UP

            # Fleche DOWN ==> déplacement du personnage en DOWN
            if event.type == KEYDOWN and event.key == K_DOWN:
                key_pressed["DOWN"] = True
                key_pressed["Last_y"] = DOWN

        # Fleche RIGHT ==> déplacement du personnage à RIGHT
        if event.type == KEYUP and event.key == K_RIGHT:
            key_pressed["RIGHT"] = False

        # Fleche LEFT ==> déplacement du personnage à LEFT
        if event.type == KEYUP and event.key == K_LEFT:
            key_pressed["LEFT"] = False

        # Fleche UP ==> déplacement du personnage en UP
        if event.type == KEYUP and event.key == K_UP:
            key_pressed["UP"] = False

        # Fleche DOWN ==> déplacement du personnage en DOWN
        if event.type == KEYUP and event.key == K_DOWN:
            key_pressed["DOWN"] = False
    ############### FIN RECUP EVENT######################

    # Mesurer le temps écoulé depuis le dernier cadre
    current_time = pygame.time.get_ticks()
    dt = (current_time - previous_time) / 100
    previous_time = current_time

    #####################################################
    ########             AVANCEMENT              ########
    ########                &                    ########
    ########         GESTION COLLISION           ########
    #####################################################

    if inGame and not inBreak and not gameOver and not next_level and not display_first_level:
        dwarf.manageDirection(key_pressed)

        # On fait les calculs seulement si mouvement
        if dwarf.getDirX() != 0 or dwarf.getDirY() != 0:
            # Avancement X
            dwarf.movement(dt * dwarf.getDirX() * dwarf.getSpeed(), 0)
            # Rectification si diagonale
            if dwarf.getDirX() != 0 and dwarf.getDirY() != 0:
                dwarf.movement(
                    -(dt * dwarf.getDirX() * dwarf.getSpeed())
                    + (dt * dwarf.getDirX() * dwarf.getSpeed()) * math.sqrt(2) / 2,
                    0,
                )

            # Gestion des collisions de X
            infoColli = collisionList(Mushroom.mushroom_list, dwarf)
            if infoColli[0]:
                remplacement = firstCollision(dwarf, True, infoColli[1], Mushroom.mushroom_list)

                # Déplacement du cube
                if dwarf.getDirX() != STOP:
                    dwarf.setPos(x=remplacement)

            # Avancement Y
            dwarf.movement(0, dt * dwarf.getDirY() * dwarf.getSpeed())
            # Rectification si diagonale
            if dwarf.getDirX() != 0 and dwarf.getDirY() != 0:
                dwarf.movement(
                    0,
                    -(dt * dwarf.getDirY() * dwarf.getSpeed())
                    + (dt * dwarf.getDirY() * dwarf.getSpeed()) * math.sqrt(2) / 2,
                )

            # Gestion des collisions de Y
            infoColli = collisionList(Mushroom.mushroom_list, dwarf)
            if infoColli[0]:
                remplacement = firstCollision(dwarf, False, infoColli[1], Mushroom.mushroom_list)

                # Déplacement du cube
                if dwarf.getDirY() != STOP:
                    dwarf.setPos(y=remplacement)
        dwarf.checkEdge()
        if (
            dwarf.getPosX() == dwarf.getWidth()[0]
            or dwarf.getPosX() + dwarf.getDimX() == dwarf.getWidth()[1]
            or dwarf.getPosY() == dwarf.getHeight()[0]
            or dwarf.getPosY() + dwarf.getDimY() == dwarf.getHeight()[1]
        ) and not wall_collision:
            try:
                wall_sound.play()
            except:
                pass  # Réinstaller pygame si ca marche pas
            wall_collision = True

        elif not (
            dwarf.getPosX() == dwarf.getWidth()[0]
            or dwarf.getPosX() + dwarf.getDimX() == dwarf.getWidth()[1]
            or dwarf.getPosY() == dwarf.getHeight()[0]
            or dwarf.getPosY() + dwarf.getDimY() == dwarf.getHeight()[1]
        ):
            wall_collision = False

        # Gestion du shot
        shot.update(dt)
        pos_score_in_loop, score_in_loop = mushroom.lifeMinus(
            shot.collisionChampi(Mushroom.mushroom_list), settings["point"]["mushroom"], dwarf
        )  # On enleve des vies aux mushrooms si touché
        if score_in_loop != 0:
            list_score_blit.append([pos_score_in_loop, score_in_loop, 0])

        pos_score_in_loop, score_in_loop = flea.dead(
            shot.collisionFleas(Flea.fleas_list), dwarf, settings["point"]["flea"]
        )
        if pos_score_in_loop != 0:
            list_score_blit.append([pos_score_in_loop, score_in_loop, 0])

        pos_score_in_loop, score_in_loop = centipede.touch(
            shot.collisionMarble(), dwarf, settings["point"]
        )
        if score_in_loop != 0:
            list_score_blit.append([pos_score_in_loop, score_in_loop, 0])

        # Déplacement de l'spider
        spider.update(dt)
        if collisionEntite(spider, dwarf):
            spider = draftTouched()

        # Déplacement du mille-pattes
        centipede.updateCentipede(dt, window)
        for k in range(len(Centipede.list_centipede)):
            if k < len(Centipede.list_centipede) and Centipede.list_centipede[k] is not None:
                if collisionList(Centipede.list_centipede[k].getList(), dwarf)[0]:
                    spider = draftTouched()

        # mort de l'spider
        colli_shot_spider = collisionList(Shot.list_shot, spider)
        if colli_shot_spider[0]:
            pos_score_in_loop, score_in_loop = spider.dead(
                dwarf,
                settings["point"]["spider"]["values"],
                settings["point"]["spider"]["rules_distance"],
            )
            list_score_blit.append([pos_score_in_loop, score_in_loop, 0])
            spider = creaElement.creaSpider(window, settings, Vect2D, Spider)

            del Shot.list_shot[colli_shot_spider[1][0]]

        # ajout et avancement des puces
        if manageFleas(dt, settings["mushroom"]["nbMax"], settings["flea"]["proba_appareance"]):
            creaElement.creaFlea(Flea, settings, Vect2D, window)

        # si collision -> mort de
        colli_fleas_dwarf = collisionList(Flea.fleas_list, dwarf)
        if colli_fleas_dwarf[0]:
            spider = draftTouched()

        # Animation si dwarf touché
        if dwarf.getExplosionAnimation().getAnimationActive():
            dwarf.getExplosionAnimation().manageFrame(
                pygame.time.get_ticks(),
                dwarf,
                dwarf.getExplosionAnimation().getFrameTimer(),
                settings["animation"]["explosion"]["OFF_SET"],
            )

        if dwarf.getLife() <= 0:
            gameOver = True

        elif len(Centipede.list_centipede) == 0:
            next_level = True

        else:
            #####################################################
            ########             RENDU                ###########
            #####################################################

            # Reconstruction de la scène
            blitElement.allElement(
                window,
                scene,
                settings,
                Mushroom,
                Shot,
                Flea,
                arcade_font,
                arcade_font_mini,
                dwarf,
                list_score_blit,
                spider,
                Centipede,
            )

    else:  # Si pause ou pas inGame
        if not inGame:  # Démarrage
            blitElement.welcome(window, settings, game_font, arcade_font_mini)
        elif display_first_level:
            blitElement.nextLevel(window, scene, arcade_font_big, arcade_font_mini, settings, 0)
        elif next_level or display_first_level:
            blitElement.nextLevel(
                window, scene, arcade_font_big, arcade_font_mini, settings, Entite.level
            )
        elif gameOver:
            if not sound_play_game_over:
                game_over_sound.play()
                sound_play_game_over = True
                if dwarf.getScore() > settings["high_score"]:
                    settings["high_score"] = dwarf.getScore()
                    modify_value_json("settings.json", ["high_score"], dwarf.getScore())

            blitElement.gameOver(
                window, scene, arcade_font_big, arcade_font_mini, settings, dwarf.getScore()
            )

            if restart:
                restart = False
                sound_play_game_over = False
                display_first_level = True
                clock, previous_time, wall_collision, inBreak, gameOver, dwarf, spider = backLevel1()

        else:  # Pause
            # Écrire du text sur la surface de la fenêtre
            if counter_break == 0:
                blitElement.rest(window, settings, arcade_font_big, arcade_font_mini)
            counter_break += 1

    # Rachaîchissement de la scène
    # if not inBreak:
    pygame.display.flip()

    # Limiter le taux de rafraîchissement à 60 FPS
    clock.tick(settings["window"]["FPS"])
