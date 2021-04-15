import pygame                                           
from pygame.constants import (                          
    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
)
import os
import random

#Habe es leider nicht geschaft das gesammte spiel fertig zu programmieren. 

class Settings(object):     
    def __init__(self): 
        self.width = 800
        self.height = 600
        self.fps = 60       
        self.title = "Bubble" 
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")


    def get_dim(self):
        return (self.width, self.height)

#Habe es leider nie hinbekommen das die sounds funktionieren weswegen es diese hier nicht gibt
class Enemy(pygame.sprite.Sprite):          
    def __init__(self, settings, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.settings = settings
        self.imageorig = pygame.image.load(os.path.join(self.settings.images_path, "Blase.png")).convert_alpha()
        self.image = self.imageorig
        self.rect = self.image.get_rect()
        self.growthrate = random.randint(1,4)
        self.last_grow_time = 0
        self.x = random.randint(0, self.settings.width-self.rect.width)
        self.y = random.randint(0, 300)
        self.radius = 5
        self.update()

    def update(self):
        if pygame.time.get_ticks() >= self.last_grow_time + self.game.timeunits:
            self.radius += self.growthrate
            self.last_grow_time = pygame.time.get_ticks()
            self.image = pygame.transform.scale(self.imageorig, (self.radius, self.radius))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y

class Gun(pygame.sprite.Sprite):          
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.images_path, "Gun.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.directionx = 0
        self.directiony = 0

    def update(self):
        cx = self.rect.centerx
        cy = self.rect.centery
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy

class Points():
    def __init__(self):
        self.font = pygame.font.Font(pygame.font.match_font("Arial"), 48)
        self.fontcolor = [0,0,0]
        self.points = 0 
        self.left = 15 
        self.top = 25

    def draw(self, screen):
        text = self.font.render(f"Punkte:{self.points}", True, self.fontcolor)     
        screen.blit(text,[self.left, self.top])

class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "BG1.jpg")).convert()
        self.background_rect = self.background.get_rect()
        self.gun = Gun(settings)
        self.done = False
        self.timeunits = 1000 
        pygame.mouse.set_visible(False)
        self.all_guns = pygame.sprite.GroupSingle()
        self.all_guns.add(self.gun)
        self.all_enemys = pygame.sprite.Group()
        self.last_enemy_time = 0
        self.enemy_rate = 1000
        self.clock = pygame.time.Clock()
        self.gun = pygame.sprite.Group()
        self.points = Points()


    def run(self): 
        while not self.done:                            
            self.clock.tick(self.settings.fps)  
            self.all_guns.sprite.rect.centerx, self.all_guns.sprite.rect.centery = pygame.mouse.get_pos()        
            for event in self.pygame.event.get():       
                if event.type == QUIT:                 
                    self.done = True 
            self.update()
            self.draw()

    def draw(self): 
        self.screen.blit(self.background, self.background_rect)
        self.all_enemys.draw(self.screen)
        self.all_guns.draw(self.screen)
        self.points.draw(self.screen) 
        self.pygame.display.flip()

    def update(self): 
        self.all_enemys.update()
        self.all_guns.update()
        if len(self.all_enemys) <= 8 and pygame.time.get_ticks() >= self.last_enemy_time + self.enemy_rate: 
            self.all_enemys.add(Enemy(settings, self))
            self.last_enemy_time = pygame.time.get_ticks()
        #if pygame.sprite.spritecollide(self.all_enemys, self.all_enemys, False): #Konnte leider keine kollisions erkennung hinbekommen egal was ich versucht habe, dies ist einer der fehlgeschlagenen versuche
            #self.done = True




if __name__ == '__main__':     
    settings = Settings()
    pygame.init()              
    game = Game(pygame, settings)
    game.run()  
    pygame.quit()              

