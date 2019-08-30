
''' 对 获取的数据进行数据分析，以及可视化 '''
import matplotlib.pyplot as plt
import pandas as pd
import os
from pylab import mpl

# 中文字体设置
# font = mpl.font_manager.FontProperties(fname='../zhaozi.ttf', size=14)  # 自定义字体
plt.rcParams['font.sans-serif']=['Simhei']
# 数据读取
data = pd.read_csv('boxoffice.csv', sep=',', encoding='utf8') # 读取数据
title = data.columns.tolist()

# 设定图表属性
plt.figure(figsize=(22, 12))
plt.xticks() # 横坐标
plt.xlabel("", fontsize=14) #X轴标签
plt.ylabel("票房（单位/万）", fontsize=20)  #Y轴标签

''' 绘制 九宫格， 展示变化趋势 '''
# 对 boxoffice 数据进行遍历
for i in range(9):
    plt.subplot(3, 3, i+1)
    y = data[title[i]].dropna().tolist()
    x = [i for i in range(len(y))]
    plt.title(title[i], fontsize=20) #图标题
    plt.plot(x, y)   #绘图
#plt.savefig(r'boxoffice.png', dpi=300) #指定分辨率保存  
plt.show()

''' 通过 变化趋势分析 ，进行数据拟合 '''
import numpy as np
#多项式拟合
def draw_fit(data):
    x = np.array(range(len(data)))
    z = np.poly1d(np.polyfit(x, data, 10))
    plt.plot(x, z(x), 'r-')
    return z

plt.figure(figsize=(22, 12))

func_fits = []
for i in range(9):
    plt.subplot(3, 3, i+1)
    y = data[title[i]].dropna().tolist()
    x = [i for i in range(len(y))]
    plt.title(title[i], fontsize=20) #图标题
    plt.plot(x, y)   #绘图
    z = draw_fit(y)  #绘制拟合曲线
    func_fits.append(z)
#plt.savefig(r'result.png', dpi=300) #指定分辨率保存
plt.show()

''' 最后，对哪吒总票房进行预估 '''
from scipy.optimize import leastsq
z = func_fits[1]
def func(x, p):
    A, k = p
    return A * z(x)

def residuals(p, y, x):
    #实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
    return y - func(x, p)

# 数据读取
data_nz = pd.read_csv('哪吒.csv', sep=',', encoding='utf8') # 读取数据
title = data_nz.columns.tolist()
y2 = data_nz[title[0]].dropna().tolist()
x2 = np.array(range(len(y2)))

p0 = [1, 1] # 第一次猜测的函数拟合参数
plsq = leastsq(residuals, p0, args=(y2, x2))

print("拟合参数", plsq[0]) # 实验数据拟合后的参数

x3 = np.array(range(60))

plt.figure(figsize=(8, 6))
plt.xticks() # 横坐标
plt.xlabel("", fontsize=14) #X轴标签
plt.ylabel("票房（单位/万）", fontsize=20)  #Y轴标签

plt.title(title[0], fontsize=20) #图标题

plt.plot(x2, y2)
y3 = func(x3, plsq[0])
plt.plot(x3, y3, 'r-')
plt.show()

print('总票房预估：%.f 万' % np.sum(y3))





