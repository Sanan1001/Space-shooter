from pygame import *
from random import randint

mixer.init()

class Wall(sprite.Sprite):
    def __init__(self, color_1, wall_x, wall_y, wall_width, wall_height):   
        super().__init__()
        self.color_1 = color_1
        self.wight = wall_width
        self.height = wall_height
        self.image = Surface((self.wight, self.height))
        self.image.fill((color_1))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def DrawWall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y, hp):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.hp = hp

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 3:
            self.rect.x -= 5 
        if keys_pressed[K_d] and self.rect.x < 900:
            self.rect.x += 5 
    
    def Fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 5, self.rect.top, 15, 10,20)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y >= 700:
            self.rect.y = 10
            lost = lost + 1
            self.rect.x = randint(100, 600)
        
    def boom(self):
        self.rect.y = 10

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y >= 700:
            self.rect.y = 10
            self.rect.x = randint(100, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y < 0:
            self.kill()

clock = time.Clock()

window = display.set_mode((1000 , 800))
display.set_caption('Шутер')

background = transform.scale(image.load("galaxy.jpg"), (1000 , 800))


game = True 
lost = 0
score = 0
finish = False

font.init()
#print(font.get_fonts() ) 
font1 = font.SysFont(None,60)
font2 = font.Font(None, 110)

mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')
fire.set_volume(0.1)

win = font2.render('YOU WIN!', True, (255,215,0))
lose = font2.render('YOU LOSE...', True, (180,0,0))
goal = font1.render('Цель: 20', True, (180,0,0))
plus1 = font2.render('+1', True, (130,5,54))

player = Player('rocket.png', 450 , 670, 1, 100, 120, 3)
health_img = GameSprite('hp.png', randint(80, 700), 100, 2, 50,50)
bomb = GameSprite('Fuse-Bomb.png', randint(80, 700), 100, 2, 50,50)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 6):
    monster = Enemy('ufo.png', randint(100,650), 100 , randint(2, 5) , 100, 70)
    monsters.add(monster)

for i in range(1, 3):
    asteroid = Asteroid('asteroid.png', randint(100,650), 100 , randint(2, 5) , 70, 50)
    asteroids.add(asteroid)
 
FPS= 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                player.Fire()

    if finish != True:
        window.blit(background, (0,0))
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(100,700), 100 , randint(2, 5) , 90, 70)
            monsters.add(monster)
           # window.blit(plus1, (randint(150, 750), randint(150, 750)))
    
        if lost >= 5: 
            window.blit(lose,(320,300))
            finish = True
            
        if score >= 20:
            window.blit(win,(320,300))
            finish = True 

        if player.hp <= 0:
            finish = True
            window.blit(lose,(320,300))

        if sprite.spritecollide(player, asteroids, True):
            if player.hp > 1:
                player.hp -= 2
                asteroid = Asteroid('asteroid.png', randint(100,650), 100 , randint(2, 5) , 70, 50)
                asteroids.add(asteroid)
            else:
                window.blit(lose,(320,300))
                finish = True  
 
        if sprite.spritecollide(player, monsters, True):
            if player.hp > 0:
                player.hp -= 1
                monster = Enemy('ufo.png', randint(100,650), 100 , randint(2, 5) , 100, 70)
                monsters.add(monster)
            else:
                window.blit(lose,(320,300))
                finish = True  

        if sprite.spritecollide(health_img, bullets, True):
            player.hp += 1
            health_img = GameSprite('hp.png', randint(150 , 700), 250, 2, 60,60)

        if sprite.spritecollide(bomb, bullets, True):
            bomb = GameSprite('Fuse-Bomb.png', randint(150, 700), 100, 2, 60,60)
            player.hp -= 1

        txt1 = font1.render('Пропущено: '+str(lost), True, (180,0,0))
        txt2 = font1.render('Счет:'+str(score), True, (180,0,0))
        health = font1.render('Жизней:'+str(player.hp), True,(180,0,0))

        window.blit(txt1, (10, 10))
        window.blit(txt2, (10, 50))
        window.blit(goal, (10, 90))
        window.blit(health, (10, 130))

        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        player.reset()
        health_img.reset()
        bomb.reset()

        player.update()
        asteroids.update()
        monsters.update()
        bullets.update()

    display.update()
    clock.tick(FPS)
