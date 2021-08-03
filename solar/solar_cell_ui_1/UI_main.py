import sys
import time
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import QMimeData,Qt
from PyQt5.QtWidgets import QApplication,QMainWindow,QTextEdit,QAction,QFileDialog,\
    QMessageBox,QFontDialog,QColorDialog,QSplashScreen,QLabel

from UI_Light_sources import UI_L_S

class NoteBook(QMainWindow):

    path = ''

    def __init__(self):
        super(NoteBook, self).__init__()

        self.cen_w = UI_L_S()
        self.setWindowTitle('SOLCORE')
        self.file_menu = self.menuBar().addMenu('文件')
        self.edit_menu = self.menuBar().addMenu('运行')
        self.choice_menu = self.menuBar().addMenu('选择')
        self.help_menu = self.menuBar().addMenu('关于')

        self.file_toolbar = self.addToolBar('文件')
        self.edit_toolbar = self.addToolBar('运行')
        self.choice_toolbar = self.addToolBar('选择')
        self.status_bar = self.statusBar()

        self.open_action = QAction('打开',self)
        self.save_action = QAction('保存',self)
        self.save_as_action = QAction('另存为',self)
        self.close_action = QAction('关闭',self)

        self.start_action = QAction('开始', self)
        self.pause_action = QAction('暂停', self)
        self.stop_action = QAction('停止',self)

        self.mime_data = QMimeData()

        # self.setCentralWidget(self.cen_w)   #主窗口控件
        self.resize(450,600)

        self.menu_init()
        self.toolbar_init()
        self.status_bar_init()
        self.action_init()
        self.text_edit_int()

    def menu_init(self):
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)

        self.edit_menu.addAction(self.elect_action)
        self.edit_menu.addAction(self.pause_action)
        self.edit_menu.addAction(self.stop_action)


        self.help_menu.addAction(self.about_action)

    def toolbar_init(self):
        self.file_toolbar.addAction(self.elect_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addAction(self.save_as_action)

        self.edit_toolbar.addAction(self.start_action)
        self.edit_toolbar.addAction(self.pause_action)
        self.edit_toolbar.addAction(self.stop_action)

    def status_bar_init(self):
        self.status_bar.showMessage('准备开始')

    def action_init(self):
        self.elect_action.setIcon(QIcon('images/elect.ico'))
        self.elect_action.setShortcut('Ctrl+E')               #快捷键
        self.elect_action.setToolTip('创建新文件')     #提示
        self.elect_action.setStatusTip('创建新文件')            #设置状态栏信息
        self.elect_action.triggered.connect(self.elect_func)

        self.open_action.setIcon(QIcon('images/open.ico'))  # 2
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setToolTip('打开已存在文件')
        self.open_action.setStatusTip('打开已存在文件')
        self.open_action.triggered.connect(self.open_file_func)

        self.save_action.setIcon(QIcon('images/save.ico'))  # 3
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('保存当前文档')
        self.save_action.setStatusTip('保存当前文档')
        self.save_action.triggered.connect(lambda: self.save_func(self.text_edit.toHtml()))

        self.save_as_action.setIcon(QIcon('images/save_as.ico'))  # 4
        self.save_as_action.setShortcut('Ctrl+A')
        self.save_as_action.setToolTip('另存为')
        self.save_as_action.setStatusTip('另存为')
        self.save_as_action.triggered.connect(lambda: self.save_as_func(self.text_edit.toHtml()))

        self.close_action.setIcon(QIcon('images/close.ico'))  # 5
        self.close_action.setShortcut('Ctrl+E')
        self.close_action.setToolTip('关闭窗口')
        self.close_action.setStatusTip('关闭窗口')
        self.close_action.triggered.connect(self.close_func)

        self.start_action.setIcon(QIcon('images/start.ico'))  # 6
        self.start_action.setShortcut('Ctrl+X')
        self.start_action.setToolTip('剪切到剪切板')
        self.start_action.setStatusTip('剪切文本')
        self.start_action.triggered.connect(self.start_func)

        self.pause_action.setIcon(QIcon('images/copy.ico'))  # 7
        self.pause_action.setShortcut('Ctrl+C')
        self.pause_action.setToolTip('复制文本')
        self.pause_action.setStatusTip('复制文本')
        self.pause_action.triggered.connect(self.suspend_func)

        self.about_action.setIcon(QIcon('images/about.ico'))  # 11
        self.about_action.setShortcut('Ctrl+Q')
        self.about_action.setToolTip('关于')
        self.about_action.setStatusTip('关于')
        self.about_action.triggered.connect(self.about_func)

    def elect_func(self):
        self.setCentralWidget(self.cen_w)   #主窗口控件

    def open_file_func(self):           #需要简化
        if not self.is_saved:
            choice = QMessageBox.question(self, '', '是否保存文档？',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func(self.text_edit.toHtml())
                file, _ = QFileDialog.getOpenFileName(self, '打开文件', './', 'Files (*.html *.txt *.log)')
                if file:
                    with open(file, 'r') as f:
                        self.text_edit.clear()
                        self.text_edit.setText(f.read())
                        self.is_saved = True
            elif choice == QMessageBox.No:
                file, _ = QFileDialog.getOpenFileName(self, '打开文件', './', 'Files (*.html *.txt *.log)')
                if file:
                    with open(file, 'r') as f:
                        self.text_edit.clear()
                        self.text_edit.setText(f.read())
                        self.is_saved = True
            else:
                pass
        else:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.html *.txt *.log)')
            if file:
                with open(file, 'r') as f:
                    self.text_edit.clear()
                    self.text_edit.setText(f.read())
                    self.is_saved = True

    def save_func(self, text):
        if self.is_saved_first:
            self.save_as_func(text)
        else:
            with open(self.path, 'w') as f:
                f.write(text)
            self.is_saved = True

    def save_as_func(self, text):
        self.path, _ = QFileDialog.getSaveFileName(self, '保存文件', './', 'Files (*.html *.txt *.log *.png)')
        if self.path:
            with open(self.path, 'w') as f:
                f.write(text)
            self.is_saved = True
            self.is_saved_first = False

    def close_func(self):
        if not self.is_saved:
            choice = QMessageBox.question(self, 'Save File', 'Do you want to save the text?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func(self.text_edit.toHtml())
                self.close()
            elif choice == QMessageBox.No:
                self.close()
            else:
                pass

    def closeEvent(self, QCloseEvent):
        if not self.is_saved:
            choice = QMessageBox.question(self, '保存文件', '确定保存文件?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func(self.text_edit.toHtml())
                QCloseEvent.accept()
            elif choice == QMessageBox.No:
                QCloseEvent.accept()
            else:
                QCloseEvent.ignore()

    def copy_func(self):
        self.mime_data.setHtml(self.text_edit.textCursor().selection().toHtml())
        self.clipboard.setMimeData(self.mime_data)

    def paste_func(self):
        self.text_edit.insertHtml(self.clipboard.mimeData().html())

    def font_func(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_edit.setFont(font)

    def about_func(self):
        QMessageBox.aboutQt(self, 'About Qt')

    def text_edit_int(self):
        self.text_edit.textChanged.connect(self.text_changed_func)

    def text_changed_func(self):
        if self.text_edit.toPlainText():
            self.is_saved = False
        else:
            self.is_saved = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    n_b = NoteBook()
    n_b.show()
    sys.exit(app.exec_())