import pygame
import sys
import random

pygame.init()

 # 화면 설정, UI
WIDTH, HEIGHT = 800, 200
GROUND_Y = 160

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("공룡 점프 게임")
clock = pygame.time.Clock()

#색상 설정
WHITE = (255, 255, 255)
GRAY = (83, 83, 83)

#공룡 설정
dino_width, dino_height = 40, 40
dino_x = 50
dino_y = GROUND_Y - dino_height
dino_vy = 0
jumping = False
GRAVITY = 0.6
JUMP_FORCE = -11

