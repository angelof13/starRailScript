import pyautogui as pa
import pydirectinput as pdi
import time
import win32con
import win32gui as w32

# 需要修改的参数
_variableParameters={
    '_resolution':[1920,1080], # 分辨率
    'loadingTime':8, # 加载等待时间，即点击传送后到角色进入地图的等待时间

    # 模拟宇宙，cosmic分支暂未完成，未合并到main分支,暂为无效参数
    'cosmicNum':6, # 世界几:1-6
    'preference':4 # [存护/0，记忆/1，虚无/2，丰饶/3，寻猎/4，毁灭/5，欢愉/6]
}
vP = _variableParameters

#不可修改的一些数据，抽象出来仅为匹配分辨率
_nonModifiableCoordiates={
    'subSign':[630,1020], # 缩放地图需要点击的坐标
    'fightMarker':[1840,1082,40,20], # 查找战斗结束的坐标及区域
    'interstellarChart':[1600,180], # 星际航线的坐标
    'gap':100,

    'select':[900,795], # 多个传送点在一起，二次选择的坐标
    'transmit':[1650,1000] # 传送按键的坐标
}
nMC=_nonModifiableCoordiates

# 窗口的坐标
_baseCoordinate=[0,0,0,0]
bC = _baseCoordinate

#大地图
# 坐标都是相对坐标，基于窗口最左上角
# 大地图的点击坐标
bigMap=([350,600], # 黑塔空间站
        [1000,300], # 雅利洛-Ⅵ
        [1500,900]) # 仙舟⌜罗浮⌟

# 选择大地图内区域的基准坐标
# 第一个为游戏地图中右边第3个区域的坐标，区域点击基准坐标
bigMapRegionStart=([1520,465],
                   [1520,585], # 雅利洛VI，当身处残响回廊后，打开地图会默认展示后面的区域，变化后的基准坐标
                   [1520,780]) # 仙舟，当身处太卜司后，打开地图会默认展示后面的区域，变化后的基准坐标

# 大地图内可战斗的区域数量，非准确数量，值为从第一个可战斗区域到最后一个可战斗区域之间的差值
bigMapRegionNum=(3,9,7)

# 区域内的传送点坐标
regionPoint=(
    (
        [840,200], # 基座舱段
        [[1030,600],[955,670],[560,600]], # 收容舱段
        [[355,620],[630,445]] # 支援舱段
    ),
    (
        [1120,600], # 城郊雪原 
        [775,765], # 边缘通路 
        [0,0], # 禁卫铁区 
        [[980,260],[735,880],[735,805],[705,810]], # 残响回廊 
        [[525,755],[780,700]], # 永冬岭 
        [0,0], # 磐岩镇 
        [[740,920],[740,840],[775,720],[770,620]], # 大矿区 
        [[820,770],[810,365]], # 铆钉镇 
        [510,690] # 机械聚落
    ),
    (
        [[910,185],[750,725],[750,690],[785,660]], # 流云渡 
        [[1040,330],[665,545],[650,705]], # 迴星港 
        [0,0], # 长乐天
        [[450,220],[540,440],[540,180],[570,800]], # 太卜司 
        [[560,230],[660,400],[960,300],[815,205]], # 工造司
        [[610,185],[650,830],[640,500],[640,390],[940,220],[690,930]], # 丹鼎司
        [[1315,570],[340,585],[735,515],[660,585],[865,585]] # 鳞渊境
    ))

# 根据设置窗口分辨率缩放相应坐标
def _correct():
    #计算比例
    _ratio=[round(vP["_resolution"][0]/1920,2),round(vP["_resolution"][1]/1080,2)]
    #修正不可修改的一些数据
    for i in nMC:
        if i == "gap": # 每个区域间的坐标差值，基准100
            nMC[i] *= _ratio[1]
        elif i == "fightMarker":
            bias = [2 if _ratio[0]<1 else -2 if _ratio[0] !=1 else 0,2 if _ratio[1]<1 else -2 if _ratio[1] != 1 else 0]
            nMC[i][0] = int(nMC[i][0]* _ratio[0] + bias[0])
            nMC[i][1] = int(nMC[i][1]* _ratio[1] + bias[1])
            nMC[i][2] = int(nMC[i][2]* _ratio[0])+1
            nMC[i][3] = int(nMC[i][3]* _ratio[1])+1
        else:
            nMC[i][0] = int(nMC[i][0]* _ratio[0])
            nMC[i][1] = int(nMC[i][1]* _ratio[1])
        
    #修正大地图坐标
    for sublist in bigMap:
        sublist[0] = int(sublist[0] * _ratio[0])
        sublist[1] = int(sublist[1] * _ratio[1])
    #修正选择大地图内区域的基准坐标
    for sublist in bigMapRegionStart:
        sublist[0] = int(sublist[0] * _ratio[0])
        sublist[1] = int(sublist[1] * _ratio[1])
    #修正区域坐标传送点
    for i, sublist in enumerate(regionPoint):
        for j, element in enumerate(sublist):
            # 如果元素是一个列表，就遍历其中的元素和索引，并根据比例修改数据
            if isinstance(element[0], list):
                for k, item in enumerate(element):
                    regionPoint[i][j][k][0] = int(regionPoint[i][j][k][0] * _ratio[0])
                    regionPoint[i][j][k][1] = int(regionPoint[i][j][k][1] * _ratio[1])
            else:
                regionPoint[i][j][0] = int(regionPoint[i][j][0] * _ratio[0])
                regionPoint[i][j][1] = int(regionPoint[i][j][1] * _ratio[1])

