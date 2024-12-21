# Modificación: Nave puede rotar y meteoritos son más difíciles de esquivar
import cv2
import mediapipe as mp
import pygame
import random
import math

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Game")
clock = pygame.time.Clock()

# Load images
spaceship_image = pygame.image.load("spaceship.png").convert_alpha()
spaceship_image = pygame.transform.scale(spaceship_image, (80, 80))

meteor_image = pygame.image.load("meteor.png").convert_alpha()

# Font for score and game over
default_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Player setup
player_position = [400, 500]
player_angle = 0  # New: Angle for rotation

# Meteor setup
meteors = []
spawn_timer = 0

def spawn_meteor():
    x_position = random.randint(50, 750)
    size = random.choice([40, 50, 60, 80, 100, 120])  # Random size for variety
    speed = random.randint(base_speed, base_speed + 3)  # Increased speed
    lateral_speed = random.uniform(-1 - difficulty * 0.1, 1 + difficulty * 0.1)   # Random lateral movement
    meteor = pygame.transform.scale(meteor_image, (size, size))
    meteors.append({"position": [x_position, -size], "speed": speed, "lateral_speed": lateral_speed, "image": meteor, "size": size})

def draw_meteor(meteor):
    screen.blit(meteor["image"], meteor["position"])

def check_collision(player_pos, meteor):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 60, 60)
    meteor_rect = pygame.Rect(meteor["position"][0], meteor["position"][1], meteor["size"], meteor["size"])
    return player_rect.colliderect(meteor_rect)

cap = cv2.VideoCapture(0)

# Game variables
running = True
game_active = True
score = 0
collision_happened = False
difficulty = 0

def draw_score():
    score_text = default_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def game_over():
    screen.fill((0, 0, 0))
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    score_text = default_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(game_over_text, (250, 200))
    screen.blit(score_text, (350, 300))
    restart_text = default_font.render("Press ENTER to restart or ESC to quit", True, (255, 255, 255))
    screen.blit(restart_text, (150, 400))
    pygame.display.flip()

# Agregar al principio del código
game_active = False  # Inicia en el menú principal
menu_active = True  # Variable para controlar el estado del menú

def main_menu():
    screen.fill((0, 0, 0))  # Limpiar la pantalla con color negro
    title_text = game_over_font.render("SPACE GAME", True, (0, 0, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 200)) 
    instruction_text = default_font.render("Press ENTER to start", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(screen.get_width() // 2, 300))
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)
    pygame.display.flip()

# Modificar el bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if menu_active:  # Lógica del menú principal
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar ENTER para comenzar
                    menu_active = False
                    game_active = True
        elif not game_active:  # Lógica de Game Over
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Reiniciar juego
                    game_active = True
                    meteors = []
                    score = 0
                    difficulty = 0
                    player_position = [400, 500]
                if event.key == pygame.K_ESCAPE:  # Salir del juego
                    running = False

    if menu_active:
        main_menu()
    elif game_active:
        # Lógica del juego (sin cambios, ya estaba implementada)
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar con MediaPipe Hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                screen_w, screen_h = screen.get_size()
                player_position[0] = int(wrist.x * screen_w - 30)  # Centrar la nave
                player_position[1] = int(wrist.y * screen_h - 30)

                # Calcular el ángulo para la rotación
                dx = index_finger.x - wrist.x
                dy = index_finger.y - wrist.y
                player_angle = -math.degrees(math.atan2(dy, dx)) - 90

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        max_spawn_rate = max(10, 30 - difficulty)
        spawn_timer += 1
        if spawn_timer > max_spawn_rate:
            spawn_meteor()
            spawn_timer = 0

        for meteor in meteors:
            meteor["position"][1] += meteor["speed"]
            meteor["position"][0] += meteor["lateral_speed"]

        for meteor in meteors[:]:
            if check_collision(player_position, meteor):
                collision_happened = True
                game_active = False
            if meteor["position"][1] > 600 or meteor["position"][0] < -100 or meteor["position"][0] > 900:
                meteors.remove(meteor)
                score += 1

        difficulty = score // 10
        base_speed = 4 + difficulty

        screen.fill((0, 0, 0))
        rotated_spaceship = pygame.transform.rotate(spaceship_image, player_angle)
        spaceship_rect = rotated_spaceship.get_rect(center=(player_position[0] + 40, player_position[1] + 40))
        screen.blit(rotated_spaceship, spaceship_rect.topleft)
        for meteor in meteors:
            draw_meteor(meteor)
        draw_score()
        pygame.display.flip()

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        clock.tick(60)
    else:
        game_over()

cap.release()
hands.close()
cv2.destroyAllWindows()
pygame.quit()
