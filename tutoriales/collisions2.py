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

def collide(arbiter,space,data):
  print("Hello")

class Ball():

  def __init__(self,x,y,radius = 10,collision_type = 1, up = 1):
    self.radius = radius
    self.body = pymunk.Body()
    self.body.position = x,y
    #self.body.velocity = random.uniform (-400,400),random.uniform (-400,400)
    self.body.velocity = 0,up*100
    self.shape = pymunk.Circle(self.body,radius)
    self.shape.elasticity = 1
    self.shape.density = 1
    self.shape.collision_type = collision_type
    space.add(self.body,self.shape)

  def draw(self):
    pygame.draw.circle(display,(255,0,0),convert_coordinates(self.body.position),self.radius)

ball = Ball(100,100,collision_type=1)
ball2 = Ball(100,500,collision_type=2,up=-1)

segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0,50),(disp_w,50),5)
segment_shape.elasticity = 1
space.add(segment_body, segment_shape)

segment_body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape2 = pymunk.Segment(segment_body2, (0,disp_h - 50),(disp_w,disp_h - 50),5)
segment_shape2.elasticity = 1
space.add(segment_body2, segment_shape2)

handler = space.add_collision_handler(1,2)
handler.separate = collide

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

  pygame.draw.line(display, (0,0,0),convert_coordinates((0,50)),convert_coordinates((disp_w,50)),9) 
  pygame.draw.line(display, (0,0,0),convert_coordinates((0,disp_h - 50)),convert_coordinates((disp_w,disp_h - 50)),9) 

  pygame.display.flip()
  clock.tick(FPS)

  
pygame.quit()
  