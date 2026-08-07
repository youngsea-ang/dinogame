import pygame   #화면,키보드,그림을 다루는 게임 라이브러리
import sys      #프로그램을 종료시킬 때 쓰는 라이브러리
import random

pygame.init()

 # 화면 설정, UI
WIDTH, HEIGHT = 800, 200
GROUND_Y = 160  #바닥의 세로 위치

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("공룡 점프 게임")
clock = pygame.time.Clock()

#색상 설정
WHITE = (255, 255, 255)
GRAY = (83, 83, 83)

#공룡 설정
dino_width, dino_height = 40, 40
dino_x = 50     #화면 왼쪽에서 50px떨어진 위치에서 시작
dino_y = GROUND_Y - dino_height     #공룡의 아랫부분이 바닥선에 딱 맞닿게
dino_vy = 0     #공룡의 세로 속도(velocity y)로, 처음엔 0(멈춘 상태)
jumping = False     #지금 점프 중인지 아닌지 표시하는 참/거짓 값
GRAVITY = 0.6       #매 프레임 아래로 잡아당기는 힘의 세기
JUMP_FORCE = -11    #점프 순간 위로 튀어 오르는 힘이에요(음수라서 위쪽 방향)

#장애물 설정 (변수만)
obstacles = []  #지금 화면에 있는 장애물들을 담는 목록
next_obstacle_frame = 0 #다음 장애물이 몇 번째 프레임에 나올지 저장하는 변수. 일단 0으로 시작하고 나중에 reset_game()에서 실제 랜덤 값으로 채워진다

#게임 상태 설정
frame = 0   #게임이 시작된 후 몇 번째 화면 갱신인지 세는 숫자(시간 재는 역할)
score = 0
game_speed = 6  #장애물이 움직이는 속도
game_over = False   #게임이 끝났는지를 나타내는 참/거짓 값
started = False     #게임이 시작됐는지를 나타내는 참/거짓 값

#글씨체 설정
font = pygame.font.SysFont("malgungothic", 20)  #malgungothic은 맑은 고딕. 20은 글자 크기

#장애물 생성을 랜덤으로 결정하는 함수
def random_obstacle_gap():
    return random.randint(60, 150)