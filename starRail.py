import configuration as cfg
from configuration import time, pa
from pathFinding import selectRegion
import random

# 选择大地图
# MapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
def clickBigMap(mapN:int):
    time.sleep(2)
    pa.click(x=cfg.nMC['interstellarChart'][0]+cfg.bC[0],y=cfg.nMC['interstellarChart'][1]+cfg.bC[1])
    time.sleep(2)
    pa.moveTo(x=cfg.bigMap[mapN][0]+cfg.bC[0],y=cfg.bigMap[mapN][1]+cfg.bC[1])
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
        pa.click(x=cfg.bigMapRegionStart[0][0]+cfg.bC[0],y=cfg.bigMapRegionStart[0][1]+cfg.bC[1]+regionN*cfg.nMC['gap'])
    else:
        if regionN < 4:
            pa.click(x=cfg.bigMapRegionStart[0][0]+cfg.bC[0],y=cfg.bigMapRegionStart[0][1]+cfg.bC[1]+regionN*cfg.nMC['gap'])
        else:
            if bigMapN == 1:
                pa.click(x=cfg.bigMapRegionStart[1][0]+cfg.bC[0],y=cfg.bigMapRegionStart[1][1]+cfg.bC[1]+(regionN-4)*cfg.nMC['gap'])
            elif bigMapN == 2:
                pa.click(x=cfg.bigMapRegionStart[2][0]+cfg.bC[0],y=cfg.bigMapRegionStart[2][1]+cfg.bC[1]+(regionN-4)*cfg.nMC['gap'])
    time.sleep(1)

    
#操作开始
def script():
    time.sleep(0.1)
    pa.press('m') # 打开地图
    time.sleep(1)
    pa.click(cfg.nMC['subSign'][0]+cfg.bC[0],cfg.nMC['subSign'][1]+cfg.bC[1],clicks=10,interval=0.3) # 点击缩放地图，保证传送点的位置正确
    time.sleep(1)
    for i in range(2,3): # 三个大体图
        print("bigMapNum=",i)
        clickBigMap(i) # 点击大地图
        for j in range(3,cfg.bigMapRegionNum[i]): # 大地图中的区域选择 
            print("regionNum=",j)
            clickRegion(i,j) # 选择区域
            time.sleep(1)
            selectRegion(i,j) # 进行区域战斗逻辑


# 脚本开始
# 需要选择人物为 娜塔莎 ，并且在非基座舱段的其他场地，并且在可操作界面
if __name__ == '__main__':
    print("Select Window")
    if 0 == cfg.getStarTrain():
        print("Not Found Game Window")
        exit()
    pa.screenshot("data/fightMarker.png",region=(cfg.nMC['fightMarker'][0]+cfg.bC[0],cfg.nMC['fightMarker'][1]+cfg.bC[1],cfg.nMC['fightMarker'][2],cfg.nMC['fightMarker'][3])) #截取右下角轮盘，以便确认是否战斗状态
    print("Start Script")
    script()
    print("End Script")
