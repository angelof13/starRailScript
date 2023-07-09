from configuration import time, pa, pdi, checkFightEnd, getStarTrain, regionPoint
import configuration as cfg

# 0：非DEBUG,将会执行完当前小地图
# 1：区域内的传送点点击,若测试区域内多个传送点时，需要将人物送到上一行动的最终位置
# 2：是区域内一个传送点的行动DEBUG，不会执行地图点击及操作结束后打开地图
DEBUG = 0

# 行动
# key:      行动按键; 
# sec:      行动时长; 
# walkFlag: 是否走路，默认False，既奔跑状态
def _run(key, sec: float, walkFlag:bool = False):
    time.sleep(0.1)
    for keyI in key:
        pa.keyDown(keyI)
    if walkFlag == False:
        pa.click(button='right')
    time.sleep(sec)
    for keyI in key:
        pa.keyUp(keyI)

# 点击地图传送 
# bigMapN:      大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
# regionN:      地图内地区序列，从0开始，但不是游戏内的第一个区域，而是第一个有怪的区域，如bigMapN=0,regionN=0，既为黑塔空间站的基座舱段 
# transportN:   该地区内的第几个传送点，-1表示该区域内仅有一个传送点需要点击 
# option:       需要点击的传送点周围有其他可点击图标时，设置为非0，表示在出现的选项框中选择第几个，目前所有该类传送点都是选择第一个，故仅实现选择第一个的坐标
def _clickRegion(bigMapN:int,regionN:int,transportN:int=-1,option:int=0):
    if DEBUG == 2:
        return 0
    #点击小地图传送点
    time.sleep(4)
    if transportN != -1:
        pa.click(x=regionPoint[bigMapN][regionN][transportN][0]+cfg.bC[0],y=regionPoint[bigMapN][regionN][transportN][1]+cfg.bC[1])
    else:
        pa.click(x=regionPoint[bigMapN][regionN][0]+cfg.bC[0],y=regionPoint[bigMapN][regionN][1]+cfg.bC[1])
    time.sleep(1)
    if option == 1:
        pa.click(x=900+cfg.bC[0],y=795+cfg.bC[1])
        time.sleep(1)
    pa.click(x=1650+cfg.bC[0],y=1000+cfg.bC[1])
    time.sleep(cfg.loadingTime)

# 地图内操作解析
# actionSequence: 需要执行的一系列行动的序列
def _action(actionSequence: tuple):
    print(actionSequence)
    for actionI in actionSequence:
        print(actionI)
        if actionI[0] == 'x' or actionI[0] == 'X': #移动横向视角，一圈大概7720，非精准操纵，慎用，负数为向左转，正数为向右转
            pdi.moveRel(xOffset=actionI[1], yOffset=0, relative=True)
        elif actionI[0] == 'y' or actionI[0] == 'Y': #移动纵向视角，非精准操纵，慎用，甚至感觉没用(ˉ▽ˉ；)...
            #一圈大概7720
            pdi.moveRel(xOffset=0, yOffset=actionI[1], relative=True)
        elif actionI[0] == 'c' or actionI[0] == 'C': #左键，平A
            pa.click()
            time.sleep(1)
        elif actionI[0] == 'cf' or actionI[0] == 'CF': #检测战斗是否结束
            aIL = len(actionI)
            if aIL == 1:
                checkFightEnd()
            else:
                checkFightEnd(actionI[1])
        elif actionI[0] == 'f' or actionI[0] == 'F': #按F，当前版本，仅有进入画卷这一操作需要
            time.sleep(1)
            pa.press(actionI[0])
            time.sleep(actionI[1])
        else: #其他按键操作，基本为'w''a''s''d'的组合，默认奔跑，需要走路时，在操作列表增加一位，例如['s',3,1]
            aIL = len(actionI)
            if aIL == 2:
                _run(actionI[0], actionI[1])
            else:
                _run(actionI[0], actionI[1], True)

    time.sleep(1)
    pa.press('m')
    time.sleep(1)

