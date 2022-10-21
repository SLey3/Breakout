# File: Breakout.py
# Name: Sergio Ley Languren

"""This program (once you have finished it) implements the Breakout game."""

from pgl import GWindow, GOval, GRect
from utils import create_bricks, Paddle, Ball
import random

# Constants

GWINDOW_WIDTH = 360               # Width of the graphics window
GWINDOW_HEIGHT = 600              # Height of the graphics window
BRICK_SEP = 2                     # Separation between bricks
BRICK_ASPECT_RATIO = 4 / 1        # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 2       # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3     # Ratio of brick to paddle width
BOTTOM_FRACTION = 0.05            # Fraction of window below paddle
N_BALLS = 3                       # Number of balls in a game
N_ROWS = 10                       # Number of brick rows
N_COLS = 10                       # Number of brick columns
TIME_STEP = 10                    # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0          # Starting y velocity downward
MIN_X_VELOCITY = 1.0              # Minimum random x velocity
MAX_X_VELOCITY = 3.0              # Maximum random x velocity

# Derived constants

BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO

# Main program

def breakout():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    
    paddle = Paddle(gw, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, BRICK_TO_PADDLE_RATIO)

    ball = Ball(gw, BALL_SIZE, INITIAL_Y_VELOCITY, MIN_X_VELOCITY, MAX_X_VELOCITY, TIME_STEP)

    create_bricks(gw)

    paddle_obj = paddle.create_paddle()
    ball_obj = ball.create_ball()
    gw.add(paddle_obj)
    gw.add(ball_obj)
    gw.add_event_listener("mousemove", paddle.animate_paddle)
    gw.add_event_listener("click", ball.click_step)

# Startup code

if __name__ == "__main__":
    breakout()
