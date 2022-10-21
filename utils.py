# File: utils.py
# Name: Sergio Ley Languren

"""
Utility Module that provides necessary functionality for the breakout Project
"""

# Imports 
from pgl import GWindow, GOval, GRect, GCompound, GTimer
from typing import Type
import random


__all__ = [
    "create_bricks",
    "Paddle",
    "Ball"
]

N_ROWS = 10                       # Number of brick rows
N_COLS = 10                       # Number of brick columns
BRICK_SEP = 2                     # Separation between bricks
BRICK_ASPECT_RATIO = 4 / 1        # Width to height ratio of a brick
GWINDOW_WIDTH = 360               # Width of the graphics window
GWINDOW_HEIGHT = 600              # Height of the graphics window
TOP_FRACTION = 0.1                # Fraction of window above bricks
BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO

brick_color_list = [
    "red",
    "orange",
    "green",
    "cyan",
    "blue"
]

brick_compound = GCompound()

def _create_brick(x, y, w, h, c):
    brick = GRect(x, y, w, h)
    brick.set_color(c)
    brick.set_filled(True)
    return brick

def create_bricks(gw: Type[GWindow]):
    for i in range(N_ROWS):
        for j in range(N_COLS):
            brick_compound.add(_create_brick(BRICK_SEP + (BRICK_WIDTH + BRICK_SEP) * j, GWINDOW_HEIGHT * TOP_FRACTION + i * (BRICK_HEIGHT + BRICK_SEP), BRICK_WIDTH, BRICK_HEIGHT, brick_color_list[int(i/2)]))
    gw.add(brick_compound)


class Paddle:
    """
    class that provides functions to create and animate the paddle
    """
    def __init__(
        self, gw: Type[GWindow], 
        paddle_y, paddle_width, 
        paddle_height, brick_paddle_ratio
        ):
        self.gw = gw
        self.gw.paddle_y = paddle_y
        self.gw.paddle_width = paddle_width
        self.gw.paddle_height = paddle_height
        self.gw.brick_paddle_ratio = brick_paddle_ratio
    
    def create_paddle(self):
        """
        Creates paddle Grect object
        """
        self.gw.paddle_x = GWINDOW_WIDTH / 2
        rect = GRect(self.gw.paddle_x, self.gw.paddle_y, self.gw.paddle_width, self.gw.paddle_height)
        rect.set_color("black")
        rect.set_filled(True)
        self.gw.paddle = rect
        return rect

    def animate_paddle(self, e):
        """
        animates the paddle
        """
        if e.get_x() >= GWINDOW_WIDTH - self.gw.paddle_width:
            self.gw.paddle.set_location(GWINDOW_WIDTH - self.gw.paddle_width, self.gw.paddle_y)
        else:
            self.gw.paddle.set_location(e.get_x(), self.gw.paddle_y)

class Ball:
    """
    class that provides functions to create and animate the ball
    """
    moving = False

    timer_created = False

    start = True
    
    obj = None


    def __init__(
        self, gw: Type[GWindow],
         ball_size, init_v,
          min_x_v, max_x_v, 
          time_step, paddle_obj
          ):
        self.gw = gw
        self.gw.ball_size = ball_size
        self.gw.init_v = init_v
        self.gw.min_x_v = min_x_v
        self.gw.max_x_v = max_x_v
        self.gw.time_step = time_step
        self.paddle_obj = paddle_obj
        
    @property
    def is_paddle(self):
        return self.obj == self.paddle_obj

    def _create_timer(self, fn):
        if not self.timer_created:
            self.gw.timer = GTimer(self.gw, fn, self.gw.time_step)
            self.gw.timer.set_repeats(True)
            self.timer_created = True

    def create_ball(self):
        """
        Create ball GOval object
        """
        self.gw.x0 = GWINDOW_WIDTH / 2
        self.gw.y0 = GWINDOW_HEIGHT / 2
        ball = GOval(self.gw.x0, self.gw.y0, self.gw.ball_size, self.gw.ball_size)
        ball.set_color("black")
        ball.set_filled(True)
        self.gw.ball = ball
        return ball

    def reset_pos(self):
        """resets ball to original pos"""
        self.gw.x0 = GWINDOW_WIDTH / 2
        self.gw.y0 = GWINDOW_HEIGHT / 2
        self.gw.timer.stop()
        self.gw.ball.set_location(self.gw.x0, self.gw.y0)

        self.start = True
        
    def check_for_collisions(self):
        r = self.gw.ball_size / 2
        p1x, p1y = self.gw.ball.get_x(), self.gw.ball.get_y()
        p2x, p2y = self.gw.ball.get_X() + 2 * r, self.gw.ball.get_y()
        p3x, p3y = self.gw.ball.get_x(), self.gw.ball.get_y() + 2 * r
        p4x, p4y = self.gw.ball.get_x() + 2 * r, self.gw.ball.get_y() + 2 * r
        
        x_cords, y_cords = [p1x, p2x, p3x, p4x], [p1y, p2y, p3y, p4y]
        
        for x, y in zip(x_cords, y_cords):
            potential_elem = self.gw.get_element_at(x, y)
            if potential_elem:
                self.obj = potential_elem
                return True, potential_elem
        return False, None

    def click_step(self, e):
        """
        Adds movement to ball
        """
        self.moving = True if not self.moving else False

        def animate_ball():
            global vy, vx
                
            if self.start:
                vy = -self.gw.init_v
                vx = random.choice([self.gw.init_v, -self.gw.init_v])
                self.start = False
            
            collision, obj = self.check_for_collisions()
            if collision:
                if self.is_paddle:
                    ...
                else:
                    ...

            self.gw.ball.set_location(
                self.gw.x0 - vx,
                self.gw.y0 - vy
            )
            
            if self.gw.y0 - self.gw.init_v == 0.0:
                vy = -self.gw.init_v
            elif self.gw.y0 - self.gw.init_v == GWINDOW_HEIGHT:
                #self.reset_pos()
                vy = self.gw.init_v
            if self.gw.x0 - self.gw.init_v == 0.0:
                vx = -self.gw.init_v
            elif self.gw.x0 - self.gw.init_v == GWINDOW_WIDTH:
                vx = self.gw.init_v
                
            self.gw.x0 = self.gw.x0 - vx
            self.gw.y0 = self.gw.y0 - vy

        self._create_timer(animate_ball)

        if not self.moving:
            self.gw.timer.stop()
        else:
            self.gw.timer.start()