# 以下为地图内操作逻辑
# 黑塔空间站
# rN: 哪一个地区 
def _region0(rN: int):
    if rN == 0: # 基座舱段
        _clickRegion(0,rN) #该区域仅需一个传送点
        if DEBUG == 1:
            return 1
        aSequence = (['s',3], ['c'], ['CF'], ['s',1], ['c'], ['s',2.8], ['c'],['a',0.2], ['c'], ['a',2.3], ['s',2], ['c'])
        _action(aSequence)
    elif rN == 1: # 收容舱段
        for rNN in range (0,3): # 扫荡该区域需要用到3个传送点
            _clickRegion(0,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['s', 5.4], ['sa', 1.8], ['c'], ['CF'], ['wd',1.3],['d',1.5],['c'],['d',1.4], ['x',3000], ['w',1.5], ['c'], ['CF'])
            elif rNN == 1:
                aSequence = (['sa', 1.5],['a',2.4],['w',5.5],['c'],['c'],['CF'],['c'],['c'])
            elif rNN == 2:
                aSequence = (['s', 0.7],['c'],['s', 0.7],['c'],['CF'],['w',3],['wa',2.6],['c'],['CF'],['ds',2.6],['s',1.6],
                             ['d',2.5],['w',3],['c'],['CF'],['d',2],['s',5],['d',1.5],['w',2.5],['c'],['CF'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 2: # 支援舱段
         for rNN in range (0,2):
            if rNN == 0:
                _clickRegion(0,rN,rNN,1)
            else:
                _clickRegion(0,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['w', 1.4],['s', 0.01],['c'],['w', 0.8], ['c'],['c'],['CF'],['c'],['w',3.5],['a',2.5],['w',2],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['w', 4.6],['c'],['CF'],['c'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    time.sleep(1)

# 雅利洛-Ⅵ
# rN: 哪一个地区
def _region1(rN: int):
    if rN == 0: # 城郊雪原
        _clickRegion(1,rN)
        if DEBUG == 1:
            return 1
        aSequence = (['a',1],['sa', 3], ['c'], ['CF'],['sa',3],['a',1],['w',4],['dw',2],['c'],['CF'],['dw',7],['w',2],['a',2],['aw',1.4],['c'],['a',4],['wa',3],['c'],['CF'],['w',3],['d',1],['c'],['CF'])
        _action(aSequence)
    elif rN == 1: # 边缘通路
        _clickRegion(1,rN)
        if DEBUG == 1:
            return 1
        aSequence = (['s',4],['c'],['a',1.9],['c'],['a',2.5],['c'],['CF'],['d',4.5],['sd',2.2],['c'],['c'],['CF'],['c'],['d',2],['c'],['c'],['CF'],['d',3.7],['w',2.7],['c'],['CF'],
                     ['d',4.3],['s',1.3],['d',5],['c'],['CF'],['d',1],['c'],['dw',2],['c'],['CF'])
        _action(aSequence)
    elif rN == 2: # 禁卫铁区
        return 1
    elif rN == 3: # 残响回廊
        for rNN in range (0,4):
            _clickRegion(1,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['c'], ['w', 0.6], ['dw',1.1], ['w',1.7],['c'],['w',3],['a',0.5],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['s', 0.6],['a',7.3],['wa',2],['w',0.3],['c'],['CF'])
            elif rNN == 2:
                aSequence = (['a',1],['w',1.5],['c'],['a',2.6],['w',3.7],['c'],['CF'],['c'],['dw',2.3],['c'],['c'],['CF'],['c'],['wd',2],['ds',2],['as',0.5],['s',0.5],['as',0.5],['c'],['CF'],['a',1],['s',0.5],['a',0.5],['s',2],['c'])
            elif rNN == 3:
                aSequence = (['w',0.4],['d',1.3],['w',1.8],['c'],['c'],['CF'],['w',1.2],['c'],['a',0.6],['w',1],['c'],['CF'],['w',2],['c'],['w',4],['c'],['c'],['CF'],['c'],['w',2.9],['c'],['CF'],['dw',1.5],['c'],
                             ['as',1.5],['s',1.4],['d',2],['c'],['CF'],['c'],['d',1.6],['c'],['CF'],['w',0.6],['d',5],['w',2],['c'],['CF'],['w',2],['c'],['CF'],['w',0.6],['a',2.5],['c'],['c'],['CF'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 4: # 永冬岭
        for rNN in range (0,2):
            if rNN == 0:
                _clickRegion(1,rN,rNN,1)
            else:
                _clickRegion(1,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['w', 4.6], ['a',5],['c'],['CF'],['a',3.3],['w',0.4],['a',1],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['s', 0.6],['a',4.7],['c'],['CF'],['w',2],['c'],['CF'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 5: # 磐岩镇
        return 1
    elif rN == 6: # 大矿区
        for rNN in range (0,4):
            if rNN == 2:
                _clickRegion(1,rN,rNN,1)
            else:
                _clickRegion(1,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['s', 0.6], ['a',5],['c'],['CF'],['a',1.5],['c'],['CF'],['w',0.5],['a',0.8],['wd',2.4],['d',0.2],['sd',3.6],['dw',2.5],['c'],['w',1],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['w', 2],['d',2],['dw',1.2],['c'],['CF'],['dw',1],['c'],['CF'])
            elif rNN == 2:
                aSequence = (['d', 5],['dw',1.3],['c'],['CF'],['c'],['w',1.5],['wd',1.5],['c'],['CF'])
            elif rNN == 3:
                aSequence = (['wa', 1],['a',3.7],['c'],['CF'],['c'],['CF'],['w',2],['wd',1.3],['c'],['CF'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 7: # 铆钉镇
        for rNN in range (0,2):
            _clickRegion(1,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['d', 1.6], ['w',0.3],['a',5.6],['w',2],['c'],['CF'],['aw',3],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['ds', 1],['a',4.6],['c'],['CF'],['w',3.5],['s',0.1],['c'],['w',5.4],['a',1.2],['w',2.6],['c'],['CF'],['c'],['CF'],['w',1.6],['c'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 8: # 机械聚落
        _clickRegion(1,rN)
        if DEBUG == 1:
            return 1
        aSequence = (['ds',0.8],['c'],['CF'],['as',2.8],['sd',2.3],['c'],['sd',2.5],['sa',1],['c'],['CF'],['dw',1],['aw',2.5],['as',4],['c'],['as',12],['w',0.3],['a',0.5],['c'],['c'],['c'],['CF'],['c'],['d',2],['sd',1.3],['c'],['CF'],
                     ['wd',1.5],['c'],['CF'])
        _action(aSequence)

# 仙舟⌜罗浮⌟
# rN: 哪一个地区
def _region2(rN: int):
    if rN == 0: # 流云渡
        for rNN in range (0,4):
            _clickRegion(2,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['w', 3],['c'],['w', 2.5],['d',4.3],['c'],['w',3.3],['c'],['c'],['CF'],['c'],['d',1],['c'],['CF'],['d',1.5],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['d', 1],['s',3],['d',0.6],['s',1.3],['c'],['s',6.4],['c'],['d',2],['c'],['CF'],['s',1],['c'],['CF'],['s',1.5],['c'],['CF'],['w',3],['c'],['CF'])#这里有时会被怪物攻击，被攻击时，视角转向攻击怪物的视角
            elif rNN == 2:
                aSequence = (['w', 0.6],['a',4],['c'],['CF'],['a',2],['c'],['CF'],['s',0.3],['a',5],['c'],['a',3.8],['s',0.3],['a',1.5],['c'],['c'],['CF'],['a',1.5],['c'],['c'],['CF'],['a',1],['c'],['c'],['CF'])
            elif rNN == 3:
                aSequence = (['d', 6.5],['w',0.8],['a',1.9],['c'],['CF'],['d',1.9],['s',3.5],['c'],['CF'],['s',1.5],['c'],['CF'],['s',2],['c'],['CF'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 1: # 迴星港
        for rNN in range (0,3):
            if rNN == 0:
                _clickRegion(2,rN,rNN,1)
            else:
                _clickRegion(2,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['dw', 1],['d', 0.2],['dw', 6],['wa',0.3],['c'],['s',0.6],['a',1.5],['c'],['CF'],['a',3],['s',0.4],['a',1],['s',0.4],['a',1],['s',1],['a',1],['c'],['d',1],
                             ['w',1],['wa',5],['d',0.3],['c'],['c'],['c'],['CF'],['sd',0.7],['wd',1],['c'],['CF'],['s',1],['sd',1],['wd',1.5],['c'],['c'],['c'],['CF'],['wd',1],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['ds', 2],['c'],['CF'],['s',1],['c'],['s',1],['a',1],['s',1.6],['d',3.2],['w',2],['c'],['CF'],['w',1],['c'],['CF'],['w',2],['c'],['CF'])
            elif rNN == 2:
                aSequence = (['a',0.4],['w',0.8],['d',1.6],['w',1],['c'],['CF'],['w',2.7],['a',2.5],['s',2],['a',1],['c'],['CF'],['s',0.4],['a',0.5],['c'],['CF'],
                             ['w',0.3],['d',1],['s',2],['a',3],['w',0.5],['a',2.5],['c'],['CF'],['w',0.5],['a',2.5],['c'],['CF'],
                             ['w',3.3],['a',1],['s',0.01],['c'],['CF'],['d',1.2],['s',2.5],['a',2],['s',0.1],['c'],
                             ['s',6.8],['d',2],['c'],['CF'],['c'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 2: # 太卜司
        for rNN in range (0,3):
            _clickRegion(2,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                time.sleep(3)
                aSequence = (['s', 2.5],['sd', 2.7],['c'],['CF'],['sd', 0.3],['c'],['CF'],['sd', 0.4],['c'],['CF'],['sa',3],['c'],['CF'],['sd', 0.4],['c'],['c'],['c'],['c'],['CF'],['dw',2.7],['sd',3.6],['d',3],['c'],['w',0.6],['d',1.8],['s',0.6],['d',2.6],['dw',2.5],['sd',0.1],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['d', 0.3],['w',3],['c'],['a',0.3],['w',2],['wd',5.2],['w',0.1],['f',7],
                             ['d',1.5],['s',0.1],['d',0.5],['c'],['CF'],['w',0.05],['d',2],['ds',2],['s',0.5],['sd',0.5],['dw',2.5],['w',0.5],['wd',2.1],['c'],['CF'],['sd',0.8],['dw',3],['c'],['CF'],['sd',1],['c'],['CF'],['aw',2.5],['c'],['CF'])
            elif rNN == 2:
                aSequence = (['s', 9],['a',1.5],['s',1],['a',5],['c'],['CF'],['d',5.5],['c'],['CF'],['s',1],['c'],['CF'],['c'],['CF'],['d',2],['c'],['CF'],['c'],['CF'],['a',0.6],['s',4.8],['d',4],['c'],['c'],['CF'],['c'],['a',4],['s',2.5],['c'],['CF'],['c'],['CF'])
            _action(aSequence)
            if DEBUG == 2:
                return 1
    elif rN == 3: # 工造司
        for rNN in range (0,4):
            _clickRegion(2,rN,rNN)
            if DEBUG == 1:
                return 1
            if rNN == 0:
                aSequence = (['w', 5],['d', 1],['c'],['c'],['CF'],['c'],['d', 3.8],['c'],['CF'],['s',0.7],['a',3],['s',1],['d',1],['s',0.3],['c'],['CF'],['d',1],['c'],['CF'],['w',0.5],['a',6],['w',0.7],['a',3.5],['s',0.1],['c'],['CF'],['a',2],['s',0.2],['c'],['CF'])
            elif rNN == 1:
                aSequence = (['a',1.5],['s',1.5],['a',5.3],['c'],['CF'],['s',0.8],['a',4],['w',1.4],['a',1],['c'],['CF'],['a',3.5],['c'],['CF'],['a',4.5],['w',3],['a',2],['c'],['c'],['CF'],['a',2],['c'],['c'],['CF'],['a',2],['c'],['c'],['CF'],['a',3],['c'],['c'],['CF'])
            elif rNN == 2:
                aSequence = (['a',1],['s',0.5],['d',1.5],['w',2],['d',2],['s',2],['d',0.5],['c'],['CF'],['d',1.5],['c'],['CF'],['d',1.5],['w',0.5],['c'],['CF'],['a',1],['c'],['w',5],['a',1],['s',0.1],['c'],['CF'],['w',1.5],['c'],['CF'],['a',3],['w',1.7],['a',2.5])
            elif rNN == 3:
                aSequence = (['w',3.7],['d',1],['c'],['d',3],['c'],['CF'],['d',2],['c'],['CF'],['a',6],['w',3],['a',0.5],['s',1],['c'],['CF'],['w',1.5],['d',3.5],['w',1],['a',1],['w',2],['d',1],['s',0.5],['c'],['CF'])
            _action(aSequence)
            if DEBUG == 2:
                return 1

# bigMapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
# regionN: 地图内地区序列，从0开始，但不是游戏内的第一个区域，而是第一个有怪的区域，如bigMapN=0,regionN=0，既为黑塔空间站的基座舱段 
def selectRegion(bigMapN: int, regionN: int):
    if 0 == bigMapN:
        _region0(regionN)
    elif 1 == bigMapN:
        _region1(regionN)
    elif 2 == bigMapN:
        _region2(regionN)

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
    selectRegion(2, 2) # Debug哪个区域直接在这里修改