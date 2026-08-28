import pygame
import sys
import random
import os
import asyncio  # 웹(GitHub Pages/Pygbag) 실행 호환성을 위해 필요

pygame.init()

# 화면 설정 (800x400 고정 해상도)
WIDTH, HEIGHT = 800, 400
GROUND_Y = 330  # 바닥 위치 조정

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("구글 공룡 게임 (800x400)")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
GRAY = (83, 83, 83)
GREEN = (34, 139, 34)

font = pygame.font.SysFont("malgungothic", 20)

GRAVITY = 0.7
JUMP_FORCE = -12

def load_dino_images():
    """image_d592d5.png에서 4마리 공룡을 800x400 해상도에 맞춰 자르고 스케일링합니다."""
    filename = "image_d592d5.png"
    
    if not os.path.exists(filename):
        if os.path.exists(os.path.join("assets", filename)):
            filename = os.path.join("assets", filename)
        else:
            # 파일이 없을 경우 대체 프레임 생성
            fallback = []
            for color in [(80,80,80), (100,100,100), (80,80,80), (60,60,60)]:
                surf = pygame.Surface((50, 54), pygame.SRCALPHA)
                surf.fill(color)
                fallback.append(surf)
            return fallback

    # Alpha 채널을 유지하며 이미지 로드
    raw_sheet = pygame.image.load(filename).convert_alpha()
    
    # 순수 흰색 배경 처리
    sheet = pygame.Surface(raw_sheet.get_size(), pygame.SRCALPHA)
    sheet.blit(raw_sheet, (0, 0))

    sw, sh = sheet.get_size()
    single_w = sw // 4  # 가로 4등분

    dino_imgs = []
    # 800x400 해상도에 시각적으로 적합한 공룡 목표 높이 설정 (55px)
    TARGET_HEIGHT = 55

    for i in range(4):
        rect = pygame.Rect(i * single_w, 0, single_w, sh)
        cropped = sheet.subsurface(rect)
        
        # 실제 공룡 그래픽이 존재하는 바운딩 박스 추출 (여백 제거)
        bbox = cropped.get_bounding_rect()
        if bbox.width > 0 and bbox.height > 0:
            dino_sprite = cropped.subsurface(bbox)
        else:
            dino_sprite = cropped

        # 비율 유지 스케일링
        aspect_ratio = dino_sprite.get_width() / dino_sprite.get_height()
        target_width = int(TARGET_HEIGHT * aspect_ratio)
        
        scaled_sprite = pygame.transform.smoothscale(dino_sprite, (target_width, TARGET_HEIGHT))
        dino_imgs.append(scaled_sprite)

    return dino_imgs

DINO_IMAGES = load_dino_images()

class Dino:
    def __init__(self):
        self.images = DINO_IMAGES
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.x = 80  # 시각적 여백 확보
        self.y = GROUND_Y - self.height
        self.vy = 0
        self.jumping = False
        self.anim_timer = 0
        self.anim_index = 0

    def jump(self):
        if not self.jumping:
            self.vy = JUMP_FORCE
            self.jumping = True

    def reset(self):
        self.height = self.images[0].get_height()
        self.x = 80
        self.y = GROUND_Y - self.height
        self.vy = 0
        self.jumping = False
        self.anim_timer = 0
        self.anim_index = 0

    def update(self):
        # 중력 계산
        self.vy += GRAVITY
        self.y += self.vy

        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vy = 0
            self.jumping = False

        # 4단계 순차 애니메이션 (0 -> 1 -> 2 -> 3 -> 0)
        self.anim_timer += 1
        if self.anim_timer >= 6:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.images)

    def draw(self, surface):
        curr_img = self.images[self.anim_index]
        surface.blit(curr_img, (self.x, self.y))

class Obstacle:
    def __init__(self, x, speed):
        self.width = random.choice([25, 35])
        self.height = random.choice([45, 60])
        self.rect = pygame.Rect(x, GROUND_Y - self.height, self.width, self.height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def is_off_screen(self):
        return self.rect.right < 0

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

class Game:
    def __init__(self):
        self.dino = Dino()
        self.obstacles = []
        self.frame = 0
        self.score = 0
        self.game_speed = 7
        self.game_over = False

    def reset(self):
        self.dino.reset()
        self.obstacles = []
        self.frame = 0
        self.score = 0
        self.game_speed = 7
        self.game_over = False

    def handle_jump(self):
        if self.game_over:
            self.reset()
        else:
            self.dino.jump()

    def update(self):
        if self.game_over:
            return

        self.frame += 1
        self.dino.update()

        if self.frame % random.randint(60, 110) == 0:
            self.obstacles.append(Obstacle(WIDTH, self.game_speed))

        for o in self.obstacles:
            o.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        # 충돌 판정
        dino_rect = pygame.Rect(self.dino.x, self.dino.y, self.dino.width, self.dino.height)
        for o in self.obstacles:
            if dino_rect.colliderect(o.rect):
                self.game_over = True

        self.score += 1
        if self.score % 400 == 0:
            self.game_speed += 0.5

    def draw(self, surface):
        surface.fill(WHITE)
        pygame.draw.line(surface, GRAY, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

        self.dino.draw(surface)
        for o in self.obstacles:
            o.draw(surface)

        score_text = font.render(f"SCORE: {self.score // 10}", True, GRAY)
        surface.blit(score_text, (20, 20))

        if self.game_over:
            msg1 = font.render("GAME OVER", True, GRAY)
            msg2 = font.render("스페이스바를 눌러 재시작", True, GRAY)
            surface.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 30))
            surface.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 10))

async def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    game.handle_jump()

        game.update()
        game.draw(screen)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)  # 웹(GitHub Pages) 빌드 패키징 호환용

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())