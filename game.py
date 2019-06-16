import json
import PongGame
import pygame


with open("Documents/pong/configuration.txt", 'r') as conf:
    try:
        data = json.load(conf)
        if 'size' in data and data['size'] >= 200 and data['size'] <= 1000:
            board_size = data['size']
        else:
            board_size = 600
    except json.JSONDecodeError:
        board_size = 600
        
  

pygame.init()
game = PongGame.PongGame(board_size, board_size)
game.run()