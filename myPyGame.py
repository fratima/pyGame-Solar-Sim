import pygame
import time
import random
import math
#import numpy as np
 
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

#------ Pygame stuff --------------
pygame.init()
pygame.display.set_caption("eBike SIMULATION")
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(pygame.font.get_default_font(), 12)

#------- Simulation Entity -------------
class SimObject:
    def __init__(self,x,y,vx,vy,ax,ay,m):
        self.position       = pygame.Vector2(x,y)
        self.acceleration   = pygame.Vector2(ax,ay)
        self.velocity       = pygame.Vector2(vx,vy)
        self.mass           = m
 
    def update_velocity(self, dt):
        self.velocity += (self.acceleration * dt) 
      
    def update_position(self, dt):
        self.position += (self.velocity * dt)
        if self.position[0] < 10 or self.position[0] >=  WIDTH-10:
            self.velocity[0] *= -1
        if self.position[1] < 10 or self.position[1] >= HEIGHT-10:
            self.velocity[1] *= -1 
       
#--------------------------------------
G = 6.67428e-2
numberOfElements = 5
elements = []
for i in range(numberOfElements):
    x = random.uniform(10,WIDTH-10)
    y = random.uniform(10,HEIGHT-10)
    vx = random.uniform(-5,5)
    vy = random.uniform(-5,5)
    ax = random.uniform(-1,1)
    ay = random.uniform(-1,1)
    elements.append(SimObject(x,y,vx,vy,ax,ay,100))

elements.append(SimObject(WIDTH/2, HEIGHT/2, 0,0,0,0,1000)) # add a heavy center star 

clock = pygame.time.Clock()
dt = 0 # TimeStep
aktiv = True

# Schleife Hauptprogramm
while aktiv:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            aktiv = False

     # Spielfeld löschen
    #screen.fill(SCHWARZ)
 
    # Spiellogik  
    for element1 in enumerate(elements):
        if element1[0] == numberOfElements+1: break # don't consider the heavy center star
        for element2 in elements[element1[0]+1:]:
            #Abstand zwischen Element
            dist_x = (element2.position[0] - element1[1].position[0] )
            dist_y = (element2.position[1] - element1[1].position[1] )
            dist = math.sqrt(dist_x**2 + dist_y**2)
        
            attraction = G * (element1[1].mass * element2.mass) / dist**2
            if attraction >= 1.5: attraction = 1.5  # limit acceleration
            attraction_angle = math.atan2(dist_y, dist_x)
            element1[1].acceleration.x = math.cos(attraction_angle) * attraction
            element1[1].acceleration.y = math.sin(attraction_angle) * attraction

        element1[1].update_velocity(dt)
        element1[1].update_position(dt)
     
        if element1[0] == numberOfElements : 
             pygame.draw.circle(surface= screen, color= WEISS, center=element1[1].position, radius=15)
        else:
            pygame.draw.circle(surface= screen, color= ORANGE, center=element1[1].position, radius=2)
        #posText = str(element.position)
        #text_surface = font.render(posText, True, WEISS)
        #screen.blit(text_surface, dest=element.position)
        
    
    # Fenster aktualisieren
    pygame.display.flip()
 
    # Refresh-Zeiten festlegen
    dt = clock.tick(60)/60

pygame.quit()
 
 