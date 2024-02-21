import pyautogui as pa
import pydirectinput as pdi
import time
import win32con
import win32gui as w32

# 需要修改的参数
_variableParameters={
    '_resolution':[1920,1080], # 分辨率,尽量选择[1920,1200], [1920,1080], [1600,1200], [1600,900], [1440,900], [1366,768], [1360,768], [1280,720]中的一个
    'scale':100, # 系统缩放，windows设置>系统>屏幕中查看，仅支持100，125，150，200
    'loadingTime':8, # 加载等待时间，即点击传送后到角色进入地图的等待时间
    'startBigMap':0, # 从那个地图开始扫荡
    'startRegion':0, # 从该地图的第几个区域开始扫荡

    # 模拟宇宙，cosmic分支暂未完成，未合并到main分支,暂为无效参数
    'cosmicNum':6, # 世界几:1-6
    'preference':4 # [存护/0，记忆/1，虚无/2，丰饶/3，寻猎/4，毁灭/5，欢愉/6]
}
vP = _variableParameters
'''需要修改的参数'''

#不可修改的一些数据，抽象出来仅为匹配分辨率
_nonModifiableCoordiates={
    'subSign':[630,1020], # 缩放地图需要点击的坐标
    'fightMarker':[0,0,20,10], # 查找战斗结束的坐标及区域,判定区域在_correct中的i == "fightMarker"分支处修改
    'interstellarChart':[1760,160], # 星际航线的坐标
    'gap':100,

    'select':[900,795], # 多个传送点在一起，二次选择的坐标
    'transmit':[1650,1000] # 传送按键的坐标
}
nMC=_nonModifiableCoordiates
'''不可修改的一些数据'''

_baseCoordinate=[0,0,0,0] 
'''窗口的基准坐标'''

bigMap=([440,600],  # 黑塔空间站
        [885,420],  # 雅利洛-Ⅵ
        [1230,820], # 仙舟⌜罗浮⌟
        [1640,440]) # 匹诺康尼
'''大地图，坐标都是相对坐标，基于窗口最左上角，大地图的点击坐标，0:黑塔空间站，1:雅利洛，2:仙州，3:匹诺康尼'''

bigMapRegionStart=([1520,465],
                   [1520,385], # 雅利洛VI，当身处残响回廊后，打开地图会默认展示后面的区域，变化后的基准坐标
                   [1520,680], # 仙舟，当身处太卜司后，打开地图会默认展示后面的区域，变化后的基准坐标
                   [1520,670]) # 匹诺康尼因为分为梦境和现实，大概率以后现实也会有战斗区域，此为梦境的第二区域的坐标
"""选择大地图内区域的基准坐标\n
0：游戏地图中第3个区域的坐标,区域点击基准坐标\n
1：雅利洛VI,当身处残响回廊后,打开地图会默认展示后面的区域,变化后的基准坐标\n
2：仙舟,当身处太卜司后,打开地图会默认展示后面的区域,变化后的基准坐标\n
3：匹诺康尼因为分为梦境和现实,大概率以后现实也会有战斗区域,此为梦境的第二区域的坐标"""

# 大地图内可战斗的区域数量，非准确数量，值为从第一个可战斗区域到最后一个可战斗区域之间的差值
bigMapRegionNum=(4,11,9,3)

# 区域内的传送点坐标
regionPoint=(
    ( # 黑塔空间站
        [840,200], # 基座舱段
        [[1010,600],[925,670],[540,600]], # 收容舱段
        [[335,620],[610,445]], # 支援舱段
        [[747,820],[890,425]] # 禁闭舱段
    ),
    ( # 雅利洛-Ⅵ
        [1120,600], # 城郊雪原 
        [[775,765],[780,340],[810,420]], # 边缘通路 
        [0,0], # 禁卫铁区 
        [[980,260],[735,880],[735,800],[705,810],[772,635]], # 残响回廊 
        [[525,755],[780,700]], # 永冬岭 
        [0,0], # 造物之柱 
        [0,0], # 旧武器实验场 
        [0,0], # 磐岩镇 
        [[740,920],[740,840],[775,720],[770,620]], # 大矿区 
        [[820,770],[810,365]], # 铆钉镇 
        [510,690] # 机械聚落
    ),
    ( # 仙舟⌜罗浮⌟
        [[910,185],[750,725],[750,690],[785,660]], # 流云渡 
        [[1040,330],[665,545],[650,705]], # 迴星港 
        [0,0], # 长乐天
        [0,0], # 金人巷
        [[450,220],[540,440],[1125,725],[558,800]], # 太卜司 
        [[560,230],[663,710],[960,300],[815,205]], # 工造司
        [[410,535],[415,490]], # 绥园
        [[610,185],[650,830],[640,500],[640,390],[940,220],[690,930]], # 丹鼎司
        [[1315,570],[340,585],[735,515],[660,585],[865,585]] # 鳞渊境
    ),
    ( # 皮诺康尼
        [[1170,224],[435,870],[325,530],[475,155]], # 筑梦边境
        [[820,440],[820,632],[780,770],[780,510]], # 稚子的梦
        [[1130,770],[1170,190],[1005,245],[590,500],[490,700],[605,285],[835,340],[650,285],[650,380]]  # 白日梦酒店(梦境)
    ))

