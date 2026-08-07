import pygame   # 화면, 키보드, 그림을 다루는 게임 라이브러리
import sys      # 프로그램 종료용
import random   # 랜덤값 생성용

pygame.init()   # pygame 기능 켜기

# 화면 설정, UI
WIDTH, HEIGHT = 800, 400
GROUND_Y = 350  # 바닥의 세로 위치

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # 실제 게임 창
pygame.display.set_caption("공룡 점프 게임")
clock = pygame.time.Clock()   # 프레임 속도 조절용

# 색상 설정
WHITE = (255, 255, 255)
GRAY = (83, 83, 83)

# 글씨체 설정
font = pygame.font.SysFont("malgungothic", 20)

GRAVITY = 0.6       # 매 프레임 아래로 잡아당기는 힘
JUMP_FORCE = -11    # 점프 시 위로 튀는 힘 (음수 = 위쪽)


class Dino:
    """공룡 캐릭터를 나타내는 클래스. 위치, 속도, 점프, 그리기를 전부 이 안에서 관리한다."""

    def __init__(self):
        # 생성자: Dino() 객체를 만드는 순간 자동으로 실행되는 초기 설정
        self.width = 40
        self.height = 40
        self.x = 50                              # 화면 왼쪽에서 50px 떨어진 시작 위치
        self.y = GROUND_Y - self.height           # 아랫부분이 바닥선에 닿게 계산
        self.vy = 0                                # 세로 속도(velocity y), 처음엔 정지
        self.jumping = False                       # 점프 중인지 여부

        # 픽셀아트 패턴 (8열 x 10행) - "1"은 그리고 "0"은 비워둠
        self.pattern = [
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

    def jump(self):
        """점프 중이 아닐 때만 위로 튀어오르게 한다."""
        if not self.jumping:
            self.vy = JUMP_FORCE   # 위쪽 방향 속도 부여
            self.jumping = True    # 중복 점프 방지

    def reset(self):
        """공룡 상태를 처음으로 되돌린다."""
        self.y = GROUND_Y - self.height
        self.vy = 0
        self.jumping = False

    def update(self):
        """매 프레임 중력을 적용해서 위치를 갱신한다."""
        self.vy += GRAVITY   # 중력을 속도에 더함
        self.y += self.vy    # 그 속도만큼 위치 이동
        if self.y > GROUND_Y - self.height:   # 바닥보다 내려가면
            self.y = GROUND_Y - self.height    # 바닥 위치로 고정
            self.vy = 0
            self.jumping = False

    def get_rect(self):
        """충돌 판정에 쓸 사각형을 돌려준다."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        """픽셀 패턴대로 공룡을 그린다 (격자를 한 칸씩 훑으며 "1"인 칸만 사각형으로 채움)."""
        cols = 8
        rows = len(self.pattern)
        pixel_w = self.width / cols
        pixel_h = self.height / rows
        for r in range(rows):
            for c in range(cols):
                if self.pattern[r][c] == "1":
                    pygame.draw.rect(
                        surface, GRAY,
                        (self.x + c * pixel_w, self.y + r * pixel_h, pixel_w, pixel_h)
                    )


class Obstacle:
    """선인장 장애물 하나를 나타내는 클래스. 자기 위치와 그리는 방법을 스스로 가지고 있다."""

    def __init__(self, x, speed):
        # 생성될 때마다 랜덤 높이로 새 장애물 하나가 만들어짐
        self.height = random.randint(30, 50)
        self.width = 18
        self.rect = pygame.Rect(x, GROUND_Y - self.height, self.width, self.height)
        self.speed = speed   # 이동 속도 (게임 속도를 그대로 물려받음)

    def update(self):
        """왼쪽으로 이동시킨다 (공룡이 앞으로 달리는 것처럼 보이게)."""
        self.rect.x -= self.speed

    def is_off_screen(self):
        """화면 밖으로 완전히 나갔는지 확인한다 (제거 대상 판단용)."""
        return self.rect.right < 0

    def draw(self, surface):
        """선인장 모양(가운데 몸통 + 좌우로 뻗은 팔 두 개)을 그린다."""
        pygame.draw.rect(surface, GRAY, self.rect)   # 몸통(기둥)
        arm_w = max(int(self.rect.width * 0.6), 4)
        arm_h = max(int(self.rect.height * 0.28), 4)
        pygame.draw.rect(   # 왼쪽 팔
            surface, GRAY,
            (self.rect.x - arm_w + 4, self.rect.y + int(self.rect.height * 0.35), arm_w, arm_h)
        )
        pygame.draw.rect(   # 오른쪽 팔
            surface, GRAY,
            (self.rect.right - 4, self.rect.y + int(self.rect.height * 0.15), arm_w, arm_h)
        )


class Game:
    """게임 전체 상태(점수, 속도, 장애물 목록 등)와 진행 흐름을 관리하는 클래스."""

    def __init__(self):
        self.dino = Dino()          # 공룡 객체 하나 생성
        self.obstacles = []         # 현재 화면에 있는 장애물 목록
        self.frame = 0              # 경과 프레임 수
        self.score = 0
        self.game_speed = 6         # 장애물 이동 속도
        self.game_over = False
        self.started = False
        self.next_obstacle_frame = 0   # 다음 장애물 등장 시점

    def random_obstacle_gap(self):
        """다음 장애물까지 몇 프레임 기다릴지 랜덤으로 정한다."""
        return random.randint(60, 150)

    def reset(self):
        """게임 전체를 처음 상태로 되돌린다 (공룡도 같이 초기화)."""
        self.dino.reset()
        self.obstacles = []
        self.frame = 0
        self.score = 0
        self.game_speed = 6
        self.game_over = False
        self.started = True
        self.next_obstacle_frame = self.random_obstacle_gap()

    def handle_jump_key(self):
        """스페이스바/↑ 키를 눌렀을 때 호출된다. 상태에 따라 재시작하거나 점프시킨다."""
        if not self.started or self.game_over:
            self.reset()
            return
        self.dino.jump()

    def spawn_obstacle(self):
        """화면 오른쪽 끝에 새 장애물 객체를 하나 만들어 목록에 추가한다."""
        self.obstacles.append(Obstacle(WIDTH, self.game_speed))

    def update(self):
        """게임이 진행 중일 때만 물리 계산(이동, 충돌, 점수)을 수행한다."""
        if not (self.started and not self.game_over):
            return

        self.frame += 1
        self.dino.update()   # 공룡 중력/위치 갱신

        # 랜덤 시점이 되면 장애물 생성
        if self.frame >= self.next_obstacle_frame:
            self.spawn_obstacle()
            self.next_obstacle_frame = self.frame + self.random_obstacle_gap()

        # 모든 장애물 이동 + 화면 밖으로 나간 것 제거
        for o in self.obstacles:
            o.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        # 공룡과 장애물 충돌 체크
        dino_rect = self.dino.get_rect()
        for o in self.obstacles:
            if dino_rect.colliderect(o.rect):
                self.game_over = True

        # 점수 증가 + 500점마다 속도 상승
        self.score += 1
        if self.score % 500 == 0:
            self.game_speed += 0.5

    def draw(self, surface):
        """배경, 바닥, 공룡, 장애물, 점수/안내문구를 순서대로 전부 그린다."""
        surface.fill(WHITE)
        pygame.draw.line(surface, GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)   # 바닥선

        self.dino.draw(surface)          # 공룡 그리기 (Dino 클래스에 위임)
        for o in self.obstacles:
            o.draw(surface)               # 장애물 그리기 (Obstacle 클래스에 위임)

        score_text = font.render(f"SCORE: {self.score // 10}", True, GRAY)
        surface.blit(score_text, (10, 10))

        if not self.started:
            msg = font.render("스페이스바를 눌러 시작", True, GRAY)
            surface.blit(msg, (WIDTH // 2 - 80, HEIGHT // 2))
        elif self.game_over:
            msg = font.render("게임 오버! 스페이스바를 눌러 재시작", True, GRAY)
            surface.blit(msg, (WIDTH // 2 - 120, HEIGHT // 2))


# 게임 루프
game = Game()   # Game 클래스의 객체(인스턴스) 하나 생성 - 이 안에 공룡, 장애물, 점수 등 모든 게 들어있음
running = True
while running:
    for event in pygame.event.get():          # 창 닫기/키 입력 등 이벤트 확인
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                game.handle_jump_key()          # Game 객체에게 "점프 키 눌렸어" 알림

    game.update()    # 물리 계산 (Game 클래스가 알아서 dino/obstacles 다 처리)
    game.draw(screen)   # 화면 그리기

    pygame.display.update()   # 실제 화면에 반영
    clock.tick(60)             # 초당 60프레임으로 속도 제한

# 게임 종료
pygame.quit()
sys.exit()