from .image import resize, load, size, ratio


def allElement(
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
):
    """
    Dessine tous les éléments du jeu à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - scene (Scene): la scène de jeu
        - settings (dict): les paramètres du jeu
        - Mushroom (Mushroom): objets champignon
        - Shot (Shot): objets tir
        - Flea (Flea): objets puce
        - arcade_font (Font): police principale pour le texte
        - arcade_font_mini (Font): police plus petite pour le texte
        - dwarf (Dwarf): le personnage du joueur
        - list_score_blit (list): liste des affichages de score
        - spider (Spider): objet araignée
        - Centipede (Centipede): objets mille-pattes
    """
    black = settings["scene"]["background_color"] != settings["color"]["black"]

    background(window, scene, settings)
    mushroom(window, Mushroom)
    shot(window, Shot)
    centipede(window, Centipede)
    blitSpider(window, spider)
    animation(window, dwarf)
    blitDwarf(window, dwarf)
    flea(window, Flea)
    score(window, arcade_font, arcade_font_mini, dwarf, settings, list_score_blit, black)
    lives(window, dwarf, settings)
    play_pause_button(window, settings, True)
    dark_button(window, settings)


def background(window, scene, settings):
    """
    Permet de construire (reconstruire) la scène.
    Args:
        - window (Window): la fenêtre de jeu
        - scene (Scene): la scène de jeu
        - settings (dict): les paramètres du jeu
    """
    # Reconstruction de la scène
    scene.fill(tuple(settings["scene"]["background_color"]))
    window.blit(scene, (0, 0))


def mushroom(window, Mushroom):
    """
    Affiche les champignons à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - Mushroom (Mushroom): objets champignon
    """
    for k in range(len(Mushroom.mushroom_list)) :
        window.blit(Mushroom.mushroom_list[k].getImage(), Mushroom.mushroom_list[k].getPos())


def shot(window, Shot):
    """
    Affiche les tirs à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - Shot (Shot): objets tir
    """
    for k in range(len(Shot.list_shot)):
        Shot.list_shot[k].resize(Shot.list_shot[k].getDimX(), Shot.list_shot[k].getDimY())
        window.blit(Shot.list_shot[k].getImage(), Shot.list_shot[k].getPos())


def flea(window, Flea):
    """
    Affiche les puces à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - Flea (Flea): objets puce
    """
    for k in range(len(Flea.fleas_list)):
        window.blit(Flea.fleas_list[k].getImage(), Flea.fleas_list[k].getPos())


