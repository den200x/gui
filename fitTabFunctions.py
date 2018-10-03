def loadFitTableWidget(self, stack):
    '''Function to populate the fit table with combobox and edit buttons'''
    statusComboBoxOptions = ['Off', 'On']
    #self.fitTableWidget.itemChanged.disconnect(self.storeFitParameters)
    self.fitTableWidget.setColumnCount(0)
    self.buttonGroup = QtWidgets.QButtonGroup()
    self.buttonGroup.buttonClicked[int].connect(self.lockEditModeForFit)
    if not stack.isEmpty():
        layer_count = stack.layer_count()
        self.fitTableWidget.setColumnCount(layer_count)
        for index in range(layer_count):
            #Prior to loading buttons remove all spans (merged cells)
            self.fitTableWidget.setSpan(5, index, 1, 1)
            box = QtWidgets.QComboBox()

            box.addItems(statusComboBoxOptions)
            box.setCurrentIndex(int(stack.material[index].fitStatus))
            box.activated[int].connect(self.storeFitStatus)
            box.setProperty("col", index)
            self.fitTableWidget.setCellWidget(2, index, box)

            if stack.material[index].model == 'drude':
                button = QtWidgets.QPushButton('Locked')
                self.buttonGroup.addButton(button)
                self.buttonGroup.setId(button, index)
                self.fitTableWidget.setCellWidget(13, index, button)
    self.loadFitParameters(self.stack)

def loadFitParameters(self, stack):
    for idx, mat in enumerate(stack.material):
        item = QtWidgets.QTableWidgetItem(mat.name)
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
        item.setBackground(QtGui.QColor(mat.color))
        #item = QtGui.QStandardItem('{} - {}'.format(stack.layers[idx], thickness_text))
        self.fitTableWidget.setItem(0, idx, item)

        item = QtWidgets.QTableWidgetItem('{}'.format(idx + 1))
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
        self.fitTableWidget.setItem(1, idx, QtWidgets.QTableWidgetItem(item))

        if mat.model == 'nk':
            #Target height
            item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.thickness[idx])))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.fitTableWidget.setItem(3, idx, QtWidgets.QTableWidgetItem(item))

            #Actual height
            item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.material[idx].actual_thickness)))
            if stack.material[idx].fit_param['thickness']:
                item = self.setFontAsFitParameter(item)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.fitTableWidget.setItem(4, idx, QtWidgets.QTableWidgetItem(item))

            self.fitTableWidget.setSpan(5, idx, 9, 1)
            item = QtWidgets.QTableWidgetItem('{}'.format('nk'))
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.fitTableWidget.setItem(5, idx, QtWidgets.QTableWidgetItem(item))

        if mat.model == 'drude':
            #Target height
            item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.thickness[idx])))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.fitTableWidget.setItem(3, idx, QtWidgets.QTableWidgetItem(item))

            #Actual height
            item = QtWidgets.QTableWidgetItem('{}'.format(getThicknessAndUnit(stack.material[idx].actual_thickness)))
            if stack.material[idx].fit_param['thickness']:
                item = self.setFontAsFitParameter(item)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.fitTableWidget.setItem(4, idx, QtWidgets.QTableWidgetItem(item))

            #de
            item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.de))
            if stack.material[idx].fit_param['de']:
                item = self.setFontAsFitParameter(item)
            item.setToolTip('Original setting: {}'.format(mat.de_org))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,255,102,127))
            self.fitTableWidget.setItem(5, idx, QtWidgets.QTableWidgetItem(item))

            #UV_wO^2
            item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.w0_U))
            if stack.material[idx].fit_param['w0_U']:
                item = self.setFontAsFitParameter(item)
            item.setToolTip('Original setting:{}'.format(mat.w0_U_org))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(214,75,255,127))
            self.fitTableWidget.setItem(6, idx, QtWidgets.QTableWidgetItem(item))

            #UV_wP^2
            item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.wp_U))
            if stack.material[idx].fit_param['wp_U']:
                item = self.setFontAsFitParameter(item)
            item.setToolTip('Original setting:{}'.format(mat.wp_U_org))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(214,75,255,127))
            self.fitTableWidget.setItem(7, idx, QtWidgets.QTableWidgetItem(item))

            #gamma__U
            item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.gamma_U))
            if stack.material[idx].fit_param['gamma_U']:
                item = self.setFontAsFitParameter(item)
            item.setToolTip('Original setting:{}'.format(mat.gamma_U_org))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(214,75,255,127))
            self.fitTableWidget.setItem(8, idx, QtWidgets.QTableWidgetItem(item))
            
            #Drude_wO^2
            item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.w0_D))
            if stack.material[idx].fit_param['w0_D']:
                item = self.setFontAsFitParameter(item)
            item.setToolTip('Original setting:{}'.format(mat.w0_D_org))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,51,51,127))
            self.fitTableWidget.setItem(9, idx, QtWidgets.QTableWidgetItem(item))
            
            #Drude_wp^2        
            item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.wp_D))
            if stack.material[idx].fit_param['wp_D']:
                item = self.setFontAsFitParameter(item)
            item.setToolTip('Original setting:{}'.format(mat.wp_D_org))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,51,51,127))
            self.fitTableWidget.setItem(10, idx, QtWidgets.QTableWidgetItem(item))
            
            #gamma__Drude
            item = QtWidgets.QTableWidgetItem('{:g}'.format(mat.gamma_D))
            if stack.material[idx].fit_param['gamma_D']:
                item = self.setFontAsFitParameter(item)
            item.setToolTip('Original setting:{}'.format(mat.gamma_D_org))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable) if mat.editMode else item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setBackground(QtGui.QColor(255,51,51,127))
            self.fitTableWidget.setItem(11, idx, QtWidgets.QTableWidgetItem(item))

        n = float(mat.get_NKspline_value('N', 550))
        k = float(mat.get_NKspline_value('K', 550))
        infoNK = '{:4.2f}, {:5.2f}'.format(n,k)
        item = QtWidgets.QTableWidgetItem('{}'.format(infoNK))
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
        self.fitTableWidget.setItem(12, idx,item)

