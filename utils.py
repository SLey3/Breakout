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
brick_compound.obj_name = "bricks"
brick_count = 0

def _create_brick(x, y, w, h, c):
    brick = GRect(x, y, w, h)
    brick.set_color(c)
    brick.set_filled(True)
    return brick

def create_bricks(gw: Type[GWindow]):
    global brick_count
    for i in range(N_ROWS):
        for j in range(N_COLS):
            brick_compound.add(_create_brick(BRICK_SEP + (BRICK_WIDTH + BRICK_SEP) * j, GWINDOW_HEIGHT * TOP_FRACTION + i * (BRICK_HEIGHT + BRICK_SEP), BRICK_WIDTH, BRICK_HEIGHT, brick_color_list[int(i/2)]))

    brick_count += brick_compound.getElementCount()
    gw.add(brick_compound)

class Paddle:
    """
    class that provides functions to create and animate the paddle
    """
    obj_name = "paddle"
    
    def __init__(
        self, gw: Type[GWindow], 
        paddle_y, paddle_width, 
        paddle_height, brick_paddle_ratio
        ):
        self.gw = gw
        self.gw.paddle_y = paddle_y
        self.gw.paddle_width = paddle_width
        self.paddle_width = self.gw.paddle_width
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
        rect.obj_name = "paddle"
        self.gw.paddle = rect
        self.paddle = self.gw.paddle
        return rect

    def animate_paddle(self, e):
        """
        animates the paddle
        """
        if e.get_x() >= GWINDOW_WIDTH - self.gw.paddle_width:
            self.gw.paddle.set_location(GWINDOW_WIDTH - self.gw.paddle_width, self.gw.paddle_y)
        else:
            self.gw.paddle.set_location(e.get_x(), self.gw.paddle_y)

class _base_obj:
    obj_name = "None"

class Ball:
    """
    class that provides functions to create and animate the ball
    """
    moving = False

    timer_created = False

    start = True
    
    obj = _base_obj()
    
    tries = 3


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
        return self.obj.obj_name == self.paddle_obj.obj_name

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
        """resets ball to original pos or resets the entire board if no more bricks are present"""
        self.gw.x0 = GWINDOW_WIDTH / 2
        self.gw.y0 = GWINDOW_HEIGHT / 2
        self.gw.ball.set_location(self.gw.x0, self.gw.y0)
        if self.tries == 0:
            self.gw.timer.stop()
            self.tries = 3
            self.start = True
            self.timer_created = False
            reset_board(self.gw, self.paddle_obj, self)
        else:
            self.tries = self.tries - 1

    def check_for_collisions(self, component):
        """
        check if ball has collided with an object
        """
        r = self.gw.ball_size / 2
        p1x, p1y = self.gw.ball.get_x(), self.gw.ball.get_y()
        p2x, p2y = self.gw.ball.get_x() + 2 * r, self.gw.ball.get_y()
        p3x, p3y = self.gw.ball.get_x(), self.gw.ball.get_y() + 2 * r
        p4x, p4y = self.gw.ball.get_x() + 2 * r, self.gw.ball.get_y() + 2 * r
        
        x_cords, y_cords = [p1x, p2x, p3x, p4x], [p1y, p2y, p3y, p4y]
        
        if isinstance(component, GCompound):
            for _ in range(component.get_element_count() + 1):
                for x, y in zip(x_cords, y_cords):
                    potential_elem = component.get_element_at(x, y)
                    if potential_elem:
                        self.obj = potential_elem
                        return True, potential_elem
        else:
            for x, y in zip(x_cords, y_cords):
                potential_elem = component.get_element_at(x, y)
                if potential_elem:
                    self.obj = potential_elem
                    return True, potential_elem
        return False, None
    
    def check_paddle_collision_area(self):
        """
        checks exactly where the ball is hitting the paddle
        """
        x1 = self.paddle_obj.paddle.get_x()
        x2 = self.paddle_obj.paddle.get_x() + self.paddle_obj.paddle_width
        xr =self.paddle_obj.paddle.get_x() + self.paddle_obj.paddle_width / 2

        if self.gw.ball.get_x() >= x1 and self.gw.ball.get_x() < xr:
            return "L"
        elif self.gw.ball.get_x() == xr:
            return "M"
        elif self.gw.ball.get_x() > xr and self.gw.ball.get_x() <= x2:
            return "R"

    def click_step(self, e):
        """
        Adds movement to ball
        """
        self.moving = True if not self.moving else False

        def animate_ball():
            global vy, vx, brick_count
                
            if self.start:
                vy = -self.gw.init_v
                vx = random.choice([self.gw.min_x_v , self.gw.max_x_v])
                self.start = False
            
            collision, obj = self.check_for_collisions(self.gw)
            if collision:
                if self.is_paddle:
                    vy = -vy

                    paddle_collision_area = self.check_paddle_collision_area()

                    if paddle_collision_area == "L":
                        vx = -vx
                    elif paddle_collision_area == "M":
                        vx = random.choice([vx, -vx])
                    elif paddle_collision_area == "R":
                        vx = vx
                else:
                    _, c_obj = self.check_for_collisions(obj)
                    obj.remove(c_obj)
                    brick_count -= 1
                    vx = random.choice([vx, -vx])
                    vy = -vy
                    

            self.gw.ball.set_location(
                self.gw.x0 - vx,
                self.gw.y0 - vy
            )
            
            if self.gw.y0 - vy == 0.0:
                vy = -self.gw.init_v
            elif self.gw.y0 - vy == GWINDOW_HEIGHT:
                self.reset_pos()
            if self.gw.x0 - vx == 0.0:
                vx = -self.gw.init_v
            elif self.gw.x0 - vx == GWINDOW_WIDTH:
                vx = self.gw.init_v
                
            self.gw.x0 = self.gw.x0 - vx
            self.gw.y0 = self.gw.y0 - vy

            if brick_count == 0:
                self.tries = 3
                self.gw.timer.stop()
                reset_board(self.gw, self.paddle_obj, self)

        self._create_timer(animate_ball)

        if not self.moving:
            self.gw.timer.stop()
        else:
            self.gw.timer.start()

def reset_board(gw: Type[GWindow], paddle_obj: Type[Paddle], ball_obj: Type[Ball]):
    """
    resets breakout board back to start stage
    """
    gw.clear()
    create_bricks(gw)
    paddle = paddle_obj.create_paddle()
    ball = ball_obj.create_ball()
    gw.add(paddle)
    gw.add(ball)