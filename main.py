#!/usr/bin/env python3
import sys, pygame
from pygame.locals import *
pygame.init()

# todo:
#  let enemies turn
#  enable damage boosting A.K.A. invicibility period
#  audio overall
#  fix flickering bullets
#! add a win screen

# gameplay
location = ( 640 / 2 ) - 16
accel = 2
acc_m = 8
tick = 3
bounds = [80, 560]
ctls = { "l": K_LEFT, "r": K_RIGHT, "f": K_z, "s": K_x }
keys = { "l": False, "r": False, "f": False, "s": False }
keys_s = { "l": False, "r": False, "f": False, "s": False }
player = pygame.image.load("assets/ship.png")
play_s = { "health": 20, "damage": 2, "spd": 2.5, "rect": pygame.Rect((320, 400), (player.get_size()[0] * 8, player.get_size()[1] * 8)) }
enemies = {
  "enemy1": { "health": 20, "damage": 4, "dir": "r", "acc": 4, "turn": 400,
    "bullets": [], "freq": 17,
    "sprite": "assets/enemy1.png" },
  "enemy2": { "health": 30, "damage": 2, "dir": "l", "acc": 3, "turn": 0,
    "bullets": [], "freq": 31,
    "sprite": "assets/enemy2.png" } }
p_bullets = []
clock = pygame.time.Clock()

# colors
bg_color = 244, 244, 244
dark = 20, 20, 20
red = 238, 32, 77
purple = 91, 37, 197
purple_light = 152, 125, 198

# screen
s_size = width, height = 640, 480
screen = pygame.display.set_mode(s_size, HWSURFACE|DOUBLEBUF)
pygame.display.set_caption("Skyshot")
pygame.display.set_icon(pygame.transform.scale(player, (32, 48)))

# images
health = pygame.image.load("assets/health.png").convert_alpha()
enemy_w = pygame.image.load("assets/enemy1.png").convert_alpha()
enemy_t = pygame.image.load("assets/enemy2.png").convert_alpha()
bullet_p = pygame.image.load("assets/bullet1.png").convert_alpha()
bullet_e = pygame.image.load("assets/bullet2.png").convert_alpha()
land = { "img": pygame.image.load("assets/forest.png").convert_alpha(), "pos1": 0, "pos2":-480 }
cloud = { "img": pygame.image.load("assets/clouds.png").convert_alpha(), "pos1": -480, "pos2": -1440 }
cloud_ac = 16
pos = 16
for i in enemies:
  enemies[i]["img"] = pygame.image.load(enemies[i]["sprite"]).convert_alpha()
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

# font
vt = pygame.font.Font("assets/font/VT323-Regular.ttf", 32)
vt_l = pygame.font.Font("assets/font/VT323-Regular.ttf", 128)

def game_over():
  screen.fill(bg_color)
  txt = vt.render("You didn't defeat the enemy ships!", True, dark)
  siz = txt.get_size()[0]
  loc = ((640 / 2) - (siz / 2)), 40
  screen.blit(txt, loc)
  # txt = vt.render("press any key to try again...", True, dark)
  # siz = txt.get_size()[0]
  # loc = ((640 / 2) - (siz / 2)), 360
  # screen.blit(txt, loc)
  pygame.display.flip()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_ESCAPE:
          sys.exit()
        # else:
        #   opening()
        #   return
    clock.tick(60)

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
    clock.tick(60)

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
      location -= play_s["spd"] + accel
      accel += 0.5
    if keys["r"]:
      location += play_s["spd"] + accel
      accel += 0.5
  elif accel >= 0.5:
    accel -= 1
  elif accel <= -0.5:
    accel += 1
  
  if keys_s["f"] == True:
    if not len(p_bullets) >= 4:
      p_bullets.append(pygame.Rect((location + 8, 400), (8, 16)))
  
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
    
    if enemies[e]["rect"].x > bounds[1] - enemies[e]["rect"].w:
      enemies[e]["rect"].x = bounds[1] - enemies[e]["rect"].w
      enemies[e]["dir"] = "l"
    elif enemies[e]["rect"].x < bounds[0]:
      enemies[e]["rect"].x = bounds[0]
      enemies[e]["dir"] = "r"
    
    if tick % enemies[e]["freq"] == 0:
      enemies[e]["bullets"].append(pygame.Rect((enemies[e]["rect"].x + (enemies[e]["rect"].w // 2), enemies[e]["rect"].y - 8),
      (enemies[e]["img"].get_size()[0], enemies[e]["img"].get_size()[1])))
  
  i = 0
  while i < len(p_bullets):
    for e in enemies:
      if p_bullets[i].colliderect(enemies[e]["rect"]):
        enemies[e]["health"] -= play_s["damage"]
        del p_bullets[i]
        break
    i += 1
  
  for e in enemies:
    i = 0
    while i < len(enemies[e]["bullets"]):
      if play_s["rect"].colliderect(enemies[e]["bullets"][i]):
        play_s["health"] -= enemies[e]["damage"]
        del enemies[e]["bullets"][i]
        break
      i += 1
  
  if accel >= acc_m:
    accel = acc_m
  elif accel <= -acc_m:
    accel = -acc_m

  if location > bounds[1] - (player.get_size()[0] * 8):
    location = bounds[1] - (player.get_size()[0] * 8)
  elif location < bounds[0]:
    location = bounds[0]
  
  play_s["rect"].x = location
  
  # drawing
  screen.fill(bg_color)
  
  draw_bg()
  
  i = 0
  while i < len(p_bullets):
    p_bullets[i].y -= 8
    screen.blit(pygame.transform.scale(bullet_p, (8, 16)), (p_bullets[i].x, p_bullets[i].y))
    if p_bullets[i].y < -32:
      del p_bullets[i]
    i += 1
  
  for e in enemies:
    size = enemies[e]["img"].get_size()
    screen.blit(pygame.transform.scale(enemies[e]["img"],
    (size[0] * 8, size[1] * 8)),
    (enemies[e]["rect"].x, enemies[e]["rect"].y))
    while i < len(enemies[e]["bullets"]):
      enemies[e]["bullets"][i].y += 8
      screen.blit(pygame.transform.scale(bullet_e, (8, 16)), (enemies[e]["bullets"][i].x, enemies[e]["bullets"][i].y))
      if enemies[e]["bullets"][i].y >= 640:
        del enemies[e]["bullets"][i]
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

  screen.blit(pygame.transform.scale(player, (32, 48)), (play_s["rect"].x, play_s["rect"].y))
  pygame.display.flip()
  
  tick += 1 
  print(clock.get_fps())
  clock.tick(60)
