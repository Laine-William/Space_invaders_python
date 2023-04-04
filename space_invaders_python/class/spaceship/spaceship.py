import pygame 
from Laser.laser import Laser

class Spaceship (pygame.sprite.Sprite) :

	def __init__ (self, 
	       		  position, 
				  constraint, 
				  speed) -> None :

		super ().__init__ ()

		self.image = pygame.image.load ("../../images/spaceship/spaceship.png").convert_alpha ()

		self.rect = self.image.get_rect (midbottom = position)
		
		self.speed = speed
		
		self.max_x_constraint = constraint
		
		self.ready = True
		
		self.laser_time = 0
		
		self.laser_cooldown = 600

		self.lasers = pygame.sprite.Group ()

		self.laser_sound = pygame.mixer.Sound ("../../audio/laser.wav")
		self.laser_sound.set_volume (0.5)

	def press_keyboard (self) -> None :

		keyboard = pygame.key.get_pressed ()

		if (keyboard [pygame.K_RIGHT]) :

			self.rect.x += self.speed
		
		elif (keyboard [pygame.K_LEFT]) :

			self.rect.x -= self.speed

		if ((keyboard[pygame.K_SPACE]) and (self.ready)) :

			self.shoot_laser ()
			
			self.ready = False
			
			self.laser_time = pygame.time.get_ticks ()
			
			self.laser_sound.play ()

	def reload_laser (self) -> None :

		if not (self.ready) :

			current_time = pygame.time.get_ticks ()

			if ((current_time - self.laser_time) >= self.laser_cooldown) :
				
				self.ready = True

	def move_constraint (self) -> None :

		if (self.rect.left <= 0) :

			self.rect.left = 0

		if (self.rect.right >= self.max_x_constraint) :

			self.rect.right = self.max_x_constraint

	def shoot_laser (self) -> None :

		self.lasers.add (Laser (self.rect.center, 
			  					-8, 
								self.rect.bottom))

	def update (self) -> None :

		self.press_keyboard ()

		self.move_constraint ()
		
		self.reload_laser ()
		
		self.lasers.update ()