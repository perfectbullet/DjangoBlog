import os
import sys

from PyQt5.QtWidgets import QGridLayout, QApplication, QDialog, QLineEdit, QPushButton, QFileDialog, QMessageBox

from upload_to_nexus import upload


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("迁移本地maven到nexus")
        self.resize(400, 200)
        grid = QGridLayout()
        # 第一行  打开文件夹
        self.qlineEdit_selectfolder = QLineEdit(r'D:\res')
        self.qpush_selectfolder = QPushButton('选择文件夹')
        grid.addWidget(self.qlineEdit_selectfolder, 0, 1)
        grid.addWidget(self.qpush_selectfolder, 0, 2)

        # 输入 nexus url
        self.qlineEdit_nexus_url = QLineEdit('http://localhost:8931')
        grid.addWidget(self.qlineEdit_nexus_url, 1, 1)
        # 仓库名称
        self.qlineEdit_nexus_repository = QLineEdit('maven_zjhost')
        # 输入 user
        self.qlineEdit_nexus_user = QLineEdit('admin')
        grid.addWidget(self.qlineEdit_nexus_user, 2, 1)
        # 输入 password
        self.qlineEdit_nexus_pwd = QLineEdit('****')
        grid.addWidget(self.qlineEdit_nexus_pwd, 3, 1)

        # 第三行, 确认
        self.qpush_ok = QPushButton('确定')
        grid.addWidget(self.qpush_ok, 4, 2)

        self.setLayout(grid)
        # 绑定按钮, 选择文件夹的按钮
        self.qpush_selectfolder.clicked.connect(self.select_folder)
        # 绑定按钮, 确认按钮
        self.qpush_ok.clicked.connect(self.confirm)

    def select_folder(self):
        """选择文件夹
        """
        foldername = QFileDialog.getExistingDirectory(self, "Select Directory", "./")
        self.qlineEdit_selectfolder.setText(foldername)

    def message(self, msg):
        # 最后的Yes表示弹框的按钮显示为Yes，默认按钮显示为OK,不填QMessageBox.Yes即为默认
        QMessageBox.information(self, "", "{}".format(msg), QMessageBox.Yes)

    def confirm(self):
        """
        确定后开始迁移
        """
        selectfolder = self.qlineEdit_selectfolder.text()
        if not os.path.exists(selectfolder):
            self.message('文件夹不存在')
        nexus_url = self.qlineEdit_nexus_url.text()
        repository = self.qlineEdit_nexus_repository.text()
        user = self.qlineEdit_nexus_user.text()
        pwd = self.qlineEdit_nexus_pwd.text()
        msg = upload(selectfolder, nexus_url, repository, user, pwd)
        self.message(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
