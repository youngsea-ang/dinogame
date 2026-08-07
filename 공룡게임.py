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

#공룡 위치, 장애물 목록, 점수, 속도 등 모든 걸 처음 상태로 되돌려서 게임을 새로 시작하게 해줌
def reset_game():
    global dino_y, dino_vy, jumping, obstacles, frame, score
    global game_speed, game_over, started, next_obstacle_frame
    dino_y = GROUND_Y - dino_height
    dino_vy = 0
    jumping = False
    obstacles = []
    frame = 0
    score = 0
    game_speed = 6
    game_over = False
    started = True
    next_obstacle_frame = random_obstacle_gap()

#점프 함수
def jump():
    global dino_vy, jumping
    if not started or game_over:    #만약 아직 게임을 시작 안 했거나(not started) 게임 오버 상태라면, reset_game()을 불러서 새로 시작하고 함수를 바로 끝낸다(return)
                                    #그게 아니고 게임이 진행 중이면서 아직 점프 중이 아니라면(not jumping), 세로 속도를 JUMP_FORCE(위 방향)로 바꿔서 튀어 오르게 하고, jumping을 True로 바꿔요(중복 점프 방지)
        reset_game()
        return
    if not jumping:
        dino_vy = JUMP_FORCE
        jumping = True

#장애물 생성 함수(높이와 위치)
def spawn_obstacle():   #pygame.Rect(...)로 사각형 하나(가로 18, 세로는 랜덤 높이)를 만든다. 
                        #위치는 WIDTH(화면 맨 오른쪽 바깥)에서 시작하도록 해서, 마치 오른쪽에서 새로 등장하는 것처럼 보이게 한다. .append(...)로 이 사각형을 obstacles 목록 맨 뒤에 추가
    height = random.randint(30, 50)
    obstacles.append(pygame.Rect(WIDTH, GROUND_Y - height, 18, height))


