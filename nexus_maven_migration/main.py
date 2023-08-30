import os
import sys

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox, QToolTip
from PyQt5.uic.properties import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from maven_to_nexus2 import Ui_Dialog
from upload_to_nexus import upload
from local_log import logger


class Uploader(QThread):
    trigger = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, selectfolder, nexus_url, repository, user, pwd):
        super().__init__()
        self.selectfolder = selectfolder
        self.nexus_url = nexus_url
        self.repository = repository
        self.user = user
        self.pwd = pwd

    def run(self):
        # Open the URL address.
        upload(self.selectfolder, self.nexus_url, self.repository, self.user, self.pwd, self.trigger, self.finished)


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.uploader = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # self.ui.lineEdit_pwd.setEchoMode(QtWidgets.QLineEdit.Password)

        # 通过 slot 发送信号, 然后绑定到业务逻辑的函数
        self.ui.selectButton.clicked.connect(self.select_folder)
        self.ui.confirmButton.clicked.connect(self.confirm)

        self.setWindowTitle('迁移Maven仓库到Nexus')
        self.setWindowIcon(QIcon('icon.ico'))
        self.show()

    def select_folder(self):
        """
        选择文件夹
        """
        foldername = QFileDialog.getExistingDirectory(self, "选择Maven仓库目录", "./")
        self.ui.lineEdit_folder.clear()
        self.ui.lineEdit_folder.setText(foldername)

    def message(self, msg):
        # 最后的Yes表示弹框的按钮显示为Yes，默认按钮显示为OK,不填QMessageBox.Yes即为默认
        QMessageBox.information(self, "", "{}".format(msg), QMessageBox.Yes)

    def confirm(self):
        """
        确定后开始迁移
        """
        selectfolder = self.ui.lineEdit_folder.text()
        if not os.path.exists(selectfolder):
            self.message('文件夹不存在')
            return
        nexus_url = self.ui.lineEdit_url.text()
        repository = self.ui.lineEdit_repository.text()
        user = self.ui.lineEdit_user.text()
        pwd = self.ui.lineEdit_pwd.text()
        if not all((nexus_url, repository, user, pwd)):
            self.message('有参数为空')
            return

        self.ui.label_6.setText("上传中...")
        # Disable the button while downloading the file.
        self.ui.confirmButton.setEnabled(False)
        # Execute the download in a new thread.
        self.uploader = Uploader(selectfolder, nexus_url, repository, user, pwd)
        self.uploader.trigger.connect(self.update_label)
        # Qt will invoke the `downloadFinished()` method once the
        # thread has finished.
        self.uploader.finished.connect(self.upload_finished)
        self.uploader.start()

    def update_label(self, msg):
        print(11111111111, msg)
        self.ui.label_6.setText(msg)

    def upload_finished(self, msg):
        print(222222, msg)
        self.ui.label_6.setText(msg)
        # Restore the button.
        self.ui.confirmButton.setEnabled(True)
        # Delete the thread when no longer needed.
        del self.uploader


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()

    sys.exit(myapp.exec_())