def lockCells(self, layer_idx):
    '''lock cells in one column of fit table'''
    self.fitTableWidget.itemChanged.disconnect(self.storeFitParameters)
    for idx in range(4,12):
        item = self.fitTableWidget.item(idx, layer_idx)
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)

def unlockCells(self, layer_idx):
    '''Unlock cells in one column of fit table'''
    for idx in range(4,12):
        item = self.fitTableWidget.item(idx, layer_idx)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
    self.fitTableWidget.itemChanged.connect(self.storeFitParameters)

def lockEditModeForFit(self, layer_idx):
    if not self.parameterMode:
        if self.stack.material[layer_idx].editMode == True:
            self.stack.material[layer_idx].editMode = False
            self.buttonGroup.button(layer_idx).setText('Locked')
            self.buttonGroup.button(layer_idx).setStyleSheet('QPushButton {color: black;}')
            self.lockCells(layer_idx)
        elif not any(t.editMode for t in self.stack.material):
            self.buttonGroup.button(layer_idx).setText('Edit Mode')
            self.buttonGroup.button(layer_idx).setStyleSheet('QPushButton {color: red;}')
            self.stack.material[layer_idx].editMode = True
            self.unlockCells(layer_idx)
    else:
        self.raiseWarningMessage('Turn off parameter selection', '''Please turn off the parameter selection mode to select 'edit mode'.''')

def restoreFit(self):
    '''Function restores fit parameters for layers in 'edit mode'.'''
    for idx, mat in enumerate(self.stack.material):
        if mat.editMode:
            self.fitTableWidget.itemChanged.disconnect(self.storeFitParameters)
            mat.restoreOriginalDrudes()
            mat.create_NKspline()
            self.loadFitParameters(self.stack)
            self.updateFitGraph(self.stack)
            self.fitTableWidget.itemChanged.connect(self.storeFitParameters)
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
        for index, material in enumerate(self.stack.material):
            material.fitStatus = bool(self.fitTableWidget.cellWidget(2, index).currentIndex())
        self.updateFitGraph(self.stack)

