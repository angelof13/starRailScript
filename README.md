## 说明 ＆ 叠甲声明：
* 该脚本是基于pyautoui制作的**星穹铁道自动化锄大地**脚本，本质上属于模拟键鼠操作，未进行任何内存数据的读取或修改
* 虽然星穹铁道这种弱联网游戏即使刷取世界资源并不会导致游戏内的经济系统膨胀或紊乱，但米忽悠将该种脚本认定为第三方外挂也是可能的，且由于操作的规律性，**<font color=red>被封号处理的可能性依然存在</font>**，请自行决定是否使用，若账号被封，**<font color=red>概不负责</font>**
* 由于该脚本并未对内存数据进行读取修改，而是模拟键鼠操作，故而在执行时，会受到电脑配置的影响，具体体现在可能出现一下情况：
    1. 加载地图的过慢，导致程序已经开始执行图内操作，而实际上游戏里还在加载页面
    2. 跑到某个图的某个地点时，会卡顿，导致后续操作对不上，而卡地形
    3. 地图界面加载时卡(没错，就是多级地图切换依据电脑配置有时会卡住)，导致没能点到传送 (←该问题现以额外增加地图点击传送点，等待点击传送的时间，很少能碰到了)
* **所以运行该脚本需要能够自己动手修改程序。**

## 准备步骤：
***
安装python：最简单的方法是去微软商店中直接安装python3

***
安装完毕后，***右键开始菜单*** 或 ***win+x***，打开 ***终端(管理员)*** 或 ***powershell(管理员)*** ，输入`python`，确定能够进入python命令行，然后输入`exit()`，退出python命令行，回到终端界面

***
输入`python -m pip install --upgrade pip`，等待pip更新完毕

***
安装所需的几个模块，-i后面为pip国内镜像源

`pip install pyautogui -i https://pypi.tuna.tsinghua.edu.cn/simple`

`pip install pydirectinput -i https://pypi.tuna.tsinghua.edu.cn/simple`

`pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple`

`pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple`
***
设置星穹铁道为**1920*1080窗口化**(已不强制需求)，其他分辨率请在`configuration.py`中，修改![修改分辨率](data/README/resolution.png)
带队人物选择**娜塔莎**，角色置于***非* 基座舱段**的其他位置，**保持在可操作界面**，脚本运行期间，队伍战斗最好别失败，若失败则该区域后续基本无法进行，只能等待脚本运行到下一区域继续

***
一且完毕后，即可使用**管理员权限**(pyautogui非管理员无法进行)运行`starRail.py`，推荐VScode + code runner插件运行

## 文件说明 & 授人以渔
***
>星穹铁道1.3版本

跟随1.3版本更新
米桑，你怎么这么爱在地图中间加地图，很有趣嘛:D
* `starRail.py`:
    * 鉴于亲爱的米桑就是喜欢在几个地图中间加地图，增加了DEBUG的判断，用于只去点击区域地图，而不进行区域内操作
    * 修改了`clickRegion()`方法中的细节，使得仙舟增加金人巷后依然能正确运行
* `pathFinding.py`：
    * 已增加金人巷（直接返回）
    * 因增加额外突破材料本，工造司和鳞渊境的怪物有些许变动，已更新行为逻辑
* `configuration.py`:
    * 修正仙舟的区域数量
    * 因PC端键鼠操作默认隐藏了底部提示，故修改了战斗检测的判断区域
    * 在`_checkFightEnd()`中增加判断，如果长时间无法检测到战斗结束，那么将点击一次屏幕，用处：战斗失败时，能继续清扫剩余地图



***
>星穹铁道1.2版本

跟随1.2版本更新
* `starRail.py`:
    * 修复`仙舟`因增加区域而导致的选择区域的位置错误问题
    * 将`selectRegion()`的调用从`clickRegion()`方法中上提到了`script()`中
* `pathFinding.py`：
    * 已增加丹鼎司，鳞渊境的行动方案
    * 将其中的`_action()`方法和`_run()`方法剥离到了`configuration.py`中
    * 将`_clickRegion()`更名为`_clickTransmitPoint()`,并将其和`_region*()`方法转为`selectRegion()`的内部函数
    * `selectRegion()`和`_region*()`增加参数`node`，能够在Debug的时候，直接输入，选择要Debug的节点，不用像先前修改`for i in range()`中的参数
* `configuration.py`:
    * 增加其他分辨率的支持
    * 将`_checkFightEnd()`和`_run()`方法转为`action()`的内部函数，修改战斗检测判断为右下角区域的轮盘是否存在(1.3版本已更改)
    * 增加`_correct()`方法，当设置分辨率非`1920*1080`时，启动脚本时调用该函数，根据设置的分辨率按比例调整相应坐标

此次修改后，若窗口设置非`1920*1080窗口化`，需要在`configuration.py`中修改`_variableParameters的_resolution`字典值，设置为当前使用的窗口化大小
* ![修改分辨率](data/README/resolution.png)



***
>星穹铁道1.0版本

`starRail.py` 为点击大地图，及选择区域的代码，后续新增大地图或区域时，修改该文件及`configuration.py`中的坐标。该文件中的main函数为脚本启动函数

`configuration.py` 为一些参数，包括需要点击的坐标，设置地图加载等待时间，寻找到游戏窗口函数，和检测战斗是否结束

`pathFinding.py` 为区域内传送点点击操作及人物行动代码，该文件中的main函数为区域内操作Debug的函数，`_clickRegion()`为点击传送点的函数，`_action()`操作解析函数，x为横向视角转动，y为纵向视角转动，这两个后面跟的数值为转动角度，非精确操作，慎用，c为左键单击，地图内即为攻击，cf为检测战斗是否结束，后面跟的数值为检测间隔单位秒，f为f键，使用场景为进入画中，后面跟的数值为等待时间，其他按键操作，基本为'w''a''s''d'的组合，后面跟的第一个数值为操作时间，第二个若有任意数值，则为走路进行，没有第二个数值，则为跑步进行