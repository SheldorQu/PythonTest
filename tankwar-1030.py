#================================================
"""TANKWAR V1.0"""

import pygame,time,random,sys
#================================================
#屏幕参数常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME = 75
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
#坦克图片资源常量
TANK_UP_IMG = 'img/myTank_UP.png'
TANK_DOWN_IMG ='img/myTank_DOWN.png'
TANK_LEFT_IMG ='img/myTank_LEFT.png'
TANK_RIGHT_IMG ='img/myTank_RIGHT.png'
ENEMY_UP_IMG = 'img/enemy1U.png'
ENEMY_DOWN_IMG = 'img/enemy1D.png'
ENEMY_LEFT_IMG = 'img/enemy1L.png'
ENEMY_RIGHT_IMG = 'img/enemy1R.png'
ENEMY2_UP_IMG = 'img/enemy2U.png'
ENEMY2_DOWN_IMG = 'img/enemy2D.png'
ENEMY2_LEFT_IMG = 'img/enemy2L.png'
ENEMY2_RIGHT_IMG = 'img/enemy2R.png'
ENEMY3_UP_IMG = 'img/enemy3U.png'
ENEMY3_DOWN_IMG = 'img/enemy3D.png'
ENEMY3_LEFT_IMG = 'img/enemy3L.png'
ENEMY3_RIGHT_IMG = 'img/enemy3R.png'
ENEMY4_UP_IMG = 'img/enemy4U.png'
ENEMY4_DOWN_IMG = 'img/enemy4D.png'
ENEMY4_LEFT_IMG = 'img/enemy4L.png'
ENEMY4_RIGHT_IMG = 'img/enemy4R.png'
#声音资源常量
START_MUSIC = 'img/start.wav'
HITBRICK_MUSIC = 'img/hitbrick.mp3'
EXPLODE_MUSIC = 'img/bomb.wav'
#墙体位置坐标列表
BRICKS_POS_List = [(40,80),(80,80),(180,80),(220,80),(340,80),(420,80),(540,80),(580,80),(680,80),(720,80),\
                   (40,120),(80,120),(180,120),(220,120),(340,120),(380,120),(420,120),(540,120),(580,120),(680,120),(720,120),\
                   (40,160),(80,160),(180,160),(220,160),(340,160),(420,160),(540,160),(580,160),(680,160),(720,160),\
                   (40,190),(80,190),(180,190),(220,190),(340,240),(420,240),(540,190),(580,190),(680,190),(720,190),\
                   (80,280),(120,280),(160,280),(200,280),(560,280),(600,280),(640,280),(680,280),\
                   (340,320),(420,320),(340,360),(420,360),(340,400),(420,400),\
                   (40,340),(80,340),(180,340),(220,340),(540,340),(580,340),(680,340),(720,340),\
                   (40,380),(80,380),(180,380),(220,380),(540,380),(580,380),(680,380),(720,380),\
                   (40,420),(80,420),(180,420),(220,420),(540,420),(580,420),(680,420),(720,420),\
                   (40,460),(80,460),(680,460),(720,460),\
                   (340,520),(380,520),(420,520),(340,560),(420,560)]
STEELS_POS_List = [(0,280),(760,280),(380,360)]
BOSS_POS_List = [(380,560)]
myTank_POS = (260,555) #我方坦克出生坐标
#相关游戏参数
STEEL_BLOOD = 4  #钢墙生命值
BRICK_BLOOD = 2    #砖墙生命值
BOSS_BLOOD = 1     #BOSS生命值
BULLET_SPEED = 6   #子弹速度
ENEMY_TANK_SPEED = random.randint(2,3)   #敌方坦克随机速度
MY_TANK_SPEED = 4  #我方坦克速度
EnemTank_count = 8  #画面中敌方坦克最大数量
MAX_BUL_COUNT = 4  #我方坦克连发炮弹最大数量
PROBABILITY = 20   #地方坦克随机发炮弹的概率：PROBABILITY‰ ，建议10-20


