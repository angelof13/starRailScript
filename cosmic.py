from configuration import time, pa, action, getStarTrain, regionPoint
import configuration as cfg


def intoCosmicSimulator(first:bool=True):
    if first == True:
        time.sleep(4)
        pa.click(x=840+cfg.bC[0],y=100+cfg.bC[1]) #主控舱段
        pa.click(x=450+cfg.bC[0],y=935+cfg.bC[1]) #主控舱段
        pa.click(x=1650+cfg.bC[0],y=1000+cfg.bC[1])
        time.sleep(cfg.loadingTime)
    

def linkStart():
    
    return 0

#该文件的main函数为区域内Debug使用
if __name__ == '__main__':
    # 0：非DEBUG,将会执行完当前小地图
    # 1：区域内的传送点点击,若测试区域内多个传送点时，需要将人物送到上一行动的最终位置
    # 2：是区域内一个传送点的行动DEBUG，不会执行地图点击及操作结束后打开地图
    DEBUG=0
    if 0 == getStarTrain():
        print("Not found game Window")
        exit()
    #0开始
    linkStart() # Debug哪个区域直接在这里修改