import cv2
import mediapipe as mp
import pygame
import random

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
spaceship_image = pygame.transform.scale(spaceship_image, (60, 60))

meteor_image = pygame.image.load("meteor.png").convert_alpha()
meteor_image = pygame.transform.scale(meteor_image, (40, 40))

# Player setup
player_position = [400, 500]

# Meteor setup
meteors = []
spawn_timer = 0

# Game variables
running = True
score = 0
collision_happened = False

def spawn_meteor():
    x_position = random.randint(50, 750)
    meteors.append({"position": [x_position, -50], "speed": random.randint(3, 6)})

def draw_meteor(meteor):
    screen.blit(meteor_image, meteor["position"])

def check_collision(player_pos, meteor_pos):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 60, 60)
    meteor_rect = pygame.Rect(meteor_pos[0], meteor_pos[1], 40, 40)
    return player_rect.colliderect(meteor_rect)

cap = cv2.VideoCapture(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            screen_w, screen_h = screen.get_size()
            player_position[0] = int(wrist.x * screen_w - 30)  # Center the spaceship
            player_position[1] = int(wrist.y * screen_h - 30)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Spawn meteors
    spawn_timer += 1
    if spawn_timer > 30:  # Spawn a meteor every 30 frames
        spawn_meteor()
        spawn_timer = 0

    # Move meteors
    for meteor in meteors:
        meteor["position"][1] += meteor["speed"]

    # Check for collisions
    for meteor in meteors[:]:
        if check_collision(player_position, meteor["position"]):
            collision_happened = True
            running = False  # End the game on collision
        if meteor["position"][1] > 600:  # Remove meteors that go out of screen
            meteors.remove(meteor)
            score += 1

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen with black color
    screen.blit(spaceship_image, player_position)  # Draw spaceship
    for meteor in meteors:
        draw_meteor(meteor)
    pygame.display.flip()

    # Display frame for debugging
    cv2.imshow('Hand Tracking', frame)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

    clock.tick(60)

print(f"Game Over! Your Score: {score}")

cap.release()
hands.close()
cv2.destroyAllWindows()
pygame.quit()
