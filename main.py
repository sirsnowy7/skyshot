# Skyshot Shooter 0.1.0
# Simple game made in Python with Pygame. Uses a font from Google
# and original graphics. Currently in alpha, and is not playable.

import sys, time, pygame
from pygame.locals import *
pygame.init()

# gameplay
location = ( 640 / 2 ) - 16
accel = 2
ctls = { "l": K_LEFT, "r": K_RIGHT, "f": K_z, "s": K_x }
keys = { "l": False, "r": False, "f": False, "s": False }
play_s = { "health": 20, "damage": 2 }
enemy1 = { "health": 20, "damage": 4, "sprite": "assets/enemy1.png" }
enemy2 = { "health": 30, "damage": 2, "sprite": "assets/enemy2.png" }

# colors
bg_color = 244, 244, 244
dark = 20, 20, 20

# screen
s_size = width, height = 640, 480
screen = pygame.display.set_mode(s_size)

# images
player = pygame.image.load("assets/ship.png")
enemy_w = pygame.image.load("assets/enemy1.png")
enemy_t = pygame.image.load("assets/enemy2.png")
pygame.display.set_caption("Skyshot")

# font
vt = pygame.font.Font("assets/font/VT323-Regular.ttf", 32)

clock = 0

def game_over():
  screen.fill(bg_color)
  txt = vt.render("You didn't defeat the enemy ships! Heheh...", True, dark)
  siz = txt.get_size()[0]
  loc = ((640 / 2) - (siz / 2)), 40
  screen.blit(txt, loc)
  pygame.display.flip()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_ESCAPE:
          sys.exit()

while True:
  clock += 1

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    if event.type == pygame.KEYUP:
      for ctl in ctls:
        if event.key == ctls[ctl]:
          keys[ctl] = False

    if event.type == pygame.KEYDOWN:
      if event.key == K_ESCAPE:
        sys.exit()
      for ctl in ctls:
        if event.key == ctls[ctl]:
          keys[ctl] = True

  if play_s["health"] <= 0:
    game_over()
    break
  
  if (keys["l"] or keys["r"]) == True:
    if keys["l"]:
      location -= 5 + accel
      accel += 1
    if keys["r"]:
      location += 5 + accel
      accel += 1
  elif accel >= 1:
    accel -= 2
  elif accel <= -1:
    accel += 2

  if accel >= 10:
    accel = 10
  elif accel <= -10:
    accel = -10

  if location > 600:
    location = 600
  elif location < 40:
    location = 40

  r_location = location, 400
  
  screen.fill(bg_color)
  screen.blit(pygame.transform.scale(player, (32, 64)), r_location)
  pygame.display.flip()
  
  print(clock, keys["l"], keys["r"], keys["f"], keys["s"], accel )
  time.sleep(0.1)
