import pygame
from PongGame import *


class Board(object):
    """
    Class representing the gameboard
    """
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Pong game")

    def draw(self, *args):
        """
        Drawing and displaying the board
        Parameters:
        args(Drawable): objects to be displayed on board (ball, rackets)
        """
        background = (192, 192, 192)
        self.surface.fill(background)

        for argument in args:
            argument.draw_on(self.surface)


class Drawable(object):
    """
    A base class for all objects that will be drawn on board(i.e. ball, rackets)
    """

    def __init__(self, board, x, y, width_ratio, height_ratio, color = (219, 112, 147)):
        self.board = board
        self.color = color
        #checking if given ratio isn't too big
        if width_ratio > 1:
            width_ratio = 0.1
        if height_ratio > 1:
            height_ratio = 0.1

        self.width = width_ratio * self.board.surface.get_width()
        self.height = height_ratio * self.board.surface.get_height()
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32).convert_alpha()
        #x -= self.width/2
        #y -= self.height/2
        self.rect = self.surface.get_rect() #coordinates of the object
        self.rect.center = (x, y)
        

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    def __init__(self, board, x, y, ):
        super(Ball, self).__init__(board, x, y, 0.03, 0.03,)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        #adjusting speed to the board size
        self.speed_ratio = board.surface.get_width()/600
        self.x_speed = self.speed_ratio * 3
        self.y_speed = self.speed_ratio * 3
        self.start_x = x 
        self.start_y = y 

    def bounce_y(self):
        """Changing the direction of movement in y axis"""
        self.y_speed *= -1

    def bounce_x(self):
        """Changing the direction of movement in x axis"""
        self.x_speed *= -1

    def move(self, board, *rackets):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.x < 0 or self.rect.x > board.surface.get_width() - self.width:
            self.bounce_x()
        if self.rect.y < 0 or self.rect.y > board.surface.get_height() - self.height:
            self.bounce_y()
        for racket in rackets:
            if self.rect.colliderect(racket.rect):
                self.bounce_x()

    def reset(self):
        """Resets the position of the ball to the beginning position"""
        self.rect.center = (self.start_x, self.start_y)

    def pause(self):
        self.last_x_speed = self.x_speed
        self.last_y_speed = self.y_speed
        self.x_speed = 0
        self.y_speed = 0

    def play(self):
        self.x_speed = self.last_x_speed #additional variable to store the speed of objects before pause
        self.y_speed = self.last_y_speed #additional variable to store the speed of objects before pause

    def change_speed(self, new_speed):
        self.x_speed = self.speed_ratio * new_speed * self.direction(self.x_speed) #saving the direction of the move
        self.y_speed = self.speed_ratio * new_speed * self.direction(self.y_speed)

    def direction(self, speed):
        if speed < 0:
            return -1
        elif speed > 0:
            return 1


class Racket(Drawable):
    """Racket that we will bounce ball with"""

    def __init__(self, board, x, y):
        self.x_start = x
        self.y_start = y
        self.speed = 27
        super(Racket, self).__init__(board, x, y, 0.03, 0.1)
        pygame.draw.rect(self.surface, self.color, [0, 0, self.width, self.height])

    def move(self, y):
        if not(y < 0 or y > self.board.surface.get_height() - self.height):
            delta = y - self.rect.y
            if abs(delta) > self.speed:
                if delta > 0:
                    delta = self.speed
                else:
                    delta = - self.speed
            self.rect.y += delta

    def pause(self):
        self.last_speed = self.speed #additional variable to store the speed of objects before pause
        self.speed = 0

    def play(self):
        self.speed = self.last_speed

    def reset(self):
        """Reseting to starting position"""
        self.rect.center = (self.x_start, self.y_start)

    def direction(self):
        """Direction of the movement"""
        return 1


class Button(Drawable):

    def __init__(self, board, label, x, y, ball, *rackets):
        super(Button, self).__init__(board, x, y, 0.1, 0.05)
        pygame.draw.rect(self.surface, self.color, [0, 0, self.width, self.height])
        self.label = label
        self.ball = ball
        self.rackets = rackets
        self.clicked = False 

        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        size = int(0.5 * self.surface.get_height()) #adjusting font size to the button size
        self.font = pygame.font.Font(font_path, size)

    def draw_text(self, surface,  text, ):
        """
        Drawing the text in exact place
        """
        text = self.font.render(text, True, (0, 0, 0))
        surface.blit(text, (self.rect.x + (self.width/2 - text.get_width()/2), self.rect.y + (self.height/2 - text.get_height()/2)))

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)
        self.draw_text(surface, self.label)
        

class Pause_button(Button):

    def __init__(self, board, ball, *rackets):
        x = 0.4 * board.surface.get_width()
        y = 0.9 * board.surface.get_height()
        super(Pause_button, self).__init__(board, 'pause', x, y, ball, *rackets)
        self.clicked = False

    def click(self):
        
        if not self.clicked:
            self.ball.pause()
            for racket in self.rackets:
                racket.pause()
            self.clicked = True
            self.label = "play"

        elif self.clicked:
            self.ball.play()
            for racket in self.rackets:
                racket.play()
            self.clicked = False
            self.label = "pause"


class Reset_button(Button):

    def __init__(self, board, ball, *rackets):
        x = (board.surface.get_width() - 0.4 * board.surface.get_width())
        y = 0.9 * board.surface.get_height()
        super(Reset_button, self).__init__(board, 'reset', x, y, ball, *rackets)

    def click(self, judge):
        self.ball.reset()
        judge.reset_score()
        for racket in self.rackets:
            racket.reset()

