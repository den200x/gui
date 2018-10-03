# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connectionSettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_connectDialog(object):
    def setupUi(self, connectDialog, ui):
        self.ui = ui
        self.settings = ui.settings
        self.connectDialog = connectDialog
        connectDialog.setObjectName("connectDialog")
        connectDialog.resize(399, 244)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        connectDialog.setWindowIcon(icon)
        self.widget = QtWidgets.QWidget(connectDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 381, 216))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.sql_driver_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.sql_driver_lineEdit.setObjectName("sql_driver_lineEdit")
        self.verticalLayout.addWidget(self.sql_driver_lineEdit)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.sql_server_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.sql_server_lineEdit.setText("")
        self.sql_server_lineEdit.setObjectName("sql_server_lineEdit")
        self.verticalLayout.addWidget(self.sql_server_lineEdit)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.sql_db_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.sql_db_lineEdit.setText("")
        self.sql_db_lineEdit.setObjectName("sql_db_lineEdit")
        self.verticalLayout.addWidget(self.sql_db_lineEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.sql_server_lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sql_driver_lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sql_db_lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.retranslateUi(connectDialog)
        QtCore.QMetaObject.connectSlotsByName(connectDialog)

        #Manually added
        self.buttonBox.accepted.connect(self.OnSave)
        self.buttonBox.rejected.connect(self.OnCancel)
        QtCore.QMetaObject.connectSlotsByName(connectDialog)

        if self.ui.stack.online:
            self.buttonBox.setEnabled(False)
            self.sql_driver_lineEdit.setEnabled(False)
            self.sql_server_lineEdit.setEnabled(False)
            self.sql_db_lineEdit.setEnabled(False)
        self.loadCurrentSettings()

    def retranslateUi(self, connectDialog):
        _translate = QtCore.QCoreApplication.translate
        connectDialog.setWindowTitle(_translate("connectDialog", "Connection Settings"))
        self.label.setText(_translate("connectDialog", "SQL DB information"))
        self.label_2.setText(_translate("connectDialog", "Driver"))
        self.label_3.setText(_translate("connectDialog", "Server"))
        self.label_4.setText(_translate("connectDialog", "Database"))

    def loadCurrentSettings(self):
        self.sql_driver_lineEdit.setText(self.settings.SQL_driver)
        self.sql_server_lineEdit.setText(self.settings.SQL_server)
        self.sql_db_lineEdit.setText(self.settings.SQL_DB)

    def OnSave(self):
        success = self.save()
        if success:
            self.connectDialog.close()

    def OnCancel(self):
        self.connectDialog.close()

    def save(self):
        self.settings.SQL_driver = self.sql_driver_lineEdit.text()
        self.settings.SQL_server = self.sql_server_lineEdit.text()
        self.settings.SQL_DB = self.sql_db_lineEdit.text()
        #Write settings to file
        self.settings.saveSettings()
        return True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectDialog = QtWidgets.QDialog()
    ui = Ui_connectDialog()
    ui.setupUi(connectDialog)
    connectDialog.show()
    sys.exit(app.exec_())

