import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
GROUND_Y = 160

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("공룡 점프 게임")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GRAY = (83, 83, 83)

font = pygame.font.SysFont("malgungothic", 20)