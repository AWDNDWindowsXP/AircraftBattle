# 搭建一个宽高为480， 650的游戏窗口
# 并且添加游戏关闭事件

import pygame
import configparser
import logging
import sys
import time
import random
import modes.modes

config = configparser.ConfigParser()
config.read('launch_config.ini', encoding='utf-8')
mode = config.get('launcher', 'debug')
if mode == 'off':
    logging.basicConfig(level=modes.modes.normal_mode, format="%(asctime)s - %(levelname)s : %(message)s")
elif mode == 'on':
    logging.basicConfig(level=modes.modes.debug_mode, format="%(asctime)s - %(levelname)s : %(message)s")
else:
    logging.basicConfig(filename='logging.log', level=logging.DEBUG, format="%(asctime)s - %(levelname)s : %(message)s")

# 创建窗口
canvas = pygame.display.set_mode((480, 650))
# 导入图片
bg = pygame.image.load('images/bg4.png')  # 背景
start = pygame.image.load('images/startGame.png')  # 开始
logo = pygame.image.load('images/LOGO.png')  # logo

hero = pygame.image.load('images/hero.png')  # 英雄机
e1 = pygame.image.load('images/enemy1.png')  # 地方飞机
e2 = pygame.image.load('images/enemy2.png')
e3 = pygame.image.load('images/enemy3.png')
b = pygame.image.load('images/bullet1.png')  # 子弹

# 导入再来一次
a1 = pygame.image.load('images/again.png')  # 图1
a2 = pygame.image.load('images/again_2.png')  # 图2

# 2、导入空投图片：images/ufo2.png
u = pygame.image.load('images/ufo2.png')


# 3、创建空投类：Ufo
class Ufo:
    def __init__(self, x):
        self.x = x
        self.y = -54
        self.w = 54
        self.h = 77
        self.img = u

    # 画图
    def paint(self):
        canvas.blit(self.img, (self.x, self.y))

    # 移动
    def move(self):
        self.y += 2


# 创建子弹类
class Bullet:
    def __init__(self, x, y):
        self.x = x  # 坐标x
        self.y = y  # 坐标y
        self.w = 9  # 宽度
        self.h = 21  # 高度
        self.img = b  # 图片

    # 画图
    def paint(self):
        canvas.blit(self.img, (self.x, self.y))

    # 移动
    def move(self):
        self.y -= 3


# 检测时间间隔
def isActionTime(interVal, lastTime):
    # 判断如果是第一次运行游戏，则直接返回Ture
    # 否则，判断时间间隔要求是否满足
    if lastTime == 0:
        return True
    else:
        nowTime = time.time()
        return nowTime - lastTime >= interVal


# 创建敌人类
class Enemy:
    def __init__(self, x, y, w, h, img, life, score):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.life = life  # 生命值
        self.score = score  # 分数

    # 画图
    def paint(self):
        canvas.blit(self.img, (self.x, self.y))

    # 移动
    def move(self):
        self.y += 2


# 创建英雄类
class Hero:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 60
        self.h = 75
        self.img = hero
        self.life = 10  # 生命值
        self.interVal = 0.2  # 发射子弹的时间间隔
        self.lastTime = 0  # 最后发射子弹的时间
        # 8、双倍火力数量：doubleNum
        self.doubleNum = 0
        # 画飞机

    def paint(self):
        canvas.blit(self.img, (self.x, self.y))

    # 移动
    def move(self):
        mx, my = pygame.mouse.get_pos()
        self.x = mx - self.w / 2
        self.y = my - self.h / 2

    # 发射子弹
    def shoot(self):
        if isActionTime(self.interVal, self.lastTime):
            self.lastTime = time.time()
            # 10、增加if逻辑：双倍活力为0时发射普通子弹，否则发射双倍子弹，并数量减一
            if GameVar.h.doubleNum:
                # 双倍火力
                for x in range(0, 852, 10):
                    GameVar.bullets.append(Bullet(x - 20, self.y - 15))
                self.doubleNum -= 1
            else:
                # 普通子弹
                GameVar.bullets.append(Bullet(self.x + 10, self.y))
                GameVar.bullets.append(Bullet(self.x + 25, self.y - 15))
                GameVar.bullets.append(Bullet(self.x + 40, self.y))


