import pygame   # 화면, 키보드, 그림을 다루는 게임 라이브러리
import sys      # 프로그램 종료용
import random   # 랜덤값 생성용
import base64   # 이미지 데이터를 텍스트로 담기 위한 인코딩/디코딩
import io       # 메모리 상의 데이터를 파일처럼 다루기 위한 라이브러리

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

# ── 스프라이트 이미지 (실제 크롬 공룡 게임 이미지에서 잘라낸 것을, 파일 없이
#     이 코드 안에 텍스트(base64)로 직접 담아뒀다. 별도 이미지 파일이나
#     assets 폴더가 없어도 이 .py 파일 하나만으로 바로 실행된다.) ──
DINO_IMG1_B64 = "iVBORw0KGgoAAAANSUhEUgAAAGAAAABUCAYAAAB9czKDAAAB6klEQVR4nO3dMVLDMBRF0Zhxk41kQ2m9vLTekDeSEioK/zD8aGTrys49HTMwGJ6fJCsKDJeDeT6f3/Q1/Od6vQ4ln/+114XoPSN9AZnsjp+mqdWl/OnxeFR9vQ2AGQDMAGBFMzYhzgH0mJ+Jc0K2KrIBsO5XQaXmeV7dcff7vevnBhsAMwCYAcBONwf0PuZHNgBmADADgBkAzABgBgA73TK0d8uyrJbJNgBmAxqJd/7tdhsuFxuAswGN/N7x0ccHUHuqoZZDEMwAYAYAe5kYspNopWcfSx3tJFzt78MGwAwAZgCwMTt5ttc6+d1z/luP+fS6P7IBMAOAGQBs970gaqzfyt7PPTYAZgAwA4Clc0Acm2vfp0uP9dn3b/2cYANgBgAzAFjxc0DpXhE95kfxeunrswEwA4AZAKx6L4geQ2vRrw/YAJgBwAwA9vFnQ/fe78/YAJgBwAwANsYx8Gh/oerobADs9KugrU8zb80GwF4a4JzQlg2AGQDMAGDFK4Le54Rsf99VkFYMAGYAsOrxkJ4TjjbmRzYAZgAwA4Btvhtae/ayt7Obe7MBsPFof228FP3zxf/oEdkA2JgllJnnefVx6XvIslesSp8zel/3RzYAZgAwA4A1PxXR+ymF1mwArLgB9Lr6bGwA7AcPyIzlBUMUBwAAAABJRU5ErkJggg=="
DINO_IMG2_B64 = "iVBORw0KGgoAAAANSUhEUgAAAFwAAABWCAYAAABCdPE+AAABr0lEQVR4nO3ay26DMBhEYVNlw/PBY8LzsUxXLGI15RJz/Jucb9tKpZPRyCLu0k0Mw/Cs+ffnee72/N7P1Q+iVwYOM3BYtyzLM6WU+r7ftUFR1N7sLe823YbDHrUf4CrTNP3783EcoSd5ZcNht234Km/yVvOvZsNhBg4zcNjtN7z2ZudsOOy2Da91zt5iw2EGDjNwmIHDDBxm4DADhxk4zMBhBg4zcNijtW/ro9h70ypnw2EGDjNw2Nsdym82nd2sUkrftKL/n/WGmw2HGTjMwGHhvtOMfiv2UzYcZuAwA4ftPofnPj3HRt/q0ud0z+GVGDjMwGGnz+FH37VE2+z8eanns+EwA4cZOKzYu5RoG30U9X7chsMMHGbgsHDvw+9qvf9jw2EGDjNw2O6zZ+vn7FytezY2HPY1p5TaN8dWNhx2+lNvbdNt+JcycJiBw4rtWrRNj7LZORsOM3CYgcMu2zl606Nuds6GwwwcZuAwbPeObvrRu39uuP5k4DADh4X5xmdrg2vd5y7NhsMMHGbgsGob3sq5uTQbDjNwmIHDwrxLObrprb5bseEwA4cZOOwXPh5py+tKJ/oAAAAASUVORK5CYII="
CACTUS_SMALL_B64 = "iVBORw0KGgoAAAANSUhEUgAAACMAAABGCAYAAABG4C2wAAABAElEQVR4nO2aQQ6DIBBFsXHjHTmed5ylrjBmykeYBjrE/5ZtbF5eyhSpSzAiIkfu9W3bFutnfqwX9mBtvSAViTEW37cUclWm2v6piGbf9xBCWyFXZSiDGC4jIgeaUa7KNM8ZK3o15ubRu8qg+ZQr5KoMZRBfMqU5MFzmn1yrqWYO9MZXmdo50BsROVyVoQyCMgjKICiDoAyi2x649p78zjvKPKFPKdz9ag8vUzq3eUeZVEBT2lPPVcYyL+5Me6a33td5CL+XsOLuFOL6zngo5LNMQhfS9Czmu0xCz4cR99yuylAGQRkEZRCUQVAGQRkEZRCUQVAG0fwvW+1eePoni06ODXGW5DfwwgAAAABJRU5ErkJggg=="
CACTUS_LARGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAADMAAABkCAYAAAArKghlAAABb0lEQVR4nO2bSQ6DMBAEIcqFP/I8/jhHcnKErDh4hdLQdQ0yKTfrjJmnzpjZnrPdsixz732/eg94J+9eA4VE1nUt2r5nQq6SaZ6V0kRitm2bpqlPQq6SkQwVyVCRDBXJUJEMFclQkQyVbm+ao0jVFH69/yiZKzh7g/1VQ/CdTMkxOoLcmkL4/ZiQz2RqjlEavpJpOUZH/7kSzGx3lYxkqEiGimSoSIaKZKhIhopkqEiGimSoSIaKZKhUdwFy12JeOZ6rZObWlXx3Ea8gdFfRxHbOUvxb0+kqma8d/dzJWWXrM5kALaGSdc++kwlclVCY+RQlHTpXySTvM8c7a85ArQnqW4CI0yeAsxnr/fTcgqtkJENFMlQkQ0UyVCRDRTJUJENFMlQkQ0UyVLAyZraXVn6wMjVkd87irzNG1cviGnfJVyHPSiY1U6O6A3Hyj+0CZFuPPmfUBYjIvprFM9c6ky1XrRSukrmdmjt9ClfJfAB5sLlKQA2dngAAAABJRU5ErkJggg=="


