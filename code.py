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
    size = random.choice([40, 50, 60, 80])  # Random size for variety
    speed = random.randint(4 + difficulty, 8 + difficulty)  # Increased speed
    lateral_speed = random.uniform(-1, 1)  # Random lateral movement
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart game
                    game_active = True
                    meteors = []
                    score = 0
                    difficulty = 0
                    player_position = [400, 500]
                if event.key == pygame.K_ESCAPE:  # Quit game
                    running = False

    if game_active:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                screen_w, screen_h = screen.get_size()
                player_position[0] = int(wrist.x * screen_w - 30)  # Center the spaceship
                player_position[1] = int(wrist.y * screen_h - 30)

                # Calculate angle for rotation
                dx = index_finger.x - wrist.x
                dy = index_finger.y - wrist.y
                player_angle = -math.degrees(math.atan2(dy, dx)) - 90

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Spawn meteors
        spawn_timer += 1
        if spawn_timer > max(10, 30 - difficulty):  # Spawn meteors faster as difficulty increases
            spawn_meteor()
            spawn_timer = 0

        # Move meteors
        for meteor in meteors:
            meteor["position"][1] += meteor["speed"]
            meteor["position"][0] += meteor["lateral_speed"]  # Add lateral movement

        # Check for collisions
        for meteor in meteors[:]:
            if check_collision(player_position, meteor):
                collision_happened = True
                game_active = False  # End the game on collision
            if meteor["position"][1] > 600 or meteor["position"][0] < -100 or meteor["position"][0] > 900:  # Remove meteors out of screen
                meteors.remove(meteor)
                score += 1

        # Increase difficulty over time
        difficulty = score // 10

        # Draw everything
        screen.fill((0, 0, 0))  # Clear screen with black color
        rotated_spaceship = pygame.transform.rotate(spaceship_image, player_angle)  # Rotate spaceship
        spaceship_rect = rotated_spaceship.get_rect(center=(player_position[0] + 40, player_position[1] + 40))
        screen.blit(rotated_spaceship, spaceship_rect.topleft)
        for meteor in meteors:
            draw_meteor(meteor)
        draw_score()  # Draw the score
        pygame.display.flip()

        # Display frame for debugging
        cv2.imshow('Hand Tracking', frame)

        # Exit on ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

        clock.tick(60)
    else:
        game_over()

cap.release()
hands.close()
cv2.destroyAllWindows()
pygame.quit()