def getStarTrain():
    '''找到星穹铁道的窗口，并调到前台聚焦'''
    startTrain = w32.FindWindow('UnityWndClass',u'崩坏：星穹铁道')
    if startTrain == 0:
        return 0
    w32.ShowWindow(startTrain,win32con.SW_NORMAL)
    w32.SetForegroundWindow(startTrain)
    time.sleep(2)
    global _baseCoordinate
    _baseCoordinate = w32.GetWindowRect(startTrain)
    print(_baseCoordinate)
    print("correct coordinates")

    def _correct():
        '''根据设置窗口分辨率缩放相应坐标，并根据获取到的窗口基准位置修改坐标'''
        #计算比例
        _ratio=[round(vP["_resolution"][0]/1920,2),round(vP["_resolution"][1]/1080,2)]
        resolution  = ( [1920,1200],[1920,1080],[1600,1200],[1600,900], [1440,900], [1366,768], [1360,768], [1280,720])
        fightMarker = (([93,1106],  [93,998],   [79,1108],  [79,838],   [72,838],   [68,719],   [68,719],   [65,675]),  # 100%系统缩放下的战斗区域检测
                       ([94,1113],  [94,1005],  [80,1115],  [80,845],   [73,845],   [69,726],   [69,726],   [65,682]),  # 125%系统缩放下的战斗区域检测
                       ([97,1120],  [97,1012],  [83,1122],  [83,852],   [76,852],   [71,733],   [71,733],   [67,690]),  # 150%系统缩放下的战斗区域检测
                       ([98,1133],  [98,1025],  [84,1135],  [84,865],   [77,865],   [73,746],   [73,746],   [69,703]))  # 200%系统缩放下的战斗区域检测)
        #修正不可修改的一些数据
        for i in nMC:
            if i == "gap": # 每个区域间的坐标差值，基准100
                nMC[i] *= _ratio[1]
            elif i == "fightMarker":
                resCorrect = False
                selectScale = 0 if vP['scale'] == 100 else 1 if vP['scale'] == 125 else 2 if vP['scale'] == 150 else 3
                for resI in range(0,len(resolution)):
                    if vP['_resolution'][0] == resolution[resI][0] and vP['_resolution'][1] == resolution[resI][1]:
                        nMC[i][0] = fightMarker[selectScale][resI][0] + _baseCoordinate[0]
                        nMC[i][1] = fightMarker[selectScale][resI][1] + _baseCoordinate[1]
                        resCorrect = True
                        break
                if resCorrect == False:
                    bias = [2 if _ratio[0]<1 else -2 if _ratio[0]!=1 else 0, 2 if _ratio[1]<1 else -2 if _ratio[1]!=1 else 0]
                    nMC[i][0] = int(nMC[i][0]* _ratio[0] + bias[0] + _baseCoordinate[0])
                    nMC[i][1] = int(nMC[i][1]* _ratio[1] + bias[1] + _baseCoordinate[1])
                    nMC[i][2] = int(nMC[i][2]* _ratio[0])+1
                    nMC[i][3] = int(nMC[i][3]* _ratio[1])+1
            else:
                nMC[i][0] = int(nMC[i][0]* _ratio[0] + _baseCoordinate[0])
                nMC[i][1] = int(nMC[i][1]* _ratio[1] + _baseCoordinate[1])

        #修正大地图坐标
        for sublist in bigMap:
            sublist[0] = int(sublist[0] * _ratio[0] + _baseCoordinate[0])
            sublist[1] = int(sublist[1] * _ratio[1] + _baseCoordinate[1])
        #修正选择大地图内区域的基准坐标
        for sublist in bigMapRegionStart:
            sublist[0] = int(sublist[0] * _ratio[0] + _baseCoordinate[0])
            sublist[1] = int(sublist[1] * _ratio[1] + _baseCoordinate[1])
        #修正区域坐标传送点
        for i, sublist in enumerate(regionPoint):
            for j, element in enumerate(sublist):
                # 如果元素是一个列表，就遍历其中的元素和索引，并根据比例修改数据
                if isinstance(element[0], list):
                    for k, item in enumerate(element):
                        regionPoint[i][j][k][0] = int(regionPoint[i][j][k][0] * _ratio[0] + _baseCoordinate[0])
                        regionPoint[i][j][k][1] = int(regionPoint[i][j][k][1] * _ratio[1] + _baseCoordinate[1])
                else:
                    regionPoint[i][j][0] = int(regionPoint[i][j][0] * _ratio[0] + _baseCoordinate[0])
                    regionPoint[i][j][1] = int(regionPoint[i][j][1] * _ratio[1] + _baseCoordinate[1])
    #调用坐标修正
    _correct()
    return 1


