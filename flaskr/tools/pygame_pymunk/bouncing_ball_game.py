import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Ball')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball settings
ball_pos = [width // 2, height - 20]  # Start on the ground
ball_radius = 20
ball_speed = [0, 0]
gravity = 0.5
bounce = -0.7
floor = height - ball_radius
ball_bouncing = False

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the ball is clicked
            if (ball_pos[0] - ball_radius < event.pos[0] < ball_pos[0] + ball_radius) and \
               (ball_pos[1] - ball_radius < event.pos[1] < ball_pos[1] + ball_radius):
                angle = random.uniform(-1, 1)  # Random angle for the jump
                ball_speed = [angle * 20, -20]  # Initial speed for the bounce
                ball_bouncing = True

    # Ball physics
    if ball_bouncing:
        ball_speed[1] += gravity
        ball_pos[0] += int(ball_speed[0])
        ball_pos[1] += int(ball_speed[1])
        # Bounce off the floor
        if ball_pos[1] >= floor:
            ball_pos[1] = floor
            ball_speed[1] *= bounce
        # Bounce off the ceiling
        if ball_pos[1] <= ball_radius:
            ball_pos[1] = ball_radius
            ball_speed[1] *= bounce
        # Bounce off the walls
        if ball_pos[0] <= ball_radius:
            ball_pos[0] = ball_radius
            ball_speed[0] *= -1
        if ball_pos[0] >= width - ball_radius:
            ball_pos[0] = width - ball_radius
            ball_speed[0] *= -1

    # Stop the ball if it's moving very slowly
    if ball_bouncing and abs(ball_speed[1]) < 0.5 and ball_pos[1] == floor:
        ball_speed = [0, 0]
        ball_bouncing = False

    # Draw the ball
    pygame.draw.circle(screen, RED, ball_pos, ball_radius)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
sys.exit()
