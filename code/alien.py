import pygame

class Alien (pygame.sprite.Sprite) :

	def __init__ (self, 
	       		  name_alien,
				  x,
				  y) -> float :
	
		super ().__init__ ()
	
		file_path = "../images/aliens/" + name_alien + ".png"
	
		self.image = pygame.image.load (file_path).convert_alpha ()
	
		self.rect = self.image.get_rect (topleft = (x, y))

	
		if (name_alien == "alien_2") : 
			
			self.value = 100
	
		elif (name_alien == "alien_1") :
			
			self.value = 200
	
		else : 
			
			self.value = 300

	def update (self, direction) -> None :
		
		self.rect.x += direction