def storeFitParameters(self, e):
    for layer in self.stack.material: #technically for statement is redundant, but leavingit in here as precaution.
        if layer.editMode:
            row = self.fitTableWidget.currentItem().row()
            column = self.fitTableWidget.currentItem().column()
            text = self.fitTableWidget.currentItem().text()
            mat = self.stack.material[column]
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
        self.fitTableWidget.itemChanged.disconnect(self.storeFitParameters)
    except TypeError:
            pass
    self.loadFitParameters(self.stack)
    self.fitTableWidget.itemChanged.connect(self.storeFitParameters)
    self.updateFitGraph(self.stack)

def selectFitParametersMode(self):
    '''Function 'puts' fitTableWidget in indentification mode to find clicked cells that become fit parameters'''
    if not any(t.editMode for t in self.stack.material):
        if not self.parameterMode:
            self.parameterMode = True
            self.selectParamPB.setStyleSheet('QPushButton {color: red;}')
            self.fitTableWidget.clicked.connect(self.identifyFitParameters)
        else:
            self.parameterMode = False
            self.selectParamPB.setStyleSheet('QPushButton {color: black;}')
            self.fitTableWidget.clicked.disconnect(self.identifyFitParameters)
    else:
        self.raiseWarningMessage('''Turn off 'edit mode'.''', '''Please turn off 'edit mode' to turn on parameter selection mode.''')

def identifyFitParameters(self, e):
    '''fitTableWidget was clicked in 'selectFitParametersMode'. Cell and status identified'''
    row = self.fitTableWidget.currentItem().row()
    column = self.fitTableWidget.currentItem().column()
    paramArray = ['thickness', 'de', 'w0_U','wp_U', 'gamma_U','w0_D', 'wp_D', 'gamma_D']
    #check if drude parameter is clicked
    if row > 3 and row < 12:
        #check how many fit parameters have already been selected, max 7
        num_fit_param = 0
        for mat in self.stack.material:
            num_fit_param += sum(mat.fit_param.values())
        mat = self.stack.material[column]
        dic = self.stack.material[column].fit_param
        #If currently True can always set to False.
        if dic[paramArray[row - 4]]:
            dic[paramArray[row - 4]] = False
            item = self.fitTableWidget.item(row, column)
            item.setForeground(QtGui.QColor('black'))
            font = QtGui.QFont()
            font.setBold(False)
            item.setFont(font)
        #If currently False can only set to True if 6 or less are already True.
        elif num_fit_param < 7:
            dic[paramArray[row - 4]] = True
            item = self.fitTableWidget.item(row, column)
            item = self.setFontAsFitParameter(item)

def updateFitGraph(self, stack):
    '''Function updates TRA plot in Fit tab'''
    stack.RMSerror = ''
    if stack.isEmpty():
        stack.fit_wvl = standard_wvl_list
    else:
        #Calculate fitted splines
        stack.fit_wvl = getWaveList(stack, standard_wvl_list)
        #This parameters determines if curve is calculated based on theoretical thickness or estimated actual thickness
        ActualThicknessCurve = True
        stack.fT, stack.fR, stack.fA = calculateTRA(stack, 'fit', fitting_layer, incident_angle, incoherence_factor, ActualThicknessCurve, self.REVERSE_STACK)
        stack.setTRAsplines(stack.fit_wvl, type = 'fitted')
        #Calculate measured splines
        if online:
            stack.mT, stack.mR, stack.mA = self.getMeasurementTRA()
            stack.setTRAsplines(stack.measure_wvl, type = 'measured')
            if not len(stack.fitT) == 0:
                stack.RMSerror = calculateRMS(stack.spline_measureT(stack.fit_wvl), stack.spline_measureR(stack.fit_wvl), stack.spline_fitT(stack.fit_wvl), stack.spline_fitR(stack.fit_wvl))
        #Calculate original spline to be plotted in fit tab
        else:
            if not len(stack.excelT) == 0:
                #stack.setTRAsplines(stack.wvl, type = 'original'), not needed: designGraph must have created this already.
                stack.RMSerror = calculateRMS(stack.spline_excelT(stack.fit_wvl), stack.spline_excelR(stack.fit_wvl), stack.spline_fitT(stack.fit_wvl), stack.spline_fitR(stack.fit_wvl))
    self.plotFitFrame.graph_view.plot_graph(stack.fit_wvl, stack)

