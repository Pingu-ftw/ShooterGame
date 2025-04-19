from pygame import *
from random import randint
from pygame import sprite
from time import time as timer

#Music
#font
font.init()
font1 = font.Font(None, 80)
winText = font1.render("You win!", True, (255, 255, 255))
loseText = font1.render("You lose!", True, (180, 0, 0))
font2 = font.Font(None, 36)

#Images
imgBg = "images.jpg"
imgPlayer = "fairy.png"
imgEnemy = "frog.png"
imgBullet = "star.png"
img_ast = "ast.png"

#Variables
score = 0
lost = 0
maxLost = 10
goal = 20
life = 3

#create a window
win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Magical fairy! Pew pew power full throttle!!!")
background = transform.scale(image.load(imgBg), (win_width, win_height))

#class for other sprites
class GameSprite(sprite.Sprite):
    def __init__(self, playerImage, playerX, playerY, sizeX, sizeY, playerSpeed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(playerImage), (sizeX, sizeY))
        self.speed = playerSpeed
        self.rect = self.image.get_rect()
        self.rect.x = playerX
        self.rect.y = playerY

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappear
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y=0
            lost += 1


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(imgBullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()


#generate characters
player = Player(imgPlayer, 5, win_height - 110, 125, 125, 10)
enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy(imgEnemy, randint(80, win_width-80), -40, 60, 60, randint(1, 5))
    enemies.add(enemy)

bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

finish = False
rel_time = False
num_fire = 0
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    #fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
        if not finish:
            window.blit(background, (0,0))

            #text
            text = font2.render("Score: "+str(score), 1, (255, 255, 255))
            window.blit(text,(10, 20))

            text_lose = font2.render("Missed: "+str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))

            player.update()
            enemies.update()
            bullets.update()
            asteroids.update()

            player.reset()
            enemies.draw(window)
            bullets.draw(window)
            asteroids.draw(window)

            if rel_time == True:
                now_time = timer()
                if now_time - last_time < 3:
                    reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                    window.blit(reload, (260, 460))
                else:
                    num_fire = 0
                    rel_time = False

            #Check collision between star and enemy
            collides = sprite.groupcollide(enemies, bullets, True, True)
            for collide in collides:
                score += 1 #score = score + 1
                enemy = Enemy(imgEnemy, randint(80, win_width-80), -40, 60, 60, randint(1, 5))
                enemies.add(enemy)

            if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
                sprite.spritecollide(player, enemies, True)
                sprite.spritecollide(player, asteroids, True)
                life = life -1
            if life == 0 or lost >= maxLost:
                finish = True

                window.blit(loseText, (200, 200))

                #conditional statement for winning the game
            if score >= goal:

                finish = True
                window.blit(winText, (200, 200))

            if life == 3:
                life_color = (0, 150, 0)
            if life == 2:
                life_color = (150, 150, 0)
            if life == 1:
                life_color = (150, 0, 0)
            text_life = font1.render(str(life), 1, life)
            window.blit(text_life, (650, 10))
            display.update()

        else:
            finish = False
            score = 0
            lost = 0
            num_fire = 0
            life = 3
            for a in asteroids:
                a.kill()
            for bullet in bullets:
                bullet.kill()
            for enemy in enemies:
                enemy.kill()
            time.delay(3000)
            for i in range(1, 6):
                enemy = Enemy(imgEnemy, randint(80, win_width - 80), -40, 60, 60, randint(1, 5))
                enemies.add(enemy)
            for i in range(1, 3):
                asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
                asteroids.add(asteroid)


        time.delay(50)