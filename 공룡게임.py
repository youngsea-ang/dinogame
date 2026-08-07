import pygame   #화면,키보드,그림을 다루는 게임 라이브러리
import sys      #프로그램을 종료시킬 때 쓰는 라이브러리
import random

pygame.init()

 # 화면 설정, UI
WIDTH, HEIGHT = 800, 400
GROUND_Y = 350  #바닥의 세로 위치

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

#공룡을 네모가 아니라 픽셀아트(도트) 모양으로 그리는 함수
def draw_dino(x, y, w, h):
    pattern = [   #8칸x10줄짜리 격자에 1과 0으로 공룡 실루엣(머리,몸통,다리)을 표현
        "00111100",
        "01111110",
        "01111111",
        "01111100",
        "01111100",
        "11111100",
        "11111100",
        "01100110",
        "01100110",
        "01100110",
    ]
    cols = 8
    rows = len(pattern)
    pixel_w = w / cols
    pixel_h = h / rows
    for r in range(rows):
        for c in range(cols):
            if pattern[r][c] == "1":
                pygame.draw.rect(screen, GRAY, (x + c * pixel_w, y + r * pixel_h, pixel_w, pixel_h))

#장애물을 네모가 아니라 선인장 모양으로 그리는 함수 (몸통 + 좌우로 뻗은 팔)
def draw_cactus(rect):
    pygame.draw.rect(screen, GRAY, rect)   #몸통(세로로 긴 기둥)
    arm_w = max(int(rect.width * 0.6), 4)
    arm_h = max(int(rect.height * 0.28), 4)
    #왼쪽 팔
    pygame.draw.rect(screen, GRAY, (rect.x - arm_w + 4, rect.y + int(rect.height * 0.35), arm_w, arm_h))
    #오른쪽 팔
    pygame.draw.rect(screen, GRAY, (rect.right - 4, rect.y + int(rect.height * 0.15), arm_w, arm_h))

#게임 루프
running = True  #running = True로 시작해서 while running:이 이 값이 True인 동안 계속 반복
while running:
    for event in pygame.event.get():    #pygame.event.get()은 그 순간까지 발생한 모든 사건(창 닫기, 키보드 입력 등)을 목록으로 가져옴
        if event.type == pygame.QUIT:   #event.type == pygame.QUIT는 사용자가 창의 X 버튼을 눌렀다는 뜻이라 running을 False로 바꿔서 반복문을 곧 멈추게 함
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):  #pygame.K_SPACE나 pygame.K_UP(스페이스바, ↑ 키)를 눌렀으면 jump() 함수를 실행
                jump()

    #메인 루프 물리계산
    if started and not game_over:   #게임이 시작됐고(started) 아직 안 끝났을 때만(not game_over) 이 블록이 실행
        frame += 1
        dino_vy += GRAVITY  #dino_vy += GRAVITY, dino_y += dino_vy: 매 프레임 중력을 속도에 더하고, 그 속도만큼 위치를 바꿔서 자연스럽게 떨어지게 함
        dino_y += dino_vy
        if dino_y > GROUND_Y - dino_height: #공룡이 바닥보다 더 내려가려 하면 바닥 위치로 딱 고정하고 속도를 0으로, 점프 상태를 해제
            dino_y = GROUND_Y - dino_height
            dino_vy = 0
            jumping = False
        if frame >= next_obstacle_frame:    #정해둔 랜덤 시점이 되면 장애물을 만들고 다음 랜덤 시점을 새로 뽑음
            spawn_obstacle()
            next_obstacle_frame = frame + random_obstacle_gap()
        for o in obstacles: #모든 장애물을 왼쪽으로 이동시킴(공룡이 앞으로 달리는 것처럼 보이게)
            o.x -= game_speed
        obstacles = [o for o in obstacles if o.right > 0]   #화면 왼쪽 밖으로 완전히 사라진 장애물은 목록에서 제거(안 지우면 계속 쌓여서 느려짐)
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        for o in obstacles:
            if dino_rect.colliderect(o):    #공룡 사각형과 장애물 사각형이 겹치는지 확인. 겹치면 게임 오버로 바꿈
                game_over = True
        score += 1  #매 프레임 점수를 1씩 올리고, 500점마다 속도를 0.5씩 빠르게 함
        if score % 500 == 0:
            game_speed += 0.5

    #화면 그리기
    screen.fill(WHITE)
    pygame.draw.line(screen, GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2) #바닥선을 그림
    draw_dino(dino_x, dino_y, dino_width, dino_height)   #공룡을 픽셀아트 모양으로 그림
    for o in obstacles:
        draw_cactus(o)   #장애물을 선인장 모양으로 그림
    score_text = font.render(f"SCORE: {score // 10}", True, GRAY)   #font.render(...)는 글자를 이미지로 그려서 만들어주는 함수
    screen.blit(score_text, (10, 10))
    if not started:
        msg = font.render("스페이스바를 눌러 시작", True, GRAY)
        screen.blit(msg, (WIDTH // 2 - 80, HEIGHT // 2))    #creen.blit(...)는 그 이미지를 화면의 특정 위치에 "붙이는" 함수. 게임 시작 전이면 "눌러서 시작" 문구를, 게임 오버 상태면 "재시작" 문구를 보여줌
    elif game_over:
        msg = font.render("게임 오버! 스페이스바를 눌러 재시작", True, GRAY)
        screen.blit(msg, (WIDTH // 2 - 120, HEIGHT // 2))
    pygame.display.update() #지금까지 그린 걸 실제 화면에 반영
    clock.tick(60)  #1초에 60번만 반복하도록 속도를 맞춤

#게임 종료
pygame.quit()
sys.exit()