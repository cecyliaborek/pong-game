import json
import PongGame
import pygame


with open("configuration.json", 'r') as conf:
    try:
        data = json.load(conf)
        if 'size' in data and data['size'] >= 200 and data['size'] <= 1000:
            board_size = data['size']
        else:
            board_size = 600
        
        if 'opponent' in data and (data['opponent'] == 'player' or data['opponent'] == 'computer'):
            opponent = data['opponent']
        else:
            opponent = "computer"
    except json.JSONDecodeError:
        #default configuration
        board_size = 600
        opponent = "computer"
        
  

pygame.init()
if opponent == "player":
    game = PongGame.PongGamePlayer(board_size, board_size)
    game.run()
elif opponent == 'computer':
    game = PongGame.PongGameComputer(board_size, board_size, 1)
    game.run()