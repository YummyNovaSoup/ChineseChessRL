import Table
import pygame
import sys
import random

table1 = Table.Table()

usercolor = 1 if random.random()>0.5 else -1

table1.initial(usercolor)


# 初始化pygame
pygame.init()

# 设置窗口尺寸
screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)

# 设置窗口标题
pygame.display.set_caption('中国象棋')
running = 1
while running:
    running = table1.screenshow(screen)

# 退出pygame
print(table1.whowin)
pygame.quit()
sys.exit()