# 创建天空类
class Sky:
    def __init__(self):
        self.x = 0
        self.w = 480
        self.h = 852
        self.y1 = 0  # 图一y坐标
        self.y2 = -self.h  # 图二y坐标
        self.img = bg

    # 绘制图片
    def paint(self):
        canvas.blit(self.img, (self.x, self.y1))
        canvas.blit(self.img, (self.x, self.y2))

    # 移动方法
    def move(self):
        self.y1 += 1
        self.y2 += 1
        if self.y1 > self.h:
            self.y1 = -self.h
        if self.y2 > self.h:
            self.y2 = -self.h


# 事件函数
def event():
    for event in pygame.event.get():
        # 关闭事件
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 鼠标点击事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            logging.debug("Mouse clicked!")
            # 从开始状态切换到运行状态
            if GameVar.state == 1:
                GameVar.state = 2
            # 重新开始游戏
            mx, my = pygame.mouse.get_pos()
            if GameVar.state == 4 and 150 < mx < 150 + 170 and 300 < my < 300 + 50:
                GameVar.state = 1  # 进入状态一
                # 重置游戏变量
                GameVar.h.life = 3  # 生命值
                GameVar.score = 0  # 游戏得分
                GameVar.enemies = []  # 敌机列表
                GameVar.bullets = []  # 子弹列表
        # 鼠标移动事件  480, 650
        if event.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            if GameVar.state == 2 or GameVar.state == 3:
                if mx < 5 or mx > 475 or my < 5 or my > 645:
                    GameVar.state = 3
                else:
                    GameVar.state = 2


# 创建敌人的函数
def createEnemies():
    r1 = random.randint(0, 480 - 57)  # 小
    r2 = random.randint(0, 480 - 50)  # 中
    r3 = random.randint(0, 480 - 100)  # 大
    # 4、创建空投对象需要的x坐标范围
    u = random.randint(0, 480 - 54)

    r = random.randint(1, 10)  # 获取随机数决定产生飞机的类型

    if isActionTime(GameVar.interVal, GameVar.lastTime):
        GameVar.lastTime = time.time()  # 记录敌机创建的时间
        # 5、修改if语句，创建空投对象并加入列表ufos
        if r < 5:
            # 生成小飞机
            GameVar.enemies.append(Enemy(r1, -45, 57, 45, e1, 5, 1))
        elif r < 7:
            # 生成空投
            GameVar.ufos.append(Ufo(u))
        elif r < 10:
            # 生成中飞机
            GameVar.enemies.append(Enemy(r2, -68, 50, 68, e2, 8, 5))
        else:
            # 生成大飞机
            GameVar.enemies.append(Enemy(r3, -153, 100, 153, e3, 20, 20))


# 判断碰撞的函数
def hit(a, b):
    return a.x + a.w > b.x and \
        b.x + b.w > a.x and \
        a.y + a.h > b.y and \
        b.y + b.h > a.y


# 处理碰撞的函数
def checkHit():
    # 11、空投和英雄：删掉空投并增加双倍火力
    for i in GameVar.ufos:
        if hit(i, GameVar.h):
            GameVar.ufos.remove(i)
            GameVar.h.life += 2
            GameVar.h.doubleNum += 20

    # 敌人和英雄机
    for i in GameVar.enemies:
        if hit(i, GameVar.h):
            GameVar.h.life -= 1  # 减少英雄机生命值
            GameVar.enemies.remove(i)  # 删除碰撞的敌机
    # 敌机和子弹
    for i in GameVar.enemies:
        for j in GameVar.bullets:
            if hit(i, j):
                i.life -= 1  # 减少敌机生命值
                GameVar.bullets.remove(j)  # 删除子弹
    # 删除死亡敌机
    for i in GameVar.enemies:
        if i.life <= 0:
            GameVar.score += i.score  # 增加得分
            GameVar.enemies.remove(i)  # 删除敌机
    # 判断英雄机死亡
    if GameVar.h.life <= 0:
        GameVar.state = 4  # 切换游戏状态：结束状态
        logging.info("Game over!")


