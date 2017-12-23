#!/usr/bin/env python3
import sys, pygame
from pygame.locals import *
pygame.init()

# ideas:
# use l and r bound to track boundaries

# gameplay
location = ( 640 / 2 ) - 16
accel = 2
acc_m = 8
tick = 0
bounds = [80, 560]
ctls = { "l": K_LEFT, "r": K_RIGHT, "f": K_z, "s": K_x }
keys = { "l": False, "r": False, "f": False, "s": False }
keys_s = { "l": False, "r": False, "f": False, "s": False }
play_s = { "health": 20, "damage": 2 }
enemies = {
  "enemy1": { "health": 20, "damage": 4, "dir": "r", "acc": 8,
    "sprite": "assets/enemy1.png" },
  "enemy2": { "health": 30, "damage": 2, "dir": "l", "acc": 6,
    "sprite": "assets/enemy2.png" } }
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
pos = 16
for i in enemies:
  enemies[i]["img"] = pygame.image.load(enemies[i]["sprite"])
  enemies[i]["rect"] = enemies[i]["img"].get_rect()
  size = enemies[i]["img"].get_size()
  enemies[i]["rect"].x = 320 - size[0]
  enemies[i]["rect"].y = pos
  enemies[i]["rect"].w = size[0] * 8
  enemies[i]["rect"].h = size[1] * 8
  pos += 48
del pos

# sfx
# music = pygame.mixer.music.load("")

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
      p_bullets.append({"h": 400, "w": location + 8, "r": pygame.Rect((location + 8, 400), (8, 16))})
  
  enemies_new = enemies.copy()
  for e in enemies:
    if enemies[e]["health"] <= 0:
      del enemies_new[e]
  
  enemies = enemies_new.copy()
  del enemies_new
  
  for e in enemies:
    if enemies[e]["dir"] == "l":
      enemies[e]["rect"].x -= enemies[e]["acc"]
    elif enemies[e]["dir"] == "r":
      enemies[e]["rect"].x += enemies[e]["acc"]
    
    if enemies[e]["rect"].x > bounds[1]:
      enemies[e]["rect"].x = bounds[1]
      enemies[e]["dir"] = "l"
    elif enemies[e]["rect"].x < bounds[0]:
      enemies[e]["rect"].x = bounds[0]
      enemies[e]["dir"] = "r"
  
  i = 0
  while i < len(p_bullets):
    for e in enemies:
      if p_bullets[i]["r"].colliderect(enemies[e]["rect"]):
        enemies[e]["health"] -= play_s["damage"]
        del p_bullets[i]
        break
    i += 1

  if accel >= acc_m:
    accel = acc_m
  elif accel <= -acc_m:
    accel = -acc_m

  if location > bounds[1]:
    location = bounds[1]
  elif location < bounds[0]:
    location = bounds[0]
  
  r_location = location, 400
  
  # drawing
  screen.fill(bg_color)
  
  draw_bg()
  
  i = 0
  while i < len(p_bullets):
    p_bullets[i]["h"] -= 16
    p_bullets[i]["r"].y -= 16
    screen.blit(pygame.transform.scale(bullet_p, (8, 16)), (p_bullets[i]["w"], p_bullets[i]["h"]))
    if p_bullets[i]["h"] < -32:
      del p_bullets[i]
    i += 1
  
  for e in enemies:
    size = enemies[e]["img"].get_size()
    screen.blit(pygame.transform.scale(enemies[e]["img"],
    (size[0] * 8, size[1] * 8)),
    (enemies[e]["rect"].x, enemies[e]["rect"].y))
  
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
