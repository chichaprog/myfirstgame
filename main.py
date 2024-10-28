import pygame

image_path = "/data/data/com.itproger.myapp/files/app/"
image_path = ""

my_clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((950,555))
pygame.display.set_caption("Pygame itProger Game")
icon = pygame.image.load(image_path + "icons/4527378_game_lightbringer_of_series_sword_icon.png").convert_alpha()


tree = pygame.image.load(image_path +"backgrounds/808841-nkjfmqva-v4.jpg").convert_alpha()
#tree = pygame.transform.scale(tree, (800, 600)) // Растянуть под определенный размер


walk_left = [ pygame.transform.scale(pygame.image.load(image_path + "spriters/hero/sprite-4.png"), (50,72)).convert_alpha(),
             pygame.transform.scale(pygame.image.load(image_path + "spriters/hero/sprite-5.png"), (50,72)).convert_alpha(),
             pygame.transform.scale(pygame.image.load(image_path + "spriters/hero/sprite-6.png"), (50,72)).convert_alpha()
]
walk_right = [ pygame.transform.scale(pygame.image.load(image_path + "spriters/hero/sprite-7.png"), (50,72)).convert_alpha(),
             pygame.transform.scale(pygame.image.load(image_path + "spriters/hero/sprite-8.png"), (50,72)).convert_alpha(),
             pygame.transform.scale(pygame.image.load(image_path + "spriters/hero/sprite-9.png"), (50,72)).convert_alpha()
]



ghost = pygame.image.load(image_path +"myghost/ghost.png").convert_alpha()

ghost_list_in_game = []

player_anim_count = 0
tree_x = 0

player_speed = 5
player_x = 150
player_y = 400

is_jamp = False
jump_count = 9

tree_music = pygame.mixer.Sound(image_path +"musics/coniferous-forest-142569.mp3")
tree_music.play()

ghost_timer =  pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer,3000)

label = pygame.font.Font(image_path + "fonts/Roboto-Black.ttf",40)
lose_label = label.render("You lose!",False,(193,196,199))
restart_label = label.render("Play again",False,(115,132,148))
restart_label_rect = restart_label.get_rect(topleft=(200,200))

bullets_left = 50
bullet = pygame.image.load(image_path + "bullet/bullet.png").convert_alpha()
bullets = []

gameplay = True

running = True
while running:

   screen.blit(tree, (tree_x,0))
   screen.blit(tree, (tree_x + 950, 0))

   if gameplay:

       player_rect = walk_left[2].get_rect(topleft=(player_x, player_y))

       if ghost_list_in_game:
           for (i,el) in enumerate(ghost_list_in_game):
               screen.blit(ghost, el)
               el.x -= 10

               if el.x < -10:
                   ghost_list_in_game.pop(i)

               if player_rect.colliderect(el):
                  gameplay = False

       keys = pygame.key.get_pressed()

       if keys[pygame.K_LEFT]:
           screen.blit(walk_left[player_anim_count], (player_x, player_y))
       else:
           screen.blit(walk_right[player_anim_count], (player_x,player_y))

       if keys[pygame.K_LEFT] and player_x > 50:
           player_x -= player_speed
       elif keys[pygame.K_RIGHT] and player_x < 600:
           player_x += player_speed

       if not is_jamp:
           if keys[pygame.K_SPACE]:
               is_jamp = True

       else:
           if jump_count >= -9:
               if jump_count > 0:
                   player_y -= (jump_count ** 2) / 2

               else:
                   player_y += (jump_count ** 2) / 2
               jump_count -= 1

           else:
               is_jamp = False
               jump_count = 9

       if player_anim_count == 2:
           player_anim_count = 0
       else:
           player_anim_count += 1

       tree_x -= 2
       if tree_x == -950:
           tree_x = 0


       if bullets:
           for (i,el) in enumerate(bullets):
               screen.blit(bullet,(el.x, el.y))
               el.x += 4

               if el.x > 950:
                   bullets.pop(i)

               if ghost_list_in_game:
                   for (index,ghost_el) in enumerate(ghost_list_in_game):
                       if el.colliderect(ghost_el):
                           ghost_list_in_game.pop(index)
                           bullets.pop(i)


   else:
       screen.fill((87,88,89))
       screen.blit(lose_label,(200,100))
       screen.blit(restart_label,restart_label_rect)

       mouse = pygame.mouse.get_pos()
       if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
           gameplay = True
           player_x = 150
           ghost_list_in_game.clear()
           bullets.clear()

   pygame.display.update()

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
           pygame.quit()

       if event.type == ghost_timer:
           ghost_list_in_game.append(ghost.get_rect(topleft =(900,400)))
       if gameplay and event.type  == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0 :
           bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))

           bullets_left -= 1

   my_clock.tick(15)