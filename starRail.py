import configuration as cfg
from configuration import time, pa
from pathFinding import selectRegion
from cosmic import linkStart
import random

# 0：非DEBUG
# 1：只执行到点击区域的操作
DEBUG = 0

# 选择大地图
# MapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
def clickBigMap(mapN:int):
    time.sleep(2)
    pa.click(x=cfg.nMC['interstellarChart'][0],y=cfg.nMC['interstellarChart'][1])
    time.sleep(2)
    pa.moveTo(x=cfg.bigMap[mapN][0],y=cfg.bigMap[mapN][1])
    time.sleep(1)
    for i in range(5):  
        time.sleep((random.randint(1,11)/10))
        pa.mouseDown()
        time.sleep((random.randint(1,5)/10))
        pa.mouseUp()

moveFlag:int=0
# 选择大地图内的可战斗区域
# bigMapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
# regionN: 地图内地区序列，从0开始，但不是游戏内的第一个区域，而是第一个有怪的区域，如bigMapN=0,regionN=0，既为黑塔空间站的基座舱段 
def clickRegion(bigMapN:int,regionN:int):
    time.sleep(2)
    def move():
        global moveFlag
        if moveFlag == 0:
                pa.mouseDown(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1])
                time.sleep(0.5)
                pa.moveRel(0,-400,1)
                pa.mouseUp()
                time.sleep(0.5)
                moveFlag = 1
    if bigMapN == 0: # 黑塔空间站
        pa.click(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1]+regionN*cfg.nMC['gap'])
    elif bigMapN == 1: # 雅利洛-Ⅵ
        if regionN < 4:
            pa.click(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1]+regionN*cfg.nMC['gap'])
        else:
            move()
            pa.click(x=cfg.bigMapRegionStart[1][0],y=cfg.bigMapRegionStart[1][1]+(regionN-4)*cfg.nMC['gap'])
    elif bigMapN == 2: # 仙舟
        if regionN < 5:
            pa.click(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1]+regionN*cfg.nMC['gap'])
        else:
            move()
            pa.click(x=cfg.bigMapRegionStart[2][0],y=cfg.bigMapRegionStart[2][1]+(regionN-5)*cfg.nMC['gap'])
    time.sleep(1)

    
#操作开始
def script(mode:int,times:int=34):
    time.sleep(0.1)
    pa.press('m') # 打开地图
    time.sleep(1)
    pa.click(cfg.nMC['subSign'][0],cfg.nMC['subSign'][1],clicks=10,interval=0.3) # 点击缩放地图，保证传送点的位置正确
    time.sleep(1)
    if mode == 1:
        global moveFlag
        for i in range(cfg.vP['startBigMap'],3): # 三个大体图
            print("bigMapNum=",i)
            moveFlag = 0
            clickBigMap(i) # 点击大地图
            for j in range(cfg.vP['startRegion'],cfg.bigMapRegionNum[i]): # 大地图中的区域选择 
                print("regionNum=",j)
                clickRegion(i,j) # 选择区域
                time.sleep(1)
                if DEBUG == 0:
                    selectRegion(i,j) # 进行区域战斗逻辑
    elif mode == 2:
        clickBigMap(0) # 黑塔空间站
        clickRegion(0,-1) # 主控舱段
        pa.click(x=450+cfg.bC[0],y=935+cfg.bC[1]) # 黑塔办公室坐标
        time.sleep(1)
        pa.click(x=900+cfg.bC[0],y=795+cfg.bC[1]) # 选择黑塔办公室
        time.sleep(1)
        pa.click(x=1650+cfg.bC[0],y=1000+cfg.bC[1]) # 点击传送
        time.sleep(cfg._variableParameters['loadingTime'])
        linkStart(times)

# 脚本开始
# 需要选择人物为 娜塔莎 ，并且在非基座舱段的其他场地，并且在可操作界面
# 模拟宇宙仅需在可操作界面
if __name__ == '__main__':
    print("Select Window")
    if 0 == cfg.getStarTrain():
        print("Not Found Game Window")
        exit()
    pa.screenshot("data/fightMarker.png",region=(cfg.nMC['fightMarker'][0],cfg.nMC['fightMarker'][1],cfg.nMC['fightMarker'][2],cfg.nMC['fightMarker'][3])) #截取右下角轮盘，以便确认是否战斗状态
    print("Start Script")
    script(mode=1,times=2)
    print("End Script")
