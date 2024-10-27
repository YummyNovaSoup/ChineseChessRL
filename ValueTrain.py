import Table
import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class Robot:
    def __init__(self, table):
        self.table = table
        #self.color = color
        self.unitscore = 100
        #self.state = self.table.turn,[row[:] for row in self.table.table]
        #self.pi = policy
        self.epsilon = 0.1


    def convertState(self):
        return torch.cat((torch.tensor([self.table.turn]),torch.tensor(self.table.table).view(-1))).float()

    def observe(self):
        return self.table.AllCanGo()

    def randomAct(self):
        #只返回可走的，并不实际走
        allcango = self.observe()
        size = len(allcango)
        piecego = allcango[np.random.randint(0,size)]
        size2 = len(piecego[3])
        loctogo = piecego[3][np.random.randint(0,size2)]
        return (piecego[0:2],) + (loctogo,) + (piecego[2],) #返回一个元组,包含起点,终点,操作子
    
    def policy2act(self, pi):
        locfrom,locto = pi.state2act(self.convertState())
        return locfrom,locto
    
    def greedyAct(self, pi):
        if np.random.rand() < self.epsilon:
            sample = self.randomAct()
            action = sample[0:2]
            
        else:
            action = self.policy2act(pi)
        return action  #(locfrom,locto)

    def act(self, locfrom, locto):
        try:
            #空位置
            if self.table.table[locfrom[0]][locfrom[1]] == 0:
                return -1*self.unitscore, False
            color = self.table.turn
            self.table.go(locfrom, locto)
            whowin = self.table.waittingtowin()
            #self.table.withdraw() 不撤回
            #self.updateState()
            return(whowin*color*self.unitscore,True)
        except:
            #走错直接算负
            return -1*self.unitscore, False
        
    def withdraw(self):
        self.table.withdraw()
        self.updateState()

    def getReward(self, locfrom, locto):
        try:
            if self.table.table[locfrom[0]][locfrom[1]] == 0:
                return -1*self.unitscore
            color = self.table.turn
            self.table.go(locfrom, locto)
            whowin = self.table.waittingtowin()
            self.table.withdraw()
            return(whowin*color*self.unitscore)
        except:
            #走错直接算负
            return -1*self.unitscore

    def sampling(self, n, pi, error, frominitial=True, ifshow = False):
        if frominitial:
            self.table.initial(1)
        samples = []
        for i in range(n):
            winning = self.table.waittingtowin()

            if winning == 0:
                action = self.greedyAct(pi)

                state0 = (self.table.turn, [row[:] for row in self.table.table])  # Deep copy of the state, .copy()只能拷贝最外层
                reward, ifnormal = self.act(action[0], action[1])
                #这里有点问题，如果走错了，不应该影响phi的参数，单独开一个error来给pi学习
                if ifnormal == False:
                    if len(error) < 10000:
                        error.append((torch.cat((torch.tensor([state0[0]]).view(-1).float(),torch.tensor(state0[1]).view(-1).float())), torch.tensor(action).view(-1).float(), reward))
                    else:
                        error.pop(0)
                        error.append((torch.cat((torch.tensor([state0[0]]).view(-1).float(),torch.tensor(state0[1]).view(-1).float())), torch.tensor(action).view(-1).float(), reward))
                    continue
                state1 = (self.table.turn, [row[:] for row in self.table.table])  # Deep copy of the state
                samples.append((state0, action, reward, state1)) #state是（turn,table）,action是（locfrom,locto）
                    
            else:
                break
        return samples
    def sampleshow(self, samples, screen):
        tableforshow = Table.Table()
        for sample in samples:
            tableforshow.table = sample[0][1]
            print(sample[1:3])
            tableforshow.screenshow(screen)
            time.sleep(0.5)
        sample = samples[-1]
        tableforshow.table = sample[3][1]
        try:
            while True:
                tableforshow.screenshow(screen)
        except KeyboardInterrupt:
            print("Interrupted by user")

