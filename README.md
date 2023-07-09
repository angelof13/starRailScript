##叠甲声明：
####该脚本基于pyautoui制作，本质上属于模拟键鼠操作，未进行任何内存数据的读取或修改，可刷取资源的脚本说到底依然是外部辅助程序，虽然铁道这种弱联网游戏即使刷取世界资源并不会导致游戏内的经济系统膨胀或紊乱，但老米将该种脚本认定为第三方外挂也是可能的，且由于操作的规律性，<font color=red>被封号处理的可能性依然存在</font>，请自行决定是否使用，若账号被封，<font color=red>概不负责</font>
####由于该脚本并未对内存数据进行读取修改，而是模拟键鼠操作，故而在执行时，会受到电脑配置的影响，具体可能体现在：加载地图的过慢，导致程序已经开始执行图内操作，而实际上游戏里还在加载页面；跑到某个图的某个地点时，会卡顿，导致后续操作对不上，而卡地形。
####所以运行该脚本需要能够自己动手修改程序。

##准备步骤：
***
安装python，最简单的方法是去微软商店中直接安装python3.11

***
安装完毕后，*右键开始菜单* 或 *win+x*，打开 *终端(管理员)* 或 *powershell(管理员)*，输入<code>python</code>，确定能够进入python命令行，然后输入<code>exit()</code>退出python命令行

***
回到终端界面，输入<code>python -m pip install \--upgrade pip</code>，等待pip更新完毕

***
安装所需的几个模块，-i后面为pip国内镜像源

<code>pip install pyautogui -i https://pypi.tuna.tsinghua.edu.cn/simple</code>

<code>pip install pydirectinput -i https://pypi.tuna.tsinghua.edu.cn/simple</code>

<code>pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple</code>

<code>pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple</code>
***
设置星穹铁道为**1920*1080窗口化**，带队人物选择**娜塔莎**，角色置于**非基座舱段**的其他位置，**保持在可操作界面，脚本运行期间，队伍战斗不能失败**

***
一且完毕后，即可使用**管理员权限**(pyautogui非管理员无法进行)运行脚本starRail.py，推荐VScode + code runner插件运行

##文件说明 & 授人以渔
<code>starRail.py</code> 为点击大地图，及选择区域的代码，后续新增大地图或区域时，修改该文件及<code>configuration.py</code>中的坐标。该文件中的main函数为脚本启动函数

<code>configuration.py</code> 为一些参数，包括需要点击的坐标，设置地图加载等待时间，寻找到游戏窗口函数，和检测战斗是否结束

<code>pathFinding.py</code> 为区域内传送点点击操作及人物行动代码，该文件中的main函数为区域内操作Debug的函数，<code>_clickRegion()</code>为点击传送点的函数，<code>_action()</code>操作解析函数，x为横向视角转动，y为纵向视角转动，这两个后面跟的数值为转动角度，非精确操作，慎用，c为左键单击，地图内即为攻击，cf为检测战斗是否结束，后面跟的数值为检测间隔单位秒，f为f键，使用场景为进入画中，后面跟的数值为等待时间，其他按键操作，基本为'w''a''s''d'的组合，后面跟的第一个数值为操作时间，第二个若有任意数值，则为走路进行，没有第二个数值，则为跑步进行