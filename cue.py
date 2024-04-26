import pygame

class Cue():
    def __init__(self, image, position):
        self.org_image = image
        
        self.angle = 0
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = image.get_rect()
        self.rect.center = position
    
    def draw(self, SCREEN):
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        SCREEN.blit(
            self.image, 
            (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2)
        )
    
    def update(self, angle):
        self.angle = angle