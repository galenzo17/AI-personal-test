import pygame
import sys

# Configuración
WIDTH, HEIGHT = 800, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Clone")
clock = pygame.time.Clock()

# Clases
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 5
        self.jump_power = 12
        self.gravity = 0.5
        self.on_ground = False

    def update(self, keys, platforms):
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = -self.jump_power

        self.velocity.y += self.gravity
        self.on_ground = False
        self.rect.y += self.velocity.y
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

        self.rect.x += self.velocity.x
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self, platforms):
        self.rect.x += self.speed * self.direction
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.direction *= -1
                self.rect.x += self.speed * self.direction

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(x, y))

class Camera:
    def __init__(self, width):
        self.offset = 0
        self.width = width

    def update(self, target):
        self.offset = min(max(0, target.rect.x - WIDTH // 2), self.width - WIDTH)

    def apply(self, rect):
        return rect.move(-self.offset, 0)

# Inicialización del juego
player = Player(50, 300)
enemy = Enemy(400, 300)
power_up = PowerUp(700, 260)

platforms = pygame.sprite.Group(
    Platform(0, 350, 1600, 50),  # Suelo
    Platform(300, 300, 200, 20),  # Plataforma
    Platform(600, 250, 200, 20)   # Plataforma
)

all_sprites = pygame.sprite.Group(player, enemy, power_up, *platforms)
camera = Camera(1600)

# Juego principal
def main():
    global player, enemy, power_up
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player = Player(50, 300)
                enemy = Enemy(400, 300)
                power_up = PowerUp(700, 260)
                all_sprites.add(player, enemy, power_up)

        # Actualización
        player.update(keys, platforms)
        enemy.update(platforms)
        camera.update(player)

        if player.rect.colliderect(enemy.rect):
            print("Game Over!")
            player = Player(50, 300)

        if player.rect.colliderect(power_up.rect):
            print("Power-up collected!")
            power_up.kill()

        # Dibujo
        screen.fill(WHITE)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()