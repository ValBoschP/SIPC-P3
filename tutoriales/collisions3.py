import pygame
import pymunk
import random



disp_w = 600
disp_h = 600
n_balls = 50

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
  def __init__(self,x,y,radius = 10,collision_type = 1):
    self.radius = radius
    self.collision_type = collision_type
    self.body = pymunk.Body()
    self.body.position = x,y
    self.body.velocity = random.uniform (-400,400),random.uniform (-400,400)
    self.shape = pymunk.Circle(self.body,radius)
    self.shape.elasticity = 1
    self.shape.density = 1
    self.shape.collision_type = collision_type
    space.add(self.body,self.shape)

  def draw(self):
    color = (0,0,0)
    if self.collision_type == 1:
      color = (255,0,0)
    elif self.collision_type == 2:
      color = (0,0,255)
    pygame.draw.circle(display,color,convert_coordinates(self.body.position),self.radius)

balls = [Ball(random.randint(20,disp_w-20),random.randint(20,disp_h-20)) for x in range(n_balls)]
balls.append(Ball(random.randint(20,disp_w-20),random.randint(20,disp_h-20),collision_type=2))
segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0,0),(disp_w,0),5)
segment_shape.elasticity = 1
space.add(segment_body, segment_shape)

segment_body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape2 = pymunk.Segment(segment_body2, (0,disp_h),(disp_w,disp_h),5)
segment_shape2.elasticity = 1
space.add(segment_body2, segment_shape2)

segment_body3 = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape3 = pymunk.Segment(segment_body3, (0,0),(0,disp_h),5)
segment_shape3.elasticity = 1
space.add(segment_body3, segment_shape3)

segment_body4 = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape4 = pymunk.Segment(segment_body4, (disp_w,0),(disp_w,disp_h),5)
segment_shape4.elasticity = 1
space.add(segment_body4, segment_shape4)


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
  for ball in balls:
    ball.draw()
  

  pygame.draw.line(display, (0,0,0),convert_coordinates((0,0)),convert_coordinates((disp_w,0)),9) 
  pygame.draw.line(display, (0,0,0),convert_coordinates((0,disp_h)),convert_coordinates((disp_w,disp_h)),9) 
  pygame.draw.line(display, (0,0,0),convert_coordinates((0,0)),convert_coordinates((0,disp_h)),9) 
  pygame.draw.line(display, (0,0,0),convert_coordinates((disp_w,0)),convert_coordinates((disp_w,disp_h)),9) 
  pygame.display.flip()
  clock.tick(FPS)

  
pygame.quit()
  