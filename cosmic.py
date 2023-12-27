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
        for i in range(0+cfg.vP['cosmicNum'],8):
            pa.scroll(1)
            time.sleep(0.5)
    time.sleep(1)
    pa.click(cfg.nMCC['choiceWord'][0],cfg.nMCC['choiceWord'][1]) # 点击世界
    time.sleep(1)
    pa.click(cfg.nMCC['choiceRoleAndStart'][0],cfg.nMCC['choiceRoleAndStart'][1]) # 下载初始角色
    time.sleep(1)
    pa.click(cfg.nMCC['choiceRoleAndStart'][0],cfg.nMCC['choiceRoleAndStart'][1]) # 启动模拟宇宙
    time.sleep(1)
    pa.click(cfg.nMCC['closeAlert'][0],cfg.nMCC['closeAlert'][1])  # 等级不达标的提示确认
    time.sleep(2)
    pa.click(cfg.nMCC['choiceDestinyBase'][0]+cfg.nMCC['choiceDestinyGap']*cfg.vP['cosmicNum'],cfg.nMCC['choiceDestinyBase'][1]) # 选择命途
    time.sleep(2)
    pa.click(cfg.nMCC['choiceRoleAndStart'][0],cfg.nMCC['choiceRoleAndStart'][1]) # 确认命途
    return 0

# 选择祝福
def selectBlessing():
    blessing="data/cosmic/"+str(cfg.vP['_resolution'][0])+"x"+str(cfg.vP['_resolution'][1])+"/blessing"+str(cfg.vP['cosmicNum'])+".png"
    for check in (0,2):
        time.sleep(3)
        sub=pa.locateAllOnScreen(blessing, region=(cfg.nMCC['choiceBlessing'][0], cfg.nMCC['choiceBlessing'][1], cfg.nMCC['choiceBlessing'][2], cfg.nMCC['choiceBlessing'][3]), confidence=0.8)
        temp = list(sub)
        tempL=len(temp)
        if tempL == 0:
            pa.click(cfg.nMCC['refresh'][0],cfg.nMCC['refresh'][1]) # 刷新一次
            time.sleep(1)
        else:
            pa.click(pa.center(temp[0])) # 有多个偏好命途的祝福时，选择第一个
            time.sleep(0.5)
            pa.click(cfg.nMCC['determine'][0],cfg.nMCC['determine'][1])
            time.sleep(1)
            return 0
    pa.click(cfg.nMCC['firstBlessing'][0],cfg.nMCC['firstBlessing'][1]) # 两次刷新都没有偏好命途的祝福，选择第一个祝福
    time.sleep(0.5)
    pa.click(cfg.nMCC['determine'][0],cfg.nMCC['determine'][1])
    time.sleep(1)
    return 0

# 根据代号，进行相应的行动
def choiceAction(index:int):
    # if allEnd: # 打完最终boss后，返回-1，结束一次
    #    return -1
    return 0

# 根据小地图和界面信息，获取应该的行动逻辑代号
def getMapIndex():
    # if allEnd: # 打完最终boss后，返回-1，结束一次
    #    return -1
    return 0

# 模拟宇宙行动的大框架
def cosmicSimulatorAction():
    time.sleep(1)
    sub=pa.locateOnScreen("data/cosmic/"+str(cfg.vP['_resolution'][0])+"x"+str(cfg.vP['_resolution'][1])+"/start.png", region=(cfg.nMCC['choiceStartBlessing'][0], cfg.nMCC['choiceStartBlessing'][1], cfg.nMCC['choiceStartBlessing'][2], cfg.nMCC['choiceStartBlessing'][3]), confidence=0.8)
    if sub != None:
        pa.click(sub) # 选择1-2星祝福
        time.sleep(0.5)
        pa.click(cfg.nMCC['determineDestiny'][0],cfg.nMCC['determineDestiny'][1]) # 确认命途
        time.sleep(1)
        selectBlessing() # 选择具体祝福
        index = getMapIndex()
        choiceAction(index)
    return 0


def linkStart(times:int=34):
    intoCosmicSimulator()
    for i in range(0,times):
        cosmicSimulatorAction()
    return 0

#该文件的main函数为区域内Debug使用
if __name__ == '__main__':

    if 0 == getStarTrain():
        print("Not found game Window")
        exit()
    linkStart(times=1)


    