#================================================
class MainGame():
    #游戏主窗口
    window = None
    #创建我方坦克
    TANK_P1 = None
    #存储所有敌方坦克
    EnemyTank_list = []    
    #存储我方子弹的列表
    Bullet_list = []
    #存储敌方子弹的列表
    Enemy_bullet_list = []
    #爆炸效果列表
    Explode_list = []
    #墙壁列表
    Wall_list = []

    #开始游戏的方法
    def startGame(self):
        pygame.init()
        #创建窗口
        MainGame.window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        #设置游戏标题
        pygame.display.set_caption("坦克大战")
        #创建坦克和墙壁
        self.creatMyTank()
        self.creatEnemyTank()
        self.creatWalls()
        #停止处理输入法事件（否则按WASD无效）
        pygame.key.stop_text_input()        
        
        #让窗口持续刷新操作        
        while True :            
            #设置游戏帧率
            pygame.time.Clock().tick(FRAME)
            #给窗口填充颜色
            MainGame.window.fill(COLOR_BLACK)
            #在循环中持续完成事件的获取
            self.getEvent()
            #绘制文字，粘贴到窗口中            
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克 %d 辆"%len(MainGame.EnemyTank_list)),(5,5))
            #调用展示墙壁的方法，并用endgameLabel检查BOSS是否活着
            endgameLabel = self.blitWalls()                     
            #如果遍历墙壁时发现BOSS血量为零，则3秒内关闭游戏。（可后续优化RESTART按钮...）
            if endgameLabel == True:                              
                print("THE BOSS IS KILLED...\n THE GAME WILL EXIT IN 3 SECONDS...")
                time.sleep(1)
                print(" 3...")
                time.sleep(1)
                print(" 2...")
                time.sleep(1)
                print(" 1...")
                time.sleep(1)                
                pygame.quit()
                sys.exit()                

            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                # 将我方坦克加入到窗口中
                MainGame.TANK_P1.displayTank()
            else:
                #重置我方坦克
                del MainGame.TANK_P1
                MainGame.TANK_P1 = None
            #循环展示敌方坦克
            self.blitEnemyTank()
            #根据坦克的开关状态调用坦克的移动方法
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                #调用碰撞墙壁的方法
                MainGame.TANK_P1.hitWalls()
                MainGame.TANK_P1.hitEnemyTank()
            #调用渲染子弹列表的方法
            self.blitBullet()
            #调用渲染敌方子弹列表方法
            self.blitEnemyBullet()
            #调用展示爆炸效果的方法
            self.displayExplodes()
            #窗口刷新
            pygame.display.update()            
            """flip函数将重新绘制整个屏幕对应的窗口。update函数仅仅重新绘制窗口中有变化的区域。
            如果仅仅是几个物体在移动，那么他只重绘其中移动的部分，没有变化的部分，并不进行重绘。
            update比flip速度更快。因此在一般的游戏中，如果不是场景变化非常频繁的时候，建议使用update函数。"""
   
    #创建我方坦克
    def creatMyTank(self):
        # 创建我方坦克
        MainGame.TANK_P1 = MyTank(myTank_POS[0],myTank_POS[1])
        #播放我方坦克出生音乐
        music = Music(START_MUSIC)
        music.play()

    #创建敌方坦克
    def creatEnemyTank(self):       
        if len(MainGame.EnemyTank_list) == 0: #若把上面的self.creatEnemyTank()放入主程序循环中，此句可以实现重复加载一波敌方坦克
            top = 20 #生成敌方坦克距离顶部20像素
            for i in range(EnemTank_count):
                e_speed = ENEMY_TANK_SPEED 
                #每次都随机生成一个left值
                left = random.randint(1, 9)
                #尽可能防止生成坦克位置重叠，数字尽量错开
                eTank = random.choice([EnemyTank(left*67,top,e_speed), EnemyTank2(left*54,top,e_speed),\
                                       EnemyTank3(left*75,top,e_speed),EnemyTank4(left*73,top,e_speed)])            
                MainGame.EnemyTank_list.append(eTank)

    #创建墙壁
    def creatWalls(self):
        #创建钢墙
        for pos_steel in STEELS_POS_List:
            steel_wall = Wall(pos_steel[0],pos_steel[1])            
            MainGame.Wall_list.append(steel_wall)
        #创建砖墙
        for pos_brick in BRICKS_POS_List:
            brick_wall = BrickWall(pos_brick[0],pos_brick[1])
            MainGame.Wall_list.append(brick_wall)
        #创建BOSS(墙)
        for pos_boss in BOSS_POS_List:
            boss_wall = BossWall(pos_boss[0],pos_boss[1])
            MainGame.Wall_list.append(boss_wall)
        
    #遍历显示墙壁
    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()
            else: #如果墙体死亡
                if wall.bossLabel == True: #如果该墙体为BOSS墙体
                    endgamelabel = True
                    return endgamelabel #函数返回True,标识游戏结束
                else: #砖墙或钢墙血量为零                    
                    MainGame.Wall_list.remove(wall)

    #遍历敌方坦克
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                # 坦克移动的方法
                eTank.randMove()
                #调用敌方坦克与墙壁的碰撞方法
                eTank.hitWalls()
                #敌方坦克是否撞到我方坦克
                eTank.hitMyTank()
                # 调用敌方坦克的射击
                eBullet = eTank.shot()
                #如果子弹为None，则不加入到列表
                if eBullet:
                    # 将子弹存储敌方子弹列表
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)
        
    #将我方子弹加入窗口
    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            #如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if bullet.live:
                bullet.displayBullet()
                #让子弹移动
                bullet.bulletMove()
                #调用我方子弹与敌方坦克的碰撞方法
                bullet.hitEnemyTank()
                #判断我方子弹是否碰撞到墙壁
                wall_destroy = bullet.hitWalls()
                if wall_destroy == True :
                    #播放音乐                    
                    if not pygame.mixer.music.get_busy(): #如果频道未被占用
                        music = Music(HITBRICK_MUSIC)
                        """set_volume在此处似乎不起作用"""
                        music.set_volume()
                        music.play()                    
            else:
                MainGame.Bullet_list.remove(bullet)

    #将敌方子弹加入到窗口
    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            #如果子弹还活着，绘制出来，否则从列表中移除该子弹
            if eBullet.live:
                eBullet.displayBullet()
                # 让子弹移动
                eBullet.bulletMove()
                #调用是否碰撞到墙壁的一个方法
                eBullet.hitWalls()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    eBullet.hitMyTank()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)

    #展示爆炸效果列表
    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
                explode.soundExplode()
            else:
                MainGame.Explode_list.remove(explode)

    #获取程序期间所有事件(鼠标事件，键盘事件)
    def getEvent(self):
        #获取所有事件
        eventList = pygame.event.get()
        #对事件进行判断处理
        for event in eventList:
            #判断event.type 是否QUIT，如果是,调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()                
            #判断事件类型是否为按键按下，如果是，继续判断按键,进行对应的处理
            if event.type == pygame.KEYDOWN:
                #点击ESC按键让我方坦克重生
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1:
                    #调用创建我方坦克的方法
                    self.creatMyTank()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    # 按键的处理
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'L'
                        MainGame.TANK_P1.stop = False
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w):
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        if len(MainGame.Bullet_list) < MAX_BUL_COUNT:
                            # 产生一颗子弹
                            my_bullet = Bullet(MainGame.TANK_P1)
                            # 将子弹加入到子弹列表
                            MainGame.Bullet_list.append(my_bullet)
                            if not pygame.mixer.music.get_busy():#fire音频和HitBrick音频时长略长，所以会出现有时候发炮声不响
                                music = Music('img/fire.mp3')  
                                music.play()
                        else:
                            print("子弹数量不足")                        
            #按键不松，保持移动
            if event.type == pygame.KEYUP:
                #松开的如果是方向键，才更改移动开关状态
                if event.key in [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,pygame.K_SPACE]: #比连续多个or更简洁
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        # 修改坦克的移动状态
                        MainGame.TANK_P1.stop = True

    #文字绘制
    def getTextSurface(self,text):
        # 初始化字体模块
        pygame.font.init()        
        #查看系统支持的所有字体
        #fontList = pygame.font.get_fonts()
        #print(fontList)        
        font = pygame.font.SysFont('dengxian',size=15,bold=True)
        # 使用对应的字符完成相关内容的绘制
        textSurface = font.render(text,True,(255,255,255))
        return textSurface

    #关闭游戏
    def endGame(self):
        pygame.quit()
        sys.exit()    
    
