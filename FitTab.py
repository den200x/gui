from PyQt5 import QtCore, QtGui, QtWidgets
from helperFunctions import (is_number, getThicknessAndUnit,getThicknessFromString)
from FunctionsTRA import (getWaveList, calculateTRA,  
                         addMaterialInfoToStack, calculateRMS, calculateColorValues)

class FitTab():
    def __init__(self, ui):
        self.ui = ui
    
    def loadFitTableWidget(self, stack):
        '''Function to populate the fit table with combobox and edit buttons'''
        statusComboBoxOptions = ['Off', 'On']
        
        self.ui.fitTableWidget.setColumnCount(0)
        self.ui.buttonGroup = QtWidgets.QButtonGroup()
        self.ui.buttonGroup.buttonClicked[int].connect(self.lockEditModeForFit)
        if not stack.isEmpty():
            layer_count = stack.layer_count()
            self.ui.fitTableWidget.setColumnCount(layer_count)
            for index in range(layer_count):
                #Prior to loading buttons remove all spans (merged cells)
                self.ui.fitTableWidget.setSpan(5, index, 1, 1)
                box = QtWidgets.QComboBox()

                box.addItems(statusComboBoxOptions)
                box.setCurrentIndex(int(stack.material[index].fitStatus))
                box.activated[int].connect(self.storeFitStatus)
                box.setProperty("col", index)
                self.ui.fitTableWidget.setCellWidget(2, index, box)

                if stack.material[index].model == 'drude':
                    button = QtWidgets.QPushButton('Locked')
                    self.ui.buttonGroup.addButton(button)
                    self.ui.buttonGroup.setId(button, index)
                    self.ui.fitTableWidget.setCellWidget(13, index, button)
        self.loadFitParameters(stack)

    def loadFitParameters(self, stack):
        for idx, mat in enumerate(stack.material):
            item = QtWidgets.QTableWidgetItem(mat.name)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(mat.color))
            #item = QtGui.QStandardItem('{} - {}'.format(stack.layers[idx], thickness_text))
            self.ui.fitTableWidget.setItem(0, idx, item)

            item = QtWidgets.QTableWidgetItem('{}'.format(idx + 1))
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.ui.fitTableWidget.setItem(1, idx, QtWidgets.QTableWidgetItem(item))

            if mat.model == 'nk':
                #Target height
                item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.thickness[idx])))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.fitTableWidget.setItem(3, idx, QtWidgets.QTableWidgetItem(item))

                #Actual height
                item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.material[idx].actual_thickness)))
                if stack.material[idx].fit_param['thickness']:
                    item = self.setFontAsFitParameter(item)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.fitTableWidget.setItem(4, idx, QtWidgets.QTableWidgetItem(item))

                self.ui.fitTableWidget.setSpan(5, idx, 9, 1)
                item = QtWidgets.QTableWidgetItem('{}'.format('nk'))
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.fitTableWidget.setItem(5, idx, QtWidgets.QTableWidgetItem(item))

            if mat.model == 'drude':
                #Target height
                item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.thickness[idx])))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.fitTableWidget.setItem(3, idx, QtWidgets.QTableWidgetItem(item))

                #Actual height
                item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.material[idx].actual_thickness)))
                if stack.material[idx].fit_param['thickness']:
                    item = self.setFontAsFitParameter(item)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.fitTableWidget.setItem(4, idx, QtWidgets.QTableWidgetItem(item))

                #de
                item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.de))
                if stack.material[idx].fit_param['de']:
                    item = self.setFontAsFitParameter(item)
                item.setToolTip('Original setting: {}'.format(mat.de_org))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(255,255,102,127))
                self.ui.fitTableWidget.setItem(5, idx, QtWidgets.QTableWidgetItem(item))

                #UV_wO^2
                item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.w0_U))
                if stack.material[idx].fit_param['w0_U']:
                    item = self.setFontAsFitParameter(item)
                item.setToolTip('Original setting:{}'.format(mat.w0_U_org))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(214,75,255,127))
                self.ui.fitTableWidget.setItem(6, idx, QtWidgets.QTableWidgetItem(item))

                #UV_wP^2
                item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.wp_U))
                if stack.material[idx].fit_param['wp_U']:
                    item = self.setFontAsFitParameter(item)
                item.setToolTip('Original setting:{}'.format(mat.wp_U_org))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(214,75,255,127))
                self.ui.fitTableWidget.setItem(7, idx, QtWidgets.QTableWidgetItem(item))

                #gamma__U
                item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.gamma_U))
                if stack.material[idx].fit_param['gamma_U']:
                    item = self.setFontAsFitParameter(item)
                item.setToolTip('Original setting:{}'.format(mat.gamma_U_org))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(214,75,255,127))
                self.ui.fitTableWidget.setItem(8, idx, QtWidgets.QTableWidgetItem(item))
                
                #Drude_wO^2
                item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.w0_D))
                if stack.material[idx].fit_param['w0_D']:
                    item = self.setFontAsFitParameter(item)
                item.setToolTip('Original setting:{}'.format(mat.w0_D_org))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(255,51,51,127))
                self.ui.fitTableWidget.setItem(9, idx, QtWidgets.QTableWidgetItem(item))
                
                #Drude_wp^2        
                item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.wp_D))
                if stack.material[idx].fit_param['wp_D']:
                    item = self.setFontAsFitParameter(item)
                item.setToolTip('Original setting:{}'.format(mat.wp_D_org))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(255,51,51,127))
                self.ui.fitTableWidget.setItem(10, idx, QtWidgets.QTableWidgetItem(item))
                
                #gamma__Drude
                item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.gamma_D))
                if stack.material[idx].fit_param['gamma_D']:
                    item = self.setFontAsFitParameter(item)
                item.setToolTip('Original setting:{}'.format(mat.gamma_D_org))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor(255,51,51,127))
                self.ui.fitTableWidget.setItem(11, idx, QtWidgets.QTableWidgetItem(item))

            n = float(mat.get_NKspline_value('N', 550))
            k = float(mat.get_NKspline_value('K', 550))
            infoNK = '{:4.2f}, {:5.2f}'.format(n,k)
            item = QtWidgets.QTableWidgetItem('{}'.format(infoNK))
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.ui.fitTableWidget.setItem(12, idx,item)

    def lockCells(self, layer_idx):
        '''lock cells in one column of fit table'''
        self.ui.fitTableWidget.itemChanged.disconnect(self.storeFitParameters)
        for idx in range(4,12):
            item = self.ui.fitTableWidget.item(idx, layer_idx)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)

    def unlockCells(self, layer_idx):
        '''Unlock cells in one column of fit table'''
        for idx in range(4,12):
            item = self.ui.fitTableWidget.item(idx, layer_idx)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.ui.fitTableWidget.itemChanged.connect(self.storeFitParameters)

    def lockEditModeForFit(self, layer_idx):
        if not self.ui.parameterMode:
            if self.ui.stack.material[layer_idx].editMode == True:
                self.ui.stack.material[layer_idx].editMode = False
                self.ui.buttonGroup.button(layer_idx).setText('Locked')
                self.ui.buttonGroup.button(layer_idx).setStyleSheet('QPushButton {color: black;}')
                self.lockCells(layer_idx)
            elif not any(t.editMode for t in self.ui.stack.material):
                self.ui.buttonGroup.button(layer_idx).setText('Edit Mode')
                self.ui.buttonGroup.button(layer_idx).setStyleSheet('QPushButton {color: red;}')
                self.ui.stack.material[layer_idx].editMode = True
                self.unlockCells(layer_idx)
        else:
            self.ui.raiseWarningMessage('Turn off parameter selection', '''Please turn off the parameter selection mode to select 'edit mode'.''')

    def restoreFit(self):
        '''Function restores fit parameters for layers in 'edit mode'.'''
        for idx, mat in enumerate(self.ui.stack.material):
            if mat.editMode:
                self.ui.fitTableWidget.itemChanged.disconnect(self.storeFitParameters)
                mat.restoreOriginalDrudes()
                mat.create_NKspline()
                self.loadFitParameters(self.ui.stack)
                self.updateFitGraph(self.ui.stack)
                self.updateFitColorDataToTable(self.ui.stack)
                self.ui.fitTableWidget.itemChanged.connect(self.storeFitParameters)
                #This statement needed in case 'Restore fit' is pressed
                #self.unlockCells(idx)

    def setFontAsFitParameter(self, item):
        item.setForeground(QtGui.QColor('red'))
        font = QtGui.QFont()
        font.setBold(True)
        item.setFont(font)
        return item

    def storeFitStatus(self, e):
            '''Store the status 'On or off' of layer'''
            for index, material in enumerate(self.ui.stack.material):
                material.fitStatus = bool(self.ui.fitTableWidget.cellWidget(2, index).currentIndex())
            #print(e)
            self.updateFitGraph(self.ui.stack)
            self.updateFitColorDataToTable(self.ui.stack)

    def storeFitParameters(self, e):
        for layer in self.ui.stack.material: #technically for statement is redundant, but leavingit in here as precaution.
            if layer.editMode:
                row = self.ui.fitTableWidget.currentItem().row()
                column = self.ui.fitTableWidget.currentItem().column()
                text = self.ui.fitTableWidget.currentItem().text()
                mat = self.ui.stack.material[column]
                #Status change handled in: storeFitStatus
                if row == 4:
                #Actual Height change
                    t = getThicknessFromString(text)
                    if not t == None:
                        mat.actual_thickness = t
                elif is_number(text) and float(text) > 0:
                    if row == 5: #de
                        mat.de = float(text)
                    elif row == 6: #wO_U
                        mat.w0_U = float(text)
                    elif row == 7: #wO_P
                        mat.wp_U = float(text)
                    elif row == 8: #gamma_U
                        mat.gamma_U = float(text)
                    elif row == 9: #wO_D
                        mat.w0_D = float(text)
                    elif row == 10: #wO_D
                        mat.wp_D = float(text)
                    elif row == 11: #gamma_D
                        mat.gamma_D = float(text)
                mat.create_NKspline()
        #Disable modification event before updating the FitTable.
        try:
            self.ui.fitTableWidget.itemChanged.disconnect(self.storeFitParameters)
        except TypeError:
                pass
        self.loadFitParameters(self.ui.stack)
        self.ui.fitTableWidget.itemChanged.connect(self.storeFitParameters)
        self.updateFitGraph(self.ui.stack)
        self.updateFitColorDataToTable(self.ui.stack)

    def selectFitParametersMode(self):
        '''Function 'puts' fitTableWidget in indentification mode to find clicked cells that become fit parameters'''
        if not any(t.editMode for t in self.ui.stack.material):
            if not self.ui.parameterMode:
                self.ui.parameterMode = True
                self.ui.selectParamPB.setStyleSheet('QPushButton {color: red;}')
                self.ui.fitTableWidget.clicked.connect(self.identifyFitParameters)
            else:
                self.ui.parameterMode = False
                self.ui.selectParamPB.setStyleSheet('QPushButton {color: black;}')
                self.ui.fitTableWidget.clicked.disconnect(self.identifyFitParameters)
        else:
            self.ui.raiseWarningMessage('''Turn off 'edit mode'.''', '''Please turn off 'edit mode' to turn on parameter selection mode.''')

    def identifyFitParameters(self, e):
        '''fitTableWidget was clicked in 'selectFitParametersMode'. Cell and status identified'''
        row = self.ui.fitTableWidget.currentItem().row()
        column = self.ui.fitTableWidget.currentItem().column()
        paramArray = ['thickness', 'de', 'w0_U','wp_U', 'gamma_U','w0_D', 'wp_D', 'gamma_D']
        #check if drude parameter is clicked
        if row > 3 and row < 12:
            #check how many fit parameters have already been selected, max 7
            num_fit_param = 0
            for mat in self.ui.stack.material:
                num_fit_param += sum(mat.fit_param.values())
            mat = self.ui.stack.material[column]
            dic = self.ui.stack.material[column].fit_param
            #If currently True can always set to False.
            if dic[paramArray[row - 4]]:
                dic[paramArray[row - 4]] = False
                item = self.ui.fitTableWidget.item(row, column)
                item.setForeground(QtGui.QColor('black'))
                font = QtGui.QFont()
                font.setBold(False)
                item.setFont(font)
            #If currently False can only set to True if 6 or less are already True.
            elif num_fit_param < 7:
                dic[paramArray[row - 4]] = True
                item = self.ui.fitTableWidget.item(row, column)
                item = self.setFontAsFitParameter(item)

    def updateFitGraph(self, stack, refresh = True):
        '''Function updates TRA plot in Fit tab'''
        stack.RMSerror = ''
        stack.fit_wvl = getWaveList(stack, self.ui.settings.standard_wave_list_mod)
        if not stack.isEmpty():
            #This parameters determines if curve is calculated based on theoretical thickness or estimated actual thickness
            ActualThicknessCurve = True
            stack.fitT, stack.fitR, stack.fitA = calculateTRA(stack, 'fit', stack.fitting_layer, self.ui.settings.incident_angle, self.ui.settings.incoherence_factor, ActualThicknessCurve, stack.REVERSE_STACK)
            stack.setTRAsplines(stack.fit_wvl, type = 'fitted')
            #Calculate measured splines
            if stack.online:
                #stack.mT, stack.mR, stack.mA = self.ui.getMeasurementTRA(self.ui.settings.refresh_time)
                if not len(stack.measureT) == 0 and not len(stack.fitT) == 0:
                    stack.RMSerror = calculateRMS(stack.spline_measureT(stack.fit_wvl), stack.spline_measureR(stack.fit_wvl), stack.spline_fitT(stack.fit_wvl), stack.spline_fitR(stack.fit_wvl))
            #Calculate original spline to be plotted in fit tab
            else:
                if not len(stack.excelT) == 0 and not len(stack.fitT) == 0:
                    #stack.setTRAsplines(stack.wvl, type = 'original'), not needed: designGraph must have created this already.
                    stack.RMSerror = calculateRMS(stack.spline_excelT(stack.fit_wvl), stack.spline_excelR(stack.fit_wvl), stack.spline_fitT(stack.fit_wvl), stack.spline_fitR(stack.fit_wvl))
        self.ui.plotFitFrame.graph_view.plot_fitGraph(stack.fit_wvl, stack, self.ui.settings, refresh)

    def updateFitColorDataToTable(self, stack):
        '''Function calculates color parameters and writes to table colorTableWidget in Design Tab'''
        def writeNonEditableInfo(info, row, col):
            item = QtWidgets.QTableWidgetItem(info)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            #item.setBackground(QtGui.QColor(211,211,211,70))
            table.setItem(row, col, item)
        
        table = self.ui.colorFitTableWidget

        rowCount = table.rowCount()
        columnCount = table.columnCount()

        if not stack.isEmpty():
            #vHeader = table.verticalHeader()
            #ISSUE!!!
            #for i in range(rowCount):
            #    vHeader.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            #hHeader = table.horizontalHeader()
            #for i in range(columnCount):
            #    hHeader.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            
            #else:
                #splineT = stack.spline_excelT
                #splineR = stack.spline_excelR
            
            if hasattr(stack, 'spline_measureT'):
                if stack.online:
                    splineT = stack.spline_measureT
                    splineR = stack.spline_measureR
                T_XYZ, T_xy, T_ab, T_rgb, R_XYZ, R_xy, R_ab, R_rgb = calculateColorValues(splineT, splineR, self.ui.settings)
        
                Tv = T_XYZ[1]
                writeNonEditableInfo('v: {:.3f}%'.format(Tv), 0,0)
                Tx = T_xy[0]
                writeNonEditableInfo('x: {:.3f}'.format(Tx), 1,0)
                Ty = T_xy[1]
                writeNonEditableInfo('y: {:.3f}'.format(Ty), 2,0)
                Ta = T_ab[1]
                writeNonEditableInfo('a*: {:.3f}'.format(Ta), 3,0)
                Tb = T_ab[2]
                writeNonEditableInfo('b*: {:.3f}'.format(Tb), 4,0)
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor.fromRgbF(*T_rgb, 0.5))
                table.setItem(5,0, item)

                #ab =  colour.XYZ_to_Hunter_Lab(XYZ)
                #ab =  colour.XYZ_to_Hunter_Rdab(XYZ)
                #ab =  colour.XYZ_to_K_ab_HunterLab1966(XYZ)
                Rv = R_XYZ[1]
                writeNonEditableInfo('v: {:.3f}%'.format(Rv), 0,1)
                Rx = R_xy[0]
                writeNonEditableInfo('x: {:.3f}'.format(Rx), 1,1)
                Ry = R_xy[1]
                writeNonEditableInfo('y: {:.3f}'.format(Ry), 2,1)
                Ra = R_ab[1]
                writeNonEditableInfo('a*: {:.3f}'.format(Ra), 3,1)
                Rb = R_ab[2]
                writeNonEditableInfo('b*: {:.3f}'.format(Rb), 4,1)
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                item.setBackground(QtGui.QColor.fromRgbF(*R_rgb, 0.5))
                table.setItem(5,1, item)
        else:
            '''Reset table to blank.'''
            for i in range(rowCount):
                for j in range(columnCount-1):
                    writeNonEditableInfo('', i, j)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,255,255,0))
            table.setItem(0,columnCount-1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,255,255,0))
            table.setItem(1,columnCount-1, item)
        table.viewport().update()

