import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QDate,QTime,QDateTime,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,\
    QComboBox,QDateTimeEdit,QMainWindow,QAction,QMessageBox,QFileDialog
from Light_sources_plot import L_S_Plot
import os

class UI_L_S(QWidget):
    """不同光源界面"""
    def __init__(self):
        super(UI_L_S, self).__init__()
        self.title = self.setWindowTitle('Light Sources')
        # self.setFixedSize(850,700)      #固定窗口大小

        self.place_list = ['武汉','佛山','...']
        self.humidity_list = ['高','中','低']
        self.light_dicts = {'激光':'gauss','黑体':'bb','AM0':'am0','AM1.5g':'am15g',
                            'Spectral':'spectral','All_Light_Sources':'all'}

        self.label1 = QLabel('请输入参数',self)
        self.label1.resize(300,300)
        self.label1.setAlignment(Qt.AlignCenter)

        self.label2 = QLabel('当前参数',self)
        # self.label2.setAlignment(Qt.AlignCenter)      #居中
        self.c1 = QComboBox()   #地点
        self.c2 = QDateTimeEdit(QDateTime.currentDateTime(),self)   #日期

        self.c2.setDisplayFormat('yyyy-MM-dd HH')
        self.c3 = QComboBox()   #湿度
        self.c4 = QComboBox()   #光源

        self.b1 = QPushButton('Start',self)
        self.b2 = QPushButton('Reset',self)

        self.b1.clicked.connect(self.start_stop)
        self.b2.clicked.connect(self.reset)

        self.d1 = QLabel('地点:',self)
        self.d2 = QLabel('日期:',self)
        self.d3 = QLabel('湿度:',self)
        self.d4 = QLabel('光源:',self)
        self.d1.setScaledContents(True)
        self.d2.setScaledContents(True)
        self.d3.setScaledContents(True)
        # self.d1.setAlignment(Qt.AlignCenter)

        self.d1.resize(50,50)
        self.d2.resize(50,50)
        self.d3.resize(50,50)
        self.d4.resize(50,50)

        self.h_l1 = QHBoxLayout()
        self.h_l2 = QHBoxLayout()
        self.h_l3 = QHBoxLayout()
        self.h_l4 = QHBoxLayout()
        self.h_l5 = QHBoxLayout()
        self.h_l6 = QHBoxLayout()
        self.v_l = QVBoxLayout()

        self.layout()
        self.combo()

    def layout(self):
        self.h_l1.addWidget(self.label1)
        self.h_l1.addWidget(self.label2)

        self.h_l2.addWidget(self.d1)
        self.h_l2.addWidget(self.c1)

        self.h_l3.addWidget(self.d2)
        self.h_l3.addWidget(self.c2)

        self.h_l4.addWidget(self.d3)
        self.h_l4.addWidget(self.c3)

        self.h_l5.addWidget(self.b1)
        self.h_l5.addWidget(self.b2)

        self.h_l6.addWidget(self.d4)
        self.h_l6.addWidget(self.c4)

        self.v_l.addLayout(self.h_l1)
        self.v_l.addLayout(self.h_l2)
        self.v_l.addLayout(self.h_l3)
        self.v_l.addLayout(self.h_l4)
        self.v_l.addLayout(self.h_l6)
        self.v_l.addLayout(self.h_l5)

        self.setLayout(self.v_l)

    def combo(self):
        self.c1.addItems(self.place_list)
        self.c3.addItems(self.humidity_list)
        self.c4.addItems([i for i in self.light_dicts.keys()] )

    def start_stop(self):
        if self.b1.text() == 'Start':
            self.b1.setText('Stop')
            self.update_image()
            self.current_parameter()
        else:
            self.b1.setText('Start')
            self.label1.setPixmap(QPixmap(''))
            try:
                os.remove('light_plot/{}.png'.format(self.v))
            except:
                pass
            ###需要删除或关闭图片

    def reset(self):
        self.label1.setText('请输入参数')
        self.b1.setText('Start')
        self.label2.setText('当前参数')
        try:
            os.remove('light_plot/{}.png'.format(self.v))
        except:
            pass

    def update_image(self):
        self.current_light = str(self.c4.currentText())
        for self.k,self.v in self.light_dicts.items():
            if self.current_light == self.k:
                eval('L_S_Plot().{}_plot()'.format(self.v))
                self.label1.setPixmap(QPixmap('light_plot/{}.png'.format(self.v)))
                break

    def current_parameter(self):
        current_place = str(self.c1.currentText())
        # self.current_date = self.c2.setDisplayFormat('yyyy-MM-dd HH')
        # current_date = self.c2.dateTime().toString(Qt.ISODate)
        current_date = self.c2.dateTime().toString('yyyy-MM-dd HH')
        current_humidity = str(self.c3.currentText())

        self.label2.setText("当前参数为:\n地点：{}\n时间：{}\n湿度：{}\n光源：{}".format(
            current_place,current_date,current_humidity,self.current_light))

