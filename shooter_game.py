from pygame import *
from random import randint
import time as rech_time
mixer.init()
font.init()
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.music.load('space.ogg')
'''mixer.music.play()''' 
clock = time.Clock()
run = True
finish = False
bullets = sprite.Group()
lost = 0   

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_width, player_height, player_x, player_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_LEFT] or keys_pressed[K_a]) and self.rect.x > 0:
            self.rect.x -= self.speed
        elif (keys_pressed[K_RIGHT] or keys_pressed[K_d]) and self.rect.x < 620:
            self.rect.x += self.speed
    
    def fire(self):
        center_x = self.rect.centerx
        top_x = self.rect.top
        bullet = Bullet(player_image='bullet.png', player_speed=15, player_width=15, player_height=20, player_x=center_x, player_y=top_x)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y == 500 and self in monsters:
            self.rect.y = 0
            self.rect.x = randint(5, 615)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()


rocket = Player(player_image='rocket.png', player_speed=10, player_width=80, player_height=100, player_x=310, player_y=390)

monsters = sprite.Group()
for i in range(5):
    ufo = Enemy(player_image='ufo.png', player_speed=randint(1, 5), player_width=80, player_height=50, player_x=randint(5, 615), player_y=0)
    monsters.add(ufo)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(player_image='asteroid.png', player_speed=randint(1, 5), player_width=80, player_height=50, player_x=randint(5, 615), player_y=0)
    asteroids.add(asteroid)

lives = 3

write = font.Font(None, 70)
win = write.render('YOU WIN!', True, (136, 242, 131))
lose = write.render('YOU LOSE!', True, (242, 97, 97))


score = 0

write = font.Font(None, 36)
recharge = write.render('Wait, reload...', True, (179, 14, 14))

rel_time = False
rel_num = 0



while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if rel_time != True:
                    rocket.fire()
                    rel_num += 1
                    if rel_num == 5:
                        rel_time = True
                        now_time = rech_time.time()


    if finish != True:
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        write = font.Font(None, 36)
        text_win = write.render('Счет: ' + str(score), 1, (255, 255, 255))
        text_lose = write.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_win, (5, 15))
        window.blit(text_lose, (5, 50))
        bullets.draw(window)
        bullets.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        write = font.Font(None, 70)
        

        if rel_time == True:
            if rech_time.time() - now_time >= 3:
                rel_time = False
                rel_num = 0
            else:
                window.blit(recharge, (220, 464))

        for j in collides:
            score += 1
            ufo = Enemy(player_image='ufo.png', player_speed=randint(1, 5), player_width=80, player_height=50, player_x=randint(5, 615), player_y=0)
            monsters.add(ufo)

        if score == 10:
            window.blit(win, (300, 250))
            finish = True

        if lost >= 3 or sprite.spritecollide(rocket, monsters, True) or sprite.spritecollide(rocket, asteroids, True):
            lives -= 1
            if lives <= 0:
                window.blit(lose, (250, 250))
                finish = True

        live = write.render(str(lives), True, (61, 255, 68))
        window.blit(live, (670, 0))

        
        
    display.update()
    clock.tick(60)
