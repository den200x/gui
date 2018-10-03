# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fitSettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fitSettingsDialog(object):
    def setupUi(self, fitSettingsDialog, ui):
        self.ui = ui
        self.settings = ui.settings
        self.fitSettingsDialog = fitSettingsDialog
        fitSettingsDialog.setObjectName("fitSettingsDialog")
        fitSettingsDialog.resize(544, 347)
        self.buttonBox = QtWidgets.QDialogButtonBox(fitSettingsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(180, 300, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.drudeMaxCheckBox = QtWidgets.QCheckBox(fitSettingsDialog)
        self.drudeMaxCheckBox.setGeometry(QtCore.QRect(20, 10, 261, 20))
        self.drudeMaxCheckBox.setObjectName("drudeMaxCheckBox")
        self.minHeightSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minHeightSB.setGeometry(QtCore.QRect(20, 60, 101, 24))
        self.minHeightSB.setMaximum(1e+22)
        self.minHeightSB.setObjectName("minHeightSB")
        self.maxHeightSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxHeightSB.setGeometry(QtCore.QRect(160, 60, 101, 24))
        self.maxHeightSB.setMaximum(1e+22)
        self.maxHeightSB.setObjectName("maxHeightSB")
        self.label = QtWidgets.QLabel(fitSettingsDialog)
        self.label.setGeometry(QtCore.QRect(20, 40, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_2.setGeometry(QtCore.QRect(160, 40, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 60, 16))
        self.label_3.setObjectName("label_3")
        self.maxDeSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxDeSB.setGeometry(QtCore.QRect(160, 110, 101, 24))
        self.maxDeSB.setMaximum(1e+22)
        self.maxDeSB.setObjectName("maxDeSB")
        self.label_4 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_4.setGeometry(QtCore.QRect(160, 90, 60, 16))
        self.label_4.setObjectName("label_4")
        self.minDeSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minDeSB.setGeometry(QtCore.QRect(20, 110, 101, 24))
        self.minDeSB.setMaximum(1e+22)
        self.minDeSB.setObjectName("minDeSB")
        self.label_5 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_5.setGeometry(QtCore.QRect(20, 140, 101, 16))
        self.label_5.setObjectName("label_5")
        self.maxUVw0SB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxUVw0SB.setGeometry(QtCore.QRect(160, 160, 101, 24))
        self.maxUVw0SB.setMaximum(1e+22)
        self.maxUVw0SB.setObjectName("maxUVw0SB")
        self.label_6 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_6.setGeometry(QtCore.QRect(160, 140, 111, 16))
        self.label_6.setObjectName("label_6")
        self.minUVw0SB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minUVw0SB.setGeometry(QtCore.QRect(20, 160, 101, 24))
        self.minUVw0SB.setMaximum(1e+22)
        self.minUVw0SB.setObjectName("minUVw0SB")
        self.label_7 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_7.setGeometry(QtCore.QRect(20, 190, 101, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_8.setGeometry(QtCore.QRect(20, 240, 100, 16))
        self.label_8.setObjectName("label_8")
        self.maxUVwpSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxUVwpSB.setGeometry(QtCore.QRect(160, 210, 101, 24))
        self.maxUVwpSB.setMaximum(1e+22)
        self.maxUVwpSB.setObjectName("maxUVwpSB")
        self.label_9 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_9.setGeometry(QtCore.QRect(160, 190, 101, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_10.setGeometry(QtCore.QRect(160, 240, 100, 16))
        self.label_10.setObjectName("label_10")
        self.minUVgammaSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minUVgammaSB.setGeometry(QtCore.QRect(20, 260, 101, 24))
        self.minUVgammaSB.setMaximum(1e+22)
        self.minUVgammaSB.setObjectName("minUVgammaSB")
        self.minUVwpSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minUVwpSB.setGeometry(QtCore.QRect(20, 210, 101, 24))
        self.minUVwpSB.setMaximum(1e+22)
        self.minUVwpSB.setObjectName("minUVwpSB")
        self.maxUVgammaSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxUVgammaSB.setGeometry(QtCore.QRect(160, 260, 101, 24))
        self.maxUVgammaSB.setMaximum(1e+22)
        self.maxUVgammaSB.setObjectName("maxUVgammaSB")
        self.label_11 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_11.setGeometry(QtCore.QRect(280, 240, 120, 16))
        self.label_11.setObjectName("label_11")
        self.maxConwpSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxConwpSB.setGeometry(QtCore.QRect(420, 210, 101, 24))
        self.maxConwpSB.setMaximum(1e+22)
        self.maxConwpSB.setObjectName("maxConwpSB")
        self.label_12 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_12.setGeometry(QtCore.QRect(420, 240, 120, 16))
        self.label_12.setObjectName("label_12")
        self.maxConw0SB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxConw0SB.setGeometry(QtCore.QRect(420, 160, 101, 24))
        self.maxConw0SB.setMaximum(1e+22)
        self.maxConw0SB.setObjectName("maxConw0SB")
        self.minConw0SB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minConw0SB.setGeometry(QtCore.QRect(280, 160, 101, 24))
        self.minConw0SB.setMaximum(1e+22)
        self.minConw0SB.setObjectName("minConw0SB")
        self.minConwpSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minConwpSB.setGeometry(QtCore.QRect(280, 210, 101, 24))
        self.minConwpSB.setMaximum(1e+22)
        self.minConwpSB.setObjectName("minConwpSB")
        self.label_13 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_13.setGeometry(QtCore.QRect(280, 190, 120, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_14.setGeometry(QtCore.QRect(420, 190, 120, 16))
        self.label_14.setObjectName("label_14")
        self.minCongammaSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.minCongammaSB.setGeometry(QtCore.QRect(280, 260, 101, 24))
        self.minCongammaSB.setMaximum(1e+22)
        self.minCongammaSB.setObjectName("minCongammaSB")
        self.label_15 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_15.setGeometry(QtCore.QRect(280, 140, 120, 16))
        self.label_15.setObjectName("label_15")
        self.maxCongammaSB = QtWidgets.QDoubleSpinBox(fitSettingsDialog)
        self.maxCongammaSB.setGeometry(QtCore.QRect(420, 260, 101, 24))
        self.maxCongammaSB.setMaximum(1e+22)
        self.maxCongammaSB.setObjectName("maxCongammaSB")
        self.label_16 = QtWidgets.QLabel(fitSettingsDialog)
        self.label_16.setGeometry(QtCore.QRect(420, 140, 120, 16))
        self.label_16.setObjectName("label_16")

        self.retranslateUi(fitSettingsDialog)
        #self.buttonBox.accepted.connect(fitSettingsDialog.accept)
        #self.buttonBox.rejected.connect(fitSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(fitSettingsDialog)

        #Manually added
        self.buttonBox.accepted.connect(self.OnSave)
        self.buttonBox.rejected.connect(self.OnCancel)
        self.loadCurrentSettings()

    def retranslateUi(self, fitSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        fitSettingsDialog.setWindowTitle(_translate("fitSettingsDialog", "Fit Settings"))
        self.drudeMaxCheckBox.setText(_translate("fitSettingsDialog", "Set maximum for fit parameters."))
        self.label.setText(_translate("fitSettingsDialog", "Min height"))
        self.label_2.setText(_translate("fitSettingsDialog", "Max height"))
        self.label_3.setText(_translate("fitSettingsDialog", "Min de"))
        self.label_4.setText(_translate("fitSettingsDialog", "Max de"))
        self.label_5.setText(_translate("fitSettingsDialog", "Min UV w0**2"))
        self.label_6.setText(_translate("fitSettingsDialog", "Max UV w0**2"))
        self.label_7.setText(_translate("fitSettingsDialog", "Min UV wp**2"))
        self.label_8.setText(_translate("fitSettingsDialog", "Min UV gamma"))
        self.label_9.setText(_translate("fitSettingsDialog", "Max UV wp**2"))
        self.label_10.setText(_translate("fitSettingsDialog", "Max UV gamma"))
        self.label_11.setText(_translate("fitSettingsDialog", "Min Cond. gamma"))
        self.label_12.setText(_translate("fitSettingsDialog", "Max Cond. gamma"))
        self.label_13.setText(_translate("fitSettingsDialog", "Min Cond. wp**2"))
        self.label_14.setText(_translate("fitSettingsDialog", "Max Cond. wp**2"))
        self.label_15.setText(_translate("fitSettingsDialog", "Min Cond. w0**2"))
        self.label_16.setText(_translate("fitSettingsDialog", "Max Cond. w0**2"))
    
    def loadCurrentSettings(self):
        self.drudeMaxCheckBox.setChecked(self.settings.Opt_maxIncluded)
        #self.maxIterationSB.setValue(self.settings.Opt_maxIteration)

        self.minHeightSB.setValue(self.settings.Opt_minheight)
        self.maxHeightSB.setValue(self.settings.Opt_maxheight)

        self.minDeSB.setValue(self.settings.Opt_minde)
        self.maxDeSB.setValue(self.settings.Opt_maxde)

        self.minUVw0SB.setValue(self.settings.Opt_minw0_U)
        self.maxUVw0SB.setValue(self.settings.Opt_maxw0_U)
        self.minUVwpSB.setValue(self.settings.Opt_minwp_U)
        self.maxUVwpSB.setValue(self.settings.Opt_maxwp_U)
        self.minUVgammaSB.setValue(self.settings.Opt_mingamma_U)
        self.maxUVgammaSB.setValue(self.settings.Opt_maxgamma_U)

        self.minConw0SB.setValue(self.settings.Opt_minw0_D)
        self.maxConw0SB.setValue(self.settings.Opt_maxw0_D)
        self.minConwpSB.setValue(self.settings.Opt_minwp_D)
        self.maxConwpSB.setValue(self.settings.Opt_maxwp_D)
        self.minCongammaSB.setValue(self.settings.Opt_mingamma_D)
        self.maxCongammaSB.setValue(self.settings.Opt_maxgamma_D)

    def OnSave(self):
        success = self.save()
        if success:
            self.fitSettingsDialog.close()

    def OnCancel(self):
        self.fitSettingsDialog.close()
    
    def raiseWarningMessage(self, title, error_text):
        choice = QtWidgets.QMessageBox.warning(None, title, error_text, QtWidgets.QMessageBox.Ok)

    def save(self):
        # if self.maxIterationSB.value() < 1:
        #     self.raiseWarningMessage('Error', 'Set iteratations to minimum 1. Settings not saved.')
        #     return False

        if self.drudeMaxCheckBox.isChecked():
            return_value = True
            if self.minHeightSB.value() > self.maxHeightSB.value() or self.minDeSB.value() > self.maxDeSB.value() or self.minUVw0SB.value() > self.maxUVw0SB.value() or self.minUVwpSB.value() > self.maxUVwpSB.value() or self.minUVgammaSB.value() > self.maxUVgammaSB.value() or self.minConw0SB.value() > self.maxConw0SB.value() or self.minConwpSB.value() > self.maxConwpSB.value() or self.minCongammaSB.value() > self.maxCongammaSB.value():
                self.raiseWarningMessage('Error', 'Max value is lower than min value. Settings not saved.')
                return False
        
        #self.settings.Opt_maxIteration = self.maxIterationSB.value()
        self.settings.Opt_maxIncluded = self.drudeMaxCheckBox.isChecked()

        self.settings.Opt_minheight = self.minHeightSB.value()
        self.settings.Opt_maxheight = self.maxHeightSB.value()

        self.settings.Opt_minde = self.minDeSB.value()
        self.settings.Opt_maxde = self.maxDeSB.value()

        self.settings.Opt_minw0_U = self.minUVw0SB.value()
        self.settings.Opt_maxw0_U = self.maxUVw0SB.value()
        self.settings.Opt_minwp_U = self.minUVwpSB.value()
        self.settings.Opt_maxwp_U = self.maxUVwpSB.value()
        self.settings.Opt_mingamma_U = self.minUVgammaSB.value()
        self.settings.Opt_maxgamma_U = self.maxUVgammaSB.value()

        self.settings.Opt_minw0_D = self.minConw0SB.value()
        self.settings.Opt_maxw0_D = self.maxConw0SB.value()
        self.settings.Opt_minwp_D = self.minConwpSB.value()
        self.settings.Opt_maxwp_D = self.maxConwpSB.value()
        self.settings.Opt_mingamma_D = self.minCongammaSB.value()
        self.settings.Opt_maxgamma_D = self.maxCongammaSB.value()
        
        #Write settings to file
        self.settings.saveSettings()
        return True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    fitSettingsDialog = QtWidgets.QDialog()
    ui = Ui_fitSettingsDialog()
    ui.setupUi(fitSettingsDialog)
    fitSettingsDialog.show()
    sys.exit(app.exec_())