if vP["_resolution"] != [1920,1080]:
    print("correct coordinates")
    _correct()

# 找到星穹铁道的窗口,并选中
def getStarTrain():
    startTrain = w32.FindWindow('UnityWndClass',u'崩坏：星穹铁道')
    if startTrain == 0:
        return 0
    w32.ShowWindow(startTrain,win32con.SW_NORMAL)
    w32.SetForegroundWindow(startTrain)
    time.sleep(2)
    global bC
    bC = w32.GetWindowRect(startTrain)
    print(bC)
    return 1

# 地图内操作解析
# actionSequence: 需要执行的一系列行动的序列
def action(actionSequence: tuple):
    print(actionSequence)
    for actionI in actionSequence:
        print(actionI)
        if actionI[0] == 'x' or actionI[0] == 'X': #移动横向视角，一圈大概7720，非精准操纵，慎用，负数为向左转，正数为向右转
            pdi.moveRel(xOffset=actionI[1], yOffset=0, relative=True)
        elif actionI[0] == 'y' or actionI[0] == 'Y': #移动纵向视角，非精准操纵，慎用，甚至感觉没用(ˉ▽ˉ；)...
            #一圈大概7720
            pdi.moveRel(xOffset=0, yOffset=actionI[1], relative=True)
        elif actionI[0] == 'c' or actionI[0] == 'C': #左键，平A
            aIL = len(actionI)
            if aIL == 1:
                pa.click()
            else:
                pa.click(x=actionI[1][0]+bC[0],y=actionI[1][1]+bC[1])
            time.sleep(1)
        elif actionI[0] == 'cf' or actionI[0] == 'CF': #检测战斗是否结束

            # 检测战斗是否结束 interval: 间隔几秒检查一次，默认是2秒
            def _checkFightEnd(interval:int=2):
                for i in range(2,5): #检测是否进入战斗，尝试以2s,3s,4s的间隔检查三次
                    time.sleep(i)
                    if None == pa.locateOnScreen("data/fightMarker.png",region=(nMC['fightMarker'][0]+bC[0],nMC['fightMarker'][1]+bC[1],nMC['fightMarker'][2],nMC['fightMarker'][3]),confidence=0.9,grayscale=True):
                        print("fight start")
                        break
                while True:
                    time.sleep(interval)
                    if None != pa.locateOnScreen("data/fightMarker.png",region=(nMC['fightMarker'][0]+bC[0],nMC['fightMarker'][1]+bC[1],nMC['fightMarker'][2],nMC['fightMarker'][3]),confidence=0.9,grayscale=True):
                        print("fight end")
                        return 1

            aIL = len(actionI)
            if aIL == 1:
                _checkFightEnd()
            else:
                _checkFightEnd(actionI[1])
        elif actionI[0] == 'f' or actionI[0] == 'F': #按F，进入画卷，模拟宇宙对话
            time.sleep(1)
            pa.press(actionI[0])
            time.sleep(actionI[1])
        elif actionI[0] == 'm' or actionI[0] == 'M': #打开地图
            time.sleep(1)
            pa.press(actionI[0])
            time.sleep(actionI[1])
        else: #其他按键操作，基本为'w''a''s''d'的组合，默认奔跑，需要走路时，在操作列表增加一位，例如['s',3,1]

            # 行动 key: 行动按键; sec: 行动时长; walkFlag: 是否走路，默认False，既奔跑状态
            def _run(key, sec: float, walkFlag:bool = False):
                time.sleep(0.1)
                for keyI in key:
                    pa.keyDown(keyI)
                if walkFlag == False:
                    pa.click(button='right')
                time.sleep(sec)
                for keyI in key:
                    pa.keyUp(keyI)

            aIL = len(actionI)
            if aIL == 2:
                _run(actionI[0], actionI[1])
            else:
                _run(actionI[0], actionI[1], True)

    time.sleep(1)
    
