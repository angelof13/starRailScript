from configuration import time, pa, action, getStarTrain
import configuration as cfg

# 进入模拟宇宙
# first：是否是第一次进入
def intoCosmicSimulator(first:bool=True):
    if first == True:
        aSequence = (['w',2], ['wd',0.4], ['f',5], ['c',[1780,330]],['c'])
        action(aSequence)
        for i in range(0,5):
            pa.scroll(-1)
            time.sleep(0.5)
        for i in range(0+cfg.cosmicNum,6):
            pa.scroll(1)
            time.sleep(0.5)
    time.sleep(1)
    pa.click(1270+cfg.bC[0],610+cfg.bC[1]) # 点击世界
    time.sleep(1)
    pa.click(1750+cfg.bC[0],1000+cfg.bC[1]) # 下载初始角色
    time.sleep(1)
    pa.click(1750+cfg.bC[0],1000+cfg.bC[1]) # 启动模拟宇宙
    time.sleep(1)
    pa.click(1170+cfg.bC[0],710+cfg.bC[1])  # 等级不达标的提示确认
    time.sleep(2)
    pa.click(285+cfg.bC[0]+225*cfg.preference,600+cfg.bC[1]) # 选择命途
    time.sleep(2)
    pa.click(1750+cfg.bC[0],1000+cfg.bC[1]) # 确认命途
    return 0

# 选择祝福
def selectBlessing():
    blessing="data/cosmic/blessing"+str(cfg.preference)+".png"
    for check in (0,2):
        sub=pa.locateAllOnScreen(blessing, region=(500 + cfg.bC[0], 773+cfg.bC[1], 1400, 19), confidence=0.8)
        temp = list(sub)
        tempL=len(temp)
        if tempL == 0:
            pa.click(1280+cfg.bC[0],1020+cfg.bC[1]) # 刷新一次
            time.sleep(1)
        else:
            pa.click(pa.center(temp[0])) # 有多个偏好命途的祝福时，选择第一个
            time.sleep(0.5)
            pa.click(1690+cfg.bC[0],1020+cfg.bC[1])
            time.sleep(1)
            return 0
        pa.click(533+cfg.bC[0],773+cfg.bC[1]) # 两次刷新都没有偏好命途的祝福，选择第一个祝福
        time.sleep(0.5)
        pa.click(1690+cfg.bC[0],1020+cfg.bC[1])
        time.sleep(1)
        return 0

# 根据小地图和界面信息，构建一小段行动逻辑
def buildAction():
    # if allEnd: # 打完最终boss后，返回-1，结束一次
    #    return -1
    return 0

# 模拟宇宙行动的大框架
def cosmicSimulatorAction():
    sub=pa.locateOnScreen("data/cosmic/start.png", region=(400 + cfg.bC[0], 620+cfg.bC[1], 1100, 30), confidence=0.8)
    if sub != None:
        pa.click(sub) # 选择1-2星祝福
        time.sleep(0.5)
        pa.click(960+cfg.bC[0],1020+cfg.bC[1]) # 确认命途
        time.sleep(1)
        selectBlessing() # 选择具体祝福
    while True:
        aSequence = buildAction()
        if aSequence == -1:
            break
        action(aSequence)
    return 0


def linkStart(times:int=34):
    intoCosmicSimulator()
    cosmicSimulatorAction()
    return 0

#该文件的main函数为区域内Debug使用
if __name__ == '__main__':
    if 0 == getStarTrain():
        print("Not found game Window")
        exit()
    linkStart(times=1)
    #pa.screenshot("data/cosmic/blessing2.png",region=(533+cfg.bC[0],773+cfg.bC[1],56,19)) # 533 941 1349