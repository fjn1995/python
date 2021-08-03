import sys

from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QDate,QTime,QDateTime,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit,\
    QComboBox,QDateTimeEdit,QMainWindow
from Light_sources_test_fjn import L_S_Test
import os

class UI_L_S(QWidget):
    """不同光源"""

    def __init__(self):
        super(UI_L_S, self).__init__()
        self.title = self.setWindowTitle('Light Sources')
        self.setFixedSize(850,700)      #固定窗口大小

        self.place_list = ['武汉','佛山','...']
        self.humidity_list = ['高','中','低']

        self.label1 = QLabel('请输入参数',self)
        self.label1.resize(300,300)
        self.label1.setAlignment(Qt.AlignCenter)

        self.label2 = QLabel('当前参数',self)
        # self.label2.setAlignment(Qt.AlignCenter)      #居中
        self.c1 = QComboBox()   #地点
        self.c2 = QDateTimeEdit(QDateTime.currentDateTime(),self)   #日期

        self.c2.setDisplayFormat('yyyy-MM-dd HH')
        self.c3 = QComboBox()   #湿度

        self.b1 = QPushButton('Start',self)
        self.b2 = QPushButton('Reset',self)

        self.b1.clicked.connect(self.start_stop)
        self.b2.clicked.connect(self.reset)

        self.d1 = QLabel('地点:',self)
        self.d2 = QLabel('日期:',self)
        self.d3 = QLabel('湿度:',self)
        self.d1.setScaledContents(True)
        self.d2.setScaledContents(True)
        self.d3.setScaledContents(True)
        # self.d1.setAlignment(Qt.AlignCenter)
        # self.d2.setAlignment(Qt.AlignCenter)
        # self.d3.setAlignment(Qt.AlignCenter)
        self.d1.resize(50,50)
        self.d2.resize(50,50)
        self.d3.resize(50,50)

        self.h_l1 = QHBoxLayout()
        self.h_l2 = QHBoxLayout()
        self.h_l3 = QHBoxLayout()
        self.h_l4 = QHBoxLayout()
        self.h_l5 = QHBoxLayout()
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

        self.v_l.addLayout(self.h_l1)
        self.v_l.addLayout(self.h_l2)
        self.v_l.addLayout(self.h_l3)
        self.v_l.addLayout(self.h_l4)
        self.v_l.addLayout(self.h_l5)

        self.setLayout(self.v_l)

    def combo(self):
        self.c1.addItems(self.place_list)
        self.c3.addItems(self.humidity_list)

    def start_stop(self):
        if self.b1.text() == 'Start':
            self.b1.setText('Stop')
            self.update_image()
            self.current_parameter()
        else:
            self.b1.setText('Start')
            # L_S_Test().close()
            os.remove('light_sources_test1.png')
            self.label1.setPixmap(QPixmap(''))
            ###需要删除或关闭图片

    def reset(self):
        self.label1.setText('请输入参数')
        self.b1.setText('Start')
        self.label2.setText('当前参数')

    def update_image(self):
        L_S_Test()
        self.label1.setPixmap(QPixmap('light_sources_test1.png'))

    def current_parameter(self):
        current_place = str(self.c1.currentText())
        # self.current_date = self.c2.setDisplayFormat('yyyy-MM-dd HH')
        # current_date = self.c2.dateTime().toString(Qt.ISODate)
        current_date = self.c2.dateTime().toString('yyyy-MM-dd HH')


        print(current_date)
        current_humidity = str(self.c3.currentText())
        self.label2.setText("当前参数为:\n地点：{}\n时间：{}\n湿度：{}".format(current_place,current_date,current_humidity ))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    l_s =UI_L_S()
    l_s .show()
    sys.exit(app.exec_())
