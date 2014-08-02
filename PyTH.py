#Organized in a Model-View-Controller format
#With object-oriented organization as well

import pygame, sys, os
from pygame.locals import *
import random, math
import copy

def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    color = image.get_at((0,0)) #To make image transparent
    image.set_colorkey(color)
    return image, image.get_rect()

def load_music(name):
    fullname = os.path.join('data', name)
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.25)

class Player(pygame.sprite.Sprite):
    lives = 4
    score = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('player1.bmp')
        self.health = 1
        self.lives = 3
        self.position = [200,448]
        self.rect.center = self.position
        self.dir = (0,0)
    
    def update(self):
        if (PyTH.pause == False):
            self.position[0] += self.dir[0]
            self.position[1] += self.dir[1]
            self.rect.center = self.position
            if (self.position[0] <= 25 or self.position[0] >= 375 or\
                self.position[1] <= 31 or self.position[1] >= 449):
                self.position[0] -= self.dir[0]
                self.position[1] -= self.dir[1]
                self.rect.center = self.position
        PyTH.background.blit(self.image,self.rect)
            
class Hitbox(Player):
    def __init__(self):
        super(Hitbox,self).__init__()
        self.image, self.rect = load_image('hitbox.bmp')
    
    def update(self):
        if (PyTH.pause == False):
            self.position[0] += self.dir[0]
            self.position[1] += self.dir[1]
            self.rect.center = self.position
            if (self.position[0] <= 25 or self.position[0] >= 375 or\
                self.position[1] <= 31 or self.position[1] >= 449):
                self.position[0] -= self.dir[0]
                self.position[1] -= self.dir[1]
                self.rect.center = self.position
            if (self.health <= 0): #When player dies
                for obj in PyTH.spriteManager.allSprites:
                    if (not(isinstance(obj,BossMonster))):
                        PyTH.spriteManager.allSprites.remove(obj)
                for obj in PyTH.spriteManager.monsterSprites:
                    if (not(isinstance(obj,BossMonster))):
                        PyTH.spriteManager.monsterSprites.remove(obj)
                PyTH.spriteManager.enemyBulletSprites.empty()
                PyTH.spriteManager.playerSprites.empty()
                PyTH.spriteManager.playerBulletSprites.empty()
                #Player.lives -= 1
                if (Player.lives <= 0):
                    PyTH.background.fill((0,0,20))
                    font = pygame.font.Font(None, 72)
                    self.text1=font.render("Game Over!", 1, (50,140,225))
                    self.textpos1=(160,240)
                    PyTH.background.blit(self.text1, self.textpos1)
                    PyTH.screen.blit(PyTH.background, (0,0))
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    PyTH.inMenu = True
                    PyTH.playing = False
                    PyTH.menuInit()
                else:
                    self.wait3Seconds()

    def wait3Seconds(self):
        PyTH.background.fill((0,0,20))
        font = pygame.font.Font(None, 72)
        self.text1=font.render("3", 1, (50,140,225))
        self.textpos1=(200,240)
        PyTH.background.blit(self.text1, self.textpos1)
        PyTH.sidebar.update()
        PyTH.screen.blit(PyTH.background, (0,0))
        pygame.display.flip()
        pygame.time.delay(1000)
        PyTH.background.fill((0,0,20))
        self.text1=font.render("2", 1, (50,140,225))
        PyTH.background.blit(self.text1, self.textpos1)
        PyTH.sidebar.update()
        PyTH.screen.blit(PyTH.background, (0,0))
        pygame.display.flip()
        pygame.time.delay(1000)
        PyTH.background.fill((0,0,20))
        self.text1=font.render("1", 1, (50,140,225))
        PyTH.background.blit(self.text1, self.textpos1)
        PyTH.sidebar.update()
        PyTH.screen.blit(PyTH.background, (0,0))
        pygame.display.flip()
        pygame.time.delay(1000)
        PyTH.player = Player()
        PyTH.hitbox = Hitbox()
        PyTH.spriteManager.allSprites.add(PyTH.player)
        PyTH.spriteManager.playerSprites.add(PyTH.hitbox)
        PyTH.spriteManager.allSprites.add(PyTH.hitbox)

class MonsterExplosion(pygame.sprite.Sprite):
    def __init__(self,score,position):
        pygame.sprite.Sprite.__init__(self)
        self.score = score
        self.position = position
        self.frameCount = 0
        self.image, self.rect = load_image('EmptyImage.bmp')
        
    def update(self):
        if (PyTH.pause == False):
            self.frameCount += 1
            if (self.frameCount >= 40):
            #Want to display the +Score "explosion" for 1 second
                PyTH.spriteManager.allSprites.remove(self)
            font = pygame.font.Font(None, 36)
            self.text1=font.render("+%d" %\
                                   (self.score), 1, (50,140,225))
            if (self.frameCount == 1):
                horizOffset = (font.size("+%d" % self.score)[0])/2
                self.position[0] -= horizOffset
            self.textpos1 = self.position
        PyTH.background.blit(self.text1, self.textpos1)
        
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
    def update(self):
        if (PyTH.pause == False):
            if (self.health <= 0):
                Player.score += self.score
                self.explosion = MonsterExplosion(self.score,self.position)
                PyTH.spriteManager.allSprites.add(self.explosion)
                PyTH.spriteManager.monsterSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)

