import pygame
import random
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jet Fighter")

# Load images
background = pygame.image.load("desert.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
jet_img = pygame.image.load("jet.png").convert_alpha()
jet_img = pygame.transform.scale(jet_img, (50, 30))
enemy_img = pygame.image.load("enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 30))
bubble_img = pygame.image.load("powerup.png").convert_alpha()
bubble_img = pygame.transform.scale(bubble_img, (30, 30))

# Load sounds
normal_shoot_sound = pygame.mixer.Sound("shooting.mp3")
power_shoot_sound = pygame.mixer.Sound("shooting2.mp3")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Player jet
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = jet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.health = 100
        self.speed = 5
        self.power = 1
        self.power_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 10000:
            self.power = 1

    def shoot(self):
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            normal_shoot_sound.play()
        elif self.power >= 2:
            for i in range(-1, 2):
                bullet = Bullet(self.rect.centerx + i*20, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            power_shoot_sound.play()

    def powerup(self):
        self.power = 2
        self.power_time = pygame.time.get_ticks()

# Enemy jet
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.shoot_delay = random.randrange(1000, 3000)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bubble_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game functions
def show_start_screen():
    screen.blit(background, (0, 0))
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Jet Fighter", True, BLUE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))

    play_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Play", BLUE, WHITE)
    play_button.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    return True

def show_game_over_screen(score):
    screen.blit(background, (0, 0))
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Game Over", True, RED)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))

    score_font = pygame.font.Font(None, 48)
    score_text = score_font.render(f"Score: {score}", True, BLUE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))

    play_again_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Play Again", BLUE, WHITE)
    play_again_button.draw(screen)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_clicked(event.pos):
                    return True

# Game loop
def game():
    global all_sprites, enemies, bullets, enemy_bullets, bubbles

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    bubbles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    clock = pygame.time.Clock()
    score = 0
    start_time = pygame.time.get_ticks()
    bubble_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()
        enemy_bullets.update()
        bubbles.update()

        # Spawn bubbles
        now = pygame.time.get_ticks()
        if now - bubble_spawn_time > 10000:  # Spawn bubble every 10 seconds
            bubble = Bubble()
            all_sprites.add(bubble)
            bubbles.add(bubble)
            bubble_spawn_time = now

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check for player-enemy collisions
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            player.health -= 10
            if player.health <= 0:
                running = False

        # Check for enemy bullet-player collisions
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            player.health -= 5
            if player.health <= 0:
                running = False

        # Check for player-bubble collisions
        hits = pygame.sprite.spritecollide(player, bubbles, True)
        for hit in hits:
            player.powerup()

        # Increase game speed over time
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # time in seconds
        player.speed = 5 + (elapsed_time // 10)  # Increase speed every 10 seconds

        # Draw / render
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        enemy_bullets.draw(screen)

        # Draw health bar
        pygame.draw.rect(screen, RED, (WIDTH - 110, HEIGHT - 30, player.health, 20))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        # Draw power-up timer
        if player.power >= 2:
            power_time_left = 10 - (pygame.time.get_ticks() - player.power_time) / 1000
            if power_time_left > 0:
                power_text = font.render(f"Power-up: {power_time_left:.1f}s", True, YELLOW)
                screen.blit(power_text, (10, HEIGHT - 30))

        pygame.display.flip()

    return score

# Main game loop
def main():
    while True:
        if show_start_screen():
            final_score = game()
            if not show_game_over_screen(final_score):
                break
        else:
            break

    pygame.quit()

if __name__ == "__main__":
    main()