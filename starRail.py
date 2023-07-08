import configuration as cfg
from configuration import time, pa, random, bigMap, bigMapRegionStart, bigMapRegionNum, getStarTrain
from pathFinding import selectRegion

#选择大地图
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

#选择大地图内的可战斗箱庭
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
    

#脚本开始
def script():
    time.sleep(0.1)
    pa.press('m')
    time.sleep(1)
    sub=pa.locateOnScreen("data/sub.png", region=(600 + cfg.bC[0], 990+cfg.bC[1], 200, 200), confidence=0.9)
    pa.click(sub,clicks=10,interval=0.3)
    for i in range(0,3):
        print("bigMapNum=",i)
        clickBigMap(i)
        j = 0
        while j < bigMapRegionNum[i]:
            print("regionNum=",j)
            clickRegion(i,j)
            j=j+1

if __name__ == '__main__':
    print("select windows")
    if 0 == getStarTrain():
        print("None Game")
        exit()
    print(cfg.bC)
    pa.screenshot("data/fightEnd.png",region=(35+cfg.bC[0],113+cfg.bC[1],35,20))
    print("start script")
    script()
