import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d



# Configuración de Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Configuración de Pymunk
space = pymunk.Space()
space.gravity = (0, 1000)

body = pymunk.Body()
body.position = (20, 420)  # Posición inicial en el centro
circle = pymunk.Circle(body, 20)
circle.density = 1
circle.friction = 0.3
space.add(body, circle)

#Cajas
for y in range(6):       
  size = 20
  box_body = pymunk.Body()
  box_body.position = (500, 440 - y * (size + 0.1))
  box_shape = pymunk.Poly.create_box(box_body, (size, size))
  box_shape.density = 1
  box_shape.friction = 0.3
  space.add(box_body, box_shape)

# Body y shape del suelo
segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0,450),(640,450),5)
#segment_shape.elasticity = 1
segment_shape.friction = 0.3
space.add(segment_body, segment_shape)


running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  
  keys = pygame.key.get_pressed()

  if keys[pygame.K_SPACE]:
    #body.angle = Vec2d(1,-1).angle
    impulse = 100000 * Vec2d(1,-1)
    #impulse = impulse.rotated(body.angle)
    
    body.apply_impulse_at_world_point(impulse, body.position)
        
        
      
  # Avanzar la simulación de Pymunk
  space.step(1 / 60.0)
  # Renderizar el objeto en Pygame
  screen.fill((255, 255, 255))
  space.debug_draw(draw_options)
  #pygame.draw.circle(screen, (0, 0, 255), (int(body.position.x), int(body.position.y)), int(circle.radius))
  
  pygame.display.flip()
  clock.tick(60)

  
pygame.quit()
  