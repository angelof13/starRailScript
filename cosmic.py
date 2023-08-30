from configuration import time, pa, action, getStarTrain
import configuration as cfg
import cv2
import math
import numpy as np

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
        time.sleep(3)
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
        #action(aSequence)
    return 0


def linkStart(times:int=34):
    intoCosmicSimulator()
    cosmicSimulatorAction()
    return 0

#该文件的main函数为区域内Debug使用
if __name__ == '__main__':
    def getpos(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN and param == 1:
            print(map_HSV[y,x])
        elif event == cv2.EVENT_LBUTTONDOWN and param == 2:
            print(map_gray[y,x])
    #if 0 == getStarTrain():
    #    print("Not found game Window")
    #    exit()
    #linkStart(times=1)


    #temp = pa.screenshot("data/cosmic/temp.png",region=(56+cfg.bC[0],96+cfg.bC[1],187,187)) # 533 941 1349
    temp = cv2.imread("data/cosmic/temp.png",cv2.IMREAD_COLOR)
    mask = np.zeros((187,187),dtype=np.uint8)
    cv2.circle(mask, (94,94),93,(255,255,255),-1)
    map_image = cv2.copyTo(temp,mask)
    map_image[np.where(mask == 0)] = (255,255,255) #扣出地图，对地图外填充白色

    #寻找角色图形，识别角色朝向
    angle=0
    map_HSV = cv2.cvtColor(map_image,cv2.COLOR_RGB2HSV)
    lower_user_color = np.array([20,200,240])
    upper_user_color = np.array([30,255,255])
    user_image = cv2.inRange(map_HSV, lower_user_color,upper_user_color)
    cv2.imshow("mapHSV",map_HSV)
    cv2.setMouseCallback("mapHSV",getpos,1)
    # 轮廓检测，找到图像中的轮廓
    contours, _ = cv2.findContours(user_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 获取三角形的朝向角度
    for contour in contours:
        # 计算最小外接矩形
        rect = cv2.minAreaRect(contour)
        # 获取矩形的旋转角度
        angle = int(rect[-1])
        # 打印角度
    print("angle:", angle)


    #寻找活动区域
    map_gray = cv2.cvtColor(map_image,cv2.COLOR_RGB2GRAY)
    cv2.imshow("gray",map_gray)
    cv2.setMouseCallback("gray",getpos,2)
    activeArea1 = cv2.inRange(map_gray,50,70) # 黑色
    activeArea2 = cv2.inRange(map_gray,155,165) # 桥，浅色
    activeArea3 = cv2.inRange(map_gray,170,190) # 角色视野扫过桥，更浅色
    kernel = np.ones((3, 3), np.uint8)  # 定义操作的核大小
    user_temp = cv2.dilate(user_image, kernel, iterations=7) # 进行角色像素的膨胀操作，便于路径寻找
    activeArea = cv2.bitwise_or(user_temp,cv2.bitwise_or(activeArea3,cv2.bitwise_or(activeArea1,activeArea2)))

    # 使用连通区域分析找到白色块
    _, labels, stats, _ = cv2.connectedComponentsWithStats(activeArea)
    # 设置阈值，保留大于特定值的白色块
    threshold_area = 700  # 设置特定值为700像素
    activeArea = np.zeros_like(activeArea)
    for label, stat in enumerate(stats[1:], start=1):
        if stat[4] > threshold_area:
            activeArea[labels == label] = 255
    activeArea = cv2.morphologyEx(activeArea, cv2.MORPH_CLOSE, kernel,iterations=3) #收缩

    cv2.imshow("active",activeArea)
    center=[94,94]
    redius=92
    endTempArr=[0,0]
    endPoint=[0,0]
    cumulate=0
    len=0
    for i in range(0,361):
        x=int(center[0]+redius*math.sin(i))
        y=int(center[1]+redius*math.cos(i))
        if 0 != activeArea[y][x]:
            endTempArr[0]+=x
            endTempArr[1]+=y
            len+=1
        elif 0 == activeArea[y][x] and cumulate < len:
            endPoint[0]=int(endTempArr[0]/len)
            endPoint[1]=int(endTempArr[1]/len)
            cumulate = len
            len=0
            endTempArr[0]=0
            endTempArr[1]=0
    

    cv2.waitKey(20000)
    cv2.destroyAllWindows()