def score(window, arcade_font, arcade_font_mini, dwarf, settings, list_score_blit, black):
    """
    Affiche le score à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - arcade_font (Font): police principale pour le texte
        - arcade_font_mini (Font): police plus petite pour le texte
        - dwarf (Dwarf): le personnage du joueur
        - settings (dict): les paramètres du jeu
        - list_score_blit (list): liste des affichages de score
        - black (bool): couleur du texte en noir ou blanc
    """
    color = settings["font"]["score"]["color"]["black"] if black else settings["font"]["score"]["color"]["white"]
    score_text = arcade_font.render(
        f"Score: {str(dwarf.getScore())}", True, color
    )
    text_rect = score_text.get_rect(
        center=(window.get_width() // 2, settings["font"]["score"]["spacing"])
    )
    window.blit(score_text, text_rect)

    delete = list()
    for k in range(len(list_score_blit)):

        # Gestion du temps d'apparition
        list_score_blit[k][2] += 1
        nb_tour_max = 40
        if list_score_blit[k][2] > nb_tour_max:
            delete.append(k)

        # affichage
        score_text = arcade_font_mini.render(
            str(list_score_blit[k][1]), True, color
        )
        text_rect = score_text.get_rect(
            center=(
                list_score_blit[k][0].getVect2DX(),
                list_score_blit[k][0].getVect2DY(),
            )
        )
        window.blit(score_text, text_rect)

    # Suppression des scores qui ont été affiché assez longtemps
    for k in sorted(delete, reverse=True):
        del list_score_blit[k]


def background(window, scene, settings):
    """
    Permet de construire (reconstruire) la scène.
    Args:
        - window (Window): la fenêtre de jeu
        - scene (Scene): la scène de jeu
        - settings (dict): les paramètres du jeu
    """
    # Reconstruction de la scène
    scene.fill(tuple(settings["scene"]["background_color"]))
    window.blit(scene, (0, 0))


def mushroom(window, Mushroom):
    """
    Affiche les champignons à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - Mushroom (Mushroom): objets champignon
    """
    for k in range(len(Mushroom.mushroom_list)):
        window.blit(Mushroom.mushroom_list[k].getImage(), Mushroom.mushroom_list[k].getPos())


def shot(window, Shot):
    """
    Affiche les tirs à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - Shot (Shot): objets tir
    """
    for k in range(len(Shot.list_shot)):
        Shot.list_shot[k].resize(Shot.list_shot[k].getDimX(), Shot.list_shot[k].getDimY())
        window.blit(Shot.list_shot[k].getImage(), Shot.list_shot[k].getPos())


def flea(window, Flea):
    """
    Affiche les puces à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - Flea (Flea): objets puce
    """
    for k in range(len(Flea.fleas_list)):
        window.blit(Flea.fleas_list[k].getImage(), Flea.fleas_list[k].getPos())


def blitSpider(window, spider):
    """
    Affiche l'araignée à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - spider (Spider): objet araignée
    """
    window.blit(spider.getImage(), spider.getPos())


def blitDwarf(window, dwarf):
    """
    Affiche le personnage nain à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - dwarf (Dwarf): le personnage du joueur
    """
    window.blit(dwarf.getImage(), dwarf.getPos())


def lives(window, dwarf, settings):
    """
    Affiche les vies du joueur à l'écran sous forme de cœurs.
    Args:
        - window (Window): la fenêtre de jeu
        - dwarf (Dwarf): le personnage du joueur
        - settings (dict): les paramètres du jeu
    """
    heart_image = resize(
        load(settings["dwarf"]["life"]["image"]),
        settings["dwarf"]["life"]["size"],
        settings["dwarf"]["life"]["size"] * (ratio(size("assets/images/dwarf.png"))),
    )
    margin = settings["dwarf"]["life"]["margin"]  # Marge entre les cœurs et le bord de l'écran

    # Calculez la position x de départ pour les cœurs
    start_x = window.get_width() - 2 * margin - (heart_image.get_width() + margin) * dwarf.getLife()

    # Blit les cœurs à la position calculée
    for i in range(dwarf.getLife()):
        window.blit(heart_image, (start_x + i * (heart_image.get_width() + margin), 2 * margin))


def play_pause_button(window, settings, pause):
    """
    Affiche le bouton de lecture/pause à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - settings (dict): les paramètres du jeu
        - pause (bool): indique si le jeu est en pause ou non
    """
    if pause:
        pause_image = resize(
            load(settings["button"]["pause"]["PATH"]),
            settings["button"]["pause"]["size"],
            settings["button"]["pause"]["size"]
        )
        margin = settings["button"]["pause"]["margin"]  # Marge entre le bouton et le bord de l'écran
    else:
        pause_image = resize(
            load(settings["button"]["play"]["PATH"]),
            settings["button"]["play"]["size"],
            settings["button"]["play"]["size"]
        )
        margin = settings["button"]["play"]["margin"]  # Marge entre le bouton et le bord de l'écran

    window.blit(pause_image, (margin, margin))


def dark_button(window, settings):
    """
    Affiche le bouton de mode sombre à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - settings (dict): les paramètres du jeu
    """
    dark_image = resize(
        load(settings["button"]["dark"]["PATH"]),
        settings["button"]["dark"]["size"],
        settings["button"]["dark"]["size"]
    )
    margin = settings["button"]["dark"]["margin"]  # Marge entre le bouton et le bord de l'écran
    window.blit(dark_image, (2*margin + settings["button"]["dark"]["size"], margin))


def centipede(window, Centipede):
    """
    Affiche les mille-pattes à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - Centipede (Centipede): objets mille-pattes
    """
    for k in range(len(Centipede.list_centipede)):
        for i in range(len(Centipede.list_centipede[k].getList())):
            window.blit(
                Centipede.list_centipede[k].getList(i).getImage(),
                Centipede.list_centipede[k].getList(i).getPos(),
            )


def animation(window, dwarf):
    """
    Affiche l'animation d'explosion du personnage nain à l'écran.
    Args:
        - window (Window): la fenêtre de jeu
        - dwarf (Dwarf): le personnage du joueur
    """
    if dwarf.getExplosionAnimation().getAnimationActive():
        window.blit(
            dwarf.getExplosionAnimation().getAnimationFrames(),
            dwarf.getExplosionAnimation().getPos(),
        )



def welcome(window, settings, game_font, arcade_font_mini):
    """
    Affiche l'écran d'accueil du jeu.
    Args:
        - window (Window): la fenêtre de jeu
        - settings (dict): les paramètres du jeu
        - game_font (Font): police de grande taille pour le titre
        - arcade_font_mini (Font): police de petite taille pour le texte
    """
    welcome_image = resize(
        load(settings["welcome_page"]["image"]["PATH"]),
        settings["welcome_page"]["image"]["width"],
        settings["welcome_page"]["image"]["width"]
        * (ratio(size(settings["welcome_page"]["image"]["PATH"]))),
    )

    window.blit(
        welcome_image,
        (
            (window.get_width() / 2) - settings["welcome_page"]["image"]["width"] / 2,
            (window.get_height() / 2)
            - settings["welcome_page"]["image"]["width"]
            * (ratio(size(settings["welcome_page"]["image"]["PATH"])))
            / 2,
        ),
    )

    # ombre
    text_surface = game_font.render("CENTIPEDE", True, settings["font"]["score"]["color"]["black"])
    text_rect = text_surface.get_rect(
        center=(
            (settings["window"]["DIM_SCENE"][0] // 2) + settings["welcome_page"]["gap"],
            (settings["window"]["DIM_SCENE"][1] // 2) + settings["welcome_page"]["gap"],
        )
    )
    window.blit(text_surface, text_rect)

    text_surface = game_font.render("CENTIPEDE", True, settings["font"]["score"]["color"]["white"])
    text_rect = text_surface.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2),
        )
    )
    window.blit(text_surface, text_rect)

  # affichage phrase
    score_text = arcade_font_mini.render(
        "Appuyer sur entree pour jouer",
        True,
        settings["font"]["score"]["color"]["gray"],
    )
    text_rect = score_text.get_rect(
        center=(
            (settings["window"]["DIM_SCENE"][0] // 2) + settings["welcome_page"]["gap"],
            (settings["window"]["DIM_SCENE"][1] // 2)
            + settings["font"]["game"]["spacing"]
            + settings["welcome_page"]["gap"],
        )
    )
    window.blit(score_text, text_rect)

    score_text = arcade_font_mini.render(
        "Appuyer sur entree pour jouer",
        True,
        settings["font"]["score"]["color"]["white"],
    )
    text_rect = score_text.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2) + settings["font"]["game"]["spacing"],
        )
    )
    window.blit(score_text, text_rect)


