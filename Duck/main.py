
import sys
from tkinter import font
import pygame
import random
import pygame_gui

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW = SCREEN_HEIGHT * SCREEN_WIDTH

TAIL_SIZE = 50
RANGE = (TAIL_SIZE // 2, WINDOW, TAIL_SIZE)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
playerWidht = 50
playerHeight = 50

wormWidht = 30
wormHeight = 30

chickWidht = 50
chickHeight = 50

time = 1

timeStep = 150 #speed of the game
speed = 1
run = True
directionPlayer = "right"
length = 1
playerCoord = (0, 0)
inBorder = False
borderHitted = "left"
previousDirection = "right"
#variabili verme
counterWormEaten = 0 #worm eaten by the player
wormPresence = False
changeWorm = True
score = 0

#differenza tra immagine del giocatore e bordo
gapLeft = -7
gapRight = 7
gapTop = -2
gapBot = 4

#schermo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #creazione finestra di gioco
background = pygame.image.load("Duck\\img\\grassdc.png")  #immagine di sfondo
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#giocatore
player = pygame.Rect([0, 0, TAIL_SIZE - 2, TAIL_SIZE - 2]) #creazione rettangolino giocatore

#immagine giocatore destra
playerImgRight = pygame.image.load("Duck\\img\\duckRight.png")  #immagine del giocatore
playerImgRight = pygame.transform.scale(playerImgRight, (playerWidht, playerHeight))

#immagine giocatore sinistra
playerImgLeft = pygame.image.load("Duck\\img\\duckLeft.png")  
playerImgLeft = pygame.transform.scale(playerImgLeft, (playerWidht, playerHeight))

#immagine giocatore su
playerImgUp = pygame.image.load("Duck\\img\\duckUp.png")  
playerImgUp = pygame.transform.scale(playerImgUp, (playerWidht, playerHeight))

#immagine giocatore giu
playerImgDown = pygame.image.load("Duck\\img\\duckDown.png")  
playerImgDown = pygame.transform.scale(playerImgDown, (playerWidht, playerHeight))

#vermicello
wormImg = pygame.image.load("Duck\\img\\frog.png")  #immagine del verme
wormImg = pygame.transform.scale(wormImg, (wormWidht, wormHeight))

#pulcino
chickImgLeft = pygame.image.load("Duck\\img\\chickLeft.png")  #immagine del pulcino
chickImgLeft = pygame.transform.scale(chickImgLeft, (chickWidht, chickHeight))

chickImgRight = pygame.image.load("Duck\\img\\chickRight.png")  #immagine del pulcino
chickImgRight = pygame.transform.scale(chickImgRight, (chickWidht, chickHeight))

chickImgDown = pygame.image.load("Duck\\img\\chickDown.png")  #immagine del pulcino
chickImgDown = pygame.transform.scale(chickImgDown, (chickWidht, chickHeight))

chickImgUp = pygame.image.load("Duck\\img\\chickUp.png")  #immagine del pulcino
chickImgUp = pygame.transform.scale(chickImgUp, (chickWidht, chickHeight))


trasparentImgPlayer = pygame.Surface((playerWidht, playerHeight), pygame.SRCALPHA) #quadrato trasparente per giocatore
trasparentImgWorm = pygame.Surface((wormWidht, wormHeight), pygame.SRCALPHA) #quadrato trasparente per verme
trasparentImgChick = pygame.Surface((chickWidht, chickHeight), pygame.SRCALPHA) #quadrato trasparente per pulcino

segments = [player.copy()]  # Lista per le posizioni precedenti del giocatore
clock = pygame.time.Clock() #orologio per il gioco
paused = False

# Inizializza il gestore degli elementi GUI
gui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Carica le risorse per la schermata iniziale
#background_image = pygame.image.load("pygame\\img\\grassdc.jpg")  # Sostituisci con il percorso dell'immagine desiderata
#font = pygame.font.Font(None, 36)

# Creazione di un pulsante "Play"
play_button = pygame_gui.elements.UIButton(
    relative_rect = pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)),
    text = 'Play',
    manager = gui_manager
)
score_text = pygame_gui.elements.UILabel(
    relative_rect = pygame.Rect((10, 10, 100, 30)),
    text = f'Score: {score}',
    manager = gui_manager,
    container = None,
)


# Variabile per gestire gli stati del gioco
gameState = "main_menu"
chick_positions = []  # Salva le posizioni dei pulcini
chick_directions = []
def resetVar():
    global gameState, paused, counterWormEaten, wormPresence, changeWorm, score, segments
    gameState = "main_menu"
    paused = False
    counterWormEaten = 0
    wormPresence = False
    changeWorm = True
    score = 0
    segments = [player.copy()]

def drawButton():
    gui_manager.update(0)
    gui_manager.draw_ui(screen)

def getChickImg(direction):
    if direction == "right":
        return chickImgRight
    elif direction == "left":
        return chickImgLeft
    elif direction == "up":
        return chickImgUp
    elif direction == "down":
        return chickImgDown

