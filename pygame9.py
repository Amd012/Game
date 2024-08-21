import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Get screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Game constants
CAR_WIDTH, CAR_HEIGHT = SCREEN_WIDTH // 10, SCREEN_HEIGHT // 6
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = CAR_WIDTH, CAR_HEIGHT
SPEED = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60

# Setup screen, font, and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Car Racing Game')
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Load images
car_img = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
car_img.fill(RED)
obstacle_img = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_img.fill(BLUE)

def draw_car(x, y):
    screen.blit(car_img, (x, y))

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle[0], obstacle[1]))

def draw_score(score):
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def display_game_over(score):
    screen.fill(WHITE)
    game_over_text = font.render(f"You lose! Final Score: {score}", True, (0, 0, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2 - 30))
    screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, SCREEN_HEIGHT / 2 + 30))
    pygame.display.flip()

def handle_input(car_speed):
    # Handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_speed = -SPEED
    elif keys[pygame.K_RIGHT]:
        car_speed = SPEED
    else:
        car_speed = 0

    # Handle touch input (using mouse as a proxy)
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Left mouse button pressed (proxy for touch)
        mouse_x, _ = pygame.mouse.get_pos()
        if mouse_x < SCREEN_WIDTH / 2:
            car_speed = -SPEED
        else:
            car_speed = SPEED
    
    return car_speed

def main():
    while True:
        # Initial car position and speed
        car_x, car_y = SCREEN_WIDTH / 2 - CAR_WIDTH / 2, SCREEN_HEIGHT - CAR_HEIGHT - 20
        car_speed = 0
        
        # List to keep track of obstacles
        obstacles = []
        score = 0
        obstacle_speed = SPEED
        
        # Game loop
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            
            # Handle input
            car_speed = handle_input(car_speed)
            
            # Update car position
            car_x += car_speed
            if car_x < 0:
                car_x = 0
            elif car_x > SCREEN_WIDTH - CAR_WIDTH:
                car_x = SCREEN_WIDTH - CAR_WIDTH
            
            # Update obstacle positions
            for obstacle in obstacles:
                obstacle[1] += obstacle_speed
            
            # Check for collisions
            for obstacle in obstacles:
                if (obstacle[0] < car_x + CAR_WIDTH and
                    obstacle[0] + OBSTACLE_WIDTH > car_x and
                    obstacle[1] < car_y + CAR_HEIGHT and
                    obstacle[1] + OBSTACLE_HEIGHT > car_y):
                    game_over = True
                    display_game_over(score)
                    break
            
            # Remove obstacles that have gone off the screen
            obstacles = [obstacle for obstacle in obstacles if obstacle[1] < SCREEN_HEIGHT]
            
            # Add new obstacles
            if random.random() < 0.02:
                obstacles.append([random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH), -OBSTACLE_HEIGHT])
            
            # Update score
            score += 1
            
            # Draw everything
            screen.fill(WHITE)
            draw_car(car_x, car_y)
            draw_obstacles(obstacles)
            draw_score(score)
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(FPS)
        
        # Wait for player input after game over
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        break
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            # Break out of the waiting loop to restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                break

        # To ensure game loop is restarted correctly
        continue

if __name__ == "__main__":
    main()
