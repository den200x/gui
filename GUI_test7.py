from PyQt5 import QtCore, QtGui, QtWidgets#, QtWidgets.QFileDialog
#from PyQt5 import *#.QtWidgets import QFileDialog
#from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
#from PyQt5 import QtCore, QtGui, QtWidgets
import pyodbc
import sys, os
import copy
import datetime
import time
import numpy as np
#import see as s
from Threader import StoppableThread
from dateutil import tz
from Settings import Settings

from aboutWindow import Ui_aboutDialog
from colorSettingsWindow import Ui_colorDialog
from connectionSettingsWindow import Ui_connectDialog
from fitSettingsWindow import Ui_fitSettingsDialog
from FitTab import FitTab
from fitTabFunctions import restoreFit
from FunctionsDrude import (
        eq_eU, eq_eD, e_eq,
        mag, phase, leastsq_function, 
        lorentzMag_function, lorentzPhase_function,
        leastsq_functionNK, N_function, K_function)
from FunctionsFit import fit, optimizeDrudeParameters
from FunctionsTRA import (getWaveList, calculateTRA, 
                          addMaterialInfoToStack, calculateRMS, calculateColorValues)
from generalSettingsWindow import Ui_GeneralSettingsDialog
from GUIObjects import GraphFrame, DragDropTableView, TableModel
from helperFunctions import (is_number, getThicknessAndUnit,getThicknessFromString)
from material_input import convert_drude_units, convert_to_inputunits,get_drude_param_range,get_test_param

##d = s.timeTool() #checking      
#print('here we go again=====>setupUi')#checking
##d.datetimeConverter()#checking