def increaseSpeed(): #increase speed of the game by eating worms
    global timeStep, counterWormEaten
    if counterWormEaten == 5:
        timeStep -= 10
    if counterWormEaten == 10:
        timeStep -= 10
    if counterWormEaten == 15:
        timeStep -= 10
    if counterWormEaten == 20:
        timeStep -= 10
    if counterWormEaten == 25:
        timeStep -= 10
    if counterWormEaten == 30:
        timeStep -= 10
    if counterWormEaten == 35:
        timeStep -= 10


while run:

    key = pygame.key.get_pressed() #prende il tasto premuto
    timeNow = pygame.time.get_ticks()
    #------------------------------------------eventi-----------------------------------------
    for event in pygame.event.get(): #gestisce gli eventi nel gioco
        if event.type == pygame.QUIT: #evento in cui si chiude la finestra
            run = False
        elif  key[pygame.K_p] == True:
            paused = not paused
        elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                gameState = "playing"
        gui_manager.process_events(event)

    screen.blit(background, (0, 0)) #color the screen

    if gameState == "main_menu":
        # If we are in main menu, draw the button
        drawButton()
        
    elif gameState == "playing":
        if not paused:
            #---------------------------WORM-------------------------------
            if wormPresence == False: #if no worm in map
                if changeWorm == True:
                    wormX = random.randint(0, SCREEN_WIDTH - wormWidht)
                    wormY = random.randint(0, SCREEN_HEIGHT - wormHeight)
                    changeWorm = False
                worm = pygame.Rect((wormX, wormY, wormWidht, wormHeight))
                screen.blit(wormImg, worm.topleft)
            if player.colliderect(worm):
                increaseSpeed() #increase speed
                score += 1 #increase score
                score_text.set_text(f'Score: {score}')
                changeWorm = True 
                counterWormEaten += 1
            
            #-----------------------------CHICK------------------------------
            if counterWormEaten > 0:
                for i in range(min(counterWormEaten, len(segments))):
                    chickPos = segments[-(i + 2)].topleft
                    chickDir = chick_directions[i] if i < len(chick_directions) else previousDirection
                    chick_positions.append(chickPos)
                    chick_directions.append(chickDir)
                    chickImg = getChickImg(chickDir)  # Funzione da implementare per ottenere l'immagine corretta
                    chick = pygame.Rect(chickPos[0], chickPos[1], chickWidht, chickHeight)
                    screen.blit(chickImg, chick.topleft)
                    if player.colliderect(chick):
                        gameState = "lose"

            if timeNow - time > timeStep: #se è passato un certo periodo di tempo
                time = timeNow
                if key[pygame.K_a] or key[pygame.K_LEFT]: #si muove a sinistra se viene premuto A
                    if previousDirection != "right":
                        directionPlayer = "left"
                        previousDirection = "left"
                elif key[pygame.K_d] or key[pygame.K_RIGHT]: #si muove a destra se viene premuto D
                    if previousDirection != "left":
                        directionPlayer = "right"
                        previousDirection = "right"
                elif key[pygame.K_w] or key[pygame.K_UP]: #si muove in su
                    if previousDirection != "down":
                        directionPlayer = "up"
                        previousDirection = "up"
                elif key[pygame.K_s] or key[pygame.K_DOWN]: #si muove in giù 
                    if previousDirection != "up":
                        directionPlayer = "down"
                        previousDirection = "down"

                # Calcola il nuovo movimento del giocatore
                if directionPlayer == "left":
                    playerCoord = (-TAIL_SIZE, 0)
                elif directionPlayer == "right":
                    playerCoord = (TAIL_SIZE, 0)
                elif directionPlayer == "up":
                    playerCoord = (0, -TAIL_SIZE)
                elif directionPlayer == "down":
                    playerCoord = (0, TAIL_SIZE)

                #Muovi il giocatore e gestisci la comparsa dal lato opposto se necessario
                #player.move_ip(playerCoord)
                if player.left < 0:
                    player.x = SCREEN_WIDTH
                elif player.right > SCREEN_WIDTH - 0:
                    player.x = 0 - TAIL_SIZE
                elif player.top < 0:
                    player.y = SCREEN_HEIGHT
                elif player.bottom > SCREEN_HEIGHT - 0:
                    player.y = 0 - TAIL_SIZE

                player.move_ip(playerCoord)
                segments.append(player.copy())
            chick_positions.append(None)  # Aggiungi un valore nullo per indicare la mancanza di un pulcino in questa posizione
            chick_directions.append(directionPlayer)  # Aggiungi la direzione corrente del giocatore

            # Aggiorna la lista delle posizioni e direzioni dei pulcini mantenendo solo le ultime n posizioni/direzioni
            chick_positions = chick_positions[-counterWormEaten:]
            chick_directions = chick_directions[-counterWormEaten:]
            #-----------------------------------------------------------------------------------------
            #disegna posizioni del giocatore
            if directionPlayer == "right":
                screen.blit(playerImgRight, player.topleft)  
            elif directionPlayer == "left":
                screen.blit(playerImgLeft, player.topleft)
            elif directionPlayer == "up":
                screen.blit(playerImgUp, player.topleft)
            elif directionPlayer == "down":
                screen.blit(playerImgDown, player.topleft)
    elif gameState == "lose":
        resetVar()
        drawButton()


    pygame.display.update() #aggiorna la finestra di gioco or pygame.display.flip()

pygame.quit() #chiude programma
sys.exit()
