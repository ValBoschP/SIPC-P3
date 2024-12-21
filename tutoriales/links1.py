import pygame
import pymunk

# Configuración de Pygame
pygame.init()
disp_h = 800
disp_w = 600
display = pygame.display.set_mode((disp_w,disp_h))
clock = pygame.time.Clock()

# Configuración de Pymunk
space = pymunk.Space()
space.gravity = (0,-500)

FPS = 60

def convert_coordinates (point):
  return int(point[0]), disp_h - int(point[1])

class Ball():
  def __init__(self,x,y,radius = 10,color = pygame.Color("red")):
    self.radius = radius
    self.body = pymunk.Body()
    self.body.position = x,y
    self.shape = pymunk.Circle(self.body,radius)
    self.shape.elasticity = 1
    self.shape.density = 1
    self.shape.color = color
    space.add(self.body,self.shape)

  def draw(self):
    pygame.draw.circle(display,self.shape.color,convert_coordinates(self.body.position),self.radius)

class String():
  def __init__(self,body1,body2):
    self.body1 = body1
    self.body2 = body2
    joint = pymunk.PinJoint(body1,body2)    
    space.add(joint)
  def draw(self):
    pygame.draw.line(display, (0,0,0), convert_coordinates(self.body1.position),convert_coordinates(self.body2.position),2)

anchor = pymunk.Body(body_type = pymunk.Body.STATIC)
anchor.position = 300,700

ball_1 = Ball(300,450)
ball_2 = Ball(200,150)

joint_1 = String(anchor,ball_1.body)
joint_2 = String(ball_1.body,ball_2.body)


running = True
while running:
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  display.fill ((255,255,255))
  joint_1.draw()
  joint_2.draw()
  ball_1.draw()
  ball_2.draw()
  
  pygame.display.flip()

  clock.tick(FPS)

  space.step(1/FPS)

pygame.quit()