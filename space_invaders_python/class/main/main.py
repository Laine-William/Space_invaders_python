import pygame
import sys
from random import randint
from game.game import Game

class Main :

    def __init__ (self) :

        self.background = pygame.image.load ("../../images/background/game_background.png").convert_alpha ()
        self.background = pygame.transform.scale (self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_lines_spacing (self) :

        line_height = 3
        
        line_quantity = int (SCREEN_HEIGHT / line_height)
        
        for line in range (line_quantity) :

            y_position = (line * line_height)
            
            pygame.draw.line (self.background, 
                              "black", 
                              (0, y_position), 
                              (SCREEN_WIDTH, y_position), 
                              1)

    def draw (self) :

        self.background.set_alpha (randint (75, 90))
        
        self.create_lines_spacing ()
        
        SCREEN.blit (self.background, (0, 0))


if (__name__ == "__main__") :

    pygame.init ()

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    
    SCREEN = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    
    game = Game ()
    main = Main ()

    ALIENS_LASERS = pygame.USEREVENT + 1
    
    pygame.time.set_timer (ALIENS_LASERS, 800)

    run = True

    while run :

        for event in pygame.event.get () :

            if (event.type == pygame.QUIT) :

                pygame.quit ()
                sys.exit ()

            if (event.type == ALIENS_LASERS) :

                game.alien_shoot ()

        SCREEN.fill ("black")

        game.run ()

        main.draw ()

        pygame.display.flip ()

        clock.tick (60)