# 删除越界对象
def out():
    for i in GameVar.enemies:
        if i.y > 650:
            GameVar.enemies.remove(i)  # 越界敌人
    for i in GameVar.bullets:
        if i.y < 0:
            GameVar.bullets.remove(i)  # 越界子弹


# 存储游戏变量的类
class GameVar:
    # 状态变量 1:开始状态 2：运行状态 3：暂停状态4：结束状态
    state = 1
    # 创建天空对象
    sky = Sky()
    # 创建英雄对象
    h = Hero()
    # 创建存储敌方飞机的列表
    enemies = []
    # 创建敌机的间隔时间
    interVal = 0.5
    # 最后创建敌机的时间
    lastTime = 0
    # 创建存储子弹的列表
    bullets = []
    # 游戏得分
    score = 0
    # 1、创建存储空投的列表：ufos
    ufos = []


# 写文字的函数
pygame.init()  # 初始化pygame模块——（字体功能）


def fillText(text, pos):
    # 设置字体、大小
    f = pygame.font.SysFont('微软雅黑', 30)
    # 设置文字内容、抗锯齿、颜色   render   渲染
    t = f.render(text, True, (255, 255, 255))
    # 写文字（绘制）
    canvas.blit(t, pos)


# 创建绘制飞行物的函数
def paintAll():
    GameVar.sky.paint()  # 画天空
    # 画飞行物、飞行物移动
    GameVar.h.paint()
    # 画所有敌人
    for i in GameVar.enemies:
        i.paint()
    # 画所有子弹
    for i in GameVar.bullets:
        i.paint()
    # 6、画空投
    for i in GameVar.ufos:
        i.paint()


# 创建移动飞行物的函数
def moveAll():
    GameVar.sky.move()  # 天空移动
    GameVar.h.move()
    # 移动所有敌人
    for i in GameVar.enemies:
        i.move()
    # 移动所有子弹
    for i in GameVar.bullets:
        i.move()
    # 7、移动空投
    for i in GameVar.ufos:
        i.move()


# 游戏主函数
def gameStart():
    # 游戏开始状态
    if GameVar.state == 1:
        GameVar.sky.paint()  # 画天空
        GameVar.sky.move()  # 天空移动
        canvas.blit(start, (160, 400))  # 绘制开始图片
        canvas.blit(logo, (-40, 200))  # 绘制logo
    # 游戏运行状态
    if GameVar.state == 2:
        # 画所有图片
        paintAll()
        # 移动所有图片
        moveAll()
        # 创建敌方飞机
        createEnemies()
        # 发射子弹
        GameVar.h.shoot()
        # 写文字：生命值、游戏得分
        fillText(f'life:{GameVar.h.life}', (0, 0))
        fillText(f'score:{GameVar.score}', (360, 0))
        # 9、写出双倍火力数量信息：(0, 25)
        fillText(f'doubleNum:{GameVar.h.doubleNum}', (0, 25))
        # 处理碰撞
        checkHit()
        # 删除越界函数
        out()

    # 游戏暂停状态
    if GameVar.state == 3:
        pass
    # 游戏结束状态
    if GameVar.state == 4:
        GameVar.sky.paint()  # 画天空
        GameVar.sky.move()  # 天空移动
        fillText(f'score:{GameVar.score}', (200, 200))  # 写分数
        # 绘制再来一局按钮（图片） 170*50
        mx, my = pygame.mouse.get_pos()
        if 150 < mx < 150 + 170 and 300 < my < 300 + 50:
            canvas.blit(a1, (150, 300))
        else:
            canvas.blit(a2, (150, 300))

    pygame.display.update()


while True:
    # 调用事件函数
    event()

    # 调用游戏主函数
    gameStart()
