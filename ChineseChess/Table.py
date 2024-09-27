class Table:
    def __init__(self):
        #从左上角开始为(0,0)
        self.width = 9
        self.length = 10
        self.encode = {"bju":1,"bma":2,"bxiang":3,"bshi":4,"bjiang":5,"bpao":6,"bzu":7,
                       "rju":-1,"rma":-2,"rxiang":-3,"rshi":-4,"rjiang":-5,"rpao":-6,"rzu":-7}
        self.decode = { v: k for k,v in self.encode.items()}
        self.table = [ [0]*self.width for _ in range(self.length) ]    
    
    def initial(self,color: int):
        #黑是1，红是-1
        self.clear()
        #print(self.length-1)
        self.table[self.length-1][0] = color #车
        self.table[self.length-1][self.width-1] = color
        self.table[self.length-1][1] = color * 2 #马
        self.table[self.length-1][self.width-2] = color * 2
        self.table[self.length-1][2] = color * 3 #象
        self.table[self.length-1][self.width-3] = color * 3
        self.table[self.length-1][3] = color * 4 #士
        self.table[self.length-1][self.width-4] = color * 4
        self.table[self.length-1][4] = color * 5 #将
        self.table[self.length-3][1] = color * 6 #炮
        self.table[self.length-3][self.width-2] = color * 6
        self.table[self.length-4][0] = color * 7 #卒
        self.table[self.length-4][2] = color * 7
        self.table[self.length-4][4] = color * 7
        self.table[self.length-4][6] = color * 7
        self.table[self.length-4][8] = color * 7

        color = -1 * color
        self.table[0][0] = color #车
        self.table[0][self.width-1] = color 
        self.table[0][1] = color * 2 #马
        self.table[0][self.width-2] = color * 2
        self.table[0][2] = color * 3 #象
        self.table[0][self.width-3] = color * 3
        self.table[0][3] = color * 4 #士
        self.table[0][self.width-4] = color * 4
        self.table[0][4] = color * 5 #将
        self.table[2][1] = color * 6 #炮
        self.table[2][self.width-2] = color * 6
        self.table[3][0] = color * 7 #卒
        self.table[3][2] = color * 7
        self.table[3][4] = color * 7
        self.table[3][6] = color * 7
        self.table[3][8] = color * 7
        

    def clear(self):
        for i in range(self.length):
            for j in range(self.width):
                self.table[i][j] = 0

    def show(self):
        print("-"*30)
        for i in range(self.length):
            for j in range(self.width):
                print("{:^3}".format(self.table[i][j]),end=" ")
            print("")
        print("-"*30)

    def place(self,*args: tuple):
        for arg in args:
            if isinstance(arg[2], int):
                self.table[arg[0]][arg[1]] = arg[2]
            else:
                self.table[arg[0]][arg[1]] = self.encode[arg[2]]

    def findLoc(self, piece):
        if isinstance(piece, str):
            piece = self.encode[piece]
        #可能需要每个棋子都特异
        for i in range(self.length):
            for j in range(self.width):
                if self.table[i][j] == piece:
                    return (i,j)
        return None
    def abs(self,num):
        return num if num>=0 else -1*num
    def whereCanGo(self, arg: tuple):
        canGo = []
        piece = self.table[arg[0]][arg[1]]
        if piece == 0:
            return canGo
        elif piece == 1 or piece == -1:
            #first = 0
            for i in reversed(range(0,arg[0])):
                if self.table[i][arg[1]] == 0: #空位可以走
                    canGo.append((i,arg[1]))
                elif piece*self.table[i][arg[1]]<0:   #可以吃                
                    canGo.append((i,arg[1]))
                    break
                else:
                    break
            for i in range(arg[0]+1,self.length):
                if self.table[i][arg[1]] == 0:
                    canGo.append((i,arg[1]))
                elif piece*self.table[i][arg[1]]<0:   #可以吃                
                    canGo.append((i,arg[1]))
                    break
                else:
                    break
            for j in reversed(range(0,arg[1])):
                if self.table[arg[0]][j] == 0:
                    canGo.append((arg[0],j))
                elif piece*self.table[arg[0]][j]<0:
                    canGo.append((arg[0],j))
                    break
                else:
                    break
            for j in range(arg[1]+1,self.width):
                if self.table[arg[0]][j] == 0:
                    canGo.append((arg[0],j))
                elif piece*self.table[arg[0]][j]<0:
                    canGo.append((arg[0],j))
                    break
                else:
                    break
            return canGo
        elif piece==2 or piece==-2:#马

            # for i in [-1,1,-2,2]:
            #     for j in [-1,1,-2,2]:
            #         if (abs)
            canGo = [(arg[0]-2,arg[1]-1),(arg[0]-2,arg[1]+1),(arg[0]-1,arg[1]-2),(arg[0]-1,arg[1]+2)
                     ,(arg[0]+1,arg[1]-2),(arg[0]+1,arg[1]+2),(arg[0]+2,arg[1]-1),(arg[0]+2,arg[1]+1)]
            for i,j in canGo.copy():
                if i<0 or i>=self.length or j<0 or j>=self.width:
                    canGo.remove((i,j))
                elif abs(i-arg[0])==2  and self.table[arg[0]+int((i-arg[0])/2)][arg[1]]!=0:
                    #蹩马腿
                    canGo.remove((i,j))
                elif abs(j-arg[1])==2  and self.table[arg[0]][arg[1]+int((j-arg[1])/2)]!=0:
                    canGo.remove((i,j))
                elif piece*self.table[i][j]>0:
                    canGo.remove((i,j))
                    
            return canGo
        elif piece==3 or piece ==-3:#象
            canGo = [(arg[0]-2,arg[1]-2),(arg[0]-2,arg[1]+2),(arg[0]+2,arg[1]-2),(arg[0]+2,arg[1]+2)]
            south = arg[0]<=4 #反了，但没关系
            for i,j in canGo.copy():
                if south == 1:
                    if  i<0 or i>=5 or j<0 or j>=self.width:#南方阵营
                        canGo.remove((i,j))
                    elif piece*self.table[i][j]>0:
                        canGo.remove((i,j))
                    elif self.table[int((arg[0]+i)/2)][int((arg[1]+j)/2)]: #堵象眼了
                        canGo.remove((i,j))
                else:
                    if  i<5 or i>=self.length or j<0 or j>=self.width:#北方阵营
                        canGo.remove((i,j))
                    elif piece*self.table[i][j]>0:
                        canGo.remove((i,j))
                    elif self.table[int((arg[0]+i)/2)][int((arg[1]+j)/2)]: #堵象眼了
                        canGo.remove((i,j))    
                
            return canGo
        elif piece==4 or piece==-4:
            canGo = [(arg[0]-1,arg[1]-1),(arg[0]-1,arg[1]+1),(arg[0]+1,arg[1]-1),(arg[0]+1,arg[1]+1)]
            south = arg[0]<=4 #反了，但没关系
            for i,j in canGo.copy():
                if south == 1:
                    if  i<0 or i>2 or j<3 or j>5:#南方阵营
                        canGo.remove((i,j))
                    elif piece*self.table[i][j]>0:
                        canGo.remove((i,j))
                else:
                    if  i<7 or i>9 or j<3 or j>5:#北方阵营
                        canGo.remove((i,j))
                    elif piece*self.table[i][j]>0:
                        canGo.remove((i,j))
                
            return canGo
        elif piece==5 or piece==-5:
            canGo = [(arg[0]-1,arg[1]),(arg[0],arg[1]+1),(arg[0]+1,arg[1]),(arg[0],arg[1]-1)]
            south = arg[0]<=4 #反了，但没关系, 看成小i
            for i,j in canGo.copy():
                if south == 1:
                    if  i<0 or i>2 or j<3 or j>5:#南方阵营
                        canGo.remove((i,j))
                    elif piece*self.table[i][j]>0:
                        canGo.remove((i,j))
                else:
                    if  i<7 or i>9 or j<3 or j>5:#北方阵营
                        canGo.remove((i,j))
                    elif piece*self.table[i][j]>0:
                        canGo.remove((i,j))
            return canGo
        elif piece==6 or piece==-6: #炮
            flag = 0 #待发标志
            for i in reversed(range(0,arg[0])):
                if self.table[i][arg[1]]==0 : #空位可以走
                    if flag==0:
                        canGo.append((i,arg[1]))
                    else:
                        pass
                else:
                    if flag == 1 :
                        if piece*self.table[i][arg[1]]<0: 
                            canGo.append((i,arg[1]))
                        else:
                            pass
                        break
                    else:
                        flag = 1

            flag = 0
            for i in range(arg[0]+1,self.length):
                if self.table[i][arg[1]]==0 : #空位可以走
                    if flag==0:
                        canGo.append((i,arg[1]))
                    else:
                        pass
                else:
                    if flag == 1 :
                        if piece*self.table[i][arg[1]]<0: 
                            canGo.append((i,arg[1]))
                        else:
                            pass
                        break
                    else:
                        flag = 1
            flag = 0
            for j in reversed(range(0,arg[1])):
                if self.table[arg[0]][j] == 0:
                    if flag==0:
                        canGo.append((arg[0],j))
                    else:
                        pass
                else:
                    if flag == 1 :
                        if piece*self.table[arg[0]][j]<0: 
                            canGo.append((arg[0],j))
                        else:
                            pass
                        break
                    else:
                        flag = 1
            flag = 0
            for j in range(arg[1]+1,self.width):
                if self.table[arg[0]][j] == 0:
                    if flag==0:
                        canGo.append((arg[0],j))
                    else:
                        pass
                else:
                    if flag == 1 :
                        if piece*self.table[arg[0]][j]<0: 
                            canGo.append((arg[0],j))
                        else:
                            pass
                        break
                    else:
                        flag = 1
            return canGo

        elif piece==7 or piece==-7: #卒
            
            i,j = self.findLoc(int(piece/7*(abs(piece)-2))) #找老将位置
            if i<=4: #北方阵营，这回对了
                if arg[0]>=5: #过河了
                    canGo = [(arg[0]+1,arg[1]),(arg[0],arg[1]-1),(arg[0],arg[1]+1)]
                else: #没过河
                    canGo = [(arg[0]+1,arg[1])] #塔塔开
            else:#南方阵营
                if arg[0]<=4: #过河了
                    canGo = [(arg[0]-1,arg[1]),(arg[0],arg[1]-1),(arg[0],arg[1]+1)]
                else: #没过河
                    canGo = [(arg[0]-1,arg[1])] #塔塔开
            for i,j in canGo.copy():
                if i<0 or i>=self.length or j<0 or j>=self.width: #不出界
                    canGo.remove((i,j))
                elif piece*self.table[i][j]>0: #不吃队友
                    canGo.remove((i,j))
            return canGo
        else:
            return f"findLocPieceError"

    def go(self, arg: tuple, loc_togo: tuple):
        try:
            assert self.table[arg[0]][arg[1]] == arg[2], "pieceError" #棋子不对
            assert loc_togo in self.whereCanGo((arg[0],arg[1])), "goError" #走不了
            if self.table[loc_togo[0]][loc_togo[1]]!=0:
                ate = self.table[loc_togo[0]][loc_togo[1]] #被吃棋子id
            else:
                ate = 0
            self.table[loc_togo[0]][loc_togo[1]] = arg[2] #走到
            self.table[arg[0]][arg[1]] = 0 #清楚痕迹
            return ate
        except AssertionError as e:
            print(f"Error occurred: {e}")
            return f"Error occurred: {e}"
    def win(self) -> int:
        #1黑胜，-1红胜，0没结束
        bjiang = 5
        rjiang = -5
        #后面findLoc可以优化，直接作为变量
        if self.findLoc(bjiang)==None:
            return -1
        elif self.findLoc(rjiang)==None:
            return 1
        else:
            return 0

# table1 = Table()
# table1.place((0,0,1),(0,1,2),(3,2,5),(5,5,"rju"))
# table1.show()
# table1.clear()
# table1.initial(1)
# table1.show()
# table1.go((0,0,-1),(1,0))
# table1.show()
# table1.whereCanGo((0,1,-2))