import pyautogui as pa
import pydirectinput as pdi
import time
import win32con
import win32gui as w32
import random

baseCoordinate=[0,0,0,0] #窗口的坐标
bC = baseCoordinate

bigMap=([350,600],[1000,300],[1500,900]) #大地图的点击坐标
bigMapRegionStart=([1520,465],[1520,585]) #区域的基准坐标
bigMapRegionNum=(3,9,4) #区域内可战斗的箱庭数量

#箱庭内的起始传送点坐标
regionPoint=([[840,200],  [[1030,600],[955,670],[560,600]],  [[355,620],[630,445]]],
             [[1120,600], [775,765], [0,0], [[980,260],[735,880],[735,805],[705,810]], [[525,755],[780,700]], [0,0], [[740,920],[740,840],[775,720],[770,620]], [[820,770],[810,365]],[510,690]],
             [[[910,185],[750,725],[750,690],[785,660],], [[1040,330],[665,545],[650,705]], [[450,220],[540,180],[570,800]], [[560,230],[660,400],[960,300],[815,205]]])

#找到星穹铁道的窗口
def getStarTrain():
    startTrain = w32.FindWindow('UnityWndClass',u'崩坏：星穹铁道')
    if startTrain == 0:
        return 0
    w32.ShowWindow(startTrain,win32con.SW_NORMAL)
    w32.SetForegroundWindow(startTrain)
    time.sleep(2)
    global bC
    bC = w32.GetWindowRect(startTrain)
    return 1

#检测战斗是否结束
def checkFightEnd(interval:int=3):
    for i in range(1,4):
        time.sleep(i)
        if None != pa.locateOnScreen("data/fightStart.png",region=(1140+bC[0],1070+bC[1],40,40),confidence=0.7):
            print("fight start")
            break
    while True:
        time.sleep(interval)
        if None != pa.locateOnScreen("data/fightEnd.png",region=(35+bC[0],113+bC[1],35,20),confidence=0.9):
            print("fight end")
            return 1