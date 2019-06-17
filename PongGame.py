import pygame
import time
import random
from GUI import *


class PongGame(object):
    """
    A class responsible for running of the game
    """
    def __init__(self, width, height):
        self.board = Board(width, height)
        self.ball = Ball(self.board, width/2, height/2) #starting with the ball in the middle of the board
        self.racket1 = Racket(self.board, 0.03 * width, height/2) #left racket
        self.racket2 = Racket(self.board, width - 0.03 * width, height/2) #right racket
        self.fps_clock = pygame.time.Clock()
        self.running = True #variable telling if the program is running
        self.judge = Judge(self.ball, self.board, self.racket1, self.racket2)
        self.pause_button = Pause_button(self.board, self.ball, self.racket1, self.racket2)
        self.reset_button = Reset_button(self.board, self.ball, self.racket1, self.racket2)
        self.opponent = 0 #variable telling if we play against computer or player


    def run(self):
        while self.running:
            self.board.draw()
            self.ball.move(self.board, self.racket1, self.racket2)
            self.board.draw(
                self.ball,
                self.racket1,
                self.racket2,
                self.judge,
                self.pause_button,
                self.reset_button
                )
            self.fps_clock.tick(30)
            self.handle_events()
            self.handle_events_player2()
            self.handle_events_player1()
            self.judge.update_score()
            pygame.display.update()

    def handle_events(self):
        """Function responsible for getting input from the user """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            if event.type == pygame.MOUSEMOTION:
                if self.opponent == 'player':
                    x, y = event.pos
                    self.racket1.move(y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_button.rect.collidepoint(event.pos):
                    self.pause_button.click()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.rect.collidepoint(event.pos):
                    self.reset_button.click(self.judge)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.ball.change_speed(1)
                elif event.key == pygame.K_2:
                    self.ball.change_speed(2)
                elif event.key == pygame.K_3:
                    self.ball.change_speed(3)
                elif event.key == pygame.K_4:
                    self.ball.change_speed(4)
                elif event.key == pygame.K_5:
                    self.ball.change_speed(5)
                elif event.key == pygame.K_6:
                    self.ball.change_speed(6)
                elif event.key == pygame.K_7:
                    self.ball.change_speed(7)
                elif event.key == pygame.K_8:
                    self.ball.change_speed(8)
                elif event.key == pygame.K_9:
                    self.ball.change_speed(9)

    def handle_events_player2(self):
        #getting input from arrows - player2
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            move_to = self.racket2.rect.y - self.racket2.speed
            self.racket2.move(move_to)
        if keys_pressed[pygame.K_DOWN]:
            move_to = self.racket2.rect.y + self.racket2.speed
            self.racket2.move(move_to)
    
    def handle_events_player1(self):
        pass


class PongGameComputer(PongGame):
    
    def __init__(self, width, height, difficulty):
        super(PongGameComputer, self).__init__(width, height)
        self.computer_player = ComputerPlayer(self.racket1, self.ball, difficulty)
        self.opponent = 'computer'

    def handle_events_player1(self):
        self.computer_player.move_racket()


class PongGamePlayer(PongGame):

    def __init__(self, width, height):
        super(PongGamePlayer, self).__init__(width, height)
        self.opponent = 'player'


class ComputerPlayer(object):
    """Computer as a player with 3 different difficulty levels """
    def __init__(self, racket, ball, difficulty):
        self.racket = racket
        self.ball = ball
        self.difficulty = difficulty
        self.error = 0

    def mistake(self, difficulty):
        """Function adding random mistake to racket movement depending on difficulty level """
        if difficulty == 1:
            self.error += random.randint(-2, 2) * 0.5 * self.racket.width #scaling the mistake to the size of racket
            #self.error *= self.racket.direction() #
        if difficulty == 2:
            self.error = random.randint(-1, 1) * 0.5 * self.racket.width 
            #self.error *= self.racket.direction()
        if difficulty == 3:
            self.error = 0

    def move_racket(self):
        self.mistake(self.difficulty)
        y = self.ball.rect.centery + self.error
        self.racket.move(y)


class Judge(object):
    """docstring for Judge."""

    def __init__(self, ball, board, *rackets):
        self.ball = ball
        self.rackets = rackets
        self.board = board
        self.score = [0, 0]

        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        size = int(0.05 * board.surface.get_width()) #adjusting font size to the board size
        self.font = pygame.font.Font(font_path, size)

    def update_score(self):
        if self.ball.rect.x < self.ball.width:
            self.score[1] += 1
            self.ball.reset()
        if self.ball.rect.x > self.board.surface.get_width() - self.ball.width:
            self.score[0] += 1
            self.ball.reset()

    def reset_score(self):
        self.score = [0, 0]

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
    game = PongGamePlayer(600, 600)
    game.run()