class MiniMonster1(Monster):
    def __init__(self):
        super(MiniMonster1,self).__init__()
        self.image, self.rect = load_image('MiniMonster1.bmp')
        self.health = 1
        self.speed = 1.5
        self.score = 50
        self.position = [random.randint(25,375),-10]
        self.rect.center = self.position
        
    def update(self):
        if (PyTH.pause == False):
            super(MiniMonster1,self).update()
            if (self.rect.y < 125): #Moving down initially
                self.position[1] += self.speed
                self.rect.center = self.position
            elif (self.rect.y >= 125 and self.rect.x < 200): #Moving to the left
                self.position[0] -= self.speed
                self.rect.center = self.position
            elif (self.rect.y >= 125 and self.rect.x >= 200): #Moving to the right
                self.position[0] += self.speed
                self.rect.center = self.position
            elif (self.rect.x < 0 or self.rect.x > 400):
                #Getting rid of off-screen monsters
                PyTH.spriteManager.monsterSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class MiniMonster2(Monster):
    def __init__(self):
        super(MiniMonster2,self).__init__()
        self.image, self.rect = load_image('MiniMonster2.bmp')
        self.health = 1
        self.speed = 2
        self.score = 75
        self.position = [random.randint(25,375),-10]
        self.rect.center = self.position
        
    def update(self):
        if (PyTH.pause == False):
            super(MiniMonster2,self).update()
            self.position[1] += self.speed
            self.rect.center = self.position
            if (self.rect.y > 500): #getting rid of off-screen monsters
                PyTH.spriteManager.monsterSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class MiniMonster3(Monster):
    def __init__(self):
        super(MiniMonster3,self).__init__()
        self.image, self.rect = load_image('MiniMonster3.bmp')
        self.health = 5
        self.r = 7
        self.speed = 1.5
        self.circumSpeed = (self.r*2*math.pi)/120
        #We want this to spin 1 time per second
        #120 updates per second of course
        self.radianCount = 0
        self.score = 150
        self.position = [random.randint(25,375),-10]
        self.rect.center = self.position
        
    def update(self):
        if (PyTH.pause == False):
            super(MiniMonster3,self).update()
            self.radianCount += math.pi/60
            self.position[0] += self.r*self.circumSpeed*math.cos(self.radianCount)
            self.position[1] += self.speed + self.r * self.circumSpeed *\
                                math.sin(self.radianCount)
            self.rect.center = self.position
            if (self.rect.y > 500): #getting rid of off-screen monsters
                PyTH.spriteManager.monsterSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class BossMonster(Monster):
    def __init__(self):
        super(BossMonster,self).__init__()
        self.image, self.rect = load_image('boss.bmp')
        self.health = 400
        self.ticker = 0
        self.speed = 0.5
        self.radianCount = 0
        self.score = 42
        self.position = [200,-10]
        self.rect.center = self.position
        
    def update(self):
        if (PyTH.pause == False):
            super(BossMonster,self).update()
            self.ticker += 1
            if (self.position[1] < 150):
                self.position[1] += self.speed
                self.rect.center = self.position
            else:
                if (self.ticker % 30 == 0):
                    self.circularFormation()
                if (self.ticker % 120 == 0):
                    self.randomFormation()
            if (self.health <= 0):
                PyTH.inMenu = True
                PyTH.playing = False
                PyTH.currentMenu = PyTH.winScreen
        PyTH.background.blit(self.image,self.rect)
    
    def circularFormation(self):
        PyTH.bossMonsterBullet1 = BulletBossMonster1(1)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet1)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet1)
        PyTH.bossMonsterBullet2 = BulletBossMonster1(2)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet2)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet2)
        PyTH.bossMonsterBullet3 = BulletBossMonster1(3)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet3)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet3)
        PyTH.bossMonsterBullet4 = BulletBossMonster1(4)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet4)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet4)
        PyTH.bossMonsterBullet5 = BulletBossMonster1(5)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet5)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet5)
        PyTH.bossMonsterBullet6 = BulletBossMonster1(6)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet6)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet6)
        PyTH.bossMonsterBullet7 = BulletBossMonster1(7)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet7)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet7)
        PyTH.bossMonsterBullet8 = BulletBossMonster1(8)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet8)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet8)
        PyTH.bossMonsterBullet9 = BulletBossMonster1(9)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet9)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet9)
        PyTH.bossMonsterBullet10 = BulletBossMonster1(10)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet10)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet10)
        PyTH.bossMonsterBullet11 = BulletBossMonster1(11)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet11)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet11)

    def randomFormation(self):
        PyTH.bossMonsterBullet12 = BulletBossMonster2(1)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet12)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet12)
        PyTH.bossMonsterBullet13 = BulletBossMonster2(2)
        PyTH.spriteManager.enemyBulletSprites.add(PyTH.bossMonsterBullet13)
        PyTH.spriteManager.allSprites.add(PyTH.bossMonsterBullet13)
    
