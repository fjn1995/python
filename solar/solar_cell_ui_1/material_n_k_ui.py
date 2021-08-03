import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QDate,QTime,QDateTime,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,\
    QComboBox,QDateTimeEdit,QMainWindow,QAction,QMessageBox,QFileDialog
import os
import sys
from Material_n_k_plot import Material_nk

from solcore_db import ml_data
material_datas = ml_data()

class UI_N_K_test(QWidget):
    """不同光源"""
    def __init__(self):
        super(UI_N_K_test, self).__init__()
        self.title = self.setWindowTitle('折射率,消光系数对比')
        self.resize(850,700)
        self.ml1_list = material_datas
        self.ml2_list = material_datas

        self.label1 = QLabel('请输入参数',self)
        self.label1.resize(400,300)
        self.label1.setAlignment(Qt.AlignCenter)

        self.label2 = QLabel('\n\n\n当前参数',self)

        self.c1 = QComboBox()   # 材料1
        self.c2 = QComboBox()   # 材料2

        self.b1 = QPushButton('Start',self)
        self.b2 = QPushButton('Reset',self)

        self.b1.clicked.connect(self.start_stop)
        self.b2.clicked.connect(self.reset)

        self.d1 = QLabel('材料一:',self)
        self.d2 = QLabel('材料二:',self)

        self.d1.setScaledContents(True)
        self.d2.setScaledContents(True)

        self.d1.resize(50,50)
        self.d2.resize(50,50)

        self.h_l1 = QHBoxLayout()
        self.h_l2 = QHBoxLayout()
        self.h_l3 = QHBoxLayout()
        self.h_l4 = QHBoxLayout()

        self.v_l1 = QVBoxLayout()
        self.v_l2 = QVBoxLayout()

        self.layout()
        self.combo()

    def layout(self):
        self.h_l1.addWidget(self.d1)
        self.h_l1.addWidget(self.c1)

        self.h_l2.addWidget(self.d2)
        self.h_l2.addWidget(self.c2)

        self.h_l3.addWidget(self.b1)
        self.h_l3.addWidget(self.b2)

        self.v_l1.addWidget(self.label2)
        self.v_l1.addLayout(self.h_l1)
        self.v_l1.addLayout(self.h_l2)

        self.h_l4.addWidget(self.label1)
        self.h_l4.addLayout(self.v_l1)

        self.v_l2.addLayout(self.h_l4)
        self.v_l2.addLayout(self.h_l3)

        self.setLayout(self.v_l2)

    def combo(self):
        self.c1.addItems(self.ml1_list)
        self.c1.setCurrentText('GaAs')
        self.c2.addItems(self.ml2_list)
        self.c2.setCurrentText('Ge')

    def start_stop(self):
        if self.b1.text() == 'Start':
            self.b1.setText('Stop')
            self.update_image()
            self.current_parameter()
        else:
            self.b1.setText('Start')
            self.label1.setPixmap(QPixmap(''))
            try:
                os.remove('material_n_k_plot/{}_{}_nk.png'.format(self.current_ml1,self.current_ml2))
            except:
                pass

    def reset(self):
        self.label1.setText('请输入参数')
        self.b1.setText('Start')
        self.label2.setText('\n\n\n当前参数')
        try:
            os.remove('material_n_k_plot/{}_{}_nk.png'.format(self.current_ml1,self.current_ml2))
        except:
            pass

    def update_image(self):
        self.current_ml1 = str(self.c1.currentText())
        self.current_ml2 = str(self.c2.currentText())
        if self.current_ml1 == self.current_ml2:
            QMessageBox.critical(self,'注意！','请选择不同的材料！',QMessageBox.Ok)
        else:
            eval('Material_nk().n_k_plot("{}","{}")'.format(self.current_ml1,self.current_ml2))
            self.label1.setPixmap(QPixmap('material_n_k_plot/{}_{}_nk.png'.format(self.current_ml1,self.current_ml2)))

    def current_parameter(self):
        current_ml1 = str(self.c1.currentText())
        current_ml2 = str(self.c2.currentText())
        self.label2.setText("当前参数为:\n材料一：{}\n材料二：{}".format(current_ml1,current_ml2))

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     m_w = UI_N_K_test()
#     m_w.show()
#     sys.exit(app.exec_())

