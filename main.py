import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 15
BASE_BALL_SPEED = 5
MAX_BALL_SPEED = 8

# Center line settings
CENTER_LINE_WIDTH = 2
CENTER_LINE_COLLISION_CHANCE = 0.1  # 10% chance of collision

# Create paddles and ball
player1 = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Function to reset ball with random angle and speed
def reset_ball():
    ball.center = (WIDTH//2, HEIGHT//2)
    angle = random.uniform(-math.pi/4, math.pi/4)
    speed = random.uniform(BASE_BALL_SPEED, MAX_BALL_SPEED)
    return speed * math.cos(angle), speed * math.sin(angle)

# Set initial ball direction and speed
ball_dx, ball_dy = reset_ball()

# Score
score1 = 0
score2 = 0

# Font for score display
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PADDLE_SPEED

    # Move ball
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1
        ball_dy += random.uniform(-0.5, 0.5)

    # Ball collision with paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_dx *= -1
        ball_dx += random.uniform(-1, 1)
        ball_dy += random.uniform(-1, 1)
        speed = math.sqrt(ball_dx**2 + ball_dy**2)
        if speed > MAX_BALL_SPEED:
            ball_dx = (ball_dx / speed) * MAX_BALL_SPEED
            ball_dy = (ball_dy / speed) * MAX_BALL_SPEED

    # Ball collision with center line
    center_line_rect = pygame.Rect(WIDTH//2 - CENTER_LINE_WIDTH//2, 0, CENTER_LINE_WIDTH, HEIGHT)
    if ball.colliderect(center_line_rect) and random.random() < CENTER_LINE_COLLISION_CHANCE:
        ball_dx *= -1
        ball_dx += random.uniform(-1, 1)
        ball_dy += random.uniform(-1, 1)

    # Ball out of bounds
    if ball.left <= 0:
        score2 += 1
        ball_dx, ball_dy = reset_ball()
    elif ball.right >= WIDTH:
        score1 += 1
        ball_dx, ball_dy = reset_ball()

    # Clear the screen
    window.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(window, WHITE, player1)
    pygame.draw.rect(window, WHITE, player2)
    pygame.draw.ellipse(window, WHITE, ball)

    # Draw the center line
    pygame.draw.rect(window, WHITE, center_line_rect)

    # Draw scores
    score1_text = font.render(str(score1), True, WHITE)
    score2_text = font.render(str(score2), True, WHITE)
    window.blit(score1_text, (WIDTH//4, 20))
    window.blit(score2_text, (3*WIDTH//4, 20))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
