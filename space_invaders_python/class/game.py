import pygame, sys
from spaceship import Spaceship
import obstacle
from alien import Alien 

from alien_bonus import Alien_bonus

from laser import Laser
from random import choice, randint

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game :

    def __init__ (self) -> None :

        pygame .display.set_caption ("Space Invaders")
        pygame_icon = pygame.image.load ("../images/aliens/alien_2.png")
        pygame.display.set_icon (pygame_icon)

        # Spaceship Setup
        spaceship_sprite = Spaceship ((SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, 5)
        self.spaceship = pygame.sprite.GroupSingle (spaceship_sprite)

        # Health and Score Setup
        self.lives = 3
        self.live_spaceship = pygame.image.load ("../images/spaceship/spaceship.png").convert_alpha ()
        self.live_x_start_position = SCREEN_WIDTH - (self.live_spaceship.get_size ()[0] * 3 + 20)

        self.score = 0
        self.font = pygame.font.SysFont ("arialblack", 30)

        # Obstacle Setup
        self.shape = obstacle.shape
        self.obstacle_size = 6
        self.obstacles = pygame.sprite.Group ()
        self.obstacle_quantity = 4
        self.obstacle_x_position = [
            
            number_obstacle * (SCREEN_WIDTH / self.obstacle_quantity) 
            
                for number_obstacle in range (self.obstacle_quantity) 
        ]

        self.create_multiple_obstacles (* self.obstacle_x_position, 
                                        x_start = (SCREEN_WIDTH / 15), 
                                        y_start = 480)

        # Alien Setup
        self.aliens = pygame.sprite.Group ()
        self.alien_lasers = pygame.sprite.Group ()

        self.alien_setup (rows = 6, columns = 8)

        self.alien_direction = 1

        # Alien_bonus Alien Setup
        self.alien_bonus = pygame.sprite.GroupSingle ()
        self.extra_spawn_time = randint (400, 800)

        # Audio
        music = pygame.mixer.Sound ("../audio/music.wav")
        music.set_volume (0.2)
        music.play (loops = - 1)

        self.laser_sound = pygame.mixer.Sound ('../audio/laser.wav')
        self.laser_sound.set_volume (0.2)

        self.explosion_sound = pygame.mixer.Sound ('../audio/explosion.wav')
        self.explosion_sound.set_volume (0.5)

    def create_obstacle (self, 
                        x_start, 
                        y_start, 
                        offset_x) -> None :
        
        for row_index, row in enumerate (self.shape) :

            for column_index, column in enumerate (row) :

                if (column == "x") :

                    x = x_start + (column_index * self.obstacle_size) + offset_x
                    y = y_start + (row_index * self.obstacle_size)

                    block = obstacle.Obstacle (self.obstacle_size, 
                                               ("purple"), 
                                               x, 
                                               y)
                    self.obstacles.add (block)

    def create_multiple_obstacles (self, 
                                   * offset, 
                                   x_start, 
                                   y_start) -> None :
        
        for offset_x in offset :

            self.create_obstacle (x_start, 
                                  y_start, 
                                  offset_x)

    def alien_setup (self, 
                     rows, 
                     columns, 
                     x_distance = 60, 
                     y_distance = 48, 
                     x_offset = 70, 
                     y_offset = 100) -> None :
        
        for row_index, row in enumerate (range (rows)) :

            for column_index, column in enumerate (range (columns)) :

                x = column_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                if (row_index == 0) : 
                    
                    alien_sprite = Alien ("alien_0", x, y)

                elif (1 <= row_index <= 2) :
                    
                    alien_sprite = Alien ("alien_1", x, y)

                else : 
                    
                    alien_sprite = Alien ("alien_2", x, y)

                
                self.aliens.add (alien_sprite)

    def alien_position_checker (self) -> None :

        all_aliens = self.aliens.sprites ()

        for alien in all_aliens :

            if (alien.rect.right >= SCREEN_WIDTH) :

                self.alien_direction = - 1

                self.alien_move_down (2)

            elif (alien.rect.left <= 0) :

                self.alien_direction = 1
                
                self.alien_move_down (2)

    def alien_move_down (self, distance) -> None :

        if (self.aliens) :

            for alien in self.aliens.sprites () :

                alien.rect.y += distance

    def alien_shoot (self) -> None :

        if (self.aliens.sprites ()) :

            random_alien = choice (self.aliens.sprites ())

            laser_sprite = Laser (random_alien.rect.center, 6, SCREEN_HEIGHT)

            self.alien_lasers.add (laser_sprite)
            self.laser_sound.play ()

    def bonus_alien_timer (self) -> None :

        self.extra_spawn_time -= 1
        
        if (self.extra_spawn_time <= 0) :

            self.alien_bonus.add (Alien_bonus (choice (["right", "left"]), SCREEN_WIDTH))

            self.extra_spawn_time = randint (400, 800)

    def collision (self) -> None :

        # Spaceship Lasers
        if (self.spaceship.sprite.lasers) :
            
            for laser in self.spaceship.sprite.lasers:

                # Obstacle Collisions
                if (pygame.sprite.spritecollide (laser, 
                                                 self.obstacles, 
                                                 True)) : 
                    
                    laser.kill ()

                # Alien Collisions
                aliens_hit = pygame.sprite.spritecollide (laser, 
                                                          self.aliens, 
                                                          True)
                if (aliens_hit) :

                    for alien in aliens_hit :
                    
                        self.score += alien.value

                    SCREEN.fill ("black")

                    laser.kill ()

                    self.explosion_sound.play ()

                # Alien_bonus Collisions
                if (pygame.sprite.spritecollide (laser, 
                                                 self.alien_bonus, 
                                                 True)) :
                    
                    SCREEN.fill ("black")

                    self.score += 500

                    laser.kill ()

                    self.explosion_sound.play ()
        
        # Alien Lasers
        if (self.alien_lasers) :

            for laser in self.alien_lasers :

                # Obstacle Collisions
                if (pygame.sprite.spritecollide (laser, 
                                                 self.obstacles, 
                                                 True)) :
                    
                    laser.kill ()

                # Spaceship Collisions
                if (pygame.sprite.spritecollide (laser, 
                                                 self.spaceship, 
                                                 False)) :
                    
                    laser.kill ()

                    SCREEN.fill ("black")

                    self.lives -= 1
                    
        # Aliens
        if (self.aliens) :

            for alien in self.aliens:
            
                # Obstacle Collisions
                pygame.sprite.spritecollide (alien, 
                                             self.obstacles, 
                                             True)

                # Spaceship Collisions
                if (pygame.sprite.spritecollide (alien, 
                                                 self.spaceship, 
                                                 True)) :
                    pygame.quit()
                    sys.exit()

    def display_lives (self) -> int :

        for live in range (self.lives) :
        
            x = self.live_x_start_position + (live * (self.live_spaceship.get_size () [0] + 10))
            
            SCREEN.blit (self.live_spaceship, (x, 8))

        if (self.lives <= 0) :

            pygame.quit ()
            sys.exit ()

    def display_score (self) -> None :

        score_render = self.font.render (f"Score : {self.score}", False, "white")
        score_position = score_render.get_rect (topleft = (10, - 10))

        SCREEN.blit (score_render, score_position)

    def run (self) -> None :

        # Draw and Update All Sprite Groups
        self.spaceship.update ()

        self.alien_lasers.update ()

        self.alien_bonus.update()

        self.aliens.update (self.alien_direction)

        self.alien_position_checker ()

        self.bonus_alien_timer ()

        self.collision ()


        self.spaceship.sprite.lasers.draw (SCREEN)
        self.spaceship.draw (SCREEN)

        self.obstacles.draw (SCREEN)

        self.aliens.draw (SCREEN)
        self.alien_lasers.draw (SCREEN)
        self.alien_bonus.draw (SCREEN)

        self.display_lives ()

        self.display_score ()