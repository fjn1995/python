import sys
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QDate,QTime,QDateTime,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,\
    QComboBox,QDateTimeEdit,QMainWindow,QAction,QMessageBox,QFileDialog,QTabWidget
import os
import sys
import re
from time import sleep
import threading
# from examples.solar_cell_ui import Material_sopra     #相对路径导入
from Material_nk_T_composition_plot import Material_sopra
# 同级函数导入
from solcore_db import ML_DB

ml_db = ML_DB()

class UI_N_K(QTabWidget):
    """sopra材料库界面"""
    def __init__(self):
        super(UI_N_K, self).__init__()
        self.title = self.setWindowTitle('Optical Properties(sopra database)')
        self.resize(800,750)
        # 标签页
        self.t1 = QWidget()
        self.t2 = QWidget()
        self.t3 = QWidget()
        # 设置标签页的名字
        self.addTab(self.t1,'不同材料n-k对比')
        self.addTab(self.t2,'温度变化')
        self.addTab(self.t3,'成分变化')

        self.t1_init()
        self.t2_init()
        self.t3_init()

    def t1_init(self):
        # 不同材料的n—k对比（默认温度300k）--界面布局
        self.l1_0 = QLabel('>> 不同材料的n-k对比（默认温度300k） ------',self)
        self.l1_0.setStyleSheet("background-color: #CCCCCC")
        self.l1_0.setScaledContents(True)
        self.l1_0.setFixedSize(350,30)
        self.l1_1 = QLabel('材料一：',self)
        self.l1_2 = QLabel('材料二：',self)
        self.l1_3 = QLabel('波长范围',self)
        self.l1_3.setScaledContents(True)
        self.l1_4 = QLabel('说明',self)
        self.l1_5 = QComboBox()
        self.l1_6 = QComboBox()
        self.l1_7 = QLabel(self)
        self.l1_8 = QLabel(self)
        self.l1_9 = QLabel(self)     #放置图形

        self.h_l1 = QHBoxLayout()
        self.h_l2 = QHBoxLayout()
        self.h_l3 = QHBoxLayout()
        self.h_l4 = QHBoxLayout()
        self.v_l1 = QVBoxLayout()

        self.h_l1.addWidget(self.l1_1)
        self.h_l1.addWidget(self.l1_5)
        self.h_l2.addWidget(self.l1_2)
        self.h_l2.addWidget(self.l1_6)
        self.h_l3.addWidget(self.l1_3)
        self.h_l3.addWidget(self.l1_7)
        self.h_l4.addWidget(self.l1_4)
        self.h_l4.addWidget(self.l1_8)

        self.v_l1.addWidget(self.l1_0)
        self.v_l1.addLayout(self.h_l1)
        self.v_l1.addLayout(self.h_l2)
        self.v_l1.addLayout(self.h_l3)
        self.v_l1.addLayout(self.h_l4)
        self.v_l1.addStretch()
        self.v_l1.addWidget(self.l1_9)

        self.t1.setLayout(self.v_l1)

        self.combo_1()
    def t2_init(self):
        # 与温度相关的材料--界面布局
        self.l2_0 = QLabel('>> 与温度相关的材料 ------', self)
        self.l2_0.setStyleSheet("background-color: #CCCCCC")
        self.l2_0.setFixedSize(350, 30)
        self.l2_0.setScaledContents(True)
        self.l2_1 = QLabel('材料：', self)
        self.l2_2 = QLabel('温度：', self)
        self.l2_3 = QLabel('波长范围', self)
        self.l2_4 = QComboBox()         #材料
        self.l2_5 = QComboBox()         #温度
        self.l2_6 = QLabel(self)
        self.l2_7 = QLabel(self)  # 放置图形

        self.h_l5 = QHBoxLayout()
        self.h_l6 = QHBoxLayout()
        self.h_l7 = QHBoxLayout()
        self.v_l2 = QVBoxLayout()

        self.h_l5.addWidget(self.l2_1)
        self.h_l5.addWidget(self.l2_4)
        self.h_l6.addWidget(self.l2_2)
        self.h_l6.addWidget(self.l2_5)
        self.h_l7.addWidget(self.l2_3)
        self.h_l7.addWidget(self.l2_6)

        self.v_l2.addWidget(self.l2_0)
        self.v_l2.addLayout(self.h_l5)
        self.v_l2.addLayout(self.h_l6)
        self.v_l2.addLayout(self.h_l7)
        self.v_l2.addStretch()
        self.v_l2.addWidget(self.l2_7)

        self.t2.setLayout(self.v_l2)
        self.combo_2()
    def t3_init(self):
        # 材料成分变化--界面布局
        self.l3_0 = QLabel('>> 材料成分变化 ------', self)
        self.l3_0.setStyleSheet("background-color: #CCCCCC")
        self.l3_0.setFixedSize(350, 30)
        self.l3_0.setScaledContents(True)
        self.l3_1 = QLabel('材料：', self)
        self.l3_2 = QLabel('变化成分：', self)     # 材料可变成分
        self.l3_3 = QLabel('波长范围', self)
        self.l3_4 = QLabel('说明', self)
        self.l3_5 = QComboBox()         # 不同材料
        self.l3_6 = QLabel(self)        # 可变材料
        self.l3_7 = QLabel(self)        # 波长范围
        self.l3_8 = QLabel(self)        # 说明
        self.l3_9 = QLabel(self)  # 放置图形

        self.h_l8 = QHBoxLayout()
        self.h_l9 = QHBoxLayout()
        self.h_l10 = QHBoxLayout()
        self.h_l11 = QHBoxLayout()
        self.v_l3 = QVBoxLayout()

        self.h_l8.addWidget(self.l3_1)
        self.h_l8.addWidget(self.l3_5)
        self.h_l9.addWidget(self.l3_2)
        self.h_l9.addWidget(self.l3_6)
        self.h_l10.addWidget(self.l3_3)
        self.h_l10.addWidget(self.l3_7)
        self.h_l11.addWidget(self.l3_4)
        self.h_l11.addWidget(self.l3_8)

        self.v_l3.addWidget(self.l3_0)
        self.v_l3.addLayout(self.h_l8)
        self.v_l3.addLayout(self.h_l9)
        self.v_l3.addLayout(self.h_l10)
        self.v_l3.addLayout(self.h_l11)
        self.v_l3.addStretch()
        self.v_l3.addWidget(self.l3_9)
        self.t3.setLayout(self.v_l3)

        self.com_3()
    def combo_1(self):
        # 1 选择框内容
        self.l1_5.addItems(ml_db.ml_nk_data()[0])
        self.l1_5.setCurrentText('GaAs(GAAS)')
        self.l1_5.currentTextChanged.connect(self.res_1)
        self.l1_6.addItems(ml_db.ml_nk_data()[0])
        self.l1_6.setCurrentText('Ge(GE)')
        self.l1_6.currentTextChanged.connect(self.res_1)
        self.res_1()
    def combo_2(self):
        # 2
        self.l2_4.addItems(ml_db.ml_nk_T_data()[0])
        self.l2_4.setCurrentText('GaAs')
        self.l2_4.currentTextChanged.connect(self.res_2)
        # self.l2_5.currentTextChanged.connect(self.res_2)    #不可同时使用currentTextChanged
        self.l2_5.activated.connect(self.update_image_nk_T)
        self.res_2()

    def com_3(self):
        # 3
        self.l3_5.addItems(ml_db.ml_nk_composition_data()[0])
        self.l3_5.setCurrentText('AlGaAs')
        self.l3_5.currentTextChanged.connect(self.res_3)
        self.res_3()
    def res_1(self):
        # 材料改变响应函数
        self.ml_index_1 = ml_db.ml_nk_data()[0].index(f'{self.l1_5.currentText()}')
        self.ml_index_2 = ml_db.ml_nk_data()[0].index(f'{self.l1_6.currentText()}')
        self.current_range_1 = ml_db.ml_nk_data()[1][self.ml_index_1]
        self.current_range_2 = ml_db.ml_nk_data()[1][self.ml_index_2]
        self.current_info_1 = ml_db.ml_nk_data()[2][self.ml_index_1]
        self.current_info_2 = ml_db.ml_nk_data()[2][self.ml_index_2]
        self.l1_7.setText('{}\n{}'.format(self.current_range_1, self.current_range_2))
        self.l1_8.setText('材料一：{}\n材料二：{}'.format(self.current_info_1, self.current_info_2))

        self.update_image_nk()

    def res_2(self):
        # 温度改变响应函数
        self.current_l2_4 = self.l2_4.currentText()     # 当前材料
        self.ml_T_symbols = ml_db.ml_nk_T_data()[3]        # 材料所在列表
        self.ml_T_index = [i for i,x in enumerate(self.ml_T_symbols) if x ==self.current_l2_4]  # 相同材料索引
        self.ml_T_infos = ml_db.ml_nk_T_data()[2]   # 温度所在列表
        self.ml_T_range = ml_db.ml_nk_T_data()[1]   # 波长列表

        self.current_T_list = []
        for self.i in self.ml_T_index:
            self.current_T = re.findall(r"\d+\.?\d*",self.ml_T_infos[self.i])    # 只保留数值
            self.current_T_list.append(f'{self.current_T[0]} ℃')       #获取当前材料温度
        self.l2_5.clear()   # 清空原有选项
        self.l2_5.addItems(self.current_T_list)  # 添加温度项目
        self.l2_6.setText(self.ml_T_range[self.i])  # 添加波长
        self.update_image_nk_T()

    def res_3(self):
        # 成分改变响应
        self.current_l3_5 = self.l3_5.currentText()
        self.compos_index = ml_db.ml_nk_composition_data()[0].index(self.current_l3_5)
        self.l3_6.setText(ml_db.ml_nk_composition_data()[1][self.compos_index])
        self.l3_7.setText(ml_db.ml_nk_composition_data()[2][self.compos_index])
        self.l3_8.setText(ml_db.ml_nk_composition_data()[3][self.compos_index])
        self.update_image_nk_compos()

    def update_image_nk(self):
        """更新默认温度300k的不同材料的折射率，消光系数的图片"""
        self.current_l1_5 = self.l1_5.currentText()     # 材料一
        self.current_l1_6 = self.l1_6.currentText()     # 材料二
        self.current_ml1 = ml_db.ml_nk_data()[3][self.ml_index_1]
        self.current_ml2 = ml_db.ml_nk_data()[3][self.ml_index_2]

        if self.current_l1_5 == self.current_l1_6:
            QMessageBox.critical(self,'注意！','请选择不同的材料！',QMessageBox.Ok)
        else:
            eval('Material_sopra().n_k_plot("{}","{}")'.format(self.current_ml1,self.current_ml2))
            self.l1_9.setPixmap(QPixmap('material_n_k_plot/{}_{}_nk.png'.format(self.current_ml1,self.current_ml2)))
            self.l1_9.setScaledContents(True)

    def update_image_nk_T(self):
        """更新与温度相关的材料的折射率，消光系数的图片"""
        self.current_l2_4 = self.l2_4.currentText()     # 当前材料
        self.current_l2_5 = self.l2_5.currentText()     #当前温度
        index_T =[i for i,x in enumerate(self.current_T_list) if x == self.current_l2_5]    # 获取温度索引值

        ml_index = self.ml_T_index[index_T[0]]      # 获取材料所在位置索引值
        self.current_ml_T = ml_db.ml_nk_T_data()[4][ml_index]   #获取当前温度对应的材料

        eval('Material_sopra().nk_T_plot("{}","{}","{}")'.format(self.current_ml_T,self.current_l2_4,self.current_l2_5))
        self.l2_7.setPixmap(QPixmap('material_n_k_plot/{}_{}_nk.png'.format(self.current_l2_4,self.current_l2_5)))
        self.l2_7.setScaledContents(True)

    def update_image_nk_compos(self):
        self.current_l3_5 = self.l3_5.currentText()     # 材料
        self.current_l3_6 = self.l3_6.text()    # 可变成分
        self.current_compos = ml_db.ml_nk_composition_data()[4][self.compos_index]
        self.current_compos_range = ','.join(self.current_compos.split())     # 变化范围

        eval('Material_sopra().nk_compos("{}","{}","{}")'.format(self.current_l3_5,self.current_l3_6,self.current_compos_range))
        self.l3_9.setPixmap(QPixmap('material_n_k_plot/{}_{}_nk_compos.png'.format(self.current_l3_5,self.current_l3_6)))
        self.l3_9.setScaledContents(True)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     m_w = UI_N_K()
#     m_w.show()
#     sys.exit(app.exec_())

