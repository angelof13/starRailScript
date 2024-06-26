import configuration as cfg
from configuration import time, pa
from pathFinding import selectRegion
import random

DEBUG = 0
'''0:非DEBUG， 1:只执行到点击区域的操作'''

def clickBigMap(mapN:int):
    '''选择大地图
    MapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2， 匹诺康尼:3 '''
    time.sleep(2)
    pa.click(x=cfg.nMC['interstellarChart'][0],y=cfg.nMC['interstellarChart'][1]) # 防止在匹诺康尼的小房间里，点击两次
    time.sleep(1)
    pa.click(x=cfg.nMC['interstellarChart'][0],y=cfg.nMC['interstellarChart'][1])
    time.sleep(2)
    
    def randomClick(times:int): # 此界面需要随机点击几次，才能正常点击
        for i in range(2):
            time.sleep((random.randint(1,11)/10))
            pa.mouseDown()
            time.sleep((random.randint(1,5)/10))
            pa.mouseUp()
    
    randomClick(2)
    pa.mouseDown(x=cfg.bigMap[0][0],y=cfg.bigMap[0][1])
    time.sleep(0.5)
    pa.moveRel(800,0,1)
    pa.mouseUp()
    time.sleep(1)
    
    pa.moveTo(x=cfg.bigMap[mapN][0],y=cfg.bigMap[mapN][1])
    time.sleep(1)
    randomClick(2)

moveFlag:int=0
def clickRegion(bigMapN:int,regionN:int):
    '''选择大地图内的可战斗区域
    bigMapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
    regionN: 地图内地区序列,从0开始,但不是游戏内的第一个区域,而是第一个有怪的区域,如bigMapN=0,regionN=0，既为黑塔空间站的基座舱段 '''
    time.sleep(2)
    def move(rel:int): # 移动选择区域，正数往下拉，负数往上拉
        global moveFlag
        if moveFlag == 0:
                pa.mouseDown(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1])
                time.sleep(0.5)
                pa.moveRel(0,rel,1)
                pa.mouseUp()
                time.sleep(0.5)
                moveFlag = 1
    if bigMapN == 0: # 黑塔空间站
        pa.click(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1]+regionN*cfg.nMC['gap'])
    elif bigMapN == 1: # 雅利洛-Ⅵ
        if regionN < 4:
            move(500)
            pa.click(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1]+regionN*cfg.nMC['gap'])
        else:
            move(-500)
            pa.click(x=cfg.bigMapRegionStart[1][0],y=cfg.bigMapRegionStart[1][1]+(regionN-4)*cfg.nMC['gap'])
    elif bigMapN == 2: # 仙舟
        if regionN < 5:
            move(500)
            pa.click(x=cfg.bigMapRegionStart[0][0],y=cfg.bigMapRegionStart[0][1]+regionN*cfg.nMC['gap'])
        else:
            move(-500)
            pa.click(x=cfg.bigMapRegionStart[2][0],y=cfg.bigMapRegionStart[2][1]+(regionN-5)*cfg.nMC['gap'])
    elif bigMapN == 3: # 皮诺康尼
        if regionN < 2:
            move(500)
            pa.click(x=cfg.bigMapRegionStart[3][0],y=cfg.bigMapRegionStart[3][1]+regionN*cfg.nMC['gap'])
        else:
            move(-500)
            pa.click(x=cfg.bigMapRegionStart[3][0],y=cfg.bigMapRegionStart[3][1]+(regionN-1)*cfg.nMC['gap'])

    time.sleep(1)

    
#操作开始
def script():
    time.sleep(0.1)
    pa.press('m') # 打开地图
    global moveFlag
    subSignFlag=0
    for i in range(cfg.vP['startBigMap'],4): # 四个大体图
        print("bigMapNum=",i)
        moveFlag = 0
        clickBigMap(i) # 点击大地图

        if 0 == subSignFlag:
            time.sleep(1)
            pa.click(cfg.nMC['subSign'][0],cfg.nMC['subSign'][1],clicks=10,interval=0.3) # 点击缩放地图，保证传送点的位置正确
            time.sleep(1)
            subSignFlag = 1

        startRegion = cfg.vP['startRegion']
        for j in range(startRegion,cfg.bigMapRegionNum[i]): # 大地图中的区域选择 
            print("regionNum=",j)
            if cfg.vP['startRegion'] != 0:
                cfg.vP['startRegion'] = 0
            clickRegion(i,j) # 选择区域
            time.sleep(1)
            if DEBUG == 0:
                selectRegion(i,j) # 进行区域战斗逻辑


# 脚本开始
# 需要选择人物最好为推荐角色 ，在非基座舱段的其他场地，并且在可操作界面
if __name__ == '__main__':
    DEBUG=0
    print("Select Window")
    if 0 == cfg.getStarTrain():
        print("Not Found Game Window")
        exit()
    time.sleep(2)
    print(cfg.nMC['fightMarker'])
    pa.screenshot("data/fightMarker.png",region=(cfg.nMC['fightMarker'][0],cfg.nMC['fightMarker'][1],cfg.nMC['fightMarker'][2],cfg.nMC['fightMarker'][3])) #截取Enter部分，以便确认是否战斗状态
    print("Start Script")
    script()
    print("End Script")
