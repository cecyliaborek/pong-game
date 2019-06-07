import pygame
import time


class PongGame(object):
    """
    A class responsible for running of the game
    """
    def __init__(self, width, height):
        self.board = Board(width, height)
        self.ball = Ball(self.board, width/2, height/2) #starting with the ball in the middle of the board
        self.racket1 = Racket(self.board, 20, height/2) #left racket
        self.racket2 = Racket(self.board, width - 20, height/2) #right racket
        self.fps_clock = pygame.time.Clock()
        self.running = True #variable telling if the program is running
        self.judge = Judge(self.ball, self.board, self.racket1, self.racket2)
        self.paused = False #variable telling if the game is paused


    def run(self):
        while self.running:
            self.board.draw()
            self.ball.move(self.board, self.racket1, self.racket2)
            self.board.draw(
                self.ball,
                self.racket1,
                self.racket2,
                self.judge
                )
            self.fps_clock.tick(30)
            self.handle_events()
            self.judge.update_score()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                self.racket1.move(y)

        #getting input from arrows - player2
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            move_to = self.racket2.rect.y - self.racket2.speed
            self.racket2.move(move_to)
        if keys_pressed[pygame.K_DOWN]:
            move_to = self.racket2.rect.y + self.racket2.speed
            self.racket2.move(move_to)


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

        pygame.display.update()


class Drawable(object):
    """
    A base class for all objects that will be drawn on board(i.e. ball, rackets)
    """

    def __init__(self, board, x, y, width_ratio, height_ratio, color = (219, 112, 147)):
        self.board = board
        self.color = color
        self.width = width_ratio * self.board.surface.get_width()
        self.height = height_ratio * self.board.surface.get_height()
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y) #coordinates of the object
        self.speed = 3

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)



class Ball(Drawable):
    def __init__(self, board, x, y, x_speed = 3, y_speed = 3):
        super(Ball, self).__init__(board, 0.03, 0.03, x, y)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed = x_speed
        self.y_speed = y_speed
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
        if self.rect.y < self.height or self.rect.y > board.surface.get_height():
            self.bounce_y()
        for racket in rackets:
            if self.rect.colliderect(racket.rect):
                self.bounce_x()

    def reset(self):
        """Resets the position of the ball to the beginning position"""
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def pause(self):
        self.last_x_speed = self.x_speed
        self.last_y_speed = self.y_speed
        self.x_speed = 0
        self.y_speed = 0

    def play(self):
        self.x_speed = self.last_x_speed #additional variable to store the speed of objects before pause
        self.y_speed = self.last_y_speed #additional variable to store the speed of objects before pause

    def change_speed(self, new_speed):
        self.x_speed = new_speed * int(self.x_speed < 0) #saving the direction of the move
        self.y_speed = new_speed * int(self.y_speed < 0)


class Racket(Drawable):
    """Racket that we will bounce ball with"""

    def __init__(self, board, width = 20, height = 60):
        super(Racket, self).__init__(board, 0.03, 0.1, x, y)
        pygame.draw.rect(self.surface, self.color, [0, 0, self.width, self.height])

    def move(self, y):
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

    def change_speed(self, new_speed):
        self.speed = new_speed


class Judge(object):
    """docstring for Judge."""

    def __init__(self, ball, board, *rackets):
        self.ball = ball
        self.rackets = rackets
        self.board = board
        self.score = [0, 0]

        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 32)

    def update_score(self):
        if self.ball.rect.x < 0:
            self.score[0] += 1
            self.ball.reset()
        if self.ball.rect.x > self.board.surface.get_width():
            self.score[1] += 1
            self.ball.reset()

    def draw_text(self, surface,  text, x, y):
        """
        Drawing the text in exact place
        """
        text = self.font.render(text, True, (150, 150, 150))
        rect = text.get_rect()
        rect.center = x, y
        surface.blit(text, rect)

    def draw_on(self, surface):
        width = self.board.surface.get_width()
        height = self.board.surface.get_height()

        self.draw_text(surface, "Player1: {}".format(str(self.score[0])), width * 0.3, height/2)
        self.draw_text(surface, "Player2: {}".format(str(self.score[1])), width * 0.7, height/2)


if __name__ == "__main__":
    pygame.init()
    game = PongGame(600, 600)
    game.run()
