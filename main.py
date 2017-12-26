#!/usr/bin/env python3
import sys, time, pygame
from pygame.locals import *
pygame.init()

# todo:
#  audio overall

clock = pygame.time.Clock()
if "n" in sys.argv[1:]:
  difficulty = "n"
elif "h" in sys.argv[1:]:
  difficulty = "h"
elif "e" in sys.argv[1:]:
  difficulty = "e"
else:
  difficulty = "m"
  
# sfx
# music = pygame.mixer.music.load("")

# font
vt = pygame.font.Font("assets/font/VT323-Regular.ttf", 32)
vt_l = pygame.font.Font("assets/font/VT323-Regular.ttf", 128)

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
player = pygame.image.load("assets/ship.png") # player image for window icon
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

def center(txt):
  siz = txt.get_size()[0]
  loc = ((640 / 2) - (siz / 2))
  return loc

def game_over():
  screen.fill(bg_color)
  txt = vt.render("You didn't defeat the enemy ships!", True, dark)
  loc = center(txt), 40
  screen.blit(txt, loc)
  txt = vt.render("Press any key to try again...", True, dark)
  loc = center(txt), 440 - txt.get_size()[1]
  screen.blit(txt, loc)
  pygame.display.flip()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_ESCAPE:
          sys.exit()
        else:
          opening()
          return
    clock.tick(60)

def ending(start_time):
  finish_time = time.mktime(time.gmtime()) - time.mktime(start_time)
  m, s = divmod(finish_time, 60)
  h, m = divmod(m, 60)
  if s < 10:
    s = "0" + str(int(s))
  finish_time = "{}:{}".format(int(m), str(s))
  screen.fill(bg_color)
  txt = vt.render("Congratulations! Finished in {}.".format(finish_time), True, dark)
  loc = center(txt), 40
  screen.blit(txt, loc)
  txt = vt.render("You have beaten the enemy ships.", True, dark)
  loc = center(txt), 80
  screen.blit(txt, loc)
  if difficulty == "n":
    txt = vt.render("You are the saviour of mankind.", True, dark)
    loc = center(txt), 120
    screen.blit(txt, loc)
    txt = vt_l.render("End", True, dark)
    loc = center(txt), 440 - txt.get_size()[1]
    screen.blit(txt, loc)
  else:
    txt = vt.render("This isn't over, though...", True, dark)
    loc = center(txt), 120
    screen.blit(txt, loc)
  pygame.display.flip()
  time.sleep(2)
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_ESCAPE:
          sys.exit()
        else:
          opening()
          return
    clock.tick(60)

def opening():
  title = vt_l.render("SKYSHOT", True, bg_color, dark)
  loc = center(title), 40
  txt = vt.render("Press any key to play", True, # bg_color, 
                                                dark)
  loc2 = center(txt), 440 - txt.get_size()[1]
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == K_ESCAPE:
          sys.exit()
        else:
          main()
    screen.fill(bg_color)
    draw_bg()
    screen.blit(title, loc)
    screen.blit(txt, loc2)
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

def main():
  # variables
  if difficulty == "n":
    enemies = {
      "enemy1": { "health": 20, "damage": 2, "dir": "r", "acc": 4, "freq": 17,
        "sprite": "assets/enemy1.png", "pos": 2 },                           
      "enemy2": { "health": 30, "damage": 4, "dir": "l", "acc": 3, "freq": 31,
        "sprite": "assets/enemy2.png", "pos": 1 } ,                          
      "enemy3": { "health": 30, "damage": 4, "dir": "l", "acc": 4, "freq": 23,
        "sprite": "assets/enemy3.png", "pos": 0 } }
  elif difficulty == "h":
    enemies = {
      "enemy1": { "health": 20, "damage": 2, "dir": "r", "acc": 4, "freq": 17,
        "sprite": "assets/enemy1.png", "pos": 1 },
      "enemy2": { "health": 30, "damage": 4, "dir": "l", "acc": 3, "freq": 31,
        "sprite": "assets/enemy2.png", "pos": 0 } }
  elif difficulty == "e":
    enemies = {
      "enemy1": { "health": 10, "damage": 2, "dir": "r", "acc": 3, "freq": 31,
        "sprite": "assets/enemy1.png", "pos": 1 },
      "enemy2": { "health": 15, "damage": 3, "dir": "l", "acc": 2, "freq": 55,
        "sprite": "assets/enemy2.png", "pos": 0 } }
  else:
    enemies = {
      "enemy1": { "health": 20, "damage": 2, "dir": "r", "acc": 4, "freq": 24,
        "sprite": "assets/enemy1.png", "pos": 1 },
      "enemy2": { "health": 25, "damage": 4, "dir": "l", "acc": 2.5, "freq": 43,
        "sprite": "assets/enemy2.png", "pos": 0 } }
  location = ( 640 / 2 ) - 16
  accel = 2
  acc_m = 8
  tick = 3
  bounds = [80, 560]
  ctls = { "l": K_LEFT, "r": K_RIGHT, "f": K_z, "s": K_x }
  keys = { "l": False, "r": False, "f": False, "s": False }
  keys_s = { "l": False, "r": False, "f": False, "s": False }
  play_s = { "health": 20, "damage": 2, "spd": 2.5, "rect": pygame.Rect((320, 400),
    (player.get_size()[0] * 8, player.get_size()[1] * 8)) }
  p_bullets = []
  bullets = []
  for i in enemies:
    enemies[i]["img"] = pygame.image.load(enemies[i]["sprite"]).convert_alpha()
    enemies[i]["rect"] = enemies[i]["img"].get_rect()
    size = enemies[i]["img"].get_size()
    enemies[i]["rect"].x = 320 - size[0]
    enemies[i]["rect"].y = enemies[i]["pos"] * 40 + 8
    enemies[i]["rect"].w = size[0] * 8
    enemies[i]["rect"].h = size[1] * 8
  
  t = time.gmtime()
  
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
    
    if len(enemies) == 0:
      ending(t)
      time.sleep(3)
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
      if not len(p_bullets) >= 3:
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
      
      size = enemies[e]["img"].get_size()
      if tick % enemies[e]["freq"] == 0:
        bullets.append({ "rect": pygame.Rect((enemies[e]["rect"].x + (size[0] / 2) - 8, enemies[e]["rect"].y + 8),
        (8, 16)), "shooter": enemies[e] })
      del size
    
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
      while i < len(bullets):
        if play_s["rect"].colliderect(bullets[i]["rect"]):
          play_s["health"] -= bullets[i]["shooter"]["damage"]
          del bullets[i]
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
      if p_bullets[i].y < -128:
        del p_bullets[i]
      i += 1
    
    for e in enemies:
      size = enemies[e]["img"].get_size()
      screen.blit(pygame.transform.scale(enemies[e]["img"],
      (size[0] * 8, size[1] * 8)),
      (enemies[e]["rect"].x, enemies[e]["rect"].y))
      while i < len(bullets):
        bullets[i]["rect"].y += 8
        screen.blit(pygame.transform.scale(bullet_e, (8, 16)), (bullets[i]["rect"].x, bullets[i]["rect"].y))
        if bullets[i]["rect"].y >= 656:
          del bullets[i]
        i += 1
    
    i = 0
    ammo = abs(len(p_bullets) - 3)
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
    clock.tick(60)

opening()
