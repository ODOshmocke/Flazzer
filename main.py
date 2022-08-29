import pygame
import sys
import random
from time import sleep

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x += 5
            if obstacle_rect.top == 100:
                screen.blit(enemy1_surface, obstacle_rect)
            elif obstacle_rect.top == 300:
                screen.blit(enemy2_surface, obstacle_rect)
            elif obstacle_rect.top == 500:
                screen.blit(enemy1_surface, obstacle_rect)
            elif obstacle_rect.top == 700:
                screen.blit(enemy2_surface, obstacle_rect)
            if player_rect.colliderect(obstacle_rect):
                print('Collision')
                pygame.quit()
                sys.exit()

        return obstacle_list
    else: return []

def score_display(score, high_score):

    score_surface = font.render(str(score), False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(200, 400))
    high_score_surface = font.render(f'High score {high_score}', False, (64, 64, 64))
    high_score_rect = score_surface.get_rect(center=(100, 500))
    screen.blit(score_surface, score_rect)
    screen.blit(high_score_surface, high_score_rect)
    return score


def spawn_speed_enemies_expotential(score, points_check):
    if score > points_check:

        speed = int(2000/(score/2))
        print(speed)
        pygame.time.set_timer(obstacle_timer, speed)




pygame.init()
screen = pygame.display.set_mode((400, 850))
pygame.display.set_caption('Flazzer')
clock = pygame.time.Clock()
font = pygame.font.Font('Font/Branding.ttf', 50)
game_active = True
player_move = 766
move_down = False
move_pixel = 100
obstacle_rect_list = []
score = 0
first_step = False
spawn_speed_enemies = 0
points_check = 0

#Timer
obstacle_timer = pygame.USEREVENT + 1

pygame.time.set_timer(obstacle_timer, spawn_speed_enemies)
player_surface = pygame.image.load('player/player_stand.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(200, 850))
enemy1_surface = pygame.image.load('enemy/Fly1.png').convert_alpha()
enemy2_surface = pygame.image.load('enemy/snail1.png').convert_alpha()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == pygame.KEYDOWN and move_down == False:
                if event.key == pygame.K_SPACE:
                    first_step = True
                    player_move -= move_pixel
            if event.type == pygame.KEYDOWN and move_down:
                if event.key == pygame.K_SPACE:
                    player_move += move_pixel
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 750 and first_step and move_down:
                    score += 1
                elif event.key == pygame.K_SPACE and player_rect.bottom == 150 and first_step and move_down == False:
                    score += 1

        if event.type == obstacle_timer and game_active:
            random_enemy_spawn = random.randint(0, 3)
            if random_enemy_spawn == 0:
                obstacle_rect_list.append(enemy1_surface.get_rect(midtop=(0, 100)))
            elif random_enemy_spawn == 1:
                obstacle_rect_list.append(enemy2_surface.get_rect(midtop=(0, 300)))
            elif random_enemy_spawn == 2:
                obstacle_rect_list.append(enemy1_surface.get_rect(midtop=(0, 500)))
            elif random_enemy_spawn == 3:
                obstacle_rect_list.append(enemy2_surface.get_rect(midtop=(0, 700)))

    if game_active:
        screen.fill('black')
        screen.blit(player_surface, player_rect)

        #Player
        if move_down == False:
            player_rect.y = player_move
        if move_down:
            player_rect.y = player_move
        if player_rect.top < 8:
            player_rect.top = 0
            move_down = True

        if player_rect.bottom == 850:
            player_rect.bottom = 850
            move_down = False

        with open('Score.txt', 'r') as r:
            file_score = r.read()

            if score > int(file_score):

                with open('Score.txt', 'w') as w:
                    w.write(str(score))

        with open('Score.txt', 'r') as r:
            high_score = r.read()


         #obstacle_movement


        spawn_speed_enemies_expotential(score, points_check)
        points_check = score
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        display_score = score_display(score, high_score)




    pygame.display.update()
    clock.tick(60)