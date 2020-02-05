# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import pygame

import random
import pygame.freetype

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000
FPS = 60
pygame.display.set_caption("Приключения Дока Хадсона")
screen = pygame.display.set_mode()
done = False

def main():
    pygame.init()
    screen=pygame.display.set_mode((400, 300))
    clock=pygame.time.Clock()
    font=pygame.freetype.SysFont(None, 34)
    font.origin=True
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
        screen.fill(pygame.Color('grey12'))
        ticks=pygame.time.get_ticks()
        millis=ticks%1000
        seconds=int(ticks/1000 % 60)
        minutes=int(ticks/60000 % 24)
        out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        font.render_to(screen, (100, 100), out, pygame.Color('dodgerblue'))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__': main()
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Doc_Hudson.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(10, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super(Mob, self).__init__()
        self.surf = pygame.image.load("Salli.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(20, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("Sheriff.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        
            



#background = pygame.image.load(path.join(img_dir, 'jet.png')).convert()
#background_rect = background.get_rect()
#player_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert()
#bullet_img = pygame.image.load(path.join(img_dir, 'cloud.png')).convert()

pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load("fon.mp3")
pygame.mixer.music.play(loops=-1)


#move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
#move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
#collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
#move_up_sound.set_volume(0.5)
#move_down_sound.set_volume(0.5)
#collision_sound.set_volume(0.5)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    clouds.update()

    screen.fill((200, 30, 30))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):

        player.kill()
        
        #move_up_sound.stop()
        #move_down_sound.stop()
        #collision_sound.play()
        
        running = False

    pygame.display.flip()

    clock.tick(30)

pygame.mixer.quit()
pygame.quit()