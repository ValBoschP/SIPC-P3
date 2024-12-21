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

# Body y shape de la pelota
body = pymunk.Body()
body.position = (300,600)
shape = pymunk.Circle(body, 20) 
shape.density = 1 # Con la densidad, y a través del radio, pymunk calcula la masa
space.add(body,shape)

# Body y shape del suelo
segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0,50),(disp_w,50),5)
space.add(segment_body, segment_shape)


running = True
while running:
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  display.fill ((255,255,255))
  pygame.draw.circle(display, (255,0,0), (int(body.position.x), disp_h - int(body.position.y)), int(shape.radius))
  pygame.draw.line(display, (0,0,0),(0,disp_h - 50),(disp_w,disp_h - 50),9) #el ancho del segmento dibujado no coincide con el ancho del segmento en pymunk
  pygame.display.flip()
  clock.tick(FPS)

  space.step(1/FPS)

pygame.quit()