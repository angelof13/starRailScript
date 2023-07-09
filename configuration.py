import pyautogui as pa
import pydirectinput as pdi
import time
import win32con
import win32gui as w32

#窗口的坐标
baseCoordinate=[0,0,0,0]
bC = baseCoordinate

# 大地图的点击坐标
bigMap=([350,600], # 黑塔空间站
        [1000,300], # 雅利洛-Ⅵ
        [1500,900]) # 仙舟⌜罗浮⌟

# 选择大地图内区域的基准坐标
# 第一个为游戏地图中右边第3个区域的坐标，第二个为雅利洛VI，当身处残响回廊后，打开地图会默认展示后面的区域，故应点击的坐标发生变化后的基准坐标
bigMapRegionStart=([1520,465],[1520,585]) 

# 大地图内可战斗的区域数量，非准确数量，值为从第一个可战斗区域到最后一个可战斗区域之间的差值
bigMapRegionNum=(3,9,4)

# 加载等待时间，即点击传送后到角色进入地图的等待时间
loadingTime = 6

# 区域内的传送点坐标
regionPoint=(
    [
        [840,200], # 基座舱段
        [[1030,600],[955,670],[560,600]], # 收容舱段
        [[355,620],[630,445]] # 支援舱段
    ],
    [
        [1120,600], # 城郊雪原 
        [775,765], # 边缘通路 
        [0,0], # 禁卫铁区 
        [[980,260],[735,880],[735,805],[705,810]], # 残响回廊 
        [[525,755],[780,700]], # 永冬岭 
        [0,0], # 磐岩镇 
        [[740,920],[740,840],[775,720],[770,620]], # 大矿区 
        [[820,770],[810,365]], # 铆钉镇 
        [510,690] # 机械聚落
    ],
    [
        [[910,185],[750,725],[750,690],[785,660]], # 流云渡 
        [[1040,330],[665,545],[650,705]], # 迴星港 
        [[450,220],[540,180],[570,800]], # 太卜司 
        [[560,230],[660,400],[960,300],[815,205]] # 工造司
    ])

# 找到星穹铁道的窗口,并选中
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

# 检测战斗是否结束
# interval: 间隔几秒检查一次，默认是2秒
def checkFightEnd(interval:int=2):
    for i in range(2,5): #检测是否进入战斗，尝试以2s,3s,4s的间隔检查三次
        time.sleep(i)
        if None != pa.locateOnScreen("data/fightStart.png",region=(1140+bC[0],1070+bC[1],40,40),confidence=0.6):
            print("fight start")
            break
    while True:
        time.sleep(interval)
        if None != pa.locateOnScreen("data/fightEnd.png",region=(34+bC[0],112+bC[1],35,20),confidence=0.8):
            print("fight end")
            return 1