class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.option = 0
        
    def upChoice(self): #Choosing the upward option
        if (self.option > 0):
            self.choices[self.option][1] = (50,140,225)
            self.option -= 1
            self.choices[self.option][1] = (255,255,255)
            self.display()
    
    def downChoice(self): #Choosing the downward option
        if (self.option < len(self.choices)-1):
            self.choices[self.option][1] = (50,140,225)
            self.option += 1
            self.choices[self.option][1] = (255,255,255)
            self.display()

class StartMenu(Menu):
    def __init__(self):
        super(StartMenu,self).__init__()
        self.choices = [["New Game",(255,255,255),(50,300)],
                   ["Help",(50,140,225),(50,335)],
                   ["Quit",(50,140,225),(50,370)]]
        self.image, self.rect = load_image('MenuBackground.bmp')
    
    def display(self):
        if pygame.font:
            font = pygame.font.Font(None, 36)
            for curOption in xrange(len(self.choices)):
                text = font.render(self.choices[curOption][0], 1,\
                                   self.choices[curOption][1])
                textpos = self.choices[curOption][2]
                PyTH.background.blit(text, textpos)
                PyTH.background.blit(self.image,self.rect)
            font = pygame.font.Font(None, 24)
            self.text1=font.render("Press Up and Down arrows to choose"\
                                   ,1,(50,140,225))
            self.textpos1=(50,420)
            self.text2=font.render("and 'z' to select"\
                                   ,1,(50,140,225))
            self.textpos2=(50,440)
            font = pygame.font.Font(None, 72)
            self.text3=font.render("Py-Touhou!", 1, (50,140,225))
            self.textpos3=(50,100)
            PyTH.background.blit(self.text1, self.textpos1)
            PyTH.background.blit(self.text2, self.textpos2)
            PyTH.background.blit(self.text3, self.textpos3)
    
    def select(self):
        if (self.option == 0):
            return "self.newGame()"
        elif (self.option == 1):
            PyTH.helpScreen = HelpScreen()
            return "self.helpScreen.display()"
        elif (self.option == 2):
            return "sys.exit()"
    
class HelpScreen(pygame.sprite.Sprite):
    def __init__(self):
        super(HelpScreen,self).__init__()
        font = pygame.font.Font(None, 36)
        self.text1=font.render("Hold arrow keys to move, 'z' to shoot.",\
                                1, (50,140,225))
        self.textpos1=(50,130)
        self.text2=font.render("Don't let bullets hit your heart.",\
                               1, (50,140,225))
        self.textpos2=(50,165)
        self.text3=font.render("Hold left shift to display your heart.",\
                                1, (50,140,225))
        self.textpos3=(50,200)
        self.text4=font.render("Note: This will reduce your speed by half.",\
                                1, (50,140,225))
        self.textpos4=(50,235)
        self.text5=font.render("Earn enough points to progress on difficulty.",\
                                1, (50,140,225))
        self.textpos5=(50,270)
        self.text6=font.render("Finally, press 'z' to play",\
                                1, (50,140,225))
        self.textpos6=(50,440)

    def display(self):
        PyTH.currentMenu = PyTH.helpScreen
        PyTH.background.blit(self.text1, self.textpos1)
        PyTH.background.blit(self.text2, self.textpos2)
        PyTH.background.blit(self.text3, self.textpos3)
        PyTH.background.blit(self.text4, self.textpos4)
        PyTH.background.blit(self.text5, self.textpos5)
        PyTH.background.blit(self.text6, self.textpos6)
    
    def select(self):
        return "self.newGame()"
        
    #Again, created to prevent crashing
    def upChoice(self):
        pass
    
    def downChoice(self):
        pass

class WinScreen(pygame.sprite.Sprite):
    def __init__(self):
        super(WinScreen,self).__init__()
        font = pygame.font.Font(None, 44)
        self.text1=font.render("Congratulations, you have won!",\
                                1, (50,140,225))
        self.textpos1=(80,240)
        font = pygame.font.Font(None, 36)
        self.text2=font.render("Press 'z' to return to main screen.",\
                                1, (50,140,225))
        self.textpos2=(50,440)

    def display(self):
        PyTH.currentMenu = PyTH.winScreen
        PyTH.background.blit(self.text1, self.textpos1)
        PyTH.background.blit(self.text2, self.textpos2)
    
    def select(self):
        PyTH.inMenu = True
        PyTH.playing = False
        return "self.menuInit()"
        
    def upChoice(self):
        pass
    
    def downChoice(self):
        pass

