import pygame

class Alien_bonus (pygame.sprite.Sprite) :
	
	def __init__ (self, 
	       		  direction, 
				  SCREEN_WIDTH) -> 0 :
	
		super ().__init__ ()
	
		self.image = pygame.image.load ("../../images/bonus/alien_bonus.png").convert_alpha ()
		
		if (direction == "right") :

			x = SCREEN_WIDTH + 50
			
			self.speed = - 3
		
		else :
			
			x = - 50
			
			self.speed = 3

		self.rect = self.image.get_rect (topleft = (x, 80))

	def update (self) -> None :

		self.rect.x += self.speed