#================================================
class BaseItem(pygame.sprite.Sprite):
    """自定义一个基类，继承pygame.sprite.Sprite类"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#================================================
class Tank(BaseItem):
    """坦克类"""
    def __init__(self,left,top):
        self.images = {
            'U':pygame.image.load(TANK_UP_IMG),
            'D':pygame.image.load(TANK_DOWN_IMG),
            'L':pygame.image.load(TANK_LEFT_IMG),
            'R':pygame.image.load(TANK_RIGHT_IMG)}
        
        self.direction = 'U'
        self.image = self.images[self.direction]
        #坦克所在的区域
        self.rect = self.image.get_rect()
        #指定坦克初始化位置
        self.rect.left = left
        self.rect.top = top
        #新增速度属性
        self.speed = MY_TANK_SPEED
        #新增属性： 坦克的移动开关
        self.stop = True
        #属性 live 用来记录坦克是否活着
        self.live = True
        #用来记录坦克移动之前的坐标(用于坐标还原时使用)
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
 
    #坦克的移动方法
    def move(self):
        #先记录移动之前的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top        
        
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed           
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH :
                self.rect.left += self.speed           
        elif self.direction == 'U':
            if self.rect.top > 0 :
                self.rect.top -= self.speed            
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT :
                self.rect.top += self.speed            

    #坦克保持不动
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop   

    #碰撞墙壁的方法
    def hitWalls(self):
       for wall in MainGame.Wall_list:
           if pygame.sprite.collide_rect(wall,self):
               self.stay()
    #射击方法
    def shot(self):
        return Bullet(self)

    #展示坦克方法
    def displayTank(self):
        #重新设置坦克的图片
        self.image = self.images[self.direction]
        #将坦克加入到窗口中
        MainGame.window.blit(self.image,self.rect)

#================================================
class MyTank(Tank):
    """我方坦克类"""
    def __init__(self,left,top):
        super().__init__(left,top)
    #新增主动碰撞到敌方坦克的方法
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                self.stay()
 
#================================================
class EnemyTank(Tank):
    """敌方坦克类"""
    def __init__(self,left,top,speed):
        super().__init__(left,top)
        
        self.images = {
            'U': pygame.image.load(ENEMY_UP_IMG),
            'D': pygame.image.load(ENEMY_DOWN_IMG),
            'L': pygame.image.load(ENEMY_LEFT_IMG),
            'R': pygame.image.load(ENEMY_RIGHT_IMG)}
        
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        # 坦克所在的区域
        self.rect = self.image.get_rect()
        # 指定坦克初始化位置 分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = speed
        self.stop = True
        #新增步数属性，用来控制敌方坦克随机移动
        self.step = 30
 
    #随机方向
    def randDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
   
    #随机移动
    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1

    #随机发射子弹（13‰几率，可微调）
    def shot(self):
        num = random.randint(1,1000)
        if num  <= PROBABILITY:
            return Bullet(self)

    #与我方坦克碰撞
    def hitMyTank(self):
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
                # 让敌方坦克停下来
                self.stay()

class EnemyTank2(EnemyTank):
    """敌方坦克2类"""
    def __init__(self,left,top,speed):
        super().__init__(left,top,speed)
        self.images = {
            'U': pygame.image.load(ENEMY2_UP_IMG),
            'D': pygame.image.load(ENEMY2_DOWN_IMG),
            'L': pygame.image.load(ENEMY2_LEFT_IMG),
            'R': pygame.image.load(ENEMY2_RIGHT_IMG)}

class EnemyTank3(EnemyTank):
    """敌方坦克3类"""
    def __init__(self,left,top,speed):
        super().__init__(left,top,speed)
        self.images = {
            'U': pygame.image.load(ENEMY3_UP_IMG),
            'D': pygame.image.load(ENEMY3_DOWN_IMG),
            'L': pygame.image.load(ENEMY3_LEFT_IMG),
            'R': pygame.image.load(ENEMY3_RIGHT_IMG)}

class EnemyTank4(EnemyTank):
    """敌方坦克4类"""
    def __init__(self,left,top,speed):
        super().__init__(left,top,speed)
        self.images = {
            'U': pygame.image.load(ENEMY4_UP_IMG),
            'D': pygame.image.load(ENEMY4_DOWN_IMG),
            'L': pygame.image.load(ENEMY4_LEFT_IMG),
            'R': pygame.image.load(ENEMY4_RIGHT_IMG)}

#================================================
class Bullet(BaseItem):
    """炮弹类"""
    def __init__(self,tank):
        self.COLOR = (255,255,255)   #圆形子弹颜色
        self.RADIUS = 4          #圆形子弹半径
        self.screen = MainGame.window        
        #自己画圆形子弹,返回rect位置
        self.rect = pygame.draw.circle(MainGame.window, self.COLOR, (0,0), self.RADIUS)

        #也可以使用图片子弹
        #self.image = pygame.image.load('img/enemymissile.png')
        #获得图形子弹的位置
        #self.rect = self.image.get_rect()

        #子弹方向（即坦克方向）
        self.direction = tank.direction        
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 
            self.rect.top = tank.rect.top + tank.rect.width / 2 
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 
        #子弹速度
        self.speed = BULLET_SPEED
        #用来记录子弹是否活着
        self.live = True

    #子弹移动
    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                #修改状态值
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                # 修改状态值
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改状态值
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                # 修改状态值
                self.live = False
    #展示子弹
    def displayBullet(self):
        #MainGame.window.blit(self.image,self.rect)
        POSITION = (self.rect.x,self.rect.y) #圆形子弹坐标
        pygame.draw.circle(self.screen,self.COLOR,POSITION,self.RADIUS) #绘制圆的方法
        
    #我方子弹碰撞敌方坦克
    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                #产生一个爆炸效果
                explode = Explode(eTank)
                #将爆炸效果加入到爆炸效果列表
                MainGame.Explode_list.append(explode)
                self.live = False
                eTank.live = False

    #敌方子弹与我方坦克的碰撞
    def hitMyTank(self):
        if pygame.sprite.collide_rect(self,MainGame.TANK_P1):
            # 产生爆炸效果，并加入到爆炸效果列表中
            explode = Explode(MainGame.TANK_P1)
            MainGame.Explode_list.append(explode)
            #修改子弹状态
            self.live = False
            #修改我方坦克状态
            MainGame.TANK_P1.live = False

    #子弹与墙壁碰撞
    def hitWalls(self):
        wall_destroyed = False
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall,self):
                #修改子弹的live属性
                self.live = False
                wall.hp -= 1                
                if wall.hp <= 0:
                    wall.live = False
                    wall_destroyed = True
                    return wall_destroyed                    

#================================================
class Explode():
    """爆炸类"""
    def __init__(self,tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/blast0.png'),
            pygame.image.load('img/blast1.png'),
            pygame.image.load('img/blast2.png'),
            pygame.image.load('img/blast2.png'),
            pygame.image.load('img/blast3.png'),
            pygame.image.load('img/blast3.png')
        ]
        self.image = self.images[self.step]
        self.live = True
        self.music = Music(EXPLODE_MUSIC)

    #展示爆炸效果
    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0

    #播放爆炸声音
    def soundExplode(self):
        self.music.play()

#================================================
class Wall():
    """（钢）墙类"""
    def __init__(self,left,top):
        self.image = pygame.image.load('img/steels.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        #用来判断墙壁是否应该在窗口中展示
        self.live = True
        #记录墙壁的生命值
        self.hp = STEEL_BLOOD
        #标记该墙是否是BOSS（把BOSS作为特殊的墙处理）
        self.bossLabel = False

    #展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)

class BrickWall(Wall):
    """砖墙类"""
    def __init__(self,left,top):
        super().__init__(left,top)
        self.image = pygame.image.load('img/bricks.png')
        self.hp = BRICK_BLOOD

class BossWall(BrickWall):
    """BOSS墙类"""
    def __init__(self,left,top):
        super().__init__(left,top)
        self.image = pygame.image.load('img/boss.png')
        self.hp = BOSS_BLOOD
        self.bossLabel = True #BOSS墙的标识

#================================================
class Music():
    """音乐类"""
    def __init__(self,fileName):
        self.fileName = fileName
        #初始化混合器
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)       

    #开始播放音乐
    def play(self):        
        pygame.mixer.music.play()

    #设置频道音量（0.0-1.0）
    def set_volume(self):
        """此处似乎不起作用"""
        pygame.mixer.music.set_volume(0.5)

#================================================
if __name__ == '__main__':    
    tankgame = MainGame() 
    tankgame.startGame()
       
