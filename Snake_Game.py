#CDS524 Assignment 1
#Student ID：3160239
#Chen Yujin

import pygame
import random
import time
from pygame.locals import *

# Define color variables
redColour = pygame.Color(255, 0, 0)         # Red
blackColour = pygame.Color(0, 0, 0)         # Black
whiteColour = pygame.Color(255, 255, 255)   # White
greyColour = pygame.Color(150, 150, 150)    # Grey
# game window sides
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240
GRID_SIZE = 20

# Game over function
def gameOver(playSurface, score, snakeSegments):
    gameOverFont = pygame.font.SysFont('arial', 36)  # Smaller font
    gameOverSurf = gameOverFont.render('Game Over', True, greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (160, 10)  # Adjusted to smaller screen center
    playSurface.blit(gameOverSurf, gameOverRect)

    # Display score
    scoreFont = pygame.font.SysFont('arial', 24)
    scoreSurf = scoreFont.render(f'Score: {score}', True, whiteColour)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (160, 50)
    playSurface.blit(scoreSurf, scoreRect)

    # Display snake length
    lengthFont = pygame.font.SysFont('arial', 18)
    lengthSurf = lengthFont.render(f'Snake Length: {len(snakeSegments)}', True, whiteColour)
    lengthRect = lengthSurf.get_rect()
    lengthRect.midtop = (160, 80)
    playSurface.blit(lengthSurf, lengthRect)


    pygame.display.flip()
    time.sleep(1)  # Reduced wait time
    return True

# Q-learning parameters
alpha = 0.1        # Learning rate
gamma = 0.9        # Discount factor
epsilon = 0.5      # Exploration rate
epsilon_decay = 0.995  # Exploration decay
min_epsilon = 0.05     # Minimum exploration rate

# Initialize Q-table
q_table = {}

# Get enhanced state function
def get_enhanced_state(snake_head, raspberry_position, direction, snake_segments):
    # Relative position of food
    head_x, head_y = snake_head
    food_x, food_y = raspberry_position
    delta_x = food_x - head_x
    delta_y = food_y - head_y

    # Direction of movement
    direction_map = {
        'right': 0,
        'left': 1,
        'up': 2,
        'down': 3
    }
    dir_code = direction_map.get(direction, 0)

    # Check for danger in three directions (front, right, left)
    danger_front = False
    danger_right = False
    danger_left = False

    if direction == 'right':
        front = (head_x + 20, head_y)
        right = (head_x, head_y + 20)
        left = (head_x, head_y - 20)
    elif direction == 'left':
        front = (head_x - 20, head_y)
        right = (head_x, head_y - 20)
        left = (head_x, head_y + 20)
    elif direction == 'up':
        front = (head_x, head_y - 20)
        right = (head_x + 20, head_y)
        left = (head_x - 20, head_y)
    elif direction == 'down':
        front = (head_x, head_y + 20)
        right = (head_x - 20, head_y)
        left = (head_x + 20, head_y)

    # Check walls and snake body for danger
    def is_danger(position):
        x, y = position
        if x < 0 or x >= 320 or y < 0 or y >= 240:
            return True
        for segment in snake_segments[1:]:
            if segment[0] == x and segment[1] == y:
                return True
        return False

    danger_front = is_danger(front)
    danger_right = is_danger(right)
    danger_left = is_danger(left)

    # Create state tuple
    state = (
        (delta_x, delta_y),    # Relative position of food
        (danger_front, danger_right, danger_left),  # Danger in three directions
        dir_code             # Current direction
    )
    return state

# Choose action function (ε-greedy strategy)
def choose_action(state):
    global epsilon
    # Explore vs exploit
    if random.uniform(0, 1) < epsilon:
        return random.choice(['right', 'left', 'up', 'down'])  # Explore
    else:
        # Use Q-table to choose best action
        if state in q_table:
            action = max(q_table[state], key=q_table[state].get)
        else:
            # Random action if state not in Q-table
            action = random.choice(['right', 'left', 'up', 'down'])
        return action

# Update Q-table function
def update_q_table(state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = {}
    if action not in q_table[state]:
        q_table[state][action] = 0.0

    # Get current Q-value and next state's maximum Q-value
    current_q = q_table[state][action]
    max_future_q = 0.0
    if next_state in q_table:
        max_future_q = max(q_table[next_state].values(), default=0.0)

    # Update Q-value using Bellman equation
    new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)
    q_table[state][action] = new_q

# Main function
def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    playSurface = pygame.display.set_mode((320, 240))
    pygame.display.set_caption('CDS524 Enhanced Q-Learning Snake')

    # Game variables
    snakePosition = [50, 50]  # Starting position
    snakeSegments = [[50,50], [30,50], [10,50]]  # Initial snake body
    raspberryPosition = [150, 150]  # Initial food position
    raspberrySpawned = 1
    direction = 'right'
    changeDirection = direction
    score = 0
    high_score = 0
    episodes = 1000
    current_episode = 0
    running = True  # Game running flag

    # Game loop
    while current_episode < episodes and running:
        # Reset game variables
        snakePosition = [100,60]
        snakeSegments = [[100,60], [80,60], [60,60]]
        raspberryPosition = [random.randint(0, (WINDOW_WIDTH//GRID_SIZE) - 1) * GRID_SIZE,
                             random.randint(0, (WINDOW_HEIGHT//GRID_SIZE) - 1) * GRID_SIZE]
        raspberrySpawned = 1
        direction = 'right'
        changeDirection = direction
        score = 0
        steps_without_food = 0  # Hunger mechanism
        game_over = False

        # Episode loop
        while not game_over:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False  # Set exit flag

            # Choose action using Q-learning with enhanced state
            state = get_enhanced_state(snakePosition, raspberryPosition, direction, snakeSegments)
            action = choose_action(state)

            # Update snake's direction
            if action == 'right' and direction != 'left':
                changeDirection = 'right'
            if action == 'left' and direction != 'right':
                changeDirection = 'left'
            if action == 'up' and direction != 'down':
                changeDirection = 'up'
            if action == 'down' and direction != 'up':
                changeDirection = 'down'
            direction = changeDirection

            # Move snake head
            if direction == 'right':
                snakePosition[0] += 20
            if direction == 'left':
                snakePosition[0] -= 20
            if direction == 'up':
                snakePosition[1] -= 20
            if direction == 'down':
                snakePosition[1] += 20
            snakePosition[0]=max(0,min(snakePosition[0],WINDOW_WIDTH-GRID_SIZE))
            snakePosition[1]=max(0,min(snakePosition[1],WINDOW_HEIGHT-GRID_SIZE))
            # Grow snake body
            snakeSegments.insert(0, list(snakePosition))

            # Check if snake ate the raspberry
            food_eaten = False
            if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
                raspberrySpawned = 0
                score += 1
                high_score = max(high_score, score)
                food_eaten = True
            else:
                snakeSegments.pop()

            # Spawn new raspberry if eaten
            if raspberrySpawned == 0:
                while True:
                    x = random.randint(0, (WINDOW_WIDTH//GRID_SIZE) - 1)  # Reduced grid size
                    y = random.randint(0, (WINDOW_HEIGHT//GRID_SIZE) - 1)
                    new_raspberry = [x * GRID_SIZE, y * GRID_SIZE]
                    if new_raspberry not in snakeSegments:
                        raspberryPosition = new_raspberry
                        raspberrySpawned = 1
                        break

            # Draw game elements
            playSurface.fill(blackColour)
            for pos in snakeSegments:
                pygame.draw.rect(playSurface, whiteColour, pygame.Rect(pos[0], pos[1], 20, 20))
            pygame.draw.rect(playSurface, redColour, pygame.Rect(raspberryPosition[0], raspberryPosition[1], 20, 20))

            # Display score and snake length
            scoreFont = pygame.font.SysFont('arial', 12)  # Smaller font
            scoreSurf = scoreFont.render(f'Score: {score}', True, whiteColour)
            scoreRect = scoreSurf.get_rect()
            scoreRect.topleft = (5, 5)
            playSurface.blit(scoreSurf, scoreRect)

            lengthFont = pygame.font.SysFont('arial', 12)
            lengthSurf = lengthFont.render(f'Snake Length: {len(snakeSegments)}', True, whiteColour)
            lengthRect = lengthSurf.get_rect()
            lengthRect.topleft = (5, 20)
            playSurface.blit(lengthSurf, lengthRect)

            highScoreFont = pygame.font.SysFont('arial', 12)
            highScoreSurf = highScoreFont.render(f'High Score: {high_score}', True, whiteColour)
            highScoreRect = highScoreSurf.get_rect()
            highScoreRect.topleft = (5, 35)
            playSurface.blit(highScoreSurf, highScoreRect)

            pygame.display.flip()

            # Check for game over conditions
            if snakePosition[0] < 0 or snakePosition[0] >= 320 or snakePosition[1] < 0 or snakePosition[1] >= 240:
                game_over = True
            for segment in snakeSegments[1:]:
                if segment[0] == snakePosition[0] and segment[1] == snakePosition[1]:
                    game_over = True
                    break

            # Calculate reward with proximity to food
            head_x, head_y = snakePosition
            food_x, food_y = raspberryPosition
            distance = ((head_x - food_x) ** 2 + (head_y - food_y) ** 2) ** 0.5
            reward = 0
            if game_over:
                reward = -10
            elif food_eaten:
                reward = 10
                steps_without_food = 0  # Reset hunger counter
            else:
                previous_distance = ((snakeSegments[1][0] - food_x)**2 + (snakeSegments[1][1] - food_y)**2)**0.5
                if distance < previous_distance:
                    reward = 1  # Encourage moving closer to food
                else:
                    reward = -1  # Discourage moving away from food
                steps_without_food += 1
                if steps_without_food > 200:
                    reward = -10  # Hunger penalty
                    game_over = True

            # Get next state and update Q-table
            next_state = get_enhanced_state(snakePosition, raspberryPosition, direction, snakeSegments)
            update_q_table(state, action, reward, next_state)

            # Decay exploration rate
            global epsilon
            epsilon = max(0.05, epsilon * 0.995)

            # Cap FPS
            fpsClock.tick(30)

        # Show game over screen
        gameOver(playSurface, score, snakeSegments)
        current_episode += 1

    # Print Q-table after training
    print("Q Table:")
    for state, actions in q_table.items():
        print(f"State: {state}, Actions: {actions}")

if __name__ == "__main__":
    main()