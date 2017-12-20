# Skyshot Shooter 0.1.0
# Simple game made in Python with Pygame. Uses a font from Google
# and original graphics. Currently in alpha, and is not playable.

import sys, pygame
from pygame.locals import *
pygame.init()

# gameplay
location = ( 640 / 2 ) - 16
accel = 2
acc_m = 8
tick = 0
ctls = { "l": K_LEFT, "r": K_RIGHT, "f": K_z, "s": K_x }
keys = { "l": False, "r": False, "f": False, "s": False }
keys_s = { "l": False, "r": False, "f": False, "s": False }
play_s = { "health": 20, "damage": 2 }
enemies = { "enemy1": { "health": 20, "damage": 4, "sprite": "assets/enemy1.png" },
  "enemy2": { "health": 30, "damage": 2, "sprite": "assets/enemy2.png" } }
p_bullets = []
bullets = []
clock = pygame.time.Clock()

# colors
bg_color = 244, 244, 244
dark = 20, 20, 20
red = 238, 32, 77
purple = 91, 37, 197
purple_light = 152, 125, 198

# images
player = pygame.image.load("assets/ship.png")
health = pygame.image.load("assets/health.png")
enemy_w = pygame.image.load("assets/enemy1.png")
enemy_t = pygame.image.load("assets/enemy2.png")
bullet_p = pygame.image.load("assets/bullet1.png")
bullet_e = pygame.image.load("assets/bullet2.png")
land = { "img": pygame.image.load("assets/forest.png"), "pos1": 0, "pos2":-480 }
cloud = { "img": pygame.image.load("assets/clouds.png"), "pos1": -480, "pos2": -1440 }
cloud_ac = 32

# screen
s_size = width, height = 640, 480
screen = pygame.display.set_mode(s_size)
pygame.display.set_caption("Skyshot")
pygame.display.set_icon(pygame.transform.scale(player, (32, 48)))

# font
vt = pygame.font.Font("assets/font/VT323-Regular.ttf", 32)
vt_l = pygame.font.Font("assets/font/VT323-Regular.ttf", 128)

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
    clock.tick(30)

def opening():
  title = vt_l.render("SKYSHOT", True, bg_color, dark)
  siz = title.get_size()[0]
  loc = ((640 / 2) - (siz / 2)), 40
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_ESCAPE:
          sys.exit()
        else:
          return
    screen.fill(bg_color)
    draw_bg()
    screen.blit(title, loc)
    pygame.display.flip()
    clock.tick(30)

def draw_bg():
    cloud["pos1"] += cloud_ac
    if cloud["pos1"] >= 480:
      cloud["pos1"] = -1440
    
    cloud["pos2"] += cloud_ac
    if cloud["pos2"] >= 480:
      cloud["pos2"] = -1440
  
    land["pos1"] += cloud_ac / 4
    if land["pos1"] >= 480:
      land["pos1"] = -480
  
    land["pos2"] += cloud_ac / 4
    if land["pos2"] >= 480:
      land["pos2"] = -480
  
    screen.blit(land["img"], (0, land["pos1"]))  
    screen.blit(land["img"], (0, land["pos2"]))
    screen.blit(cloud["img"], (0, cloud["pos1"]))
    screen.blit(cloud["img"], (0, cloud["pos2"]))

opening()
while True:
  tick += 1

  for key in keys_s:
    keys_s[key] = False

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
          keys_s[ctl] = True

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
  
  if keys_s["f"] == True:
    if not len(p_bullets) >= 4:
      p_bullets.append({"h": 400, "w": location + 8})

  if accel >= acc_m:
    accel = acc_m
  elif accel <= -acc_m:
    accel = -acc_m

  if location > 600:
    location = 600
  elif location < 40:
    location = 40
  
  r_location = location, 400
  
  # drawing
  screen.fill(bg_color)
  
  draw_bg()
  
  i = 0
  while i < len(p_bullets):
    p_bullets[i]["h"] -= 16
    screen.blit(pygame.transform.scale(bullet_p, (8, 16)), (p_bullets[i]["w"], p_bullets[i]["h"]))
    if p_bullets[i]["h"] < -32:
      del p_bullets[i]
    i += 1

  i = 0
  ammo = abs(len(p_bullets) - 4)
  spot = 8
  while i < ammo:
    screen.blit(pygame.transform.scale(bullet_p, (8, 16)), (spot, 432))
    spot += 16
    i += 1

  screen.blit(pygame.transform.scale(health, (24, 24)), (8, 452))
  screen.blit(vt.render(str(play_s["health"]), True, purple), (36, 448))

  screen.blit(pygame.transform.scale(player, (32, 48)), r_location)
  pygame.display.flip()

  clock.tick(30)
