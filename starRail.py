import configuration as cfg
from configuration import time, pa, bigMap, bigMapRegionStart, bigMapRegionNum, getStarTrain
from pathFinding import selectRegion
import random

# 选择大地图
# MapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
def clickBigMap(mapN:int):
    time.sleep(2)
    pa.click(x=1600+cfg.bC[0],y=180+cfg.bC[1])
    time.sleep(2)
    pa.moveTo(x=bigMap[mapN][0]+cfg.bC[0],y=bigMap[mapN][1]+cfg.bC[1])
    time.sleep(1)
    for i in range(7):  
        time.sleep((random.randint(1,11)/10))
        pa.mouseDown()
        time.sleep((random.randint(1,5)/10))
        pa.mouseUp()

# 选择大地图内的可战斗区域
# bigMapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
# regionN: 地图内地区序列，从0开始，但不是游戏内的第一个区域，而是第一个有怪的区域，如bigMapN=0,regionN=0，既为黑塔空间站的基座舱段 
def clickRegion(bigMapN:int,regionN:int):
    time.sleep(2)
    if bigMapN == 0:
        pa.click(x=bigMapRegionStart[0][0]+cfg.bC[0],y=bigMapRegionStart[0][1]+cfg.bC[1]+regionN*100)
    elif bigMapN == 1:
        if regionN < 4:
            pa.click(x=bigMapRegionStart[0][0]+cfg.bC[0],y=bigMapRegionStart[0][1]+cfg.bC[1]+regionN*100)
        else:
            pa.click(x=bigMapRegionStart[1][0]+cfg.bC[0],y=bigMapRegionStart[1][1]+cfg.bC[1]+(regionN-4)*100)
    elif bigMapN == 2:
        pa.click(x=bigMapRegionStart[0][0]+cfg.bC[0],y=bigMapRegionStart[0][1]+cfg.bC[1]+(regionN+1)*100)
    time.sleep(1)
    #进行区域战斗逻辑
    selectRegion(bigMapN,regionN)
    

# 脚本开始
# 需要选择人物为 娜塔莎 ，并且在非基座舱段的其他场地，并且在可操作界面
def script():
    time.sleep(0.1)
    pa.press('m') # 打开地图
    time.sleep(1)
    sub=pa.locateOnScreen("data/sub.png", region=(600 + cfg.bC[0], 990+cfg.bC[1], 200, 200), confidence=0.9)
    pa.click(sub,clicks=10,interval=0.3) # 点击缩放地图，保证传送点的位置正确
    for i in range(0,3): # 三个大体图
        print("bigMapNum=",i)
        clickBigMap(i) # 点击大地图
        for j in range(0,bigMapRegionNum[i]): # 大地图中的区域选择 
            print("regionNum=",j)
            clickRegion(i,j) # 选择区域

if __name__ == '__main__':
    print("Select Window")
    if 0 == getStarTrain():
        print("Not Found Game Window")
        exit()
    print(cfg.bC)
    pa.screenshot("data/fightEnd.png",region=(34+cfg.bC[0],112+cfg.bC[1],35,20)) #截取左上角手机底部图案，以便确认是否结束战斗
    print("Start Script")
    script()
    print("End Script")