def action(actionSequence: tuple):
    '''地图内操作解析
    actionSequence: 需要执行的一系列行动的序列，不区分大小写\n
    其中C为左键,平A,有第二个参数(形如[c,[100,100]]),即为点击某个相对位置，\n
    'CF'为检测战斗是否结束,有第二个参数即为检测间隔,默认2s一次\n
    'QM'为退出3d小房间的操作
    'SP'为等待一段时间，必须有第二参数，为等待时长，秒
    'W''A''S''D'的组合,第二参数为运行时长,第三参数为是否行走,默认奔跑\n
    'X','Y'分别为移动横向纵向视角,非精准操作,慎用\n
    其他按键只能为单一按键,必须有第二参数,第二参数为操作后等待时间'''
    print(actionSequence)
    for actionI in actionSequence:
        print(actionI)
        if actionI[0] == 'x' or actionI[0] == 'X': #移动横向视角，一圈大概7720，非精准操纵，慎用，负数为向左转，正数为向右转
            pdi.moveRel(xOffset=actionI[1], yOffset=0, relative=True)
        elif actionI[0] == 'y' or actionI[0] == 'Y': #移动纵向视角，非精准操纵，慎用，甚至感觉没用(ˉ▽ˉ；)...
            #一圈大概7720
            pdi.moveRel(xOffset=0, yOffset=actionI[1], relative=True)
        elif actionI[0] == 'c' or actionI[0] == 'C': #左键，平A,有第二个参数(形如[c,[100,100]]),即为点击某个相对位置
            aIL = len(actionI)
            if aIL == 1:
                pa.click()
            else:
                pa.click(x=actionI[1][0]+_baseCoordinate[0],y=actionI[1][1]+_baseCoordinate[1])
            time.sleep(1)
        elif actionI[0] == 'cf' or actionI[0] == 'CF': #检测战斗是否结束

            def _checkFightEnd(interval:int=2):
                '''检测战斗是否结束
                interval: 间隔几秒检查一次，默认是2秒'''
                for i in range(2,5): #检测是否进入战斗，尝试以2s,3s,4s的间隔检查三次
                    time.sleep(i)
                    try:
                        if None == pa.locateOnScreen("data/fightMarker.png",region=(nMC['fightMarker'][0],nMC['fightMarker'][1],nMC['fightMarker'][2],nMC['fightMarker'][3]),confidence=0.9,grayscale=True):
                            print("fight start")
                            break
                    except pa.ImageNotFoundException:
                        print("fight start")
                        break
                times = 0
                while True:
                    time.sleep(interval)
                    try:
                        if None != pa.locateOnScreen("data/fightMarker.png",region=(nMC['fightMarker'][0],nMC['fightMarker'][1],nMC['fightMarker'][2],nMC['fightMarker'][3]),confidence=0.9,grayscale=True):
                            print("fight end")
                            return 1
                    except pa.ImageNotFoundException:
                        None
                    times += 1
                    if times >= 30:
                        pa.click()
                        times=0

            aIL = len(actionI)
            if aIL == 1:
                _checkFightEnd()
            else:
                _checkFightEnd(actionI[1])
        elif actionI[0] == 'caps' or actionI[0] == 'Caps': #旋转视角，将视角调整为人物朝向，会连续按两次，保证大写键的原装
            time.sleep(1)
            pa.press('capslock')
            time.sleep(0.2)
            pa.press('capslock')
            time.sleep(0.5)
        elif actionI[0] == 'qm' or actionI[0] == 'QM': #退出匹诺康尼的3D小房间地图
            time.sleep(2)
            pa.click(x=nMC['interstellarChart'][0],y=nMC['interstellarChart'][1])
            time.sleep(2)
        elif actionI[0] == 'sp' or actionI[0] == 'SP': #等待，第二个参数为等待时间
            time.sleep(actionI[1])
        elif actionI[0][0] == 'w' or actionI[0][0] == 'W' or actionI[0][0] == 'a' or actionI[0][0] == 'A' or actionI[0][0] == 's' or actionI[0][0] == 'S' or actionI[0][0] == 'd' or actionI[0][0] == 'D': #'w''a''s''d'的组合，默认奔跑，需要走路时，在操作列表增加一位，例如['s',3,1]

            # 行动 key: 行动按键; sec: 行动时长; walkFlag: 是否走路，默认False，既奔跑状态
            def _run(key, sec: float, walkFlag:bool = False):
                '''行动 key: 行动按键; 
                sec: 行动时长; 
                walkFlag: 是否走路，默认False，既奔跑状态'''
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
        else: #其他按键，必须有第二参数，第二个参数为等待时间
            time.sleep(1)
            pa.press(actionI[0])
            time.sleep(actionI[1])

    time.sleep(1)
