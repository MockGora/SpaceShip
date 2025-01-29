from pygame import *
import random


class GameSprite(sprite.Sprite):
    def __init__(self, p_image, speed, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
    def OpenFire(self):
        bullet = Bullet('bullet.png', -15, self.rect.centerx, self.rect.top, 15, 20)
        bullet_group.add(bullet)
        


class Enemy(GameSprite):
    def update(self):   
        global skiped
        self.rect.y += self.speed
        if self.rect.y >= 435:
            self.rect.y = 0
            self.rect.x = random.randint(0, 700)
            self.speed = random.randint(1, 3)
            skiped += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y < 0:
            self.kill()
            

window = display.set_mode((700, 500))
display.set_caption('Space Wars')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
spaceship = Player('rocket.png', 6, 70, 420, 80, 100)
enemy_group = sprite.Group()
bullet_group = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', random.randint(1, 3), random.randint(40, 650), 0, 80, 50)
    enemy_group.add(enemy)

mixer.init()

mixer.music.load('space.ogg')
firesound = mixer.Sound('fire.ogg')
mixer.music.play()



game = True
run = False

FPS = 60
clock = time.Clock()

font.init()

Main_Font = font.SysFont('Arial', 36)
Total_Font = font.SysFont('Arial', 60)
Kiled = 0
skiped = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                firesound.play()
                spaceship.OpenFire()
    if not run:
        window.blit(background, (0, 0))
        spaceship.update()
        spaceship.reset()
        enemy_group.update()
        enemy_group.draw(window)
        bullet_group.update()
        bullet_group.draw(window)

        collides = sprite.groupcollide(enemy_group, bullet_group, True, True)

        for collide in collides:
            Kiled += 1
            enemy = Enemy('ufo.png', random.randint(1, 3), random.randint(40, 650), 0, 80, 50)
            enemy_group.add(enemy)

        if Kiled == 11:
            win = Total_Font.render('YOU WIN', 1 ,(255, 255, 255))
            window.blit(win, (200, 200))
            game = False
        elif skiped == 4:
            lose = Total_Font.render('YOU LOSE', 1 ,(255, 255, 255))
            window.blit(lose, (200, 200))
            game = False


        Score = Main_Font.render('Счет:' + str(Kiled), 1 ,(255, 255, 255))
        window.blit(Score, (10, 20))
        Skiped = Main_Font.render('Пропущено:' + str(skiped), 1 ,(255, 255, 255))
        window.blit(Skiped, (10, 60))

        clock.tick(FPS)
        display.update()
    
    else:
        run = False
        enemy_group.kill()
        bullet_group.kill()
        Skiped = 0 
        Kiled = 0

        