class Bullet(pygame.sprite.LayeredUpdates,pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()

class PlayerBullet(Bullet):
    def __init__(self):
        super(PlayerBullet, self).__init__()
        self.image, self.rect = load_image('missile1.bmp')
        self.position = copy.copy(PyTH.player.position)
        self.position[1] -= 15
        self.rect.center = self.position
        self.speed = 7.5
    
    def update(self):
        if (PyTH.pause == False):
            self.rect.y -= self.speed
            if (self.rect.y < -20): #getting rid of off-screen bullets
                PyTH.spriteManager.playerBulletSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class BulletMiniMonster1(Bullet):
    def __init__(self):
        super(BulletMiniMonster1, self).__init__()
        self.playerPosition = copy.copy(PyTH.player.position)
        self.monsterPosition = copy.copy(PyTH.miniMonster1.position)
        self.image, self.rect = load_image('MiniMonster1Bullet.bmp')
        self.position = self.monsterPosition
        self.rect.center = self.position
    
    def update(self):
        if (PyTH.pause == False):
            self.position[1] += 2
            self.rect.center = self.position
            if (self.rect.y > 500.0 or self.rect.y < -30.0 or\
                self.rect.x > 420.0 or self.rect.x < -20.0):
                #getting rid of off-screen bullets
                PyTH.spriteManager.enemyBulletSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class BulletMiniMonster2(Bullet):
    def __init__(self):
        super(BulletMiniMonster2, self).__init__()
        self.playerPosition = copy.copy(PyTH.player.position)
        self.monsterPosition = copy.copy(PyTH.miniMonster2.position)
        self.image, self.rect = load_image('MiniMonster2Bullet.bmp')
        self.position = self.monsterPosition
        self.rect.center = self.position
        if (self.playerPosition[0] == self.monsterPosition[0]):
            #We don't want a zero float division
            #Velocity given by [speed,direction in radians]
            self.velocity = [3,1.5707963267948966192313216916398]
        else:
            self.velocity =[3,\
                math.atan2(self.playerPosition[1]-self.monsterPosition[1],\
                          (self.playerPosition[0]-self.monsterPosition[0]))]
    
    def update(self):
        if (PyTH.pause == False):
            self.position[0] += self.velocity[0]*math.cos(self.velocity[1])
            self.position[1] += self.velocity[0]*math.sin(self.velocity[1])
            self.rect.center = self.position
            if (self.rect.y > 500.0 or self.rect.y < -30.0 or\
                self.rect.x > 420.0 or self.rect.x < -20.0):
                #getting rid of off-screen bullets
                PyTH.spriteManager.enemyBulletSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class BulletMiniMonster3(Bullet):
    def __init__(self,direction):
        super(BulletMiniMonster3, self).__init__()
        self.playerPosition = copy.copy(PyTH.player.position)
        self.monsterPosition = copy.copy(PyTH.miniMonster3.position)
        self.image, self.rect = load_image('MiniMonster3Bullet.bmp')
        self.direction = direction
        self.position = self.monsterPosition
        self.rect.center = self.position
        if (self.direction == 1):
            if (self.playerPosition[0] == self.monsterPosition[0]):
                #We don't want a zero float division
                #Velocity given by [speed,direction in radians]
                self.velocity = [4,1.5707963267948966192313216916398\
                                 + (math.pi/9)]
            else:
                self.velocity =[4,\
                    math.atan2(self.playerPosition[1]-self.monsterPosition[1],\
                              (self.playerPosition[0]-self.monsterPosition[0]))\
                               + (math.pi/9)]
        elif (self.direction == 2):
            if (self.playerPosition[0] == self.monsterPosition[0]):
                self.velocity = [4,1.5707963267948966192313216916398]
            else:
                self.velocity =[4,\
                    math.atan2(self.playerPosition[1]-self.monsterPosition[1],\
                              (self.playerPosition[0]-self.monsterPosition[0]))]
        elif (self.direction == 3):
            if (self.playerPosition[0] == self.monsterPosition[0]):
                self.velocity = [4,1.5707963267948966192313216916398\
                                 - (math.pi/9)]
            else:
                self.velocity =[4,\
                    math.atan2(self.playerPosition[1]-self.monsterPosition[1],\
                              (self.playerPosition[0]-self.monsterPosition[0]))\
                               - (math.pi/9)]
    
    def update(self):
        if (PyTH.pause == False):
            self.position[0] += self.velocity[0]*math.cos(self.velocity[1])
            self.position[1] += self.velocity[0]*math.sin(self.velocity[1])
            self.rect.center = self.position
            if (self.rect.y > 500.0 or self.rect.y < -30.0 or\
                self.rect.x > 420.0 or self.rect.x < -20.0):
                #getting rid of off-screen bullets
                PyTH.spriteManager.enemyBulletSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class BulletBossMonster1(Bullet):
    def __init__(self,direction):
        super(BulletBossMonster1, self).__init__()
        self.monsterPosition = copy.copy(PyTH.bossMonster.position)
        self.image, self.rect = load_image('MiniMonster1Bullet.bmp')
        self.direction = direction
        self.position = self.monsterPosition
        self.rect.center = self.position
        self.velocity =[3,(self.direction-1)*(math.pi/10)]
    
    def update(self):
        if (PyTH.pause == False):
            self.position[0] += self.velocity[0]*math.cos(self.velocity[1])
            self.position[1] += self.velocity[0]*math.sin(self.velocity[1])
            self.rect.center = self.position
            if (self.rect.y > 500.0 or self.rect.y < -30.0 or\
                self.rect.x > 420.0 or self.rect.x < -20.0):
                #getting rid of off-screen bullets
                PyTH.spriteManager.enemyBulletSprites.remove(self)
                PyTH.spriteManager.allSprites.remove(self)
        PyTH.background.blit(self.image,self.rect)

class BulletBossMonster2(Bullet):
    def __init__(self,eyePosition):
        super(BulletBossMonster2, self).__init__()
        self.monsterPosition = copy.copy(PyTH.bossMonster.position)
        self.image, self.rect = load_image('MiniMonster2Bullet.bmp')
        self.eyePosition = eyePosition
        if (self.eyePosition == 1):
            #Left eye
            self.monsterPosition[0] -= 18
            self.position = self.monsterPosition
        elif (self.eyePosition == 2):
            #Right eye
            self.monsterPosition[0] += 18
            self.position = self.monsterPosition
        self.rect.center = self.position
        self.randomAccelX = 0.05*(random.random()-0.5)*3
        self.randomAccelY = math.sqrt(0.005625 - self.randomAccelX**2)
        self.velocity = [0,0]
        self.acceleration = [self.randomAccelX,self.randomAccelY]
    
    def update(self):
        if (PyTH.pause == False):
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]
            if (self.velocity[0]**2 + self.velocity[1]**2 < 9):
                self.velocity[0] += self.acceleration[0]
                self.velocity[1] += self.acceleration[1]
            self.rect.center = self.position
            if (self.rect.y >= 455.0 or self.rect.y < 0.0):
                self.velocity[1] = -self.velocity[1]
            elif(self.rect.x >= 375.0 or self.rect.x < 0.0):
                self.velocity[0] = -self.velocity[0]
        PyTH.background.blit(self.image,self.rect)

