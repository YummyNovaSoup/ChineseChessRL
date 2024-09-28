import pygame
import sys
import os
import math
from . import Pieces
abs_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(abs_path)
ui_path = os.path.join(parent_dir,'UI')
chessboard_path = os.path.join(ui_path,'ChessBoard.png')
pieces_path = os.path.join(ui_path,'pieces')

# 初始化pygame
pygame.init()

# 设置窗口尺寸
screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)

# 设置窗口标题
pygame.display.set_caption('中国象棋')

# 加载图片 (确保图片文件与代码文件在同一目录下，或者给出完整路径)
image = pygame.image.load(chessboard_path)
rju = [pygame.image.load(os.path.join(pieces_path,"qizi_ju_red_"+str(i)+".png")) for i in range(1,6)]
qizibackground = [pygame.image.load(os.path.join(pieces_path,"qizi_"+str(i)+".png")) for i in range(1,6)]

# 获取图片的矩形对象（用于定位）
image_rect = image.get_rect()
rju_size = [(rju[i].get_width(),rju[i].get_height()) for i in range(5)]
qizibackground_size = [(qizibackground[i].get_width(),qizibackground[i].get_height()) for i in range(5)]
# 可以将图片移动到窗口的中心
image_rect.center = (screen_size[0] // 2, screen_size[1] // 2)

#原点
zeroplace = (130,80)
radius=25
#颜色
RED = (255, 0, 0)
YELLOW = (255,255,0)
allCircleCenter = [ [(zeroplace[0]+i*67,zeroplace[1]+j*67) for j in range(10)] for i in range(9)]
allCollision = [[0]*10 for i in range(9)]
def ifCollision(circle,radius,mouseplace):
    #print(circle)
    #print(mouseplace)
    return (circle[0]-mouseplace[0])**2+(circle[1]-mouseplace[1])**2 <= radius**2

# 游戏循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
            for i in range(9):
                for j in range(10):
                    allCollision[i][j] = ifCollision(allCircleCenter[i][j],radius,mouse_pos)
    # 填充背景颜色
    screen.fill((255, 255, 255))  # 白色背景

    # 在窗口中绘制图片
    screen.blit(image, image_rect)
    
    # 原点绘制圆
    for i in range(9):
        for j in range(10):
            #circlecenter = (zeroplace[0]+i*67,zeroplace[1]+j*67)
            if allCollision[i][j]==0:
                screen.blit(qizibackground[0], (allCircleCenter[i][j][0]-(qizibackground_size[0][0]//2),allCircleCenter[i][j][1]-(qizibackground_size[0][1]//2)))
                screen.blit(rju[0], (allCircleCenter[i][j][0]-(rju_size[0][0]//2),allCircleCenter[i][j][1]-(rju_size[0][1]//2)))
            elif allCollision[i][j]==1:
                for k in range(5):
                    screen.blit(qizibackground[k], (allCircleCenter[i][j][0]-(qizibackground_size[k][0]//2),allCircleCenter[i][j][1]-(qizibackground_size[k][1]//2)))
                    screen.blit(rju[k], (allCircleCenter[i][j][0]-(rju_size[k][0]//2),allCircleCenter[i][j][1]-(rju_size[k][1]//2)))
                allCollision[i][j]=2
            else:
                k=4
                screen.blit(qizibackground[k], (allCircleCenter[i][j][0]-(qizibackground_size[k][0]//2),allCircleCenter[i][j][1]-(qizibackground_size[k][1]//2)))
                screen.blit(rju[k], (allCircleCenter[i][j][0]-(rju_size[k][0]//2),allCircleCenter[i][j][1]-(rju_size[k][1]//2)))
            #pygame.draw.circle(screen, color, allCircleCenter[i][j], radius)

    # 更新屏幕
    pygame.display.flip()

# 退出pygame
pygame.quit()
sys.exit()