class Policy(nn.Module):
    #输入为turn和table，输出为action（locfrom,locto）(90*90)
    def __init__(self, input_size=91, hidden_size=10000, output_size=90+90):
        super(Policy, self).__init__()
        # input_size = 91
        # hidden_size = 10000
        # output_size = 90*90
        self.fc1 = nn.Linear(input_size, hidden_size)  # 输入层到隐藏层
        #self.bn1 = nn.BatchNorm1d(hidden_size)  # 批量归一化
        self.fc2 = nn.Linear(hidden_size, hidden_size)  # 隐藏层到隐藏层
        #self.bn2 = nn.BatchNorm1d(hidden_size)  # 批量归一化
        self.fc3_1 = nn.Linear(hidden_size, output_size//2)  # 隐藏层到输出层,分类一
        self.fc3_2 = nn.Linear(hidden_size, output_size//2)  # 隐藏层到输出层,分类二
        self.dropout = nn.Dropout(p=0.5)  # 丢弃层

    def forward(self, x):
        #作用于(turn,state)
        #x = torch.cat(torch.tensor(x[1]))
        x = torch.relu(self.fc1(x))  # 输入层
        x = self.dropout(x)  # 丢弃层
        x = torch.relu(self.fc2(x))  # 隐藏层
        y1 = F.softmax(self.fc3_1(x),dim=0)  # 输出层
        y2 = F.softmax(self.fc3_2(x),dim=0)
        return y1,y2
    
    def state2act(self,x):
        locfrom_p, locto_p = self.forward(x) #得到90+90的概率分布
        maxindex = torch.argmax(locfrom_p)
        locfrom = (maxindex//9,maxindex%9)
        maxindex2 = torch.argmax(locto_p)
        locto = (maxindex2//9,maxindex2%9)
        return locfrom,locto

class QNet(nn.Module):
    #输入为turn和table和action，输出为Q值
    def __init__(self, input_size=1+90+4, hidden_size=10000, output_size=1):
        super(QNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)  # 输入层到隐藏层
        #self.bn1 = nn.BatchNorm1d(hidden_size)  # 批量归一化
        self.fc2 = nn.Linear(hidden_size, hidden_size)  # 隐藏层到隐藏层
        #self.bn2 = nn.BatchNorm1d(hidden_size)  # 批量归一化
        self.fc3 = nn.Linear(hidden_size, output_size)  # 隐藏层到输出层
        self.dropout = nn.Dropout(p=0.5)  # 丢弃层

    def forward(self, state, action):
        x = torch.cat((state,action))
        x = torch.relu(self.fc1(x))  # 输入层
        x = self.dropout(x)  # 丢弃层
        x = torch.relu(self.fc2(x))  # 隐藏层
        x = self.fc3(x)  # 输出层
        return x

class Trainer:
    def __init__(self, policy, qnet, qnetcopy, robot, gamma=0.9):
        self.policy = policy
        self.qnet = qnet
        self.qnetcopy = qnetcopy
        qnet.train()
        qnetcopy.train()
        self.robot = robot
        self.gamma = gamma
        self.optimizer_policy = optim.Adam(self.policy.parameters(), lr=0.001)
        self.optimizer_qnet = optim.Adam(self.qnet.parameters(), lr=0.001)
        self.optimizer_qnetcopy = optim.Adam(self.qnetcopy.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.epsilon = self.robot.epsilon
        self.rebuff = []
        self.rebuffsize = 100000
        self.error = []
        self.times = 0
    
    def pi(self, state):
        if np.random.rand() < self.epsilon:
            return self.robot.randomAct()[0:2]
        else:
            return self.policy.state2act(state)
    
    def q(self, state, action):
        return self.qnet(state, action)
    
    def updaterebuff(self, sample):
        state0 = torch.cat((torch.tensor([sample[0][0]]),torch.tensor(sample[0][1]).view(-1))).float()
        state1 = torch.cat((torch.tensor([sample[3][0]]),torch.tensor(sample[3][1]).view(-1))).float()

        action = torch.tensor(sample[1]).view(-1).float()
        reward = torch.tensor(sample[2]).float()
        sample_out = (state0, action, reward, state1)
        if self.rebuffsize > len(self.rebuff):
            self.rebuff.append(sample_out)
        else:
            self.rebuff.pop(0)
            self.rebuff.append(sample_out)
        

    def policytrain(self, samples):
        for sample in samples:
            state0 = sample[0]
            #act = sample[1]
            #reward = sample[2]
            #state1 = sample[3]
            locfrom_p, locto_p = self.policy.forward(state0) #得到90+90的概率分布
            maxindex = torch.argmax(locfrom_p)
            locfrom = (maxindex//9,maxindex%9)
            maxindex2 = torch.argmax(locto_p)
            locto = (maxindex2//9,maxindex2%9)
            action = torch.cat((torch.tensor(locfrom),torch.tensor(locto))).view(-1).float()
            loss = -(locfrom_p[maxindex] + locto_p[maxindex2])* (self.q(state0,action)+self.robot.unitscore/10)
            self.optimizer_policy.zero_grad()
            loss.backward()
            self.optimizer_policy.step()
            #print("policy Loss:", loss.item())
    
    def policyerrortrain(self, samples):
        for sample in samples:
            state0 = sample[0]
            #act = sample[1]
            #reward = sample[2]
            #state1 = sample[3]
            locfrom_p, locto_p = self.policy.forward(state0) #得到90+90的概率分布
            maxindex = torch.argmax(locfrom_p)
            locfrom = (maxindex//9,maxindex%9)
            maxindex2 = torch.argmax(locto_p)
            locto = (maxindex2//9,maxindex2%9)
            action = torch.cat((torch.tensor(locfrom),torch.tensor(locto))).view(-1).float()
            loss = -(locfrom_p[maxindex] + locto_p[maxindex2])* (self.q(state0,action)-self.robot.unitscore)
            self.optimizer_policy.zero_grad()
            loss.backward()
            self.optimizer_policy.step()
            #print("policy Loss:", loss.item())
    def train(self, N=1, K=1, n_samples=100):
        self.times += 1
        print("times:",self.times,end=' ')
        print(len(self.rebuff))
        for _ in range(N):
            samples = self.robot.sampling(n_samples, self.policy, self.error)
            for sample in samples:
                self.updaterebuff(sample)
            for __ in range(K):
                if len(self.rebuff) == 0:
                    break
                if n_samples > len(self.rebuff):
                    n_samples = len(self.rebuff)
                randindex = np.random.randint(0,len(self.rebuff),n_samples)
                samples = [self.rebuff[i] for i in randindex]
                for sample in samples:
                    state0 = sample[0]
                    act = sample[1]
                    reward = sample[2]
                    state1 = sample[3]
                    y_q = reward + self.gamma * self.q(state1, torch.tensor(self.pi(state1)).view(-1).float()) #?
                    y_q.detach()
                    self.optimizer_qnet.zero_grad()
                    loss = self.criterion(self.qnet(state0, act), y_q)
                    loss.backward()
                    gradients = []
                    for param in self.qnet.parameters():
                        gradients.append(param.grad.clone() if param.grad is not None else torch.zeros_like(param))
                    # 清除参考模型的梯度
                    self.qnet.zero_grad()

                    # 清除目标模型的梯度
                    self.qnetcopy.zero_grad()
                    # 将参考模型的梯度应用到目标模型的参数上
                    for param, grad in zip(self.qnetcopy.parameters(), gradients):
                        param.grad = grad

                    # 更新目标模型的参数
                    self.optimizer_qnetcopy.step()
                    #self.optimizer_qnet.step()
                    # 打印损失以便监控训练过程
                    #print("qnet Loss:", loss)
        '''更新phi''' 
        #结束后把参数还回来
        datas = []
        for param in self.qnetcopy.parameters():
            datas.append(param.data.clone())
        # 清除参考模型的梯度
        self.optimizer_qnet.zero_grad()

        # 清除目标模型的梯度
        self.optimizer_qnetcopy.zero_grad()

        # 将copy模型的梯度应用到原模型的参数上
        for i,param in enumerate(self.qnet.parameters()):
            param.data = datas[i]

        '''更新policy'''
        for _ in range(N):
            #先error
            if n_samples > len(self.error):
                ne_samples = len(self.error)
            else:
                ne_samples = n_samples
            randindex = np.random.randint(0,len(self.error),ne_samples)
            samples = [self.error[i] for i in randindex]
            self.policyerrortrain(samples)
            #再qnet
            if len(self.rebuff) == 0:
                break
            if n_samples > len(self.rebuff):
                n_samples = len(self.rebuff)
            randindex = np.random.randint(0,len(self.rebuff),n_samples)
            samples = [self.rebuff[i] for i in randindex]
            self.policytrain(samples)

    

    '''用不到'''
    def rebufftrain(self,n_sample,K,N):
        size = len(self.rebuff)
        if size < n_sample:
            n_sample = size
        for i in range(K):
            samples = [self.rebuff[int(i)] for i in np.random.randint(0,size,n_sample)]
            self.train(samples)
            self.policytrain(samples)
        
    

if __name__ == '__main__':
    table1 = Table.Table()
    table1.initial(1)
    # 初始化pygame
    # import pygame
    # pygame.init()

    # 设置窗口尺寸
    # screen_size = (800, 800)
    # screen = pygame.display.set_mode(screen_size)

    # # 设置窗口标题
    # pygame.display.set_caption('中国象棋')
    
    #table1.screenshow(screen)

    robot1 = Robot(table1)
    # samples = robot1.sampling(100)
    # robot1.sampleshow(samples,screen)
    #print(samples)

    policy1 = Policy()
    qnet1 = QNet()
    qnetcopy1 = QNet()
    trainer1 = Trainer(policy1, qnet1, qnetcopy1, robot1)
    while True:
        trainer1.train()