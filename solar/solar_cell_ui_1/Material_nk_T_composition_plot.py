""" Quick example code to generate some data from the SOPRA database
    从SOPRA数据库生成一些数据的快速示例代码
    材料的折射率n 消光系数k
"""
from solcore import material
import numpy as np
import matplotlib.pyplot as plt


import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
# mpl.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
# plt.rcParams['axes.unicode_minus']=False


class Material_sopra():
    """sopra材料库绘图"""
    def __init__(self):
        self.wl = np.linspace(100, 1800, 1000)   #生成有序列表，从300到1800，划分为1000个点---x值

    def n_k_plot(self,ml1,ml2):
        """
        选择不同材料,绘制折射率n和消光系数k的对比图
        """
        self.ml1 = ml1
        self.ml2 = ml2

        # 从Sopra数据库获取材料的n、k
        self.m_l1 = material(f'{self.ml1}', sopra=True)(T=300)
        self.m_l1_n = self.m_l1.n(self.wl*1e-9)
        self.m_l1_k = self.m_l1.k(self.wl*1e-9)
        self.m_l2 = material(f'{self.ml2}', sopra=True)(T=300)
        self.m_l2_n = self.m_l2.n(self.wl*1e-9)
        self.m_l2_k = self.m_l2.k(self.wl*1e-9)

        # 绘图
        f, (self.ax1) = plt.subplots(1,1)  #1行，1列
        self.ax1b = self.ax1.twinx()  #twinx()函数表示共享x轴
        lns1 = self.ax1.plot(self.wl, self.m_l1_n, 'b', label=f'n, {self.ml1}')
        lns2 = self.ax1b.plot(self.wl, self.m_l1_k, 'r', label=f'k, {self.ml1}')

        lns3 = self.ax1.plot(self.wl, self.m_l2_n, ls="--", color='blue', label=f'n, {self.ml2}')
        lns4 = self.ax1b.plot(self.wl, self.m_l2_k,ls="--", color='red', label=f'k, {self.ml2}')
        # 设置坐标范围
        self.ax1.set_xlim([200,1800])
        self.ax1b.set_xlim([200,1800])
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
        # 如果后期需要方法缩小--可以更新dpi
        plt.savefig('material_n_k_plot/{}_{}_nk.png'.format(self.ml1,self.ml2),dpi=120,facecolor='#FAFFF0')
        plt.close()

    def nk_T_plot(self,ml_T,ml_symbol,current_T):
        """选择不同材料的不同温度,绘制折射率n和消光系数k的对比图"""
        self.ml_T = ml_T
        self.ml_symbol = ml_symbol
        self.current_T = current_T
        # 从Sopra数据库获取材料的n、k
        self.m_l_T = material(f'{self.ml_T}', sopra=True)(T=300)
        self.m_l_T_n = self.m_l_T.n(self.wl * 1e-9)
        self.m_l_T_k = self.m_l_T.k(self.wl * 1e-9)

        # 绘图
        f, (self.ax1) = plt.subplots(1, 1)  # 1行，1列
        self.ax1b = self.ax1.twinx()  # twinx()函数表示共享x轴
        lns1 = self.ax1.plot(self.wl, self.m_l_T_n, 'b', label=f'n, {self.ml_symbol}')
        lns2 = self.ax1b.plot(self.wl, self.m_l_T_k, 'r', label=f'k, {self.ml_symbol}')

        # 设置坐标范围
        self.ax1.set_xlim([200, 1200])
        self.ax1b.set_xlim([200, 1200])
        # self.ax1b.set_ylim([0, 3.8])

        # 画线
        lns = lns1 + lns2
        labs = [l.get_label() for l in lns]
        self.ax1.legend(lns, labs, loc="upper right", bbox_to_anchor=(1.3, 1), frameon=False)  # 图例放在右上，去掉边框
        # self.ax1.text(0.05, 0.9, '(n—k)', transform=self.ax1.transAxes, fontsize=12)    #添加文字说明

        self.ax1.set_xlabel("波长 (nm)")
        self.ax1.set_ylabel("折射率, n")
        self.ax1b.set_ylabel("消光系数, k")
        plt.title('材料{}在{}的折射率，消光系数'.format(self.ml_symbol, self.current_T), verticalalignment='top')
        plt.tight_layout()  # 紧凑布局

        plt.savefig('material_n_k_plot/{}_{}_nk.png'.format(self.ml_symbol, self.current_T), dpi=120, facecolor='#FAFFF0')
        plt.close()

    def nk_compos(self,ml_compos,current_compos,current_compos_range):
        # 复合材料，可变材料，材料可变百分比
        # self.ml_compos = ml_compos
        # self.current_compos = current_compos
        # print(current_compos)

        self.compos = material(f'{ml_compos}', sopra=True)      # 复合物种类
        self.compos_k = []
        self.compos_n = []

        # self.compos_ranges = np.linspace(f'{self.current_compos_range}', 4)     # 混合物含量百分比
        compos_ranges = eval('np.linspace({}, 5)'.format(current_compos_range))     # 混合物含量百分比
        # print(compos_ranges)

        for comp in compos_ranges:
            current_ml_compos = '{}={}'.format(current_compos,comp/100)
            # print(type(current_ml_compos))
            ml_compos_k=eval('self.compos(T=300,{}).k(self.wl*1e-9)'.format(current_ml_compos))     # k值数据列表
            ml_compos_n=eval('self.compos(T=300,{}).n(self.wl*1e-9)'.format(current_ml_compos))     # n值数据列表

            self.compos_k.append(ml_compos_k)
            self.compos_n.append(ml_compos_n)

        # 绘图
        f, (self.ax2) = plt.subplots(1,1)
        self.ax2b = self.ax2.twinx()  # twinx()函数表示共享x轴
        self.colors = plt.cm.jet(np.linspace(0,1,len(compos_ranges)*2))       #颜色映射
        for i, k in enumerate(compos_ranges * 2):
            self.ax2.plot(self.wl, self.compos_n[i], color=self.colors[i], label='{}%'.format(int(compos_ranges[i])))
            self.ax2b.plot(self.wl, self.compos_k[i], color=self.colors[i*2],ls='--',label='{}%'.format(int(compos_ranges[i])))

        # self.ax2.set_xlim([200, 1200])
        # self.ax2.set_ylim([0, 2.8])
        self.ax2.set_xlabel("波长 (nm)")
        self.ax2.set_ylabel("折射率, n")
        self.ax2b.set_ylabel("消光系数, k")

        self.ax2.legend(loc="upper right", bbox_to_anchor=(1.3, 0.6),frameon=False)
        self.ax2b.legend(loc="upper right",bbox_to_anchor=(1.3, 1), frameon=False)
        plt.title('材料{}成分{}不同时的折射率，消光系数'.format(ml_compos,current_compos), verticalalignment='top')
        # plt.subplots_adjust(left=0, bottom=0, right=0.1, top=1,hspace = 0.1, wspace = 0.1)
        # self.ax2.text(0.05, 0.9, '(b)', transform=self.ax2.transAxes, fontsize=12)
        plt.tight_layout()   # 自动调整子图参数，使之填充整个图像区域
        # plt.show()
        plt.savefig('material_n_k_plot/{}_{}_nk_compos.png'.format(ml_compos, current_compos), dpi=120, facecolor='#FAFFF0')
        plt.close()


# Material_sopra().nk_compos('AlGaAs','Al','0,100')