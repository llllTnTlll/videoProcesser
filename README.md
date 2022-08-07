# videoProcessing
本项目是为四氧化三铁水合物磁场扰动编写的灰度值分析程序（简介项目）
## 主要功能
- 借助OpenCV实现对视频特定区域的灰度值追踪
- 借助Matplotlib实现灰度折线图绘制
- 将灰度值检测结果以.txt的形式保存至本地
## 依赖环境
我们推荐您在python 3.8环境下以下列包运行本应用程序：
- colorama==0.4.4
- matplotlib==3.2.2
- numpy==1.22.2
- opencv_python==4.5.5.62
## 关键参数配置
您可以从编译器直接运行或是通过命令提示符的方式从终端运行本程序，使用终端运行时关键参数如下：<br />
- _--path 待分析视频的存储路径_
- _--save 是否将检测结果以.txt文件保存到result文件夹中_
- _--left_top 兴趣区域左上角坐标点位置_
- _--right-bottom 兴趣区域右下角坐标点位置_
- _--color 兴趣区域矩形框BGR颜色_
需要注意的是，OpenCV为左上角坐标系，即左上角第一个像素为（0，0）点
## 我是新手
本章将从一个初学者的角度讲述关于环境配置及使用过程的注意事项
### 环境配置
python程序的运行依赖于解释器，向系统解释器中其他项目不需要的包会导致解释器臃肿，一般来说，我们通过conda进行python虚拟环境的创建和管理。
<br /><br />安装conda后，在Anaconda Prompt控制台使用如下命令创建名为env的python3.8虚拟环境：
```commandline
conda create -n env python==3.7
```
激活刚刚创建的虚拟环境：
```commandline
activate env
```
使用requirements.txt还原依赖环境,其中最后一个参数为当前项目下的requirements.txt路径：
```commandline
pip install -r C:\...\requirements.txt
```
### 在Pycharm中运行程序
使用pycharm打开本项目，在菜单中依次选择:<br />
File-->Settings-->Project-->Python Interpreter