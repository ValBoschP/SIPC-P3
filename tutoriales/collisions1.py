import pygame
import pymunk
import random



disp_w = 600
disp_h = 600
# Configuración de Pygame
pygame.init()
display = pygame.display.set_mode((disp_w, disp_h))
clock = pygame.time.Clock()

# Configuración de Pymunk
space = pymunk.Space()

FPS = 50

def convert_coordinates (point):
  return int(point[0]), disp_h - int(point[1])

class Ball():
  def __init__(self,x,y,radius=10):
    self.radius = radius
    self.body = pymunk.Body()
    self.body.position = x,y
    self.body.velocity = random.uniform (-400,400),random.uniform (-400,400)
    self.shape = pymunk.Circle(self.body,radius)
    self.shape.elasticity = 1
    self.shape.density = 1
    space.add(self.body,self.shape)

  def draw(self):
    pygame.draw.circle(display,(255,0,0),convert_coordinates(self.body.position),self.radius)

ball = Ball(100,100)
ball2 = Ball(100,300)

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Avanzar la simulación de Pymunk
  space.step(1 / FPS)
  # Renderizar el objeto en Pygame
  display.fill((255, 255, 255))
  ball.draw()
  ball2.draw()
  
  pygame.display.flip()
  clock.tick(FPS)

  
pygame.quit()
  