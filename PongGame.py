import pygame


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
        """
        background = (192, 192, 192)
        self.surface.fill(background)

        for argument in args:
            argument.draw_on(self.surface)

        pygame.display.update()


class PongGame(object):
    def __init__(self, width, height):
        self.board = Board(width, height)
        self.ball = Ball(20, 20, width/2, height/2) #starting with the ball in the middle of the board
        self.racket1 = Racket(20, height/2) #left racket
        self.racket2 = Racket(width - 20, height/2) #right racket
        self.fps_clock = pygame.time.Clock()
        self.running = True #variable telling if the program is running

    def run(self):
        while self.running:
            self.board.draw()
            self.ball.move(self.board, self.racket1, self.racket2)
            self.board.draw(
                self.ball,
                self.racket1,
                self.racket2
                )
            self.fps_clock.tick(30)
            self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                self.racket1.move(y)
            if event.type == pygame.KEYDOWN:
                move_to = self.racket2.rect.y - self.racket2.speed
                self.racket2.move(move_to)
            if event.type == pygame.KEYUP:
                move_to = self.racket2.rect.y + self.racket2.speed
                self.racket2.move(move_to)


class Drawable(object):
    """
    A base class for all objects that will be drawn on board(i.e. ball, rackets)
    """

    def __init__(self, width, height, x, y, color = (219, 112, 147)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y) #coordinates of the object
        self.speed = 3

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    def __init__(self, width, height, x, y, x_speed = 3, y_speed = 3):
        super(Ball, self).__init__(width, height, x, y)
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
        if self.rect.x < 0 or self.rect.x > board.surface.get_width():
            self.bounce_x()
        if self.rect.y < 0 or self.rect.y > board.surface.get_height():
            self.bounce_y()
        for racket in rackets:
            if self.rect.colliderect(racket.rect):
                self.bounce_x()

    def reset(self):
        """Resets the position of the ball to the beginning position"""
        self.rect.move(self.start_x, self.start_y)


class Racket(Drawable):
    """Racket that we will bounce ball with"""

    def __init__(self, x, y, width = 20, height = 60):
        super(Racket, self).__init__(width, height, x, y)
        pygame.draw.rect(self.surface, self.color, [0, 0, self.width, self.height])

    def move(self, y):
        delta = y - self.rect.y
        if abs(delta) > self.speed:
            if delta > 0:
                delta = self.speed
            else:
                delta = - self.speed
        self.rect.y += delta




if __name__ == "__main__":
    game = PongGame(600, 600)
    game.run()
