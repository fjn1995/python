""" Quick example code to generate some data from the SOPRA database
    从SOPRA数据库生成一些数据的快速示例代码
    材料的折射率n 消光系数k
"""
from solcore import material
import numpy as np
import matplotlib.pyplot as plt


import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']

class Material_nk():
    def __init__(self):
        self.wl = np.linspace(300, 1800, 1000)   #生成有序列表，从300到1800，划分为1000个点---x值

    def n_k_plot(self,ml1,ml2):
        """
        选择不同材料,绘制折射率n和消光系数k的对比图
        """
        self.ml1 = ml1
        self.ml2 = ml2

        # 从Sopra数据库获取Ge的n、k
        self.m_l1 = material(f'{self.ml1}', sopra=True)(T=300)
        self.m_l1_n = self.m_l1.n(self.wl*1e-9)
        self.m_l1_k = self.m_l1.k(self.wl*1e-9)
        self.m_l2 = material(f'{self.ml2}', sopra=True)(T=300)
        self.m_l2_n = self.m_l2.n(self.wl*1e-9)
        self.m_l2_k = self.m_l2.k(self.wl*1e-9)

        # 绘图__没问题
        f, (self.ax1) = plt.subplots(1,1)  #1行，1列
        self.ax1b = self.ax1.twinx()  #twinx()函数表示共享x轴
        lns1 = self.ax1.plot(self.wl, self.m_l1_n, 'b', label=f'n, {self.ml1}')
        lns2 = self.ax1b.plot(self.wl, self.m_l1_k, 'r', label=f'k, {self.ml1}')

        lns3 = self.ax1.plot(self.wl, self.m_l2_n, ls="--", color='blue', label=f'n, {self.ml2}')
        lns4 = self.ax1b.plot(self.wl, self.m_l2_k,ls="--", color='red', label=f'k, {self.ml2}')
        # 设置坐标范围
        self.ax1.set_xlim([300,1800])
        self.ax1b.set_xlim([300,1800])
        # self.ax1b.set_ylim([0, 3.8])

        # 画线
        lns = lns1+lns2+lns3+lns4
        labs = [l.get_label() for l in lns]
        self.ax1.legend(lns, labs, loc="upper right",bbox_to_anchor=(1.3,1),frameon=False) #图例放在右上，去掉边框
        # self.ax1.text(0.05, 0.9, '(n—k)', transform=self.ax1.transAxes, fontsize=12)    #添加文字说明

        self.ax1.set_xlabel("波长 (nm)")
        self.ax1.set_ylabel("折射率, n")
        self.ax1b.set_ylabel("消光系数, k")
        plt.title('{}和{}的折射率，消光系数对比图'.format(self.ml1,self.ml2),verticalalignment='top')
        plt.tight_layout()      # 紧凑布局

        plt.savefig('material_n_k_plot/{}_{}_nk.png'.format(self.ml1,self.ml2))
        plt.close()
    def material_AL_fraction(self):
        # Load AlGaAs k data for a range of compositions...

        self.AlGaAs = material("AlGaAs", sopra=True)
        self.AlGaAs_k = [self.GaAs_k]
        self.Al_fraction = np.linspace(10, 100, 10)     # AL含量百分比
        for comp in self.Al_fraction:
            self.AlGaAs_k.append(self.AlGaAs(T=300, Al=comp/100).k(self.wl*1e-9))  # 加AL的百分比
        # 绘图
        f, (self.ax2) = plt.subplots(1,1)
        self.colors = plt.cm.jet(np.linspace(0,1,len(self.Al_fraction)+1))       #颜色映射
        for i, k in enumerate(self.Al_fraction):
            self.ax2.plot(self.wl, self.AlGaAs_k[i], color=self.colors[i+1], label='{}%'.format(int(self.Al_fraction[i])))

        self.ax2.set_xlim([300, 900])
        self.ax2.set_ylim([0, 2.8])

        self.ax2.set_xlabel("波长 (nm)")
        self.ax2.set_ylabel("消光系数, k")
        self.ax2.legend(loc="upper right", frameon=False)
        self.ax2.text(0.05, 0.9, '(b)', transform=self.ax2.transAxes, fontsize=12)
        # plt.tight_layout(w_pad=4)   # 自动调整子图参数，使之填充整个图像区域

        # plt.show()

# Material_nk().material_AL_fraction()
# Material_nk().n_k_plot('GaAS','Al')
