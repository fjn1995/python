import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QDate,QTime,QDateTime,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,\
    QComboBox,QDateTimeEdit,QMainWindow,QAction,QMessageBox,QFileDialog
# from Light_sources_test_fjn_2 import L_S_Test_2
from light_sources_ui import UI_L_S
from material_n_k_ui import UI_N_K_test
from material_sopra_ui import UI_N_K
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(850,700)
        self.is_saved = False
        self.is_saved_first = True
        self.path = ''
        self.model = ''
        # 主窗口
        self.setWindowTitle('Auxiliary')
        self.file_menu = self.menuBar().addMenu('文件')
        self.edit_menu = self.menuBar().addMenu('编辑')
        self.select_menu = self.menuBar().addMenu('模型选择')
        self.help_menu = self.menuBar().addMenu('帮助')

        self.file_toolbar = self.addToolBar('文件')
        self.edit_toolbar = self.addToolBar('编辑')
        self.select_toolbar = self.addToolBar('模型选择')

        self.status_bar = self.statusBar()
        # 文件
        # self.new_action = QAction('新建', self)
        self.open_action = QAction('打开', self)
        self.save_action = QAction('保存', self)
        self.save_as_action = QAction('另存为', self)
        self.close_action = QAction('关闭', self)
        # 编辑
        self.start_action = QAction('启动',self)
        self.stop_action = QAction('暂停', self)
        self.reset_action = QAction('停止', self)

        #模型选择
        self.l_s_action = QAction('光源',self)
        self.m_l_nk_action = QAction('sopra材料库', self)
        self.mj_s_c_action = QAction('多结太阳能电池',self)
        #帮助
        self.about_action = QAction('关于',self)

        self.menu_bar()
        self.tool_bar()
        self.status_bar_init()
        self.action_init()

        self.select_model('l_s')    #默认模块

    def menu_bar(self):
        """菜单栏"""
        # self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)

        self.edit_menu.addAction(self.start_action)
        self.edit_menu.addAction(self.stop_action)
        self.edit_menu.addSeparator()   #分割线
        self.edit_menu.addAction(self.reset_action)

        self.select_menu.addAction(self.l_s_action)
        self.select_menu.addAction(self.m_l_nk_action)
        self.select_menu.addAction(self.mj_s_c_action)

        self.help_menu.addAction(self.about_action)
    def tool_bar(self):
        """工具栏"""
        # self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addAction(self.save_as_action)

        self.edit_toolbar.addAction(self.start_action)
        self.edit_toolbar.addAction(self.stop_action)
        self.edit_toolbar.addAction(self.reset_action)

        self.select_toolbar.addAction(self.l_s_action)
        self.select_toolbar.addAction(self.m_l_nk_action)
        self.select_toolbar.addAction(self.mj_s_c_action)
    def status_bar_init(self):
        """状态栏"""
        self.status_bar.showMessage('>> 状态栏 <<')
    def action_init(self):
        """响应栏"""
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

        self.stop_action.setIcon(QIcon('images/pause.ico'))
        self.stop_action.setShortcut('Ctrl+P')
        self.stop_action.setToolTip('暂停')
        self.stop_action.setStatusTip('暂停')
        self.stop_action.triggered.connect(lambda: self.start_stop_func('Stop'))

        self.reset_action.setIcon(QIcon('images/stop.ico'))
        self.reset_action.setShortcut('Ctrl+I')
        self.reset_action.setToolTip('终止')
        self.reset_action.setStatusTip('终止')
        self.reset_action.triggered.connect(self.reset_func)

        #设置模型选项按钮
        self.l_s_action.setIcon(QIcon('images/sun.ico'))
        self.l_s_action.setToolTip('光源')
        self.l_s_action.setStatusTip('光源')
        self.l_s_action.triggered.connect(lambda:self.select_model('l_s'))   #光源接口

        self.m_l_nk_action.setIcon(QIcon('images/om.ico'))
        self.m_l_nk_action.setToolTip('sopra材料库')
        self.m_l_nk_action.setStatusTip('sopra材料库')
        self.m_l_nk_action.triggered.connect(lambda:self.select_model('sopra_ml'))

        self.mj_s_c_action.setIcon(QIcon('images/solar_panel.ico'))
        self.mj_s_c_action.setToolTip('太阳能电池')
        self.mj_s_c_action.setStatusTip('多结太阳能电池组件')
        # self.cppb_action.triggered.connect()

        self.about_action.setIcon(QIcon('images/about.ico'))
        self.about_action.setShortcut('Ctrl+Q')
        self.about_action.setToolTip('关于')
        self.about_action.setStatusTip('关于')
        # self.about_action.triggered.connect(self.about_func)

######----功能-------
    def select_model(self,model):
        """选择模块"""
        self.model = model
        eval('self.{}_model()'.format(self.model))

    def sopra_ml_model(self):
        self.sopra_ml_nk = UI_N_K()
        self.setCentralWidget(self.sopra_ml_nk)
        self.sopra_ml_nk.setParent(self)

    def l_s_model(self):
        """光源模块"""
        self.l_s = UI_L_S()
        self.setCentralWidget(self.l_s)
        self.l_s.setParent(self)
        self.label1 = self.l_s.label1
        self.b1 = self.l_s.b1

    def m_l_nk_model(self):
        """sopra材料数据库的test模块"""
        self.m_l_nk = UI_N_K_test()
        self.setCentralWidget(self.m_l_nk)
        self.m_l_nk.setParent(self)
        self.label1 = self.m_l_nk.label1
        self.b1 = self.m_l_nk.b1


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

    def start_stop_func(self,start_stop):
        if self.b1.text() == start_stop:
            eval('self.{}.start_stop()'.format(self.model))
        else:
            pass
    def reset_func(self):
        eval('self.{}.reset()'.format(self.model))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m_w = MainWindow()
    m_w.show()
    sys.exit(app.exec_())




