import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QDate,QTime,QDateTime,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,\
    QComboBox,QDateTimeEdit,QMainWindow,QAction,QMessageBox,QFileDialog
from Light_sources_test_fjn_2 import L_S_Test_2
import os

class UI_L_S(QWidget):
    """不同光源"""
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
                eval('L_S_Test_2().{}_plot()'.format(self.v))
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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(850,700)
        self.is_saved = False
        self.is_saved_first = True
        self.path = ''
        # 主窗口
        self.setWindowTitle('Light Sources')
        self.file_menu = self.menuBar().addMenu('文件')
        self.edit_menu = self.menuBar().addMenu('编辑')
        self.help_menu = self.menuBar().addMenu('帮助')

        self.file_toolbar = self.addToolBar('文件')
        self.edit_toolbar = self.addToolBar('编辑')

        self.status_bar = self.statusBar()
        # 文件
        self.new_action = QAction('新建', self)
        self.open_action = QAction('打开', self)
        self.save_action = QAction('保存', self)
        self.save_as_action = QAction('另存为', self)
        self.close_action = QAction('关闭', self)
        # 编辑
        self.start_action = QAction('启动',self)
        self.pause_action = QAction('暂停',self)
        self.stop_action = QAction('停止',self)
        #帮助
        self.about_action = QAction('关于',self)

        self.menu_bar()
        self.tool_bar()
        self.status_bar_init()
        self.action_init()

        #加入中间窗口控件
        self.l_s = UI_L_S()
        self.setCentralWidget(self.l_s)
        self.l_s.setParent(self)
        self.label1 = self.l_s.label1

    def menu_bar(self):
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)

        self.edit_menu.addAction(self.start_action)
        self.edit_menu.addAction(self.pause_action)
        self.edit_menu.addSeparator()   #分割线
        self.edit_menu.addAction(self.stop_action)

        self.help_menu.addAction(self.about_action)

    def tool_bar(self):
        self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addAction(self.save_as_action)

        self.edit_toolbar.addAction(self.start_action)
        self.edit_toolbar.addAction(self.pause_action)
        self.edit_toolbar.addAction(self.stop_action)

    def status_bar_init(self):
        self.status_bar.showMessage('>> 状态栏 <<')
    def action_init(self):
        self.new_action.setIcon(QIcon('images/new.ico'))
        self.new_action.setShortcut('Ctrl+X')  # 快捷键
        self.new_action.setToolTip('创建新文件')  # 提示
        self.new_action.setStatusTip('创建新文件')  # 设置状态栏信息
        self.new_action.triggered.connect(self.new_func)

        self.open_action.setIcon(QIcon('images/open.ico'))  # 2
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setToolTip('打开已存在文件')
        self.open_action.setStatusTip('打开已存在文件')
        self.open_action.triggered.connect(self.open_file_func)

        self.save_action.setIcon(QIcon('images/save.ico'))  # 3
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('保存当前文档')
        self.save_action.setStatusTip('保存当前文档')
        self.save_action.triggered.connect(self.save_func)

        self.save_as_action.setIcon(QIcon('images/save_as.ico'))  # 4
        self.save_as_action.setShortcut('Ctrl+A')
        self.save_as_action.setToolTip('另存为')
        self.save_as_action.setStatusTip('另存为')
        self.save_as_action.triggered.connect(self.save_as_func)

        self.close_action.setIcon(QIcon('images/close.ico'))  # 5
        self.close_action.setShortcut('Ctrl+E')
        self.close_action.setToolTip('关闭窗口')
        self.close_action.setStatusTip('关闭窗口')
        self.close_action.triggered.connect(self.close_func)

        self.start_action.setIcon(QIcon('images/start.ico'))
        self.start_action.setShortcut('Ctrl+T')
        self.start_action.setToolTip('启动')
        self.start_action.setStatusTip('启动')
        self.start_action.triggered.connect(lambda: self.start_stop_func('Start'))

        self.pause_action.setIcon(QIcon('images/pause.ico'))
        self.pause_action.setShortcut('Ctrl+P')
        self.pause_action.setToolTip('暂停')
        self.pause_action.setStatusTip('暂停“')
        self.pause_action.triggered.connect(lambda: self.start_stop_func('Stop'))

        self.stop_action.setIcon(QIcon('images/stop.ico'))
        self.stop_action.setShortcut('Ctrl+I')
        self.stop_action.setToolTip('终止')
        self.stop_action.setStatusTip('终止')
        self.stop_action.triggered.connect(self.stop_func)

        self.about_action.setIcon(QIcon('images/about.ico'))
        self.about_action.setShortcut('Ctrl+Q')
        self.about_action.setToolTip('关于')
        self.about_action.setStatusTip('关于')
        # self.about_action.triggered.connect(self.about_func)

    def new_func(self):
        if self.label1.text() == '请输入参数':
            self.start_stop_func('Start')
        else:
            if not self.is_saved:
                choice = QMessageBox.question(self, '', '是否保存图像？',
                                              QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if choice == QMessageBox.Yes:
                    self.save_func()
                    self.is_saved_first = True
                elif choice == QMessageBox.No:
                    self.stop_func()
                else:
                    pass
            else:
                self.stop_func()
                self.is_saved = False
                self.is_saved_first = True

    def open_file_func(self):           #需要简化
        if not self.is_saved:
            choice = QMessageBox.question(self, '', '是否保存图像？',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func()
                file, _ = QFileDialog.getOpenFileName(self, '打开文件', './', 'Files (*.jpg *.png *.html)')
                if file:
                        self.label1.setPixmap(QPixmap(file))
                        self.is_saved = True
            elif choice == QMessageBox.No:
                file, _ = QFileDialog.getOpenFileName(self, '打开文件', './', 'Files (*.jpg *.png *.html)')
                if file:
                        self.label1.setPixmap(QPixmap(file))
                        self.is_saved = True
            else:
                pass
        else:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.jpg *.png *.html)')
            if file:
                self.label1.setPixmap(QPixmap(file))
                self.is_saved = True

    def save_func(self):
        if self.is_saved_first:
            self.save_as_func()
        else:
            self.pic = self.label1.pixmap().toImage()
            self.pic.save(self.path, 'PNG', 100)
            self.is_saved = True


    def save_as_func(self):
        if self.label1.text() != '请输入参数':
            self.pic = self.label1.pixmap().toImage()
            self.path, _ = QFileDialog.getSaveFileName(self, '保存图像', './', 'Files (*.jpg *.png *.html)')   #对话框返回绝对路径(我们保存在path中)和扩展过滤器
            if self.path:
                self.pic.save(self.path,'PNG',100)
                self.is_saved = True
                self.is_saved_first = False
        else:
            pass

    def close_func(self):
        if not self.is_saved:
            choice = QMessageBox.question(self, '保存图像', '是否保存图像?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func()
                self.close()
            elif choice == QMessageBox.No:
                self.close()
            else:
                pass

    def closeEvent(self, QCloseEvent):
        if not self.is_saved:
            choice = QMessageBox.question(self, '关闭框', '是否保存图像？',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func()
                QCloseEvent.accept()
            elif choice == QMessageBox.No:
                QCloseEvent.accept()
            else:
                QCloseEvent.ignore()

    def start_stop_func(self,start_pause):
        if self.l_s.b1.text() == start_pause:
            self.l_s.start_stop()
        else:
            pass
    def stop_func(self):
        self.l_s.reset()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m_w = MainWindow()
    m_w.show()
    sys.exit(app.exec_())