class SpriteManager(object):
    def __init__(self):
        self.allSprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.playerBulletSprites = pygame.sprite.Group()
        self.monsterSprites = pygame.sprite.Group()
        self.enemyBulletSprites = pygame.sprite.Group()

class Sidebar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sidebar = pygame.Surface([240, 480])
        self.sidebar.fill((20,0,0))
        self.sidebarRect = self.sidebar.get_rect()
        self.sidebarRect.center = (520,240)
    
    def update(self):
        self.score = Player.score
        self.lives = Player.lives
        font = pygame.font.Font(None, 36)
        self.text1=font.render("Score: %d" %\
                               (self.score), 1, (50,140,225))
        self.textpos1=(440,50)
        self.text2=font.render("Lives: %d" %\
                               (self.lives), 1, (50,140,225))
        self.textpos2=(440,80)
        self.text3=font.render("Points to", 1, (50,140,225))
        self.textpos3=(440,150)
        self.text4=font.render("next level: %d" %\
                               (PyTH.nextLevelScore), 1, (50,140,225))
        self.textpos4=(440,180)
        PyTH.background.blit(self.sidebar,self.sidebarRect)
        PyTH.background.blit(self.text1, self.textpos1)
        PyTH.background.blit(self.text2, self.textpos2)
        PyTH.background.blit(self.text3, self.textpos3)
        PyTH.background.blit(self.text4, self.textpos4)

