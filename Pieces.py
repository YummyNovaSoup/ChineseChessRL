import os
import pygame

abs_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(abs_path)
ui_path = os.path.join(parent_dir,'UI')
chessboard_path = os.path.join(ui_path,'ChessBoard.png')
pieces_path = os.path.join(ui_path,'pieces')
kind2path = {1:"ju_black",-1:"ju_red",2:"ma_black",-2:"ma_red",3:"xiang_black",-3:"xiang_red",4:"shi_black",-4:"shi_red"
             ,5:"jiang_black",-5:"shuai_red",6:"pao_black",-6:"pao_red",7:"zu_black",-7:"bing_red"}

zeroplace = (130,80)
radius=25
allCircleCenter = [ [(zeroplace[0]+i*67,zeroplace[1]+j*67) for j in range(10)] for i in range(9)]
#allCollision = [[0]*10 for i in range(9)]

class Pieces:
    def __init__(self,kind:int,status=0,ifdeath=0):
        #loc是竖直为i，水平为j
        self.path = os.path.join(pieces_path,"qizi_"+kind2path[kind]+"_1.png")
        self.pathes = [os.path.join(pieces_path,"qizi_"+kind2path[kind]+"_"+str(i)+".png") for i in range(1,6)]
        self.image = pygame.image.load(self.path)
        self.images = [pygame.image.load(self.pathes[i]) for i in range(5)]
        self.background =pygame.image.load(os.path.join(pieces_path,"qizi_1.png"))
        self.backgrounds = [pygame.image.load(os.path.join(pieces_path,"qizi_"+str(i)+".png")) for i in range(1,6)]
        #self.loc = (loc[1],loc[0]) #反转了
        self.kind = kind
        self.status = status
        self.ifdeath = ifdeath
        self.sizes = [(self.images[i].get_width(),self.images[i].get_height()) for i in range(5)]
        self.backsizes = [(self.backgrounds[i].get_width(),self.backgrounds[i].get_height()) for i in range(5)]
        #self.circle = allCircleCenter[self.loc[0],self.loc[1]]
        self.radius = radius

    def show(self,screen,loc:tuple):
        i=loc[1]
        j=loc[0]
        screen.blit(self.backgrounds[0], (allCircleCenter[i][j][0]-(self.backsizes[0][0]//2),allCircleCenter[i][j][1]-(self.backsizes[0][1]//2)))
        screen.blit(self.images[0], (allCircleCenter[i][j][0]-(self.sizes[0][0]//2),allCircleCenter[i][j][1]-(self.sizes[0][1]//2)))

    # def updateloc(self,loc):
    #     self.loc = (loc[1],loc[0]) #反转了
    #     self.circle = allCircleCenter[self.loc[0],self.loc[1]]

    # def ifcollision(self,mouseplace:tuple):
    #     self.status = (self.circle[0]-mouseplace[0])**2+(self.circle[1]-mouseplace[1])**2 <= self.radius**2
    #     return self.status
        
    def chosen(self,screen,loc):
        i=loc[1]
        j=loc[0]
        for k in range(5):
            screen.blit(self.backgrounds[k], (allCircleCenter[i][j][0]-(self.backsizes[k][0]//2),allCircleCenter[i][j][1]-(self.backsizes[k][1]//2)))
            screen.blit(self.images[k], (allCircleCenter[i][j][0]-(self.sizes[k][0]//2),allCircleCenter[i][j][1]-(self.sizes[k][1]//2)))
        self.status=2

    def showbig(self,screen,loc:tuple):
        i=loc[1]
        j=loc[0]
        k=4
        screen.blit(self.backgrounds[k], (allCircleCenter[i][j][0]-(self.backsizes[k][0]//2),allCircleCenter[i][j][1]-(self.backsizes[k][1]//2)))
        screen.blit(self.images[k], (allCircleCenter[i][j][0]-(self.sizes[k][0]//2),allCircleCenter[i][j][1]-(self.sizes[k][1]//2)))
        
    # def statusclear(self):
    #     self.status = 0



#test
