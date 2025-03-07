# Importiamo le librerie necessarie
import pygame  # Libreria principale per creare videogiochi
import random  # Per generare numeri casuali
import sys     # Per gestire l'uscita dal gioco
import os      # Per gestire i file musicali
from pygame import mixer  # Per la riproduzione della musica

# Inizializziamo Pygame e il mixer audio
pygame.init()
mixer.init()

# Configurazioni schermo
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colori
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PERGAMENA = (255, 253, 208)  # Colore pergamena per il menu
BORDER_COLOR = (139, 69, 19)  # Marrone per i bordi

# Parametri del gioco - Questi valori influenzano la difficoltà
# Puoi modificarli per rendere il gioco più facile o difficile

# Dimensioni e fisica del bird
CUBE_SIZE = 30          # Dimensione del bird (pixel)
GRAVITY = 0.35          # Forza di gravità (più alto = cade più velocemente)
JUMP_STRENGTH = -8      # Forza del salto (più negativo = salta più in alto)

# Parametri degli ostacoli e movimento
BASE_SPEED = 3          # Velocità iniziale del gioco
GAP_HEIGHT = 180        # Spazio tra i tubi (più alto = più facile)
SPEED_INCREASE = 0.4    # Aumento velocità per punto (ridotto per essere più graduale)
MAX_SPEED = 12          # Velocità massima del gioco

# La velocità degli ostacoli è uguale a BASE_SPEED
OBSTACLE_SPEED = BASE_SPEED

# Animazione del bird
BIRD_ANIMATION_SPEED = 0.15  # Velocità dell'animazione del battito d'ali
bird_frame = 0               # Frame corrente dell'animazione

# Caricamento e preparazione asset
BACKGROUND = pygame.image.load("assets/sprites/background-day.png").convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Menu assets
MESSAGE = pygame.image.load("assets/sprites/message.png").convert_alpha()
MESSAGE = pygame.transform.scale(MESSAGE, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200))
GAMEOVER = pygame.image.load("assets/sprites/gameover.png").convert_alpha()
GAMEOVER = pygame.transform.scale(GAMEOVER, (SCREEN_WIDTH - 200, 100))

# UI Icons
UI_SHEET = pygame.image.load("assets/UI/FREE - Ultimate UI PixelArt Icons/UI ICONS_BLACK_pixel art_Sprite Sheet.png").convert_alpha()

# Dimensioni di ogni icona nel sprite sheet (assumendo che siano 128x128)
ICON_SIZE = 128

# Estrai le icone che ci servono (le coordinate sono basate sulla posizione nello sprite sheet)
def get_icon(x, y):
    icon = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    icon.blit(UI_SHEET, (0, 0), (x * ICON_SIZE, y * ICON_SIZE, ICON_SIZE, ICON_SIZE))
    return pygame.transform.scale(icon, (64, 64))  # Aumentato a 64x64

# Estrai le icone necessarie
PLAY_ICON = get_icon(2, 0)
STOP_ICON = get_icon(8, 1)
MUSIC_ON_ICON = get_icon(4, 0)
MUSIC_OFF_ICON = get_icon(4, 1)

# Variabili per la musica
music_enabled = False
current_song = None

def load_and_play_random_song():
    global current_song
    if not music_enabled:
        if current_song:
            mixer.music.stop()
            current_song = None
        return
    
    music_dir = "music"
    if not os.path.exists(music_dir):
        return
    
    songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.ogg'))]
    if not songs:
        return
    
    if not mixer.music.get_busy() or current_song is None:
        new_song = random.choice(songs)
        if new_song != current_song:
            current_song = new_song
            mixer.music.load(os.path.join(music_dir, current_song))
            mixer.music.play()

def draw_menu_background(screen, rect):
    """Disegna uno sfondo stile pergamena con bordi arrotondati"""
    pygame.draw.rect(screen, PERGAMENA, rect, border_radius=20)
    pygame.draw.rect(screen, BORDER_COLOR, rect, 3, border_radius=20)

BASE = pygame.image.load("assets/sprites/base.png").convert_alpha()
BASE_HEIGHT = 112
BASE = pygame.transform.scale(BASE, (SCREEN_WIDTH, BASE_HEIGHT))

BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_IMGS = [
    pygame.transform.scale(
        pygame.image.load(f"assets/sprites/bluebird-{flap}flap.png").convert_alpha(),
        (BIRD_WIDTH, BIRD_HEIGHT)
    ) for flap in ['up', 'mid', 'down']
]

PIPE_IMG = pygame.image.load("assets/sprites/pipe-green.png").convert_alpha()
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (PIPE_WIDTH, PIPE_HEIGHT))
PIPE_IMG_INV = pygame.transform.flip(PIPE_IMG, False, True)