class Ui_MainWindow(object):#big ass qt object class holding all the objects which will be randered to ui
    def setupUi(self, MainWindow, stack, settings):
        self.stack = stack
        self.settings = settings
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1230, 716)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setSizeIncrement(QtCore.QSize(1, 1))
        self.tabWidget.setObjectName("tabWidget")
        self.tabBuild = QtWidgets.QWidget()
        self.tabBuild.setObjectName("tabBuild")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tabBuild)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.saveStackPB = QtWidgets.QPushButton(self.tabBuild)
        self.saveStackPB.setObjectName("saveStackPB")
        self.gridLayout_3.addWidget(self.saveStackPB, 1, 0, 1, 1)
        self.deleteLayerPB = QtWidgets.QPushButton(self.tabBuild)
        self.deleteLayerPB.setObjectName("deleteLayerPB")
        self.gridLayout_3.addWidget(self.deleteLayerPB, 1, 1, 1, 1)
        self.loadStackPB = QtWidgets.QPushButton(self.tabBuild)
        self.loadStackPB.setObjectName("loadStackPB")
        self.gridLayout_3.addWidget(self.loadStackPB, 0, 0, 1, 1)
        self.reverseStackPB = QtWidgets.QPushButton(self.tabBuild)
        self.reverseStackPB.setObjectName("reverseStackPB")
        self.gridLayout_3.addWidget(self.reverseStackPB, 0, 2, 1, 1)
        self.addLayerPB = QtWidgets.QPushButton(self.tabBuild)
        self.addLayerPB.setObjectName("addLayerPB")
        self.gridLayout_3.addWidget(self.addLayerPB, 0, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.materialTabWidget = QtWidgets.QTabWidget(self.tabBuild)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.materialTabWidget.sizePolicy().hasHeightForWidth())
        self.materialTabWidget.setSizePolicy(sizePolicy)
        self.materialTabWidget.setObjectName("materialTabWidget")
        self.tabStack = QtWidgets.QWidget()
        self.tabStack.setObjectName("tabStack")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabStack)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.stackListWidget = QtWidgets.QListWidget(self.tabStack)
        self.stackListWidget.setObjectName("stackListWidget")
        self.gridLayout_4.addWidget(self.stackListWidget, 0, 0, 1, 1)
        self.materialTabWidget.addTab(self.tabStack, "")
        self.tabMaterial = QtWidgets.QWidget()
        self.tabMaterial.setObjectName("tabMaterial")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabMaterial)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.materialListWidget = QtWidgets.QListWidget(self.tabMaterial)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.materialListWidget.sizePolicy().hasHeightForWidth())
        self.materialListWidget.setSizePolicy(sizePolicy)
        self.materialListWidget.setObjectName("materialListWidget")
        self.gridLayout_2.addWidget(self.materialListWidget, 0, 0, 1, 1)
        self.materialTabWidget.addTab(self.tabMaterial, "")
        self.verticalLayout_4.addWidget(self.materialTabWidget)
        self.materialDetailTable = QtWidgets.QTableWidget(self.tabBuild)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.materialDetailTable.sizePolicy().hasHeightForWidth())
        self.materialDetailTable.setSizePolicy(sizePolicy)
        self.materialDetailTable.setMinimumSize(QtCore.QSize(200, 220))
        self.materialDetailTable.setMaximumSize(QtCore.QSize(16777215, 220))
        self.materialDetailTable.setAcceptDrops(False)
        self.materialDetailTable.setDragEnabled(True)
        self.materialDetailTable.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.materialDetailTable.setAlternatingRowColors(False)
        self.materialDetailTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.materialDetailTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.materialDetailTable.setShowGrid(True)
        self.materialDetailTable.setObjectName("materialDetailTable")
        self.materialDetailTable.setColumnCount(1)
        self.materialDetailTable.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.materialDetailTable.setItem(5, 0, item)
        self.materialDetailTable.horizontalHeader().setVisible(False)
        self.materialDetailTable.horizontalHeader().setCascadingSectionResizes(False)
        self.materialDetailTable.horizontalHeader().setSortIndicatorShown(False)
        self.materialDetailTable.horizontalHeader().setStretchLastSection(True)
        self.materialDetailTable.verticalHeader().setDefaultSectionSize(33)
        self.materialDetailTable.verticalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.materialDetailTable)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.plotFrame = GraphFrame(self.tabBuild)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plotFrame.sizePolicy().hasHeightForWidth())
        self.plotFrame.setSizePolicy(sizePolicy)
        self.plotFrame.setMinimumSize(QtCore.QSize(800, 361))
        self.plotFrame.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.plotFrame.setAutoFillBackground(True)
        self.plotFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plotFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.plotFrame.setLineWidth(2)
        self.plotFrame.setMidLineWidth(3)
        self.plotFrame.setObjectName("plotFrame")
        self.verticalLayout_7.addWidget(self.plotFrame)
        self.colorTableWidget = QtWidgets.QTableWidget(self.tabBuild)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorTableWidget.sizePolicy().hasHeightForWidth())
        self.colorTableWidget.setSizePolicy(sizePolicy)
        self.colorTableWidget.setMaximumSize(QtCore.QSize(16777215, 61))
        self.colorTableWidget.setAutoFillBackground(True)
        self.colorTableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.colorTableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.colorTableWidget.setAutoScroll(True)
        self.colorTableWidget.setTabKeyNavigation(False)
        self.colorTableWidget.setProperty("showDropIndicator", False)
        self.colorTableWidget.setDragDropOverwriteMode(False)
        self.colorTableWidget.setShowGrid(True)
        self.colorTableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.colorTableWidget.setColumnCount(6)
        self.colorTableWidget.setObjectName("colorTableWidget")
        self.colorTableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorTableWidget.setHorizontalHeaderItem(5, item)
        self.colorTableWidget.horizontalHeader().setVisible(False)
        self.colorTableWidget.horizontalHeader().setHighlightSections(False)
        self.colorTableWidget.verticalHeader().setVisible(True)
        self.colorTableWidget.verticalHeader().setHighlightSections(False)
        self.verticalLayout_7.addWidget(self.colorTableWidget)
        self.designTabBottomFrame = QtWidgets.QFrame(self.tabBuild)
        self.designTabBottomFrame.setMinimumSize(QtCore.QSize(300, 150))
        self.designTabBottomFrame.setAcceptDrops(True)
        self.designTabBottomFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.designTabBottomFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.designTabBottomFrame.setObjectName("designTabBottomFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.designTabBottomFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelLightTop = QtWidgets.QLabel(self.designTabBottomFrame)
        self.labelLightTop.setTextFormat(QtCore.Qt.PlainText)
        self.labelLightTop.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLightTop.setObjectName("labelLightTop")
        self.verticalLayout_2.addWidget(self.labelLightTop)
        self.stackWidget = DragDropTableView(self.designTabBottomFrame, self)
        self.stackWidget.setMaximumSize(QtCore.QSize(380, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.stackWidget.setFont(font)
        self.stackWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.stackWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.stackWidget.setDragEnabled(True)
        self.stackWidget.setDragDropOverwriteMode(False)
        self.stackWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.stackWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.stackWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.stackWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.stackWidget.setObjectName("stackWidget")
        self.stackWidget.horizontalHeader().setDefaultSectionSize(0)
        self.stackWidget.horizontalHeader().setMinimumSectionSize(100)
        self.stackWidget.verticalHeader().setCascadingSectionResizes(True)
        self.stackWidget.verticalHeader().setMinimumSectionSize(16)
        self.verticalLayout_2.addWidget(self.stackWidget)
        self.labelLightBottom = QtWidgets.QLabel(self.designTabBottomFrame)
        self.labelLightBottom.setEnabled(True)
        self.labelLightBottom.setInputMethodHints(QtCore.Qt.ImhNone)
        self.labelLightBottom.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLightBottom.setObjectName("labelLightBottom")
        self.verticalLayout_2.addWidget(self.labelLightBottom)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.stackDetailTable = QtWidgets.QTableWidget(self.designTabBottomFrame)
        self.stackDetailTable.setAutoFillBackground(True)
        self.stackDetailTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.stackDetailTable.setObjectName("stackDetailTable")
        self.stackDetailTable.setColumnCount(1)
        self.stackDetailTable.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.stackDetailTable.setHorizontalHeaderItem(0, item)
        self.stackDetailTable.horizontalHeader().setVisible(False)
        self.stackDetailTable.horizontalHeader().setDefaultSectionSize(100)
        self.stackDetailTable.horizontalHeader().setStretchLastSection(True)
        self.stackDetailTable.verticalHeader().setCascadingSectionResizes(True)
        self.stackDetailTable.verticalHeader().setDefaultSectionSize(27)
        self.stackDetailTable.verticalHeader().setMinimumSectionSize(20)
        self.stackDetailTable.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.stackDetailTable)
        self.verticalLayout_7.addWidget(self.designTabBottomFrame)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.tabWidget.addTab(self.tabBuild, "")
        self.tabFit = QtWidgets.QWidget()
        self.tabFit.setObjectName("tabFit")
        self.gridLayout = QtWidgets.QGridLayout(self.tabFit)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plotFitFrame = GraphFrame(self.tabFit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotFitFrame.sizePolicy().hasHeightForWidth())
        self.plotFitFrame.setSizePolicy(sizePolicy)
        self.plotFitFrame.setMinimumSize(QtCore.QSize(400, 300))
        self.plotFitFrame.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.plotFitFrame.setAutoFillBackground(True)
        self.plotFitFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plotFitFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.plotFitFrame.setLineWidth(2)
        self.plotFitFrame.setMidLineWidth(3)
        self.plotFitFrame.setObjectName("plotFitFrame")
        self.gridLayout.addWidget(self.plotFitFrame, 0, 1, 1, 1)
        #self.gridLayout.addWidget(self.plotFitFrame)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fitTableWidget = QtWidgets.QTableWidget(self.tabFit)
        self.fitTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.fitTableWidget.setObjectName("fitTableWidget")
        self.fitTableWidget.setColumnCount(7)
        self.fitTableWidget.setRowCount(14)
        self.fitTableWidget.setMaximumSize(QtCore.QSize(16777215, 360))
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.fitTableWidget.setHorizontalHeaderItem(6, item)
        self.fitTableWidget.horizontalHeader().setVisible(False)
        self.fitTableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.fitTableWidget.horizontalHeader().setMinimumSectionSize(15)
        self.fitTableWidget.verticalHeader().setDefaultSectionSize(22)
        self.fitTableWidget.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout_2.addWidget(self.fitTableWidget)
        self.colorFitTableWidget = QtWidgets.QTableWidget(self.tabFit)
        self.colorFitTableWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.colorFitTableWidget.setMaximumSize(QtCore.QSize(200, 360))
        self.colorFitTableWidget.setObjectName("tableWidget")
        self.colorFitTableWidget.setColumnCount(2)
        self.colorFitTableWidget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.colorFitTableWidget.setHorizontalHeaderItem(1, item)
        self.colorFitTableWidget.horizontalHeader().setVisible(True)
        self.colorFitTableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.colorFitTableWidget)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.deviceComboBox = QtWidgets.QComboBox(self.tabFit)
        self.deviceComboBox.setObjectName("deviceComboBox")
        self.verticalLayout_5.addWidget(self.deviceComboBox)
        self.onlinePB = QtWidgets.QPushButton(self.tabFit)
        self.onlinePB.setObjectName("onlinePB")
        self.verticalLayout_5.addWidget(self.onlinePB)
        self.selectParamPB = QtWidgets.QPushButton(self.tabFit)
        self.selectParamPB.setObjectName("selectParamPB")
        self.verticalLayout_5.addWidget(self.selectParamPB)
        self.fitPB = QtWidgets.QPushButton(self.tabFit)
        self.fitPB.setObjectName("fitPB")
        self.verticalLayout_5.addWidget(self.fitPB)
        self.restoreFitPB = QtWidgets.QPushButton(self.tabFit)
        self.restoreFitPB.setToolTip("")
        self.restoreFitPB.setObjectName("restoreFitPB")
        self.verticalLayout_5.addWidget(self.restoreFitPB)
        self.reportFitPB = QtWidgets.QPushButton(self.tabFit)
        self.reportFitPB.setObjectName("reportFitPB")
        self.verticalLayout_5.addWidget(self.reportFitPB)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabFit, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1230, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Stack = QtWidgets.QAction(MainWindow)
        self.actionOpen_Stack.setObjectName("actionOpen_Stack")
        self.actionOpen_Material = QtWidgets.QAction(MainWindow)
        self.actionOpen_Material.setObjectName("actionOpen_Material")
        self.actionSave_Stack = QtWidgets.QAction(MainWindow)
        self.actionSave_Stack.setObjectName("actionSave_Stack")
        self.actionConnections = QtWidgets.QAction(MainWindow)
        self.actionConnections.setObjectName("actionConnections")
        self.actionFit = QtWidgets.QAction(MainWindow)
        self.actionFit.setObjectName("actionFit")
        self.actionDeleteStack = QtWidgets.QAction(MainWindow)
        self.actionDeleteStack.setObjectName("actionDeleteStack")
        self.actionReload_DBs = QtWidgets.QAction(MainWindow)
        self.actionReload_DBs.setObjectName("actionReload_DBs")
        self.actionInstructions = QtWidgets.QAction(MainWindow)
        self.actionInstructions.setObjectName("actionInstructions")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionGeneral = QtWidgets.QAction(MainWindow)
        self.actionGeneral.setObjectName("actionGeneral")
        self.actionFit_Turn_all_On_Off = QtWidgets.QAction(MainWindow)
        self.actionFit_Turn_all_On_Off.setObjectName("actionFit_Turn_all_On_Off")
        self.actionColor = QtWidgets.QAction(MainWindow)
        self.actionColor.setObjectName("actionColor")
        self.menuFile.addAction(self.actionOpen_Stack)
        self.menuFile.addAction(self.actionOpen_Material)
        self.menuFile.addAction(self.actionSave_Stack)
        self.menuEdit.addAction(self.actionDeleteStack)
        self.menuEdit.addAction(self.actionReload_DBs)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFit_Turn_all_On_Off)
        self.menuSettings.addAction(self.actionGeneral)
        self.menuSettings.addAction(self.actionColor)
        self.menuSettings.addAction(self.actionFit)
        self.menuSettings.addAction(self.actionConnections)
        self.menuHelp.addAction(self.actionInstructions)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.materialTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.plotFrame.setContentsMargins(0,0,0,0)
        self.plotFitFrame.setContentsMargins(0,0,0,0)
        self.menubar.setNativeMenuBar(False) #FOR MAC
        #FILE
        self.actionSave_Stack.triggered.connect(self.saveStack)
        self.actionOpen_Stack.triggered.connect(self.addStacksToDB)
        self.actionOpen_Material.triggered.connect(self.addMaterialToDB)
        #EDIT
        self.actionDeleteStack.triggered.connect(self.removeCompleteStack)
        self.actionReload_DBs.triggered.connect(self.reload_DBs)
        self.actionFit_Turn_all_On_Off.triggered.connect(self.fit_Turn_all_On_Off)
        #SETTINGS
        self.actionGeneral.triggered.connect(self.openGeneralSettingsWindow)
        self.actionFit.triggered.connect(self.openFitSettingsWindow)
        self.actionColor.triggered.connect(self.openColorSettingsWindow)
        self.actionConnections.triggered.connect(self.openConnectWindow)
        self.actionAbout.triggered.connect(self.openAboutWindow)

    ##d.processingTime()#checking
  
    def openGeneralSettingsWindow(self):
        ##print('here we go again=====>openGeneralSettingsWindow')#checking
        ###d.datetimeConverter()#checking
        self.generalDialog = QtWidgets.QDialog()
        self.uiGeneralDialog = Ui_GeneralSettingsDialog()
        self.uiGeneralDialog.setupUi(self.generalDialog, self)
        self.generalDialog.show()
        ###d.processingTime()#checking
    def openColorSettingsWindow(self):
        ##print('here we go again=====>openColorSettingsWindow')#checking
        ###d.datetimeConverter()#checking
        self.colorDialog = QtWidgets.QDialog()
        self.uiColorDialog = Ui_colorDialog()
        self.uiColorDialog.setupUi(self.colorDialog, self)
        self.colorDialog.show()
        ###d.processingTime()#checking

    def openFitSettingsWindow(self):
        ##print('here we go again=====>openFitSettingsWindow')#checking
        ###d.datetimeConverter()#checking
        self.fitDialog = QtWidgets.QDialog()
        self.uiFitDialog = Ui_fitSettingsDialog()
        self.uiFitDialog.setupUi(self.fitDialog, self)
        self.fitDialog.show()
        ###d.processingTime()#checking

    def openConnectWindow(self):
        ##print('here we go again=====>openConnectWindow')#checking
        ###d.datetimeConverter()#checking
        self.connectDialog = QtWidgets.QDialog()
        self.uiConnectDialog = Ui_connectDialog()
        self.uiConnectDialog.setupUi(self.connectDialog, self)
        self.connectDialog.show()
        ###d.processingTime()#checking
    
    def openAboutWindow(self):
        ##print('here we go again=====>openAboutWindow')#checking
        ###d.datetimeConverter()#checking
        self.aboutDialog = QtWidgets.QDialog()
        self.uiAboutDialog = Ui_aboutDialog()
        self.uiAboutDialog.setupUi(self.aboutDialog)
        self.aboutDialog.show()
        ###d.processingTime()#checking

    def retranslateUi(self, MainWindow):
        ##print('here we go again=====>retranslateUi')#checking
        ###d.datetimeConverter()#checking
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TOMware"))
        self.saveStackPB.setText(_translate("MainWindow", "Save Stack"))
        self.deleteLayerPB.setText(_translate("MainWindow", "Delete Layer"))
        self.loadStackPB.setText(_translate("MainWindow", "Load Stack"))
        self.reverseStackPB.setText(_translate("MainWindow", "Reverse Stack"))
        self.addLayerPB.setText(_translate("MainWindow", "Add Material"))
        self.materialTabWidget.setTabText(self.materialTabWidget.indexOf(self.tabStack), _translate("MainWindow", "Stacks"))
        self.materialTabWidget.setTabText(self.materialTabWidget.indexOf(self.tabMaterial), _translate("MainWindow", "Materials"))
        item = self.materialDetailTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.materialDetailTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Details"))
        item = self.materialDetailTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Material"))
        item = self.materialDetailTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Thickness"))
        item = self.materialDetailTable.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Model"))
        item = self.materialDetailTable.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Comments"))
        item = self.materialDetailTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        __sortingEnabled = self.materialDetailTable.isSortingEnabled()
        self.materialDetailTable.setSortingEnabled(False)
        item = self.materialDetailTable.item(0, 0)
        item.setText(_translate("MainWindow", "Ag-SiO2-TiO2-HB3"))
        item = self.materialDetailTable.item(1, 0)
        item.setText(_translate("MainWindow", "5"))
        item = self.materialDetailTable.item(2, 0)
        item.setText(_translate("MainWindow", "Ag (version 112017)"))
        item = self.materialDetailTable.item(3, 0)
        item.setText(_translate("MainWindow", "20 nm"))
        item = self.materialDetailTable.item(4, 0)
        item.setText(_translate("MainWindow", "Drude"))
        item = self.materialDetailTable.item(5, 0)
        item.setText(_translate("MainWindow", "N: 1.3, K: -1"))
        self.materialDetailTable.setSortingEnabled(__sortingEnabled)
        item = self.colorTableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Transmission"))
        item = self.colorTableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Reflection"))
        item = self.colorTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.colorTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.colorTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.colorTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.colorTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.colorTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Column"))
        self.labelLightTop.setText(_translate("MainWindow", "Light enters here at 2˚"))
        self.labelLightBottom.setText(_translate("MainWindow", "Light enters here at 2˚"))
        item = self.stackDetailTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.stackDetailTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Stack"))
        item = self.stackDetailTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Stack Count"))
        item = self.stackDetailTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Layer #"))
        item = self.stackDetailTable.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Material"))
        item = self.stackDetailTable.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Thickness"))
        item = self.stackDetailTable.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Index @ 550 nm"))
        item = self.stackDetailTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBuild), _translate("MainWindow", "Build"))
        item = self.fitTableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Material"))
        item = self.fitTableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Layer #"))
        item = self.fitTableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        item = self.fitTableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Target Height"))
        item = self.fitTableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Actual Height"))
        item = self.fitTableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "de"))
        item = self.fitTableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "UV oscil. freq. ω0^2"))
        item = self.fitTableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "UV oscil. strength ωp^2"))
        item = self.fitTableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "UV line width γ"))
        item = self.fitTableWidget.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "Cond. oscil. freq. ω0^2"))
        item = self.fitTableWidget.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "Cond. oscil. strength ωp^2"))
        item = self.fitTableWidget.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "Cond. line width γ"))
        item = self.fitTableWidget.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "N,K @ 550 nm"))
        item = self.fitTableWidget.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "Edit"))
        item = self.fitTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.fitTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.fitTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.fitTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.fitTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.fitTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.fitTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.colorFitTableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.colorFitTableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.colorFitTableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.colorFitTableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.colorFitTableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.colorFitTableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.colorFitTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Tranmission"))
        item = self.colorFitTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Reflection"))
        self.onlinePB.setText(_translate("MainWindow", "Go Online"))
        self.selectParamPB.setText(_translate("MainWindow", "Select Fit Param"))
        self.fitPB.setText(_translate("MainWindow", "Fit"))
        self.restoreFitPB.setText(_translate("MainWindow", "Restore Fit"))
        self.reportFitPB.setText(_translate("MainWindow", "Report of Run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFit), _translate("MainWindow", "Fit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen_Stack.setText(_translate("MainWindow", "Add Stack File"))
        self.actionOpen_Material.setText(_translate("MainWindow", "Add Material File"))
        self.actionSave_Stack.setText(_translate("MainWindow", "Save Stack"))
        self.actionConnections.setText(_translate("MainWindow", "Connections"))
        self.actionFit.setText(_translate("MainWindow", "Fit"))
        self.actionDeleteStack.setText(_translate("MainWindow", "Delete Entire Stack"))
        self.actionDeleteStack.setIconText(_translate("MainWindow", "Delete Entire Stack"))
        self.actionDeleteStack.setToolTip(_translate("MainWindow", "Delete Entire Stack. <Shift + Del> over visual stack performs same action."))
        self.actionReload_DBs.setText(_translate("MainWindow", "Reload DBs"))
        self.actionInstructions.setText(_translate("MainWindow", "Instructions"))
        self.actionAbout.setText(_translate("MainWindow", "About..."))
        self.actionGeneral.setText(_translate("MainWindow", "General"))
        self.actionFit_Turn_all_On_Off.setText(_translate("MainWindow", "Fit - Turn all \'On\' / \'Off\'"))
        self.actionFit_Turn_all_On_Off.setToolTip(_translate("MainWindow", "Turns status all layers to \'On\' or \'Off\'"))
        self.actionColor.setText(_translate("MainWindow", "Color"))

#***************************************
        #CHANGE QtWidgets.QFrame to GraphFrame
        #CHANGE self.plotFitFrame = GraphFrame(self.tabFit)
        #CHANGE self.stackWidget = DragDropTableView(self.designTabBottomFrame, self) FROM self.stackWidget = QtWidgets.QTableView(self.frame)
        
        #REMOVE lableLightTop and Bottom labels from original QT Builder file.
        #ADD self.plotFrame.setContentsMargins(0,0,0,0)
        #ADD self.menubar.setNativeMenuBar(False) #FOR MAC
        #ADD stack to def setupUi(self, MainWindow, stack):
        #ADD self.stack = stack in SetupUi()
        #ADD self.MainWindow = MainWindow in SetupUi()

        MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.labelLightTop.setText(_translate("MainWindow", "Light enters here at {}˚".format(self.settings.incident_angle)))
        self.labelLightBottom.setText(_translate("MainWindow", "Light enters here at {}˚".format(self.settings.incident_angle)))
        self.activeLayer = None
        #Design tab
        self.labelLightTop.setVisible(not self.stack.REVERSE_STACK)
        self.labelLightBottom.setVisible(self.stack.REVERSE_STACK)
        self.loadStackPB.clicked.connect(self.loadStack)
        self.saveStackPB.clicked.connect(self.saveStack)
        self.addLayerPB.clicked.connect(self.addMaterialToStack)
        self.deleteLayerPB.clicked.connect(self.removeMaterialFromStack)
        self.reverseStackPB.clicked.connect(self.reverseStack)
        self.stackDetailTable.itemChanged.connect(self.changeInStackDetails)
        self.materialListWidget.currentRowChanged.connect(self.updateMaterialDBDetailTable)
        self.stackListWidget.currentRowChanged.connect(self.updateStackDBDetailTable)
        self.materialTabWidget.currentChanged.connect(self.enableStackMaterialPB)
        self.tabWidget.currentChanged.connect(self.updateScreens)

        header = self.colorTableWidget.horizontalHeader()
        for i in range(self.colorTableWidget.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        
        header = self.stackDetailTable.verticalHeader()
        for i in range(self.stackDetailTable.rowCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        
        header = self.materialDetailTable.verticalHeader()
        for i in range(self.materialDetailTable.rowCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.fitTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        
        #Fit tab
        self.fitTab = FitTab(self)
        self.restoreFitPB.clicked.connect(self.fitTab.restoreFit)
        self.onlinePB.clicked.connect(self.checkOnlineStatus)
        self.parameterMode = False
        self.selectParamPB.clicked.connect(self.fitTab.selectFitParametersMode)
        self.fitPB.clicked.connect(self.initiateFit)

        for device in self.settings.device_list:
            self.deviceComboBox.addItem(device)
        self.deviceComboBox.setCurrentIndex(0)
        self.deviceComboBox.activated[str].connect(self.deviceSelect)
       
        self.enableStackMaterialPB(0)
        #self.buttonGroup = QtWidgets.QButtonGroup()
        #self.buttonGroup.buttonClicked[int].connect(self.lockEditModeForFit)
        self.updateDesignGraph(self.stack)
        ###d.processingTime()#checking
    
    def deviceSelect(self, txt):
        self.settings.device_select = txt
    
    
    def initiateFit(self):
        ##print('here we go again=====>openGeneralSettingsWindow')#checking

        ###d.datetimeConverter()#checking
        if any(mat.fitStatus == True for mat in self.stack.material):
            if any(any(mat.fit_param.values()) and mat.fitStatus for mat in self.stack.material):
                if any(mat.editMode for mat in self.stack.material):
                    self.fitTableWidget.itemChanged.disconnect(self.fitTab.storeFitParameters)
                self.stack = fit(self.stack, self.settings)
                self.fitTab.loadFitParameters(self.stack)
                self.fitTab.updateFitGraph(self.stack)
                self.fitTab.updateFitColorDataToTable(self.stack)
                if any(mat.editMode for mat in self.stack.material):
                    self.fitTableWidget.itemChanged.connect(self.fitTab.storeFitParameters)
            else:
                self.raiseWarningMessage('No fit parameters selected.', 'Please select 1 to 7 fit parameters in an enabled layer.') 
        else:
            self.raiseWarningMessage('No layer is enabled for fit.', 'Please enable at least one layer for fit.')
        ###d.processingTime()#checking

    def updateScreens(self, e):
        ##print('here we go again=====>updateScreens')#checking

        ###d.datetimeConverter()#checking
        if e == 1: #when main tab is changed to 'Fit'
            self.fitTab.loadFitTableWidget(self.stack)
            self.fitTab.updateFitGraph(self.stack)
            self.fitTab.updateFitColorDataToTable(self.stack)
        if e == 0:
            try:
                self.fitTableWidget.itemChanged.disconnect(self.fitTab.storeFitParameters)
            except TypeError:
                pass
            for mat in self.stack.material:
                mat.editMode = False
            self.updateDesignGraph(self.stack)
            self.updateStackDetailTable(0, self.stack)
        ###d.processingTime()#checking

    def updateMaterialDBDetailTable(self):
        ##print('here we go again=====>updateMaterialDBDetailTable')#checking

        ###d.datetimeConverter()#checking
        '''Function to update detail table when a material from DB is selected'''
        def writeNonEditableInfo(row, col, info):
            if not isinstance(info, str):
                info = '-'
            item = QtWidgets.QTableWidgetItem(info)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.materialDetailTable.setItem(row, col, item)

        row = self.materialListWidget.currentRow()
        mat = self.material_db[row]

        self.materialDetailTable.verticalHeaderItem(0).setText('Name')
        if mat.version == '':
            version = '-'
        else:
            version = mat.version
        writeNonEditableInfo(0,0, '{} (version: {}, date: {})'.format(mat.name, version, mat.date))

        self.materialDetailTable.verticalHeaderItem(1).setText('Thickness (std.)')
        thickness_text = getThicknessAndUnit(mat.standard_thickness)
        writeNonEditableInfo(1,0, thickness_text)

        self.materialDetailTable.verticalHeaderItem(2).setText('Model')
        item = QtWidgets.QTableWidgetItem('{}'.format(mat.model))
        if mat.model == 'drude':
            item.setToolTip('''Dielectric constant de: {:5.3f}\n\nUV band:\nOscil. freq ω0^2: {:6.2f}\nOscil. strength ωp^2: {:6.2f}\nLinewidth gamma: {:6.4f}\n\nConduction band:\nOscil. freq ω0^2: {:6.2f}\nOscil. strength ωp^2: {:6.2f}\nLinewidth gamma: {:6.4f}'''.format(*mat.getDrudeParamsForPrint()))
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
        self.materialDetailTable.setItem(2, 0, item)

        self.materialDetailTable.verticalHeaderItem(3).setText('Source')
        writeNonEditableInfo(3,0, mat.source)

        try:
            n = float(mat.get_NKspline_value('N', 550))
            k = float(mat.get_NKspline_value('K', 550))
            infoNK = 'n: {:5.3f}, k: {:6.3f}'.format(n,k)
        except ValueError:
            infoNK = 'n: -, k: -'
        self.materialDetailTable.verticalHeaderItem(4).setText('Index @ 550 nm')
        writeNonEditableInfo(4,0, infoNK)

        self.materialDetailTable.verticalHeaderItem(5).setText('Comments')
        self.materialDetailTable.setItem(5, 0, QtWidgets.QTableWidgetItem('{}'.format(mat.comment)))

        columnCount = self.materialDetailTable.columnCount()
        header = self.materialDetailTable.verticalHeader()
        for i in range(columnCount):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        ###d.processingTime()#checking

    def updateStackDBDetailTable(self):
        ##print('here we go again=====>updateStackDBDetailTable')#checking

        ###d.datetimeConverter()#checking
        '''Function to update detail table when a stack from DB is selected'''
        def writeNonEditableInfo(row, col, info):
            if not isinstance(info, str):
                info = '-'
            item = QtWidgets.QTableWidgetItem(info)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.materialDetailTable.setItem(row, col, item)

        row = self.stackListWidget.currentRow()
        stack = self.stack_db[row]
        self.materialDetailTable.verticalHeaderItem(0).setText('Name')
        writeNonEditableInfo(0,0, stack.name)
        self.materialDetailTable.verticalHeaderItem(1).setText('Layers')
        writeNonEditableInfo(1,0,'-'.join(stack.layers))
        self.materialDetailTable.verticalHeaderItem(2).setText('Thickness')
        t_list = '-'.join(str(x) for x in stack.thickness)
        writeNonEditableInfo(2,0,t_list)
        self.materialDetailTable.verticalHeaderItem(3).setText('Source')
        writeNonEditableInfo(3,0,stack.source)
        self.materialDetailTable.verticalHeaderItem(4).setText('Date')
        writeNonEditableInfo(4,0,stack.date)
        self.materialDetailTable.verticalHeaderItem(5).setText('Comments')
        writeNonEditableInfo(5,0,stack.comment)

        columnCount = self.materialDetailTable.columnCount()
        header = self.materialDetailTable.verticalHeader()
        for i in range(columnCount):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        ##d.processingTime()#checking

    def enableStackMaterialPB(self, e):
        #print('here we go again=====> enableStackMaterialPB')#checking

        ###d.datetimeConverter()#checking
        if e == 0:
            self.loadStackPB.setEnabled(True)
            self.addLayerPB.setEnabled(False) 
        elif e == 1:
            self.loadStackPB.setEnabled(False)
            self.addLayerPB.setEnabled(True)
        ##d.processingTime()#checking

    def changeInStackDetails(self, e):
        #print('here we go again=====>changeInStackDetails')#checking

        ##d.datetimeConverter()#checking
        row = self.stackDetailTable.currentItem().row()
        t = None
        text = self.stackDetailTable.currentItem().text()
        #Change name of stack
        if row == 0:
            self.stack.name = text
        #Change layer number
        if row == 3:
            data = text.split()
        

            if is_number(text) and self.stack.layer_count() > (int(text) - 1):
                self.updateStackDetailTable(int(text) - 1, self.stack)
            #enable function to write layer to other location in stack by 'X to Y'
            elif len(data) == 3 and data[1] == 'to' and is_number(data[0]) and is_number(data[2]):
                self.rearrangeStackTable(int(data[0])-1, int(data[2])-1, self.stack)
            else: #restore original values in table.
                self.updateStackDetailTable(self.activeLayer, self.stack)
        #Change thickness
        elif row == 5:
            if self.stack.material[self.activeLayer].type == 'lbl':
                text += 'l'
            t = getThicknessFromString(text)
            if not t == None:
                # update stack
                self.stack.thickness[self.activeLayer] = t
                #REMOVE AFTER TESTING COMPLETE
                self.stack.material[self.activeLayer].actual_thickness = t
            #update stackDetailTable
            self.updateStackDetailTable(self.activeLayer, self.stack)
        #Update graph and stack
        self.populateStackWidget(self.stack)
        self.updateDesignGraph(self.stack)
        ##d.processingTime()#checking

    def reverseStack(self):
        #print('here we go again=====>reverseStack')#checking

        ##d.datetimeConverter()#checking
        if self.stack.REVERSE_STACK:
            self.stack.REVERSE_STACK = False
        else:
            self.stack.REVERSE_STACK = True
        self.labelLightTop.setVisible(not self.stack.REVERSE_STACK)
        self.labelLightBottom.setVisible(self.stack.REVERSE_STACK)
        self.updateDesignGraph(self.stack)
        self.updateStackDetailTable(0, self.stack)
        ##d.processingTime()#checking

    def populateStackDBList(self, stackList):
        #print('here we go again=====>populateStackDBList')#checking

        ##d.datetimeConverter()#checking
        self.stack_db = stackList
        self.stackListWidget.clear()
        for i in stackList:
            self.stackListWidget.addItem(i.name)
        ##d.processingTime()#checking

    def populateMaterialDBList(self, materialList):
        #print('here we go again=====>populateMaterialDBList')#checking

        ##d.datetimeConverter()#checking
        self.material_db = materialList
        self.materialListWidget.clear()
        for i in materialList:
            self.materialListWidget.addItem('{} ({})'.format(i.name, i.model))
        ##d.processingTime()#checking

    def populateStackWidget(self, stack):
        #print('here we go again=====> populateStackWidget')#checking

        ##d.datetimeConverter()#checking
        #self.stackWidget.setRowCount(0)
        self.stackWidget.model = TableModel()
        self.stackWidget.setModel(self.stackWidget.model)
        #widgetItem = QtWidgets.QTableWidgetItem(str(stack.layer_count()))
        for idx in range(len(stack.layers)):
            thickness_text = getThicknessAndUnit(stack.thickness[idx])
            model = stack.material[idx].model
            item = QtGui.QStandardItem('{} - {} ({})'.format(stack.layers[idx], thickness_text, model))
            item.setEditable(False)
            item.setDropEnabled(False)
            item.setBackground(stack.material[idx].color)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            
            if  not isinstance(stack.thickness[idx], str):
                height = stack.thickness[idx]/3 if stack.thickness[idx] < 150 else 50
            else:
                height = 10
            item.setSizeHint(QtCore.QSize(1,height))
           
            self.stackWidget.model.appendRow([item])
        ##d.processingTime()#checking
                
    def addMaterialToStack(self):
        #print('here we go again=====>addMaterialToStack')#checking

        ##d.datetimeConverter()#checking
        currentRow = self.materialListWidget.currentRow()
        if currentRow > -1:
            selectedMaterial = self.material_db[currentRow]
            self.stack.addMaterialToStack(selectedMaterial)
            self.populateStackWidget(self.stack)
            self.updateDesignGraph(self.stack)
            self.updateStackDetailTable(0, self.stack)
        ##d.processingTime()#checking

    def removeMaterialFromStack(self):
        #print('here we go again=====>removeMaterialFromStack')#checking

        ##d.datetimeConverter()#checking
        idx = self.activeLayer
        if not idx == None and idx > -1:
            self.stack.removeMaterialFromStack(idx)
            self.populateStackWidget(self.stack)
            idx = idx - 1
            self.populateStackWidget(self.stack)
            self.updateDesignGraph(self.stack)
            self.updateStackDetailTable(idx, self.stack)
        ##d.processingTime()#checking

    def removeCompleteStack(self):
        
        self.stack = Stack()
        self.populateStackWidget(self.stack)
        self.updateDesignGraph(self.stack)
        self.updateStackDetailTable(0, self.stack)
        self.updateScreens(1) #Quick way to update Fit Screen.
        

    def updateStackDetailTable(self, layer_idx, stack = None):
        #print('here we go again=====>updateStackDetailTable')#checking

        ##d.datetimeConverter()#checking
        def writeNonEditableInfo(info, row):
            item = QtWidgets.QTableWidgetItem(info)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(211,211,211,70))
            self.stackDetailTable.setItem(row, 0, item)
        #temporarily remove connection to stackDetailTable to prevent looping
        self.stackDetailTable.itemChanged.disconnect(self.changeInStackDetails)
        if stack == None:
            stack = self.stack
        self.activeLayer = layer_idx
    
        #Name
        self.stackDetailTable.setItem(0, 0, QtWidgets.QTableWidgetItem(stack.name))

        #Layer info
        info = '{}'.format('-'.join(stack.layers))
        writeNonEditableInfo(info, 1)
    
        #Set Layer count
        info = '' if stack.isEmpty() else str(stack.layer_count())
        writeNonEditableInfo(info, 2)

        #Set selected layer
        info = '' if stack.isEmpty() else "{}".format(layer_idx + 1)
        self.stackDetailTable.setItem(3, 0, QtWidgets.QTableWidgetItem(info))

        #Set material
        if not stack.isEmpty():
            mat = stack.material[layer_idx]
            if mat.version == '':
                version = '-'
            else:
                version = mat.version
            info = "{} ({}, version: {})".format(mat.name, mat.model, version) 
            try:
                n = float(mat.get_NKspline_value('N', 550))
                k = float(mat.get_NKspline_value('K', 550))
                infoNK = 'n: {:5.3f}, k: {:6.3f}'.format(n,k)
            except ValueError:
                infoNK = 'n: -, k: -'
        else:
            info = ''
            infoNK = 'n: -, k: -'
        writeNonEditableInfo(info, 4)
                
        #Write thickness
        if not stack.isEmpty():
            info = getThicknessAndUnit(stack.thickness[layer_idx])
        else:
            info = ''
        self.stackDetailTable.setItem(5, 0, QtWidgets.QTableWidgetItem(info))
        writeNonEditableInfo(infoNK, 6)
        self.stackDetailTable.itemChanged.connect(self.changeInStackDetails)
        ##d.processingTime()#checking

    def rearrangeStackTable(self, dragLocation, dropLocation, stack):
        #print('here we go again=====>rearrangeStackTable')#checking

        ##d.datetimeConverter()#checking
        '''Function rearranges stack based upon drag and drop location in widget'''
        lastRowIdx = len(stack.layers) - 1
        if dropLocation > lastRowIdx:
            dropLocation = lastRowIdx
        stack.material.insert(dropLocation, stack.material.pop(dragLocation))
        stack.thickness.insert(dropLocation, stack.thickness.pop(dragLocation))
        stack.layers.insert(dropLocation, stack.layers.pop(dragLocation))
        self.updateDesignGraph(self.stack)
        self.updateStackDetailTable(0, self.stack)
        self.populateStackWidget(self.stack)
        ##d.processingTime()#checking
    
    #print('here we go again=====>updateDesignGraph')#checking

    #d.datetimeConverter()#checking
    def updateDesignGraph(self, stack):
        
        '''Function updates TRA plot in Design tab'''
        stack.RMSerror = ''
        if stack.isEmpty():
            stack.fit_wvl = self.settings.standard_wave_list
        else:
            #Calculate fitted splines
            stack.fit_wvl = getWaveList(stack, self.settings.standard_wave_list_mod)
            #This parameters determines if curve is calculated based on theoretical thickness or estimated actual thickness
            ActualThicknessCurve = False
            stack.designT, stack.designR, stack.designA = calculateTRA(stack, 'design', stack.fitting_layer, self.settings.incident_angle, self.settings.incoherence_factor, ActualThicknessCurve, stack.REVERSE_STACK)
            stack.setTRAsplines(stack.fit_wvl, type = 'design')

            #Calculate original splines
            if not len(stack.excelT) == 0:
                stack.setTRAsplines(stack.excel_wvl, type = 'original')
                stack.RMSerror = calculateRMS(stack.spline_excelT(stack.fit_wvl), stack.spline_excelR(stack.fit_wvl), stack.spline_designT(stack.fit_wvl), stack.spline_designR(stack.fit_wvl))
        self.plotFrame.graph_view.plot_designGraph(stack.fit_wvl, stack, self.settings)
        self.updateColorDataToTable(stack)
        ##d.processingTime()#checking

    def updateColorDataToTable(self, stack):
        #print('here we go again=====>updateColorDataToTable')#checking

        ###d.datetimeConverter()#checking
        '''Function calculates color parameters and writes to table colorTableWidget in Design Tab'''
        def writeNonEditableInfo(info, row, col):
            item = QtWidgets.QTableWidgetItem(info)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            #item.setBackground(QtGui.QColor(211,211,211,70))
            self.colorTableWidget.setItem(row, col, item)
        
        rowCount = self.colorTableWidget.rowCount()
        columnCount = self.colorTableWidget.columnCount()

        if not stack.isEmpty():
            header = self.colorTableWidget.horizontalHeader()
            for i in range(columnCount):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

            T_XYZ, T_xy, T_ab, T_rgb, R_XYZ, R_xy, R_ab, R_rgb = calculateColorValues(stack.spline_designT, stack.spline_designR, self.settings)
        
            Tv = T_XYZ[1]
            writeNonEditableInfo('v: {:.3f}%'.format(Tv), 0,0)
            Tx = T_xy[0]
            writeNonEditableInfo('x: {:.3f}'.format(Tx), 0,1)
            Ty = T_xy[1]
            writeNonEditableInfo('y: {:.3f}'.format(Ty), 0,2)
            Ta = T_ab[1]
            writeNonEditableInfo('a*: {:.3f}'.format(Ta), 0,3)
            Tb = T_ab[2]
            writeNonEditableInfo('b*: {:.3f}'.format(Tb), 0,4)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor.fromRgbF(*T_rgb, 0.5))
            self.colorTableWidget.setItem(0,5, item)

            #ab =  colour.XYZ_to_Hunter_Lab(XYZ)
            #ab =  colour.XYZ_to_Hunter_Rdab(XYZ)
            #ab =  colour.XYZ_to_K_ab_HunterLab1966(XYZ)
            Rv = R_XYZ[1]
            writeNonEditableInfo('v: {:.3f}%'.format(Rv), 1,0)
            Rx = R_xy[0]
            writeNonEditableInfo('x: {:.3f}'.format(Rx), 1,1)
            Ry = R_xy[1]
            writeNonEditableInfo('y: {:.3f}'.format(Ry), 1,2)
            Ra = R_ab[1]
            writeNonEditableInfo('a*: {:.3f}'.format(Ra), 1,3)
            Rb = R_ab[2]
            writeNonEditableInfo('b*: {:.3f}'.format(Rb), 1,4)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor.fromRgbF(*R_rgb, 0.5))
            self.colorTableWidget.setItem(1,5, item)
        else:
            '''Reset table to blank.'''
            for i in range(rowCount):
                for j in range(columnCount-1):
                    writeNonEditableInfo('', i, j)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,255,255,0))
            self.colorTableWidget.setItem(0,columnCount-1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,255,255,0))
            self.colorTableWidget.setItem(1,columnCount-1, item)
    #d.processingTime()#checking
    
    def loadStack(self):
        #print('here we go again=====>loadStack')#checking

        ##d.datetimeConverter()#checking
        currentRow = self.stackListWidget.currentRow()
        if currentRow > -1:
            self.stack = copy.deepcopy(self.stack_db[currentRow])
            self.stack, error, error_text, title = addMaterialInfoToStack(self.material_db, self.stack, False)
            if error:
                self.raiseWarningMessage(title, error_text)
            else:    
                self.populateStackWidget(self.stack)
                self.updateDesignGraph(self.stack)
                self.updateStackDetailTable(0, self.stack)
        ##d.processingTime()#checking

    def raiseWarningMessage(self, title, error_text):
        #print('here we go again=====>raiseWarningMessage')#checking

        ##d.datetimeConverter()#checking
        self.choice = QtWidgets.QMessageBox.warning(self.MainWindow, title, error_text, QtWidgets.QMessageBox.Ok)
        #DL
        ##d.processingTime()#checking

    def saveStack(self):
        #print('here we go again=====>saveStack')#checking

        ##d.datetimeConverter()#checking
        for stack in self.stack_db:
            if stack.name.lower() == self.stack.name.lower():
                self.raiseWarningMessage('Error stack name', 'Stack name already exists. Please modify the stack name.') 
                return
        if len(stack.name) == 0:
                self.raiseWarningMessage('Error stack name', 'No stack name. Please add unique stack name.') 
                return
        try:    
            self.stack.saveStack()
        except ValueError:
            self.raiseWarningMessage('Error', 'Stack not saved.')
            return
        self.reload_DBs()
        self.raiseWarningMessage('Stack saved.', 'Stack has been added to DB file. Please reload excel file in case file was open.') 
        ##d.processingTime()#checking

    def checkOnlineStatus(self):
        #print('here we go again=====> checkOnlineStatus')#checking

        ##d.datetimeConverter()#checking
        if self.stack.online:
            self.stack.online = False
            self.onlinePB.setStyleSheet('QPushButton {color: black;}')
            self.onlinePB.setText('Go Online')
            self.deviceComboBox.setEnabled(True)
            self.goOffline()
        else:
            self.stack.online = True
            self.onlinePB.setStyleSheet('QPushButton {color: green;}')
            self.onlinePB.setText('Online')
            self.deviceComboBox.setEnabled(False)
            self.goOnline()
            
    def goOnline(self):
        #print('here we go again=====>goOnline')#checking

        ##d.datetimeConverter()#checking
        import pyodbc
        #ESTABLISH CONNECTION
        connect_string = "Driver={" + self.settings.SQL_driver + "};\
                        Server=" + self.settings.SQL_server + ";\
                        Database=" + self.settings.SQL_DB + ";\
                        Trusted_Connection=yes;"
        cnxn = pyodbc.connect(connect_string)
        devices = [self.settings.device_select + ' Transmission', self.settings.device_select + ' Reflection']
        #Get spectra with wave info
        query_string_wave = 'SELECT TOP 1 WavelengtsArrays.Wavelengths FROM Spectra \
                            JOIN WavelengtsArrays ON Spectra.ResultId = WavelengtsArrays.ResultId \
                            WHERE Spectra.ResultName = \'{}\' ORDER BY Spectra.Id DESC'.format(devices[0])
        cursor = cnxn.cursor()
        cursor.execute(query_string_wave)
        data = cursor.fetchone()
        self.stack.measure_wvl = list(map(float, data[0].split(';')))

        start_time = datetime.datetime.now()
        self.thread = StoppableThread(self.getMeasurementTRA, (devices, cnxn, start_time))
        self.thread.start()
        #timer.add_operation(self.getMeasurementTRA, self.settings.refresh_time, args=[devices, cnxn, start_time])
        ##d.processingTime()#checking

    def goOffline(self):
        #print('here we go again=====>goOffline')#checking

        ##d.datetimeConverter()#checking
        if self.thread.isAlive():
            self.thread.stop()
            self.thread.join()
            del(self.thread)
        ##d.processingTime()#checking

    def getMeasurementTRA(self, devices, cnxn, start_time):
        #print('here we go again=====>getMeasurementTRA')#checking

        ##d.datetimeConverter()#checking
        '''Get new data from Zeiss DB and update fit graph'''
        stack = self.stack
        #end_of_cycle_time = start_time#DL
        cursor = cnxn.cursor()
        
        while not self.thread.stopped():
            #QUERY FIRST DEVICE FOR TRANSMISSION

            query_string_spectrum = 'SELECT TOP 1 Spectra.Id,  Spectra.Run_Id, Spectra.[values], Spectra.[Timestamp] \
                                    FROM Spectra WHERE Spectra.ResultName = \'{}\' ORDER BY Spectra.Id DESC' .format(devices[0])
            cursor.execute(query_string_spectrum)
            data = cursor.fetchone()
            #run_id = data[1],DL
            spectrum = list(map(float, data[2].split(';')))
            stack.measureT  = np.array([x / 100.0 for x in spectrum])
            #local_time = self.getLocalTime(data[3])

            #QUERY SECOND DEVICE FOR REFLECTION
            query_string_spectrum = 'SELECT TOP 1 Spectra.Id,  Spectra.Run_Id, Spectra.[values], Spectra.[Timestamp] \
                                    FROM Spectra WHERE Spectra.ResultName = \'{}\' ORDER BY Spectra.Id DESC' .format(devices[1])
            # find number of rows in table from spec table SELECT * "index?row count?"
            cursor.execute(query_string_spectrum)
            data = cursor.fetchone()
            spectrum = list(map(float, data[2].split(';')))
            stack.measureR = np.array([x / 100.0 for x in spectrum])
            time_UTC = data[3]
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            time_UTC = time_UTC.replace(tzinfo=from_zone)
            local_time = time_UTC.astimezone(to_zone)
            stack.measuredTime = local_time

            stack.measureA = 1 - np.array(stack.measureT) - np.array(stack.measureR)
            #UNUSED AT THE MOMENT
            '''#DL
            if (datetime.datetime.now() - start_time).total_seconds() > (self.settings.refresh_time + 0.5):
                refresh = False
            else:
                refresh = True'''
            self.updateGraphOnline()
            '''#DL
            seconds = (datetime.datetime.now() - end_of_cycle_time).total_seconds()
            if seconds < self.settings.refresh_time:
                time.sleep(self.settings.refresh_time - seconds)
            print('T_delta: ' + str(seconds) + '  Refresh_delta: ' + str((datetime.datetime.now() - end_of_cycle_time).total_seconds()))
            end_of_cycle_time = datetime.datetime.now()
            '''
        ##d.processingTime()#checking
    
    def updateGraphOnline(self):
        #print('here we go again=====>updateGraphOnline')#checking

        ##d.datetimeConverter()#checking
        self.stack.setTRAsplines(stack.measure_wvl, type = 'measured')
        self.fitTab.updateFitGraph(stack, refresh = True)
        self.fitTab.updateFitColorDataToTable(self.stack) #ADD BACK IF SLOWDOWN IS LIMITED
        ##d.processingTime()#checking

    def reload_DBs(self):
        #print('here we go again=====>reload_DBs')#checking

        ##d.datetimeConverter()#checking
        '''Reloads Stack and Materials databases from Excel file in case user wants to modify.'''
        self.stack_db = Stack.get_stacks(self.settings.defaultFile)
        self.material_db = Material.get_materials(self.settings.standard_wave_list_mod, self.settings.defaultFile)
        self.populateStackDBList(self.stack_db)
        self.populateMaterialDBList(self.material_db)
        ##d.processingTime()#checking

    def fit_Turn_all_On_Off(self):
        #print('here we go again=====>fit_Turn_all_On_Off')#checking

        ##d.datetimeConverter()#checking
        '''Function called in menubar turns fitStatus of all layers On (True) or Off (False) in the Fit screen, and updates
        fitscreen.'''
        if not any(mat.editMode for mat in self.stack.material):
            if any(mat.fitStatus == False for mat in self.stack.material):
                for mat in self.stack.material:
                    mat.fitStatus = True
            else:
                for mat in self.stack.material:
                    mat.fitStatus = False
            self.updateScreens(1) #Updates fit screen.
        else:
            self.raiseWarningMessage('Exit Edit Mode.', 'Please exit mode to turn all layers on or off.') 
        ##d.processingTime()#checking
    
    def addStacksToDB(self):
        #print('here we go again=====>addStacksToDB')#checking

        ##d.datetimeConverter()#checking
        fileName = self.openFileNameDialog('Add Stack File')
        if fileName:
            try:
                new_stacks = Stack.get_stacks(fileName)
                self.stack_db.extend(new_stacks)
                self.populateStackDBList(self.stack_db)
                self.raiseWarningMessage('Stacks added.', 'Stack(s) have been added to DB.') 
            except:
                self.raiseWarningMessage('Error', 'Input file not compatible. Check file format and sheet name.') 
        ##d.processingTime()#checking

    def addMaterialToDB(self):
        #print('here we go again=====>addMaterialToDB')#checking

        ##d.datetimeConverter()#checking
        fileName = self.openFileNameDialog('Add Material File')
        if fileName:
            try:
                new_mats = Material.get_materials(self.settings.standard_wave_list_mod, fileName)
                self.material_db.extend(new_mats)
                self.populateMaterialDBList(self.material_db)
                self.raiseWarningMessage('Materials added.', 'Material(s) have been added to DB.') 
            except:
                self.raiseWarningMessage('Error', 'Input file not compatible. Check file format and sheet name.') 
        ##d.processingTime()#checking
    
    ##d.datetimeConverter()#checking
       
    def openFileNameDialog(self, title): 
        #print('here we go again=====>openFileNameDialog')#checking

        from PyQt5.QtWidgets import QFileDialog   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, title, "","All Files (*);;Excel Files (*.xlsx)", options=options)
        return fileName
    ##d.processingTime()#checking
    '''
    def openGeneralPropertiesButton(self):
        #print('here we go again=====>openGeneralPropertiesButton')#checking

        ##d.datetimeConverter()#checking
        window = PropertiesGeneralWindow(self)
        window.show()
        ##d.processingTime()#checking
    '''
        
if __name__ == "__main__":
    import sys
    from Stack import Stack, Material

    app = QtWidgets.QApplication(sys.argv)
    
    stack = Stack()
    settings = Settings()

    import ctypes
    import platform
    if platform.system() == 'Windows':
        myappid = 'TomWare.1_0' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    # Create and display the splash screen
    splash_pix = QtGui.QPixmap('icon.png')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    app.processEvents()

    stack_db = Stack.get_stacks(settings.defaultFile)
    material_db = Material.get_materials(settings.standard_wave_list, settings.defaultFile)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, stack, settings)
    ui.populateStackDBList(stack_db)
    ui.populateMaterialDBList(material_db)
    MainWindow.show()
    splash.finish(MainWindow)
    ui.updateDesignGraph(stack)
    sys.exit(app.exec_())





   