def gameOver(window, scene, arcade_font_big, arcade_font_mini, settings, score):
    """
    Affiche l'écran de fin de jeu.
    Args:
        - window (Window): la fenêtre de jeu
        - scene (Surface): la surface de la scène
        - arcade_font_big (Font): police plus grande pour le titre
        - arcade_font_mini (Font): police plus petite pour le texte
        - settings (dict): les paramètres du jeu
        - score (int): le score du joueur
    """
    color = settings["font"]["score"]["color"]["black"] if settings["scene"]["background_color"] != settings["color"]["black"] else settings["font"]["score"]["color"]["white"]
    scene.fill(settings["scene"]["background_color"])
    window.blit(scene, (0, 0))

    text_surface = arcade_font_big.render("GAME OVER", True, color)
    text_rect = text_surface.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2),
        )
    )
    window.blit(text_surface, text_rect)

    # affichage phrase
    score_text = arcade_font_mini.render(
        "Appuyer sur entree pour relancer une partie",
        True,
        color,
    )
    text_rect = score_text.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2) + 70,
        )
    )
    window.blit(score_text, text_rect)

    # affichage phrase
    score_text = arcade_font_mini.render(
        f"Score : {score}",
        True,
        color,
    )
    text_rect = score_text.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2) + settings["font"]["game"]["spacing"] * 2,
        )
    )
    window.blit(score_text, text_rect)
    # affichage phrase
    score_text = arcade_font_mini.render(
        "Meilleur score : "+str(settings["high_score"]),
        True,
        color,
    )
    text_rect = score_text.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2) + (settings["font"]["game"]["spacing"] * 2)+40,
        )
    )
    window.blit(score_text, text_rect)