# Giocatore
cube_size = CUBE_SIZE
cube_x = SCREEN_WIDTH // 4  # Posizionamento proporzionale alla nuova larghezza
cube_y = SCREEN_HEIGHT // 2
cube_velocity = 0

# Ostacoli
obstacles = []
OBSTACLE_WIDTH = 70

# Punteggio
score = 0
font = pygame.font.Font(None, 36)

def draw_bird():
    global bird_frame
    bird_frame += BIRD_ANIMATION_SPEED
    current_bird = BIRD_IMGS[int(bird_frame % 3)]
    screen.blit(current_bird, (cube_x - BIRD_WIDTH//2, cube_y - BIRD_HEIGHT//2))

def create_obstacle():
    """Crea un nuovo ostacolo (coppia di tubi)
    
    Questa funzione:
    1. Sceglie un'altezza casuale per il gap tra i tubi
    2. Crea due tubi: uno sopra e uno sotto
    3. Il terzo valore (False) serve per tracciare se il giocatore ha superato questo ostacolo
    """
    # Calcoliamo limiti più variabili per l'altezza del gap
    min_gap_y = 100  # Minima altezza del gap
    max_gap_y = SCREEN_HEIGHT - 150 - GAP_HEIGHT  # Massima altezza
    
    # Scegliamo una posizione casuale per il gap
    gap_position = random.randint(min_gap_y, max_gap_y)
    
    # Creiamo i rettangoli per i tubi (sopra e sotto)
    # Aggiungiamo un offset casuale per variare la distanza tra le coppie di tubi
    x_offset = random.randint(-50, 50)
    pipe_top = PIPE_IMG_INV.get_rect(midbottom=(SCREEN_WIDTH + x_offset, gap_position))
    pipe_bottom = PIPE_IMG.get_rect(midtop=(SCREEN_WIDTH + x_offset, gap_position + GAP_HEIGHT))
    
    return [pipe_top, pipe_bottom, False]  # False = ostacolo non ancora superato

def move_obstacles():
    """Muove gli ostacoli e aggiorna il punteggio"""
    global obstacles, score, BASE_SPEED, OBSTACLE_SPEED
    for obstacle_pair in obstacles:
        # Muoviamo gli ostacoli alla velocità corrente
        obstacle_pair[0].x -= BASE_SPEED
        obstacle_pair[1].x -= BASE_SPEED
        
        # Se l'ostacolo è stato superato
        if obstacle_pair[0].x + OBSTACLE_WIDTH < cube_x and not obstacle_pair[2]:
            score += 1
            obstacle_pair[2] = True
            
            # Aumentiamo gradualmente la velocità ad ogni punto
            if BASE_SPEED < MAX_SPEED:
                BASE_SPEED += SPEED_INCREASE
                OBSTACLE_SPEED = BASE_SPEED  # Manteniamo sincronizzate le velocità

def check_collisions():
    bird_mask = pygame.mask.from_surface(BIRD_IMGS[0])
    for obstacle_pair in obstacles:
        top_mask = pygame.mask.from_surface(PIPE_IMG)
        bottom_mask = pygame.mask.from_surface(PIPE_IMG)
        
        offset_top = (obstacle_pair[0].x - cube_x, obstacle_pair[0].y - cube_y)
        offset_bottom = (obstacle_pair[1].x - cube_x, obstacle_pair[1].y - cube_y)
        
        if bird_mask.overlap(top_mask, offset_top) or bird_mask.overlap(bottom_mask, offset_bottom):
            return True
    return cube_y < 0 or cube_y + CUBE_SIZE > SCREEN_HEIGHT

def show_menu(is_game_over=False):
    """Mostra il menu iniziale o di game over"""
    global music_enabled
    waiting = True
    
    # Dimensioni e posizione del menu
    menu_width = 300
    menu_height = 400
    menu_x = (SCREEN_WIDTH - menu_width) // 2
    menu_y = (SCREEN_HEIGHT - menu_height) // 2
    menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    
    # Posizione dei bottoni e relative etichette
    button_y_start = menu_y + 180
    button_spacing = 90
    button_size = 64
    
    # Calcoliamo le posizioni per centrare i tre bottoni
    total_buttons_width = 3 * button_size + 2 * 20  # 20 pixels di spazio tra i bottoni
    first_button_x = menu_x + (menu_width - total_buttons_width) // 2
    
    button_rects = {
        'play': pygame.Rect(first_button_x, button_y_start, button_size, button_size),
        'stop': pygame.Rect(first_button_x + button_size + 20, button_y_start, button_size, button_size),
        'music': pygame.Rect(first_button_x + 2 * (button_size + 20), button_y_start, button_size, button_size)
    }
    
    # Creiamo un font più piccolo per le etichette
    label_font = pygame.font.Font(None, 24)
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rects['play'].collidepoint(mouse_pos):
                    return True
                elif button_rects['stop'].collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif button_rects['music'].collidepoint(mouse_pos):
                    music_enabled = not music_enabled
                    load_and_play_random_song()

        # Disegna lo sfondo
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BASE, (0, SCREEN_HEIGHT - BASE_HEIGHT))

        # Disegna il menu con sfondo pergamena
        draw_menu_background(screen, menu_rect)

        # Titolo del menu
        title = font.render('FLAPPY BIRD', True, BLACK)
        title_rect = title.get_rect(center=(menu_x + menu_width//2, menu_y + 50))
        screen.blit(title, title_rect)

        if is_game_over:
            # Testo Game Over
            text = font.render('GAME OVER', True, BLACK)
            text_rect = text.get_rect(center=(menu_x + menu_width//2, menu_y + 120))
            screen.blit(text, text_rect)
            
            score_text = font.render(f'Score: {score}', True, BLACK)
            score_rect = score_text.get_rect(center=(menu_x + menu_width//2, menu_y + 160))
            screen.blit(score_text, score_rect)

        # Disegna i bottoni e le loro etichette
        # Play
        screen.blit(PLAY_ICON, button_rects['play'])
        play_label = label_font.render('Play', True, BLACK)
        play_label_rect = play_label.get_rect(midtop=(button_rects['play'].centerx, button_rects['play'].bottom + 5))
        screen.blit(play_label, play_label_rect)
        
        # Stop
        screen.blit(STOP_ICON, button_rects['stop'])
        stop_label = label_font.render('Exit', True, BLACK)
        stop_label_rect = stop_label.get_rect(midtop=(button_rects['stop'].centerx, button_rects['stop'].bottom + 5))
        screen.blit(stop_label, stop_label_rect)
        
        # Music
        screen.blit(MUSIC_ON_ICON if music_enabled else MUSIC_OFF_ICON, button_rects['music'])
        music_label = label_font.render('Music', True, BLACK)
        music_label_rect = music_label.get_rect(midtop=(button_rects['music'].centerx, button_rects['music'].bottom + 5))
        screen.blit(music_label, music_label_rect)

        pygame.display.update()
        clock.tick(60)
        
        # Gestione musica
        load_and_play_random_song()

def game_over():
    """Gestisce la schermata di Game Over"""
    global BASE_SPEED, OBSTACLE_SPEED
    if show_menu(True):
        # Reset delle velocità quando si riprende il gioco
        BASE_SPEED = 3
        OBSTACLE_SPEED = BASE_SPEED
        return True
    pygame.quit()
    sys.exit()

# Stati di gioco
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2

# Game loop
clock = pygame.time.Clock()
running = True
game_state = STATE_MENU
obstacle_timer = 0
base_x = 0
score = 0  # Aggiunto score globale

# Aumentiamo l'intervallo tra gli ostacoli per il campo più largo
OBSTACLE_INTERVAL = 120  # Era 100 prima

# Mostra il menu iniziale
if not show_menu(False):
    running = False

while running:
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BASE, (base_x, SCREEN_HEIGHT - BASE_HEIGHT))
    screen.blit(BASE, (base_x + SCREEN_WIDTH, SCREEN_HEIGHT - BASE_HEIGHT))
    # Muoviamo il terreno alla stessa velocità degli ostacoli
    base_x = (base_x - BASE_SPEED) % -SCREEN_WIDTH
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cube_velocity = JUMP_STRENGTH
            if event.key == pygame.K_ESCAPE:
                # Pausa il gioco
                if show_menu():
                    continue
                else:
                    pygame.quit()
                    sys.exit()

    # Fisica cubo
    cube_velocity += GRAVITY
    cube_y += cube_velocity
    
    # Generazione ostacoli
    obstacle_timer += 1
    if obstacle_timer > OBSTACLE_INTERVAL:
        obstacles.append(create_obstacle())
        obstacle_timer = 0
    
    # Movimento ostacoli
    move_obstacles()
    
    # Rimozione ostacoli usciti dallo schermo
    obstacles = [pair for pair in obstacles if pair[0].x + OBSTACLE_WIDTH > 0]
    
    # La difficoltà aumenta automaticamente con il punteggio nella funzione move_obstacles
    
    # Disegno elementi
    for obstacle_pair in obstacles:
        screen.blit(PIPE_IMG_INV, obstacle_pair[0])
        screen.blit(PIPE_IMG, obstacle_pair[1])
    draw_bird()
    
    # Punteggio
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Collisioni
    if check_collisions():
        if game_over():
            # Reset gioco
            cube_y = SCREEN_HEIGHT // 2
            cube_velocity = 0
            obstacles = []
            score = 0
            BASE_SPEED = 3  # Resettiamo alla velocità iniziale
            OBSTACLE_SPEED = BASE_SPEED
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
