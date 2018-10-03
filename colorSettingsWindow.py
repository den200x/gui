# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colorSettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_colorDialog(object):
    def setupUi(self, colorDialog, ui):
        self.ui = ui
        self.settings = ui.settings
        self.colorDialog = colorDialog
        colorDialog.setObjectName("colorDialog")
        colorDialog.resize(488, 268)
        colorDialog.setMinimumSize(QtCore.QSize(480, 260))
        self.gridLayout = QtWidgets.QGridLayout(colorDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(colorDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(colorDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(colorDialog)
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.listWidget_2 = QtWidgets.QListWidget(colorDialog)
        self.listWidget_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.gridLayout.addWidget(self.listWidget_2, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(colorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(colorDialog)
       
        #Manually added
        self.buttonBox.accepted.connect(self.OnSave)
        self.buttonBox.rejected.connect(self.OnCancel)
        QtCore.QMetaObject.connectSlotsByName(colorDialog)
        self.loadCurrentSettings()

    def retranslateUi(self, colorDialog):
        _translate = QtCore.QCoreApplication.translate
        colorDialog.setWindowTitle(_translate("colorDialog", "Color settings"))
        self.label.setText(_translate("colorDialog", "Standard Observer"))
        self.label_2.setText(_translate("colorDialog", "Illuminants"))

    def loadCurrentSettings(self):
        self.listWidget.addItems(self.settings.color_cmfs_list)
        self.listWidget.setCurrentRow(self.settings.color_cmfs_list.index(self.settings.color_cmfs))

        self.listWidget_2.addItems(self.settings.color_illuminant_list)
        self.listWidget_2.setCurrentRow(self.settings.color_illuminant_list.index(self.settings.color_illuminant))

    def OnSave(self):
        success = self.save()
        if success:
            self.colorDialog.close()
            self.ui.updateScreens(0)
            self.ui.updateScreens(1)

    def OnCancel(self):
        self.colorDialog.close()

    def save(self):
        self.settings.color_cmfs = self.settings.color_cmfs_list[self.listWidget.currentRow()]
        self.settings.color_illuminant = self.settings.color_illuminant_list[self.listWidget_2.currentRow()]
        #Write settings to file
        self.settings.saveSettings()
        return True


if __name__ == "__main__":
    import sys
    from Settings import Settings
    app = QtWidgets.QApplication(sys.argv)
    colorDialog = QtWidgets.QDialog()
    ui = Ui_colorDialog()
    settings = Settings()
    ui.setupUi(colorDialog, settings)
    colorDialog.show()
    sys.exit(app.exec_())

