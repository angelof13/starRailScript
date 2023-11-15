from configuration import time, pa
import configuration as cfg

# 0：非DEBUG,将会执行完当前小地图
# 1：区域内的传送点点击,若测试区域内多个传送点时，需要将人物送到上一行动的最终位置
# 2：是区域内一个传送点的行动DEBUG，不会执行地图点击及操作结束后打开地图
DEBUG = 0

# bigMapN: 大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
# regionN: 地图内地区序列，从0开始，但不是游戏内的第一个区域，而是第一个有怪的区域，如bigMapN=0,regionN=0，既为黑塔空间站的基座舱段 
# _node: 方便DeBug，有多个节点时，测试第几个节点
def selectRegion(bigMapN: int, regionN: int, _node:int=0):
    # 点击地图传送 
    # bigMapN:      大地图的序列 黑塔:0, 雅利洛:1, 仙舟:2 
    # regionN:      地图内地区序列，从0开始，但不是游戏内的第一个区域，而是第一个有怪的区域，如bigMapN=0,regionN=0，既为黑塔空间站的基座舱段 
    # transportN:   该地区内的第几个传送点，-1表示该区域内仅有一个传送点需要点击 
    # option:       需要点击的传送点周围有其他可点击图标时，设置为非0，表示在出现的选项框中选择第几个，目前所有该类传送点都是选择第一个，故仅实现选择第一个的坐标
    def _clickTransmitPoint(bigMapN:int,regionN:int,transportN:int=-1,option:int=0):
        if DEBUG == 2:
            return 0
        #点击小地图传送点
        time.sleep(4)
        if transportN != -1:
            pa.click(x=cfg.regionPoint[bigMapN][regionN][transportN][0],y=cfg.regionPoint[bigMapN][regionN][transportN][1])
        else:
            pa.click(x=cfg.regionPoint[bigMapN][regionN][0],y=cfg.regionPoint[bigMapN][regionN][1])
        time.sleep(2)
        if option == 1:
            pa.click(x=cfg.nMC['select'][0],y=cfg.nMC['select'][1])
            time.sleep(2)
        pa.click(x=cfg.nMC['transmit'][0],y=cfg.nMC['transmit'][1])
        time.sleep(0.5)
        pa.press('m')
        time.sleep(cfg.vP['loadingTime'])