class main(object):
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(0)
        self.size = self.width,self.height = 640,480
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("PyTH")
        self.clock = pygame.time.Clock()
        self.playing = False
        self.shooting = False
        self.spriteManager = SpriteManager()
        self.inMenu = True
    
    def newGame(self):
        self.spriteManager.allSprites.empty()
        self.spriteManager.playerSprites.empty()
        self.spriteManager.monsterSprites.empty()
        self.spriteManager.playerBulletSprites.empty()
        self.spriteManager.enemyBulletSprites.empty()
        self.inMenu = False
        self.playing = True
        self.showHitbox = False
        self.miniMonster1Count = 0
        self.miniMonster2Count = 0
        self.miniMonster3Count = 0
        self.ticker = 0
        self.bossTicker = 0
        self.player = Player()
        self.hitbox = Hitbox()
        self.sidebar = Sidebar()
        self.pause = False
        Player.lives = 4
        Player.score = 0
        self.nextLevelScore = 2000
        self.spriteManager.allSprites.add(self.player)
        self.spriteManager.playerSprites.add(self.hitbox)
        self.spriteManager.allSprites.add(self.hitbox)
    
    def miniEnemy1Spawn(self):
        #Want to spawn minimonsters every 0.33 second
        self.miniMonster1Count += 1
        if (self.miniMonster1Count == 40):
            self.miniMonster1Count = 0
            self.miniMonster1 = MiniMonster1()
            self.spriteManager.monsterSprites.add(self.miniMonster1)
            self.spriteManager.allSprites.add(self.miniMonster1)
            self.miniMonster1Bullet = BulletMiniMonster1()
            self.spriteManager.enemyBulletSprites.add(self.miniMonster1Bullet)
            self.spriteManager.allSprites.add(self.miniMonster1Bullet)

    def miniEnemy2Spawn(self):
        #Want to spawn minimonsters every 0.25 second
        self.miniMonster2Count += 1
        if (self.miniMonster2Count == 30):
            self.miniMonster2Count = 0
            self.miniMonster2 = MiniMonster2()
            self.spriteManager.monsterSprites.add(self.miniMonster2)
            self.spriteManager.allSprites.add(self.miniMonster2)
            self.miniMonster2Bullet = BulletMiniMonster2()
            self.spriteManager.enemyBulletSprites.add(self.miniMonster2Bullet)
            self.spriteManager.allSprites.add(self.miniMonster2Bullet)
    
    def miniEnemy3Spawn(self):
        #Want to spawn minimonsters every 0.20 second
        self.miniMonster3Count += 1
        if (self.miniMonster3Count == 24):
            self.miniMonster3Count = 0
            self.miniMonster3 = MiniMonster3()
            self.spriteManager.monsterSprites.add(self.miniMonster3)
            self.spriteManager.allSprites.add(self.miniMonster3)
            self.miniMonster3Bullet1 = BulletMiniMonster3(1)
            self.spriteManager.enemyBulletSprites.add(self.miniMonster3Bullet1)
            self.spriteManager.allSprites.add(self.miniMonster3Bullet1)
            self.miniMonster3Bullet2 = BulletMiniMonster3(2)
            self.spriteManager.enemyBulletSprites.add(self.miniMonster3Bullet2)
            self.spriteManager.allSprites.add(self.miniMonster3Bullet2)
            self.miniMonster3Bullet3 = BulletMiniMonster3(3)
            self.spriteManager.enemyBulletSprites.add(self.miniMonster3Bullet3)
            self.spriteManager.allSprites.add(self.miniMonster3Bullet3)
    
    def bossSpawn(self):
        self.bossMonster = BossMonster()
        self.spriteManager.monsterSprites.add(self.bossMonster)
        self.spriteManager.allSprites.add(self.bossMonster)

    def stageSet(self):
        if (PyTH.pause == False):
            if (Player.score >= 0 and Player.score < 2000):
                self.miniEnemy1Spawn()
                self.nextLevelScore = 2000
            elif (Player.score >= 2000 and Player.score < 5000):
                self.miniEnemy2Spawn()
                self.nextLevelScore = 5000
            elif (Player.score >= 5000 and Player.score < 15000):
                self.miniEnemy3Spawn()
                self.nextLevelScore = 15000
            elif (Player.score >= 15000):
                self.bossTicker += 1
                if (self.bossTicker == 1):
                    self.bossSpawn()
                self.nextLevelScore = 0
    
    def mainInit(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,20))
        self.menuInit()

    def menuInit(self):
        self.startMenu = StartMenu()
        self.winScreen = WinScreen()
        self.currentMenu = self.startMenu
        self.currentMenu.display()
        load_music('menu.mp3')
        self.mainLoop()
    
    def mainLoop(self):
        while True:
            self.background.fill((0,0,20))
            pygame.time.wait(8) #for smooth performance
            pygame.event.pump()
            for event in pygame.event.get(): #keyPressed equivalent
                if event.type == pygame.QUIT: sys.exit()
                if (self.inMenu == True):
                    if event.type == KEYDOWN:
                        if (event.key == K_UP):
                            self.currentMenu.upChoice()
                        elif (event.key == K_DOWN):
                            self.currentMenu.downChoice()
                        elif (event.key == K_z):
                            eval(self.currentMenu.select())
                else:
                    keys = pygame.key.get_pressed()
                    #273 - Up
                    #274 - Down
                    #275 - Right
                    #276 - Left
                    #304 - Left Shift
                    if(event.type == KEYDOWN):
                        if (keys[273] == 1 and keys[274] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (0,-5.6)
                            self.hitbox.dir = (0,-5.6)
                        elif (keys[274] == 1 and keys[273] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (0,+5.6)
                            self.hitbox.dir = (0,+5.6)
                        elif (keys[276] == 1 and keys[274] == keys[275] ==\
                            keys[273] == 0 and keys[304] == 0):
                            self.player.dir = (-5.6,0)
                            self.hitbox.dir = (-5.6,0)
                        elif (keys[275] == 1 and keys[274] == keys[273] ==\
                            keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (+5.6,0)
                            self.hitbox.dir = (+5.6,0)
                        elif (keys[273] == keys[276] == 1 and\
                              keys[274] == keys[275] == 0 and keys[304] == 0):
                            self.player.dir = (-4.0,-4.0)
                            self.hitbox.dir = (-4.0,-4.0)
                        elif (keys[273] == keys[275] == 1 and\
                              keys[274] == keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (+4.0,-4.0)
                            self.hitbox.dir = (+4.0,-4.0)
                        elif (keys[274] == keys[276] == 1 and\
                              keys[273] == keys[275] == 0 and keys[304] == 0):
                            self.player.dir = (-4.0,+4.0)
                            self.hitbox.dir = (-4.0,+4.0)
                        elif (keys[274] == keys[275] == 1 and\
                              keys[273] == keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (+4.0,+4.0)
                            self.hitbox.dir = (+4.0,+4.0)
                        #From here on, holding shift makes you move slower
                        #But displays the hitbox
                        elif (keys[273] == 1 and keys[274] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (0,-2.8)
                            self.hitbox.dir = (0,-2.8)
                        elif (keys[274] == 1 and keys[273] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (0,+2.8)
                            self.hitbox.dir = (0,+2.8)
                        elif (keys[276] == 1 and keys[274] == keys[275] ==\
                            keys[273] == 0 and keys[304] == 1):
                            self.player.dir = (-2.8,0)
                            self.hitbox.dir = (-2.8,0)
                        elif (keys[275] == 1 and keys[274] == keys[273] ==\
                            keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (+2.8,0)
                            self.hitbox.dir = (+2.8,0)
                        elif (keys[273] == keys[276] == 1 and\
                              keys[274] == keys[275] == 0 and keys[304] == 1):
                            self.player.dir = (-2.0,-2.0)
                            self.hitbox.dir = (-2.0,-2.0)
                        elif (keys[273] == keys[275] == 1 and\
                              keys[274] == keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (+2.0,-2.0)
                            self.hitbox.dir = (+2.0,-2.0)
                        elif (keys[274] == keys[276] == 1 and\
                              keys[273] == keys[275] == 0 and keys[304] == 1):
                            self.player.dir = (-2.0,+2.0)
                            self.hitbox.dir = (-2.0,+2.0)
                        elif (keys[274] == keys[275] == 1 and\
                              keys[273] == keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (+2.0,+2.0)
                            self.hitbox.dir = (+2.0,+2.0)
                        if (keys[304] == 0):
                            self.showHitbox = False
                        elif (keys[304] == 1):
                            self.showHitbox = True
                        if (event.key == K_z):
                            self.shooting = True
                        if (event.key == K_r):
                            self.newGame()
                        if (event.key == K_p):
                            self.pause = not(self.pause)

                    elif(event.type == KEYUP):
                        if (keys[273] == keys[276] ==\
                            keys[274] == keys[275] == 0):
                            self.player.dir = (0,0)
                            self.hitbox.dir = (0,0)
                        elif (keys[273] == 1 and keys[274] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (0,-5.6)
                            self.hitbox.dir = (0,-5.6)
                        elif (keys[274] == 1 and keys[273] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (0,+5.6)
                            self.hitbox.dir = (0,+5.6)
                        elif (keys[276] == 1 and keys[274] == keys[275] ==\
                            keys[273] == 0 and keys[304] == 0):
                            self.player.dir = (-5.6,0)
                            self.hitbox.dir = (-5.6,0)
                        elif (keys[275] == 1 and keys[274] == keys[273] ==\
                            keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (+5.6,0)
                            self.hitbox.dir = (+5.6,0)
                        elif (keys[273] == keys[276] == 1 and\
                              keys[274] == keys[275] == 0 and keys[304] == 0):
                            self.player.dir = (-4.0,-4.0)
                            self.hitbox.dir = (-4.0,-4.0)
                        elif (keys[273] == keys[275] == 1 and\
                              keys[274] == keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (+4.0,-4.0)
                            self.hitbox.dir = (+4.0,-4.0)
                        elif (keys[274] == keys[276] == 1 and\
                              keys[273] == keys[275] == 0 and keys[304] == 0):
                            self.player.dir = (-4.0,+4.0)
                            self.hitbox.dir = (-4.0,+4.0)
                        elif (keys[274] == keys[275] == 1 and\
                              keys[273] == keys[276] == 0 and keys[304] == 0):
                            self.player.dir = (+4.0,+4.0)
                            self.hitbox.dir = (+4.0,+4.0)
                        #Same deal as before
                        elif (keys[273] == 1 and keys[274] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (0,-2.8)
                            self.hitbox.dir = (0,-2.8)
                        elif (keys[274] == 1 and keys[273] == keys[275] ==\
                            keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (0,+2.8)
                            self.hitbox.dir = (0,+2.8)
                        elif (keys[276] == 1 and keys[274] == keys[275] ==\
                            keys[273] == 0 and keys[304] == 1):
                            self.player.dir = (-2.8,0)
                            self.hitbox.dir = (-2.8,0)
                        elif (keys[275] == 1 and keys[274] == keys[273] ==\
                            keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (+2.8,0)
                            self.hitbox.dir = (+2.8,0)
                        elif (keys[273] == keys[276] == 1 and\
                              keys[274] == keys[275] == 0 and keys[304] == 1):
                            self.player.dir = (-2.0,-2.0)
                            self.hitbox.dir = (-2.0,-2.0)
                        elif (keys[273] == keys[275] == 1 and\
                              keys[274] == keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (+2.0,-2.0)
                            self.hitbox.dir = (+2.0,-2.0)
                        elif (keys[274] == keys[276] == 1 and\
                              keys[273] == keys[275] == 0 and keys[304] == 1):
                            self.player.dir = (-2.0,+2.0)
                            self.hitbox.dir = (-2.0,+2.0)
                        elif (keys[274] == keys[275] == 1 and\
                              keys[273] == keys[276] == 0 and keys[304] == 1):
                            self.player.dir = (+2.0,+2.0)
                            self.hitbox.dir = (+2.0,+2.0)
                        if (keys[304] == 0):
                            self.showHitbox = False
                        elif (keys[304] == 1):
                            self.showHitbox = True
                        if (event.key == K_z):
                            self.shooting = False

            if self.inMenu == True:
                self.moveable = False
                self.playing = False
                self.currentMenu.display()
            
            if self.playing == True:
                self.inMenu = False
                self.ticker += 1 #Preventing unnecessary spamming
                if (self.shooting == True and self.ticker % 5 == 0):
                    self.bullet = PlayerBullet()
                    # Add the bullet to the lists
                    self.spriteManager.playerBulletSprites.add(self.bullet)
                    self.spriteManager.allSprites.add(self.bullet)
                self.stageSet()
                for bullet in self.spriteManager.playerBulletSprites:
                    # See if bullet hits a monster
                    monsterList = pygame.sprite.spritecollide(bullet,\
                                    self.spriteManager.monsterSprites, False)
                    for monster in monsterList:
                        self.spriteManager.playerBulletSprites.remove(bullet)
                        self.spriteManager.allSprites.remove(bullet)
                        monster.health -= 1
                for bullet in self.spriteManager.enemyBulletSprites:
                    # See if enemy bullet hits your hitbox
                    myList = pygame.sprite.spritecollide(bullet,\
                                self.spriteManager.playerSprites, False)
                    for player in myList:
                        self.spriteManager.playerBulletSprites.remove(bullet)
                        self.spriteManager.allSprites.remove(bullet)
                        player.health -= 1
                self.spriteManager.allSprites.update()
                if (self.showHitbox == True):
                    self.background.blit(self.hitbox.image,self.hitbox.rect)
                self.sidebar.update()
            self.spriteManager.allSprites.draw(self.screen)
            self.screen.blit(self.background, (0,0))
            pygame.display.flip()

PyTH = main()
PyTH.mainInit()

#References:
#Images borrowed from:
#http://i187.photobucket.com/albums/x308/Xenomic/RPG%20Maker%20Stuff/Battle%20Animations/HakureiBorderPersuasionNeedle.png
#http://i187.photobucket.com/albums/x308/Xenomic/RPG%20Maker%20Stuff/Battle%20Animations/PhotosynthesisPhilosophersStone.png
#http://img217.imageshack.us/img217/78/stg7enm.png
#http://th02.deviantart.net/fs71/PRE/f/2014/095/b/d/touhou_kokichi_spritework___bullets_by_popfan95b-d77iitu.png
#http://wallpoper.com/images/00/40/79/46/video-games_00407946.png
#http://kosbie.net/cmu/dkosbie.jpg
#http://4.bp.blogspot.com/_Y4WHRLSPsxo/TJq6nq69bdI/AAAAAAAAADg/2RwWDBRzybU/s1600/cdbg07a.png
#Background Music - Paul Van Dyk - For An Angel