import pygame
from pygame import mixer
from classes import *

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_pause = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mortal Fighter")

fontArialTitulo = pygame.font.SysFont("Arial", 36)
fontArialTexto = pygame.font.SysFont("Arial", 15)
# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
BLUESCURO = (18, 10, 143)

# define game variables
intro_screen = True
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
round_one_sound = pygame.mixer.Sound('assets/audio/round-one-fight.mp3')
round_one_sound.set_volume(1)

pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
sword_esp = pygame.mixer.Sound("assets/audio/ataqueEspecial1.mp3")
sword_esp.set_volume(3.5)

magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)
magic_esp = pygame.mixer.Sound("assets/audio/ataqueEspecial2.mp3")
magic_esp.set_volume(3.5)

# load background image
bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()

# load buttons
exit_img = pygame.image.load("assets/images/icons/exitbtt.png")
continue_img = pygame.image.load("assets/images/icons/continuebtt.png").convert_alpha()
options_img = pygame.image.load("assets/images/icons/Options.png").convert_alpha()
audio_img = pygame.image.load("assets/images/icons/sombtt.png").convert_alpha()
video_img = pygame.image.load("assets/images/icons/videobtt.png").convert_alpha()
keys_img = pygame.image.load("assets/images/icons/keys.png").convert_alpha()
voltar_img = pygame.image.load('assets/images/icons/voltar.png').convert_alpha()

# instaciando buttons
continue_btt = Button(SCREEN_WIDTH / 2 - 50, 125, continue_img, 1)
options_btt = Button(SCREEN_WIDTH / 2 - 50, 325, options_img, 1)
quit_btt = Button(SCREEN_WIDTH / 2 - 50, 525, exit_img, 1)
audio_btt = Button(SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2, audio_img, 1)
video_btt = Button(SCREEN_WIDTH / 2 + 0, SCREEN_HEIGHT / 2, video_img, 1)
keys_btt = Button(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2, keys_img, 1)
voltar_btt = Button(10, 10, voltar_img, 1)

# load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 445, 34))
    pygame.draw.rect(screen, RED, (x, y, 440, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


def draw_mana_bar(mana, x, y):
    if mana > 100:
        mana = 100
    ratio = mana / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, BLUESCURO, (x, y, 400, 30))
    pygame.draw.rect(screen, BLUE, (x, y, 400 * ratio, 30))


# create two instances of fighters
x_guerreiro = 200
y_guerreiro = 310

x_mago = 700
y_mago = 310

fighter_1 = Fighter(1, x_guerreiro, y_guerreiro, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, x_mago, y_mago, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

moving_sprites = pygame.sprite.Group()

# game loop
run = True
jogo_pausado = False
som_tocou = False
menu_state = 'main'
while run:
    key = pygame.key.get_pressed()
    clock.tick(FPS)
    # check if intro screen is active
    if intro_screen:
        screen.fill((0, 0, 0))
        draw_text("Pressione Enter para Jogar", count_font, WHITE, SCREEN_WIDTH / 6 - 150, SCREEN_HEIGHT / 4)
        pygame.display.update()

        # event handler for intro screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                intro_screen = False
    elif jogo_pausado == True:
        screen.fill((0, 0, 0))
        # checar estado menu
        if menu_state == 'main':
            # exibir botoes do menu principal
            if continue_btt.draw(screen):
                jogo_pausado = False
            if options_btt.draw(screen):
                menu_state = 'options'
            if quit_btt.draw(screen):
                run = False
        # se o estado nao for main
        if menu_state == "options":
            # exibir options
            if video_btt.draw(screen):
                print("video")
            if audio_btt.draw(screen):
                print('audio')
            if keys_btt.draw(screen):
                menu_state = 'keys'
        if menu_state == 'keys':
            if voltar_btt.draw(screen):
                menu_state = 'main'
            draw_text("Jogador 1(Guerreiro)", fontArialTitulo, BLUE, 100, 100)
            draw_text("Jogador 2(Mago)", fontArialTitulo, BLUE, 600, 100)
            draw_text("Ataque:(R)", fontArialTexto, BLUE, 100, 200)
            draw_text("Ataque:(T)", fontArialTexto, BLUE, 100, 250)
            draw_text("Especial:(E)", fontArialTexto, BLUE, 100, 300)
            draw_text("Mover:(W,A,D)", fontArialTexto, BLUE, 100, 350)
            draw_text("Ataque:(1)", fontArialTexto, BLUE, 600, 200)
            draw_text("Ataque:(2)", fontArialTexto, BLUE, 600, 250)
            draw_text("Especial:(3)", fontArialTexto, BLUE, 600, 300)
            draw_text("Mover:(SETA CIMA,SETA ESQ,SETA DIR)", fontArialTexto, BLUE, 600, 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    else:  # Game loop
        if key [pygame.K_SPACE]:
            jogo_pausado = True

        x_guerreiro = fighter_1.rect.x
        y_guerreiro = fighter_2.rect.y

        x_mago = fighter_2.rect.x
        y_mago = fighter_2.rect.y

        if not som_tocou:
            round_one_sound.play()
            som_tocou = True
        # draw background
        draw_bg()
        moving_sprites.draw(screen)
        moving_sprites.update()
        # show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 540, 20)
        draw_mana_bar(fighter_1.mana, 20, 100)
        draw_mana_bar(fighter_2.mana, 580, 100)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 930, 60)
        if fighter_1.mana > 99:
            if key[pygame.K_e]:
                especialGuerreiro = Especialguerreiro(x_mago - 30, y_mago - 300)
                moving_sprites.add(especialGuerreiro)
                especialGuerreiro.animate()
                fighter_2.hit = True
                sword_esp.play()
                fighter_2.health -= 30
                fighter_1.mana = 0
        if fighter_2.mana > 99:
            if key[pygame.K_KP3]:
                especialMago = Especialmago(x_guerreiro + 50, y_guerreiro)
                moving_sprites.add(especialMago)
                especialMago.animate()
                fighter_1.hit = True
                magic_esp.play()
                fighter_1.health -= 35
                fighter_2.mana = 0
        # update countdown
        if intro_count <= 0:
            # move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            # display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            # update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # update fighters
        fighter_1.update()
        fighter_2.update()

        # draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            # display victory image
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    # update display
    pygame.display.flip()

# exit pygame
pygame.quit()