######selectRegion函数主体仅有三个if判断，从此处开始
    if 0 == bigMapN:
        # 黑塔空间站 rN: 哪一个地区 node: 方便DeBug，有多个节点时，测试第几个节点
        def _region0(rN: int, node:int=0):
            if rN == 0: # 基座舱段
                _clickTransmitPoint(0,rN) #该区域仅需一个传送点
                if DEBUG == 1:
                    return 1
                aSequence = (['s',3], ['c'], ['CF'], ['s',1], ['c'], ['s',2.8], ['c'],['a',0.2], ['c'], ['a',1.5], ['s',2], ['c'],['m',1])
                cfg.action(aSequence)
            elif rN == 1: # 收容舱段
                for rNN in range (node,3): # 扫荡该区域需要用到3个传送点
                    _clickTransmitPoint(0,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['s', 5.4], ['sa', 2.2],['s',1], ['c'], ['CF'],['w',1.3], ['wd',1.3],['d',1.5],['c'],['ds',1.4], ['caps'], ['wa',1.5], ['c'], ['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['sa', 1.5],['a',2.4],['w',5.5],['c'],['c'],['CF'],['c'],['c'],['m',1])
                    elif rNN == 2:
                        aSequence = (['s', 0.7],['c'],['CF'],['s', 0.7],['c'],['CF'],['w',2.8],['wa',2.6],['c'],['CF'],['ds',2.7],['s',1.6],
                                     ['d',2.5],['w',3],['c'],['CF'],['d',2.3],['s',5],['d',1.5],['w',2.5],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 2: # 支援舱段
                 for rNN in range (node,2):
                    if rNN == 0:
                        _clickTransmitPoint(0,rN,rNN,1)
                    else:
                        _clickTransmitPoint(0,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['w', 1.4],['s', 0.01],['c'],['w', 1], ['c'],['c'],['CF'],['c'],['w',3.4],['a',2.5],['w',2],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['w', 4.6],['c'],['CF'],['c'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
        _region0(regionN, _node)

    elif 1 == bigMapN:
        # 雅利洛-Ⅵ  rN: 哪一个地区 node: 方便DeBug，有多个节点时，测试第几个节点
        def _region1(rN: int, node:int=0):
            if rN == 0: # 城郊雪原
                _clickTransmitPoint(1,rN)
                if DEBUG == 1:
                    return 1
                aSequence = (['a',1],['sa', 3], ['c'], ['CF'],['sa',3],['a',1],['w',4],['dw',2],['c'],['CF'],['dw',7],['w',2],['a',2],['aw',1.4],['c'],['a',4],['wa',3],['c'],['CF'],['w',3],['d',1],['c'],['CF'],['m',1])
                cfg.action(aSequence)
            elif rN == 1: # 边缘通路
                for rNN in range (node,3):
                    if rNN in [1,2]:
                        _clickTransmitPoint(1,rN,rNN,1)
                    else:
                        _clickTransmitPoint(1,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['s',4],['c'],['a',1.9],['c'],['a',2.5],['c'],['CF'],['d',4.5],['sd',2.2],['c'],['c'],['CF'],['c'],['d',2],['c'],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['w', 0.5],['a',3.5],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['s',5.5],['c'],['c'],['CF'],['c'],['sd',1.5],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 2: # 禁卫铁区
                return 1
            elif rN == 3: # 残响回廊
                for rNN in range (node,5):
                    _clickTransmitPoint(1,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['c'], ['w', 0.6], ['dw',1.1], ['w',1.7],['c'],['w',3],['a',0.5],['c'],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['s', 0.6],['a',7.3],['wa',1.5],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['a',1],['w',1.5],['c'],['a',2.6],['w',3.7],['c'],['CF'],['c'],['dw',2.3],['c'],['c'],['CF'],['c'],['wd',2],['ds',2],['as',0.5],['s',0.5],['as',0.5],['c'],['CF'],['a',1],['s',0.5],['a',0.5],['s',2],['c'],['CF'],['m',1])
                    elif rNN == 3:
                        aSequence = (['w',0.4],['d',1.3],['w',1.8],['c'],['c'],['CF'],['c'],['w',1.2],['c'],['CF'],['c'],['a',0.6],['w',1],['c'],['CF'],['w',2],['c'],['w',4],['c'],['c'],['CF'],['c'],['w',2.9],['c'],['CF'],['dw',1.5],['c'],
                                     ['as',1.5],['s',1.4],['d',2],['c'],['d',1.6],['c'],['CF'],['m',1])
                    elif rNN == 4:
                        aSequence = (['s',4],['sd',4],['s',4.8],['a',1],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 4: # 永冬岭
                for rNN in range (node,2):
                    if rNN == 0:
                        _clickTransmitPoint(1,rN,rNN,1)
                    else:
                        _clickTransmitPoint(1,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['w', 4.6], ['a',5],['c'],['CF'],['a',3.3],['w',0.4],['a',1],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['s', 0.6],['a',4.7],['c'],['CF'],['w',2],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 5: # 造物之柱
                return 1
            elif rN == 6: # 旧武器实验场
                return 1
            elif rN == 7: # 磐岩镇
                return 1
            elif rN == 8: # 大矿区
                for rNN in range (node,4):
                    if rNN == 2:
                        _clickTransmitPoint(1,rN,rNN,1)
                    else:
                        _clickTransmitPoint(1,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['s', 0.6], ['a',5],['c'],['CF'],['a',1.5],['c'],['CF'],['w',0.5],['a',0.8],['wd',2.4],['d',0.2],['sd',3.6],['dw',2.5],['c'],['w',1],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['w', 2],['d',1.7],['c'],['CF'],['dw',3],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['d', 5],['dw',1.3],['c'],['CF'],['c'],['w',1.5],['wd',1.5],['c'],['CF'],['m',1])
                    elif rNN == 3:
                        aSequence = (['wa', 1],['a',3.7],['c'],['CF'],['c'],['CF'],['w',2],['wd',1.3],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 9: # 铆钉镇
                for rNN in range (node,2):
                    _clickTransmitPoint(1,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['d', 1.6], ['w',0.3],['a',5.6],['w',2],['c'],['CF'],['aw',3],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['ds', 1],['a',4.6],['c'],['CF'],['w',3.5],['s',0.1],['c'],['w',5.4],['a',1.2],['w',2.6],['c'],['CF'],['c'],['CF'],['w',1.6],['c'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 10: # 机械聚落
                _clickTransmitPoint(1,rN)
                if DEBUG == 1:
                    return 1
                aSequence = (['ds',0.8],['c'],['CF'],['as',2.8],['sd',2.3],['c'],['sd',2.5],['sa',1],['c'],['CF'],['dw',1],['aw',2.5],['as',4],['c'],['as',12],['w',0.3],['a',0.5],['c'],['c'],['c'],['CF'],['c'],['d',2],['sd',1.3],['c'],['CF'],
                             ['wd',1.5],['c'],['CF'],['m',1])
                cfg.action(aSequence)
        _region1(regionN, _node)
    
    elif 2 == bigMapN:
        # 仙舟⌜罗浮⌟rN: 哪一个地区 node: 方便DeBug，有多个节点时，测试第几个节点
        def _region2(rN: int, node:int=0):
            if rN == 0: # 流云渡
                for rNN in range (node,4):
                    _clickTransmitPoint(2,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['w', 3],['c'],['w', 2.5],['d',4.3],['c'],['w',3.3],['c'],['c'],['CF'],['c'],['d',1],['c'],['CF'],['d',1.5],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['d', 1],['s',3],['d',0.6],['s',1.3],['c'],['s',6.4],['c'],['d',2],['c'],['CF'],['s',1],['c'],['CF'],['s',1.5],['c'],['CF'],['w',3],['c'],['CF'],['m',1])#这里有时会被怪物攻击，被攻击时，视角转向攻击怪物的视角
                    elif rNN == 2:
                        aSequence = (['w', 0.6],['a',4],['c'],['CF'],['a',2],['c'],['CF'],['s',0.3],['a',5],['c'],['a',3.8],['s',0.3],['a',1.5],['c'],['c'],['CF'],['a',1.5],['c'],['c'],['CF'],['a',1],['c'],['c'],['CF'],['m',1])
                    elif rNN == 3:
                        aSequence = (['d', 6.5],['w',0.8],['a',1.9],['c'],['CF'],['d',1.9],['s',3.5],['c'],['CF'],['s',1.5],['c'],['CF'],['s',2],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 1: # 迴星港
                for rNN in range (node,3):
                    if rNN == 0:
                        _clickTransmitPoint(2,rN,rNN,1)
                    else:
                        _clickTransmitPoint(2,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['dw', 0.5],['d', 0.4],['w', 0.2],['d', 0.3],['dw', 5],['wa',0.3],['c'],['s',0.6],['a',1.5],['c'],['CF'],['a',3],['s',0.4],['a',1],['s',0.4],['a',1],['s',1],['a',1],['c'],['d',1],
                                     ['w',1],['wa',5],['w',0.4],['d',0.3],['c'],['c'],['CF'],['as',0.5],['sd',0.7],['wd',1],['c'],['CF'],['s',1],['sd',1],['wd',1.5],['c'],['c'],['c'],['CF'],['wd',1],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['ds', 2],['c'],['CF'],['s',1],['c'],['s',1],['a',1],['s',1.6],['d',3.2],['w',2],['c'],['CF'],['w',1],['c'],['CF'],['w',2],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['a',0.4],['w',0.8],['d',1.6],['w',1],['c'],['CF'],['w',2.7],['a',2.5],['s',2],['a',1],['c'],['CF'],['s',0.4],['a',0.5],['c'],['CF'],
                                     ['w',0.3],['d',1],['s',2],['a',3],['w',0.5],['a',2.5],['c'],['CF'],['w',0.5],['a',2.5],['c'],['CF'],
                                     ['w',3.3],['a',1],['s',0.01],['c'],['CF'],['d',1.2],['s',2.5],['a',2],['s',0.1],['c'],
                                     ['s',4.8],['d',0.2],['s',2],['d',1],['c'],['CF'],['c'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 2: # 长乐天
                return 1
            elif rN == 3: # 金人巷
                return 1
            elif rN == 4: # 太卜司
                for rNN in range (node,4):
                    _clickTransmitPoint(2,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['s', 2.5],['ds', 2.6],['c'],['CF'],['sd', 0.8],['c'],['CF'],['as',3],['w',0.2],['c'],['CF'],['wa',0.3],['sa',0.2],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['s', 2.5],['sd', 7.4],['d',3],['c'],['w',0.6],['d',1.8],['s',0.6],['d',2.5],['dw',2.5],['sd',0.1],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['s', 0.1],['caps'],['d',0.1],['w',17],['d',1.3],['c'],['CF'],
                                     ['s',1.5],['d',3],['s',2],['c'],['CF'],['w',4],['c'],['CF'],['m',1])
                    elif rNN == 3:
                        aSequence = (['s', 9.2],['a',1.4],['s',1],['a',6.5],['c'],['CF'],['d',7],['c'],['CF'],['s',1],['c'],['CF'],['c'],['CF'],['d',2],['c'],['CF'],['c'],['CF'],['a',0.6],['s',4.6],['d',3.8],['c'],['c'],['CF'],['c'],['a',4],['s',2.5],['c'],['CF'],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 5: # 工造司
                for rNN in range (node,4):
                    _clickTransmitPoint(2,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['w', 5],['d', 1],['c'],['c'],['CF'],['c'],['d', 3.8],['c'],['CF'],['s',0.7],['a',3],['s',1],['d',1],['s',0.3],['c'],['CF'],['d',1],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['a',1.5],['s',1.5],['a',5.3],['c'],['CF'],['s',0.1],['c'],['CF'],['s',0.7],['a',4],['w',1.4],['a',1],['c'],['CF'],['a',3.5],['c'],['CF'],['a',2],['c'],
                                     ['a',2.3],['w',3.2],['c'],['a',5],['sa',0.2],['c'],['c'],['CF'],['a',4],['ds',0.3],['c'],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['a',1],['s',0.5],['d',1.5],['w',2],['d',2],['s',2],['d',0.5],['c'],['CF'],['d',1.5],['c'],['CF'],['d',1.5],['w',0.5],['c'],['CF'],['a',1],['c'],['w',5],['a',1],['s',0.1],['c'],['CF'],['w',1.5],['c'],['CF'],['a',3],['w',1.7],['a',2.5],['m',1])
                    elif rNN == 3:
                        aSequence = (['w',3.7],['d',1],['c'],['d',3],['c'],['CF'],['d',2],['c'],['CF'],['a',6],['w',4],['a',0.5],['s',0.5],['c'],['c'],['c'],['c'],['c'],['c'],['c'],['CF'],['w',1.5],['d',3.5],['w',1],['a',1],['w',3],['d',1],['s',0.5],['c'],['c'],['c'],['c'],['c'],['c'],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 6: # 绥园
                for rNN in range (node,2):
                    _clickTransmitPoint(2,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['s', 3],['sa',0.6],['c'],['CF'],['c'],['wd',0.7],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['w',2],['aw',0.5],['dw',0.5],['w',2.3],['c'],['CF'],['d',2.6],['c'],['CF'],['a',0.5],['s',0.5],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 7: # 丹鼎司
                for rNN in range (node,6):
                    _clickTransmitPoint(2,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['w', 3],['d', 0.3],['w',0.3],['dw',1],['w',1],['d',0.5],['w',1],['d',1.7],['c'],['CF'],['d',1.1],['c'],['CF'],
                                     ['wd',3],['sd',2.4],['c'],['CF'],['c'],['c'],['CF'],
                                     ['as',3],['a',1.5],['as',1.5],['s',2.5],['d',0.5],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['w',4.5],['d',2.4],['s',2.4],['d',2.4],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['d',0.2],['w',6.2],['aw',3.2],['d',0.2],['s',4],['a',1],['w',1.5],['c'],['CF'],['s',1],['c'],['CF'],['m',1])
                    elif rNN == 3:
                        aSequence = (['d',0.2],['w',6.2],['aw',3.2],['w',6.3],['a',4],['w',6],['wa',1],['c'],['as',1],['c'],['CF'],['m',1])
                    elif rNN == 4:
                        aSequence = (['as', 5],['s', 1.5],['as',3.5],['sd',2.5],['wd',0.3],['d',1.5],['ds',1],['c'],['CF'],['c'],['CF'],['ds',1],
                                     ['w',3],['dw',1.5],['w',2],['d',1],['c'],['d',5],['c'],['CF'],['s',0.2],['c'],['CF'],['s',1.5],['a',0.5],['c'],['CF'],['m',1])
                    elif rNN == 5:
                        aSequence = (['s',3.3],['sa',1],['c'],['c'],['CF'],['sa',5],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
            elif rN == 8: # 鳞渊境
                for rNN in range (node,5):
                    _clickTransmitPoint(2,rN,rNN)
                    if DEBUG == 1:
                        return 1
                    if rNN == 0:
                        aSequence = (['s', 4],['wd',4],['d',0.5],['c'],['CF'],['c'],['CF'],['m',1])
                    elif rNN == 1:
                        aSequence = (['c'],['a',3],['sa',1],['a',3.5],['c'],['CF'],['wa',2],['c'],['CF'],['a',1.5],['c'],['CF'],
                                     ['d',0.9],['w',6],['c'],['CF'],['w',5.2],['c'],['a',5],['c'],['CF'],['m',1])
                    elif rNN == 2:
                        aSequence = (['s',1],['c'],['s',0.5],['d',1.8],['s',2.5],['c'],['d',0.3],['s',2.3],['c'],['CF'],['c'],['CF'],['wd',0.5],['c'],['m',1])
                    elif rNN == 3:
                        aSequence = (['s',1.9],['d',5],['c'],['CF'],['c'],['d',9.5],['w',0.5],['d',0.5],['w',6.3],['c'],['CF'],['a',1],['c'],['CF'],['m',1])
                    elif rNN == 4:
                        aSequence = (['s',2],['a',13.5],['w',2],['dw',6.5],['w',2],['wd',2.8],['c'],['CF'],['w',0.5],['wd',1],['c'],['CF'],['m',1])
                    cfg.action(aSequence)
                    if DEBUG == 2:
                        return 1
        _region2(regionN, _node)


#该文件的main函数为区域内Debug使用
if __name__ == '__main__':
    # 0：非DEBUG,将会执行完当前小地图
    # 1：区域内的传送点点击,若测试区域内多个传送点时，需要将人物送到上一行动的最终位置
    # 2：是区域内一个传送点的行动DEBUG，不会执行地图点击及操作结束后打开地图
    DEBUG=2
    if 0 == cfg.getStarTrain():
        print("Not found game Window")
        exit()
    if DEBUG == 2:
        pa.screenshot("data/fightMarker.png",region=(cfg.nMC['fightMarker'][0],cfg.nMC['fightMarker'][1],cfg.nMC['fightMarker'][2],cfg.nMC['fightMarker'][3])) #截取Enter部分，以便确认是否战斗状态
    #0开始
    selectRegion(2, 6, 1) # Debug哪个区域直接在这里修改
    
    #aSequence = (['w',10],)
    #cfg.action(aSequence)