def nextLevel(window, scene, arcade_font_big, arcade_font_mini, settings, level):
    """
    Affiche l'écran de passage au niveau suivant.
    Args:
        - window (Window): la fenêtre de jeu
        - scene (Surface): la surface de la scène
        - arcade_font_big (Font): police plus grande pour le titre
        - arcade_font_mini (Font): police plus petite pour le texte
        - settings (dict): les paramètres du jeu
        - level (int): le niveau actuel
    """
    color = settings["font"]["score"]["color"]["black"] if settings["scene"]["background_color"] != settings["color"]["black"] else settings["font"]["score"]["color"]["white"]
    scene.fill(settings["scene"]["background_color"])
    window.blit(scene, (0, 0))

    text_surface = arcade_font_big.render(
        f"Niveau {str(level+1)}", True, color
    )
    text_rect = text_surface.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2),
        )
    )
    window.blit(text_surface, text_rect)

    # affichage phrase
    score_text = arcade_font_mini.render(
        "Appuyer sur entree pour passer au niveau suivant",
        True,
        color,
    )
    text_rect = score_text.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2) + 70,
        )
    )
    window.blit(score_text, text_rect)



def rest(window, settings, arcade_font_big, arcade_font_mini):
    """
    Affiche l'écran de pause du jeu.
    Args:
        - window (Window): la fenêtre de jeu
        - settings (dict): les paramètres du jeu
        - arcade_font_big (Font): police plus grande pour le titre
        - arcade_font_mini (Font): police plus petite pour le texte
    """
    # Affichage de la transparence
    transparent = resize(
        load(settings["break"]["PATH"]),
        settings["break"]["width"],
        settings["break"]["width"] * (ratio(size(settings["break"]["PATH"]))),
    )

    window.blit(
        transparent,
        (
            (window.get_width() / 2) - settings["break"]["width"] / 2,
            (window.get_height() / 2)
            - settings["break"]["width"] * (ratio(size(settings["break"]["PATH"]))) / 2,
        ),
    )

    # Affichage du texte
    text_surface = arcade_font_big.render("PAUSE", True, settings["font"]["score"]["color"]["white"])
    text_rect = text_surface.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2),
        )
    )
    window.blit(text_surface, text_rect)

    # affichage phrase
    score_text = arcade_font_mini.render(
        "Appuyer sur tab reprendre la partie",
        True,
        settings["font"]["score"]["color"]["white"],
    )
    text_rect = score_text.get_rect(
        center=(
            settings["window"]["DIM_SCENE"][0] // 2,
            (settings["window"]["DIM_SCENE"][1] // 2) + 70,
        )
    )
    window.blit(score_text, text_rect)
    
    play_pause_button(window, settings, False)

