# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generalSettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GeneralSettingsDialog(object):
    def setupUi(self, GeneralSettingsDialog, ui):
        self.settings = ui.settings
        self.ui = ui
        self.GeneralSettingsDialog = GeneralSettingsDialog
        self.GeneralSettingsDialog.setObjectName("GeneralSettingsDialog")
        self.GeneralSettingsDialog.resize(550, 760)
        self.GeneralSettingsDialog.setMinimumSize(QtCore.QSize(550, 760))
        self.verticalLayout = QtWidgets.QVBoxLayout(GeneralSettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(GeneralSettingsDialog)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(10, 6, 151, 16))
        self.label_5.setObjectName("label_5")
        self.excelDBFilePathLineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.excelDBFilePathLineEdit.setGeometry(QtCore.QRect(10, 30, 381, 21))
        self.excelDBFilePathLineEdit.setFocusPolicy(QtCore.Qt.TabFocus)
        self.excelDBFilePathLineEdit.setObjectName("excelDBFilePathLineEdit")
        self.findDB_PB = QtWidgets.QPushButton(self.frame_2)
        self.findDB_PB.setGeometry(QtCore.QRect(400, 25, 113, 32))
        self.findDB_PB.setObjectName("findDB_PB")
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(GeneralSettingsDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setMinimumSize(QtCore.QSize(0, 200))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(0, 25))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.standardWaveTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.standardWaveTextEdit.setMinimumSize(QtCore.QSize(100, 150))
        self.standardWaveTextEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.standardWaveTextEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.standardWaveTextEdit.setObjectName("standardWaveTextEdit")
        self.verticalLayout_3.addWidget(self.standardWaveTextEdit)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.horizontalLayout_2.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setMinimumSize(QtCore.QSize(0, 25))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.includedWaveTextEdit = QtWidgets.QPlainTextEdit(self.widget_2)
        self.includedWaveTextEdit.setMinimumSize(QtCore.QSize(200, 50))
        self.includedWaveTextEdit.setMaximumSize(QtCore.QSize(100, 100))
        self.includedWaveTextEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.includedWaveTextEdit.setObjectName("includedWaveTextEdit")
        self.verticalLayout_4.addWidget(self.includedWaveTextEdit)
        self.label_8 = QtWidgets.QLabel(self.widget_2)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(GeneralSettingsDialog)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setMinimumSize(QtCore.QSize(0, 20))
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.incoherenceFactorSpinBox = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.incoherenceFactorSpinBox.setMinimumSize(QtCore.QSize(0, 25))
        self.incoherenceFactorSpinBox.setMaximumSize(QtCore.QSize(90, 16777215))
        self.incoherenceFactorSpinBox.setMaximum(999.99)
        self.incoherenceFactorSpinBox.setObjectName("incoherenceFactorSpinBox")
        self.gridLayout_2.addWidget(self.incoherenceFactorSpinBox, 1, 2, 1, 1)
        self.incidentAngleSpinBox = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.incidentAngleSpinBox.setMinimumSize(QtCore.QSize(0, 25))
        self.incidentAngleSpinBox.setMaximumSize(QtCore.QSize(90, 16777215))
        self.incidentAngleSpinBox.setMaximum(90.0)
        self.incidentAngleSpinBox.setObjectName("incidentAngleSpinBox")
        self.gridLayout_2.addWidget(self.incidentAngleSpinBox, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setMinimumSize(QtCore.QSize(0, 25))
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(GeneralSettingsDialog)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.absorbCheckBox = QtWidgets.QCheckBox(self.frame_4)
        self.absorbCheckBox.setObjectName("absorbCheckBox")
        self.verticalLayout_2.addWidget(self.absorbCheckBox)
        self.fitModelCurveCheckBox = QtWidgets.QCheckBox(self.frame_4)
        self.fitModelCurveCheckBox.setObjectName("fitModelCurveCheckBox")
        self.verticalLayout_2.addWidget(self.fitModelCurveCheckBox)
        self.verticalLayout.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(GeneralSettingsDialog)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.resetAllPB = QtWidgets.QPushButton(self.frame_5)
        self.resetAllPB.setObjectName("resetAllPB")
        self.horizontalLayout.addWidget(self.resetAllPB)
        self.label_6 = QtWidgets.QLabel(self.frame_5)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.verticalLayout.addWidget(self.frame_5)
        self.buttonBox = QtWidgets.QDialogButtonBox(GeneralSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GeneralSettingsDialog)
        #self.buttonBox.accepted.connect(GeneralSettingsDialog.accept)
        #self.buttonBox.rejected.connect(GeneralSettingsDialog.reject)
        

        self.retranslateUi(GeneralSettingsDialog)
        
        #CODE MANUALLY ADDED
        self.buttonBox.accepted.connect(self.OnSave)
        self.buttonBox.rejected.connect(self.OnCancel)
        QtCore.QMetaObject.connectSlotsByName(GeneralSettingsDialog)

        self.findDB_PB.clicked.connect(self.setDbPath)
        self.resetAllPB.clicked.connect(self.resetAllDialog)
        self.loadCurrentSettings()

    def retranslateUi(self, GeneralSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        GeneralSettingsDialog.setWindowTitle(_translate("GeneralSettingsDialog", "General Settings"))
        self.label_5.setText(_translate("GeneralSettingsDialog", "Default Excel DB file"))
        self.findDB_PB.setText(_translate("GeneralSettingsDialog", "Find..."))
        self.label.setText(_translate("GeneralSettingsDialog", "Standard waves"))
        self.label_7.setText(_translate("GeneralSettingsDialog", "Standard wave lengths (in nm). Ensure all numbers are on a new line."))
        self.label_2.setText(_translate("GeneralSettingsDialog", "Domains of analysis"))
        self.label_8.setText(_translate("GeneralSettingsDialog", "Indicate domains that (standard) wavelengths will be evaluated for fit and error. Multiple domains are possible. Example: \n"
"400 - 800 \n"
"2000 - 2200  "))
        self.label_9.setText(_translate("GeneralSettingsDialog", "If thickness of layer is greater than incoherence factor multiplied by wavelength, layer is regarded incoherent at specific wavelength."))
        self.label_3.setText(_translate("GeneralSettingsDialog", "Incoherence Factor"))
        self.label_4.setText(_translate("GeneralSettingsDialog", "Incident Angle"))
        self.label_10.setText(_translate("GeneralSettingsDialog", "Angle in degrees (˚), 0 to 90˚"))
        self.absorbCheckBox.setText(_translate("GeneralSettingsDialog", "Display absorption curves"))
        self.fitModelCurveCheckBox.setText(_translate("GeneralSettingsDialog", "Display model curves in fit graph"))
        self.resetAllPB.setText(_translate("GeneralSettingsDialog", "Reset All Settings"))
        self.label_6.setText(_translate("GeneralSettingsDialog", "Reset ALL settings. Will generate new settings file upon \'Save\'."))

    def setDbPath(self):
        fileName = self.openFileNameDialog('Set database Excel file')
        if fileName:
            self.excelDBFilePathLineEdit.setText(fileName)

    def openFileNameDialog(self, title):
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, title, "","All Files (*);;Excel Files (*.xlsx)", options=options)
        return fileName

    def loadCurrentSettings(self):
        self.excelDBFilePathLineEdit.setText(self.settings.defaultFile)
        for wvl in self.settings.standard_wave_list:
            self.standardWaveTextEdit.appendPlainText(str(wvl))
        for idx, min_wvl in enumerate(self.settings.domain_min_wvl):
            max_wvl = self.settings.domain_max_wvl[idx]
            domain = '{:g}-{:g}'.format(min_wvl, max_wvl)
            self.includedWaveTextEdit.appendPlainText(domain)
        self.incidentAngleSpinBox.setValue(self.settings.incident_angle)
        self.incoherenceFactorSpinBox.setValue(self.settings.incoherence_factor)
        self.absorbCheckBox.setChecked(self.settings.display_absorbCurve)
        self.fitModelCurveCheckBox.setChecked(self.settings.display_designCurvesInFit)

    def resetAllDialog(self):
        quit_msg = "Are you sure you want reset ALL settings to default values?"
        reply = QtWidgets.QMessageBox.question(None, 'Message', 
                     quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.settings.default()
            self.GeneralSettingsDialog.close()
    
    def save(self):
        import os
        from helperFunctions import is_number
        #Perform all checks
        filePath = self.excelDBFilePathLineEdit.text()
        if not os.path.isfile(filePath):
            self.raiseWarningMessage('Error', 'Invalid default DB file name or location detected. Settings not saved.')
            return False

        waves = self.standardWaveTextEdit.toPlainText()
        waves = waves.replace(" ", "")
        standard_wave_list = waves.split("\n")
        if standard_wave_list[0] == '':
            standard_wave_list = []
        for wave in standard_wave_list:
            if not is_number(wave):
                self.raiseWarningMessage('Error', 'Invalid entry detected in Standard Wave List. Settings not saved.')
                return False
        standard_wave_list = [float(i) for i in standard_wave_list]
       
        text = self.includedWaveTextEdit.toPlainText()
        text = text.replace(" ", "")
        domain_list = text.split("\n")
        domain_min_wvl =[]
        domain_max_wvl =[]
        if not domain_list[0] == '':
            for domain in domain_list:
                d = domain.split("-")
                if not len(d) == 2:
                    self.raiseWarningMessage('Error', 'Invalid entry detected in Domains. Settings not saved.')
                    return False
                elif (not is_number(d[0])) or (not is_number(d[1])):
                    self.raiseWarningMessage('Error', 'Invalid entry detected in Domains. Settings not saved.')
                    return False
                elif float(d[0]) > float(d[1]):
                    self.raiseWarningMessage('Error', 'Invalid entry detected in Domains. Settings not saved.')
                    return False
                domain_min_wvl.append(float(d[0]))
                domain_max_wvl.append(float(d[1]))
            standard_wave_list_mod = self.calculateStandardWaveListModified(standard_wave_list, domain_min_wvl, domain_max_wvl)
            if len(standard_wave_list_mod) < 3:
                self.raiseWarningMessage('Error', 'Total wavelengths in domain have to be more than 2. Settings not saved.')
                return False
        else:
            standard_wave_list_mod = self.settings.standard_wave_list

        
        #Save
        self.settings.defaultFile = filePath
        self.settings.standard_wave_list = standard_wave_list
        self.settings.standard_wave_list_mod = standard_wave_list_mod
        self.settings.domain_min_wvl = domain_min_wvl
        self.settings.domain_max_wvl = domain_max_wvl
        self.settings.incident_angle = self.incidentAngleSpinBox.value()
        self.settings.incoherence_factor = self.incoherenceFactorSpinBox.value()
        self.settings.display_absorbCurve = self.absorbCheckBox.isChecked()
        self.settings.display_designCurvesInFit = self.fitModelCurveCheckBox.isChecked()
        #Write settings to file
        self.settings.saveSettings()
        return True

    def calculateStandardWaveListModified(self, standard_wave_list, domain_min_wvl, domain_max_wvl):
        mod_list = []
        for idx, min_wvl in enumerate(domain_min_wvl):
            max_wvl = domain_max_wvl[idx]
            for i in standard_wave_list:
                if(i >= min_wvl and i <= max_wvl):
                    mod_list.append(i)
        mod_list = list(set(mod_list))
        return sorted(mod_list)
    
    def raiseWarningMessage(self, title, error_text):
        choice = QtWidgets.QMessageBox.warning(None, title, error_text, QtWidgets.QMessageBox.Ok)

    def OnSave(self):
        success = self.save()
        if success:
            self.GeneralSettingsDialog.close()
            self.ui.updateScreens(0)
            self.ui.updateScreens(1)

    def OnCancel(self):
        self.GeneralSettingsDialog.close()

if __name__ == "__main__":
    import sys
    from Settings import Settings
    app = QtWidgets.QApplication(sys.argv)
    GeneralSettingsDialog = QtWidgets.QDialog()
    settings = Settings()
    ui = Ui_GeneralSettingsDialog()
    ui.setupUi(GeneralSettingsDialog, settings)
    test1 = GeneralSettingsDialog.show()
    #GeneralSettingsDialog
    test = app.exec_()
    
    sys.exit(test)