def load_image_from_b64(b64_string, target_height):
    """base64 텍스트를 실제 이미지로 복원하고, 원본 비율을 유지한 채 target_height 크기로 맞춘다."""
    raw_bytes = base64.b64decode(b64_string)          # 텍스트 -> 원본 이미지 바이트로 복원
    file_like = io.BytesIO(raw_bytes)                  # 바이트를 "가짜 파일"처럼 다루게 함
    img = pygame.image.load(file_like, "sprite.png").convert_alpha()
    w, h = img.get_size()
    scale = target_height / h
    new_size = (int(w * scale), target_height)
    return pygame.transform.scale(img, new_size)


DINO_IMAGES = [
    load_image_from_b64(DINO_IMG1_B64, 50),   # 달리기 프레임 1 (다리 벌림)
    load_image_from_b64(DINO_IMG2_B64, 50),   # 달리기 프레임 2 (다리 모음)
]
CACTUS_IMAGES = {
    "small": load_image_from_b64(CACTUS_SMALL_B64, 40),
    "large": load_image_from_b64(CACTUS_LARGE_B64, 55),
}


class Dino:
    """공룡 캐릭터를 나타내는 클래스. 위치, 속도, 점프, 그리기를 전부 이 안에서 관리한다."""

    def __init__(self):
        self.images = DINO_IMAGES
        self.width, self.height = self.images[0].get_size()
        self.x = 50                              # 화면 왼쪽에서 50px 떨어진 시작 위치
        self.y = GROUND_Y - self.height           # 아랫부분이 바닥선에 닿게 계산
        self.vy = 0                                # 세로 속도(velocity y), 처음엔 정지
        self.jumping = False                       # 점프 중인지 여부
        self.anim_timer = 0                         # 달리기 애니메이션 전환 타이머
        self.anim_index = 0                         # 현재 보여줄 프레임 번호 (0 또는 1)
        self.forward_speed = 1.2                    # 왼쪽→오른쪽으로 이동하는 속도

    def jump(self):
        """점프 중이 아닐 때만 위로 튀어오르게 한다."""
        if not self.jumping:
            self.vy = JUMP_FORCE   # 위쪽 방향 속도 부여
            self.jumping = True    # 중복 점프 방지

    def reset(self):
        """공룡 상태를 처음으로 되돌린다."""
        self.x = 50
        self.y = GROUND_Y - self.height
        self.vy = 0
        self.jumping = False
        self.anim_timer = 0
        self.anim_index = 0

    def update(self):
        """매 프레임 중력을 적용해서 위치를 갱신하고, 달리기 다리 애니메이션도 갱신한다."""
        self.vy += GRAVITY   # 중력을 속도에 더함
        self.y += self.vy    # 그 속도만큼 위치 이동
        if self.y > GROUND_Y - self.height:   # 바닥보다 내려가면
            self.y = GROUND_Y - self.height    # 바닥 위치로 고정
            self.vy = 0
            self.jumping = False

        # 왼쪽에서 오른쪽으로 계속 이동 (사진 속 공룡처럼)
        self.x += self.forward_speed
        if self.x > WIDTH * 0.55:   # 화면 중간쯤 도달하면
            self.x = 50             # 다시 왼쪽 시작 위치로 돌아가서 반복

        # 땅에 있을 때만 다리를 번갈아 움직이는 애니메이션 재생
        if not self.jumping:
            self.anim_timer += 1
            if self.anim_timer >= 6:   # 6프레임마다 다리 모양 전환
                self.anim_timer = 0
                self.anim_index = 1 - self.anim_index   # 0<->1 번갈아 전환

    def get_rect(self):
        """충돌 판정에 쓸 사각형을 돌려준다."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        """현재 애니메이션 프레임에 맞는 이미지를 화면에 그린다."""
        image = self.images[1] if self.jumping else self.images[self.anim_index]
        surface.blit(image, (self.x, self.y))


class Obstacle:
    """선인장 장애물 하나를 나타내는 클래스. 자기 위치와 그리는 방법을 스스로 가지고 있다."""

    def __init__(self, x, speed):
        # 작은 선인장, 큰 선인장 중 하나를 랜덤으로 고른다
        self.kind = random.choice(["small", "large"])
        self.image = CACTUS_IMAGES[self.kind]
        self.width, self.height = self.image.get_size()
        self.rect = pygame.Rect(x, GROUND_Y - self.height, self.width, self.height)
        self.speed = speed   # 이동 속도 (게임 속도를 그대로 물려받음)

    def update(self):
        """왼쪽으로 이동시킨다 (공룡이 앞으로 달리는 것처럼 보이게)."""
        self.rect.x -= self.speed

    def is_off_screen(self):
        """화면 밖으로 완전히 나갔는지 확인한다 (제거 대상 판단용)."""
        return self.rect.right < 0

    def draw(self, surface):
        """선인장 이미지를 화면에 그린다."""
        surface.blit(self.image, self.rect)


class Game:
    """게임 전체 상태(점수, 속도, 장애물 목록 등)와 진행 흐름을 관리하는 클래스."""

    def __init__(self):
        self.dino = Dino()          # 공룡 객체 하나 생성
        self.dino.x = -self.dino.width   # 처음엔 화면 왼쪽 바깥에서 시작 (인트로용)
        self.intro_done = False     # 왼쪽→오른쪽 인트로 등장이 끝났는지 여부
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
        if not self.intro_done:   # 인트로(뛰어들어오는 중)에 키를 누르면 바로 제자리로 스킵
            self.intro_done = True
            self.dino.x = 50
        if not self.started or self.game_over:
            self.reset()
            return
        self.dino.jump()

    def spawn_obstacle(self):
        """화면 오른쪽 끝에 새 장애물 객체를 하나 만들어 목록에 추가한다."""
        self.obstacles.append(Obstacle(WIDTH, self.game_speed))

    def update(self):
        """게임이 진행 중일 때만 물리 계산(이동, 충돌, 점수)을 수행한다."""
        if not self.intro_done:
            # 인트로: 공룡이 화면 왼쪽 바깥에서 시작 위치(x=50)까지 뛰어들어옴
            self.dino.x += 4
            self.dino.anim_timer += 1
            if self.dino.anim_timer >= 6:
                self.dino.anim_timer = 0
                self.dino.anim_index = 1 - self.dino.anim_index   # 다리 번갈아 움직이기
            if self.dino.x >= 50:
                self.dino.x = 50
                self.intro_done = True
            return   # 인트로 중에는 장애물/점수 등 나머지 로직은 아직 실행하지 않음

        if not (self.started and not self.game_over):
            return

        self.frame += 1
        self.dino.update()   # 공룡 중력/위치/애니메이션 갱신

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

        if not self.intro_done:
            pass   # 인트로 중엔 안내 문구 없이 공룡이 뛰어들어오는 것만 보여줌
        elif not self.started:
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