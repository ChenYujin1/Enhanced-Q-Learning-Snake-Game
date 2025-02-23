# Enhanced Q-Learning Snake Game

## Project Background
This project aims to develop an enhanced version of the classic Snake game using Q-learning, a reinforcement learning algorithm. The goal is to train an agent (the snake) to maximize its score by consuming food while avoiding collisions with the game boundaries and its own body.

## Project Purpose
The purpose of this project is to demonstrate the application of Q-learning in a game environment and to explore how reinforcement learning can be used to optimize the snake's behavior.

## Technologies Used
- Python: The primary programming language used for the project.
- Pygame: A set of Python modules designed for writing video games.
- Q-Learning: A reinforcement learning algorithm used to train the snake.

## How to run the game
All you need to do is place the code in the python interpreter already configured in your computer and click run, the machine will automatically learn and complete the game with the number of rounds you can decide for yourself!

## How to read the result
You will see a Q-table in the result
State parsing:
- (delta_x, delta_y): the position of the food relative to the snake's head (delta_x = food_x - head_x, delta_y = food_y - head_y).
- (danger_front, danger_right, danger_left): whether there is danger in front, right and left of the snake's head (True means there is danger, False means there is none).
-  dir_code**: current direction (0: right, 1: left, 2: up, 3: down).
Actions parsing:
For each state, the Q value corresponding to each action is stored in the q_table.
The higher the Q value, the more likely the action is the best choice for the current state.

Example analysis:
State: ((100, 140), (False, False, False), 0)
State Description:
Food is on the right side of the snake's head 100 (delta_x) and on the lower side 140 (delta_y).
There is no danger around.
Current direction is to the right (dir_code=0).
Q value:
For the 'right' action only, the Q value is 0.199.
This indicates that in this state it is optimal to continue moving to the right, yielding 0.199.
