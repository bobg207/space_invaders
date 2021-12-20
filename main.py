import pygame
import random
from settings import *
from sprites import Player, Block, Enemy, Missile, Bomb, Explosion, UFO


pygame.init()

def game_start():
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Space Invaders")

    # background image
    bg_img = pygame.image.load("assets/background-black.png")
    bg_img = pygame.transform.scale(bg_img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    game_name = LRG_FONT_BLD.render(f"Space Invaders", True, BLOCK_WEAK)
    game_name_rect = game_name.get_rect()
    game_name_rect.center = DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2
    start_img = pygame.image.load("assets/space_inv.png").convert()
    started = False

    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  started = True

        screen.fill(BLACK)

        screen.blit(bg_img, (0, 0))
        screen.blit(game_name, game_name_rect)

        pygame.display.flip()

        clock.tick(FPS)


def game_over():
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    running = True

    # background image
    bg_img = pygame.image.load("assets/background-black.png")
    bg_img = pygame.transform.scale(bg_img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    font_obj = pygame.font.Font("assets/unifont.ttf", 32)
    score_obj = font_obj.render(f"Score: 0", True, WHITE)
    hi_score_obj = font_obj.render(f"Hi Score: 5342", True, WHITE)
    score_rect = score_obj.get_rect()
    hi_score_rect = hi_score_obj.get_rect()
    score_rect.center = 100, 20
    hi_score_rect.center = DISPLAY_WIDTH - 150, 20

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        screen.fill(BLACK)

        screen.blit(bg_img, (0, 0))
        screen.blit(score_obj, score_rect)
        screen.blit(hi_score_obj, hi_score_rect)

        pygame.display.flip()

        clock.tick(FPS)

    return False

def play():
    score = 0
    hi_score = 4356
    lives_remaining = 3
    running = True
    enemy_direction = 1

    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Space Invaders")

    # background image
    bg_img = pygame.image.load("assets/background-black.png")
    bg_img = pygame.transform.scale(bg_img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # font
    font_obj = pygame.font.Font("assets/unifont.ttf", 32)
    score_obj = font_obj.render(f"Score:{score}", True, WHITE)
    hi_score_obj = font_obj.render(f"Hi Score:{hi_score}", True, WHITE)
    score_rect = score_obj.get_rect()
    hi_score_rect = hi_score_obj.get_rect()
    score_rect.center = 100, 20
    hi_score_rect.center = DISPLAY_WIDTH-150, 20

    # Sounds
    player_fire = pygame.mixer.Sound("assets/shoot.wav")
    enemy_hit = pygame.mixer.Sound("assets/invaderkilled.wav")
    player_hit = pygame.mixer.Sound("assets/player_killed.wav")
    ufo_flying = pygame.mixer.Sound("assets/ufo_lowpitch.wav")
    ufo_flying.set_volume(.15)

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    missile_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    explode_group = pygame.sprite.Group()
    ufo_group = pygame.sprite.Group()
    lives_group = pygame.sprite.Group()

    # Player
    player = Player(DISPLAY_WIDTH//2, DISPLAY_HEIGHT - 125)
    player_group.add(player)
    all_sprites.add(player)

    # Create Aliens
    x_offset = DISPLAY_WIDTH // 10
    y_offset = DISPLAY_HEIGHT // 5
    h_scale = DISPLAY_WIDTH // 15
    v_scale = DISPLAY_HEIGHT // 18
    for row in range(5):
        if row <= 1: image_path = GREEN_ALIEN
        elif row <= 3: image_path = YELLOW_ALIEN
        else: image_path = RED_ALIEN
        for col in range(10):
            x_pos = col*h_scale + x_offset
            y_pos = row*v_scale + y_offset
            enemy = Enemy(x_pos, y_pos, image_path)
            enemy_group.add(enemy)

    # Create Sheilds
    sheild_amount = 4
    start_x = [num*(DISPLAY_WIDTH/(sheild_amount+1))+1.5*x_offset for num in range(sheild_amount)]
    for start in start_x:
        for row in range(len(SHEILD)):
            for col in range(len(SHEILD[row])):
                if SHEILD[row][col] == 'x':
                    x_pos = col*BLOCK_WIDTH + start
                    y_pos = row*BLOCK_HEIGHT + 600
                    block = Block(screen, x_pos, y_pos)
                    block_group.add(block)
                    all_sprites.add(block)

    # player lives images
    for i in range(lives_remaining):
        player_life = Player(60 * (i) + 10*i, DISPLAY_HEIGHT - 45)
        lives_group.add(player_life)

    clock = pygame.time.Clock()
    miss_prev_time = pygame.time.get_ticks()
    bomb_prev_time = pygame.time.get_ticks()
    ufo_prev_time = pygame.time.get_ticks()
    ufo_prev_drop = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # Shooting missiles from player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    miss_current_time = pygame.time.get_ticks()
                    if miss_current_time - miss_prev_time > MISSILE_DELAY:
                        miss_prev_time = miss_current_time
                        m_x = player.rect.centerx - .5 * MISSILE_WIDTH
                        m_y = player.rect.centery
                        missile = Missile(screen, m_x, m_y)
                        missile_group.add(missile)
                        all_sprites.add(missile)
                        player_fire.play()

        # Check for collisions
        collide_missile_enemy = pygame.sprite.groupcollide(missile_group, enemy_group, True, True)    # b/w missiles and aliens
        collide_block_enemy = pygame.sprite.groupcollide(block_group, enemy_group, True, False)  # b/w aliens and blockers
        collide_bomb_block = pygame.sprite.groupcollide(block_group, bomb_group, True, True)
        collide_player_enemy = pygame.sprite.spritecollide(player, enemy_group, True) # b/w player and aliens
        collide_shield_missile = pygame.sprite.groupcollide(missile_group, block_group, True, True)
        # collide_shield_bomb = pygame.sprite.groupcollide(bomb_group, block_group, True, True)
        # collide_bomb_player = pygame.sprite.spritecollide(player, bomb_group, True)

        # player v. bomb collisions
        for bomb in bomb_group:
            bomb_hit = pygame.sprite.collide_circle(player, bomb)
            if bomb_hit:
                bomb.kill()
                player_hit.play()
                lives_remaining -= 1
                lives_group.sprites()[lives_remaining].kill()
                explode = Explosion(player.rect.center)
                explode_group.add(explode)
                all_sprites.add(explode)
                # pygame.time.delay(3000)

        # missile v. enemy collisions
        if collide_missile_enemy:
            score += 10
            enemy_hit.play()
            for hit in collide_missile_enemy:
                explode = Explosion(hit.rect.center)
                explode_group.add(explode)
                all_sprites.add(explode)

        # player v enemy collisions
        if collide_player_enemy or lives_remaining == 0:       # or collide_bomb_player
            running = False

        # UFO's
        if not ufo_group:
            ufo = UFO()
            ufo_group.add(ufo)
            all_sprites.add(ufo)

        if ufo_group:
            # ufo_flying.play()
            pass
        # ufo bombs
        ufo_current_drop = pygame.time.get_ticks()
        if ufo_current_drop - ufo_prev_drop > UFO_BOMB_DELAY and ufo_group:
            active_ufo = ufo_group.sprites()[0]
            ufo_prev_drop = ufo_current_drop
            ufo_bomb = Bomb(active_ufo.rect.centerx, active_ufo.rect.bottom)
            bomb_group.add(ufo_bomb)
            all_sprites.add(ufo_bomb)

        # Alien bombs
        bomb_current_time = pygame.time.get_ticks()
        if bomb_current_time - bomb_prev_time > BOMB_DELAY:
            bomb_prev_time = bomb_current_time
            rand_enemy = random.choice(list(enemy_group))
            ufo_bomb = Bomb(rand_enemy.rect.centerx, rand_enemy.rect.bottom)
            bomb_group.add(ufo_bomb)
            all_sprites.add(ufo_bomb)

        # Alien movement
        enemies = enemy_group.sprites()
        if enemies[8]:
            print(enemies[8].rect.y)
        for enemy in enemies:
            if enemy.rect.right >= DISPLAY_WIDTH-20:
                enemy_direction = -1


                for alien in enemies:
                    alien.rect.y += 2

            elif enemy.rect.x <= 20:
                enemy_direction = 1


                for alien in enemies:
                    alien.rect.y += 2

        screen.fill(BLACK)

        # Drawing all assets, order matters
        screen.blit(bg_img, (0, 0))
        bomb_group.draw(screen)
        missile_group.draw(screen)
        enemy_group.draw(screen)
        block_group.draw(screen)
        player_group.draw(screen)
        explode_group.draw(screen)
        ufo_group.draw(screen)
        lives_group.draw(screen)

        score_obj = font_obj.render(f"Score:{score}", True, WHITE)
        screen.blit(score_obj, score_rect)
        screen.blit(hi_score_obj, hi_score_rect)
        pygame.draw.rect(screen, WHITE, (0, 740, 700, 5))  # lower boundary

        # updating all assets
        enemy_group.update(enemy_direction)
        all_sprites.update()



        pygame.display.flip()

        clock.tick(FPS)


game_start()
playing = True
while playing:
    play()
    playing = game_over()
pygame.quit()
