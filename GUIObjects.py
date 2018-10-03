from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

class DragDropTableView(QtWidgets.QTableView):

    def __init__(self, parent, ui):
        super().__init__(parent)
        self.ui = ui
        self.horizontalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.verticalHeader().setCascadingSectionResizes(True)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setShowGrid(True)
        #self.setAcceptDrops(True)
        #self.setDragEnabled(True)
        self.setDragDropMode(self.InternalMove)
        self.setDragDropOverwriteMode(False)
        self.setStyle(TableStyle())
        self.droppedRow = -1
        self.draggedRow = -1
        self.clicked.connect(self.viewClicked)

    def keyPressEvent(self, event):
         if type(event) == QtGui.QKeyEvent:
            key = event.key()
            shift = False
            ctrl = False
            #Check if shift was pressed (leaving ctrl in here for future use)
            if (event.modifiers() & QtCore.Qt.ShiftModifier):
                shift = True
            if (event.modifiers() & QtCore.Qt.ControlModifier):
                ctrl = True
            if shift and (key == QtCore.Qt.Key_Delete or key == QtCore.Qt.Key_Backspace):
                self.ui.removeCompleteStack()
            elif key == QtCore.Qt.Key_Delete or key == QtCore.Qt.Key_Backspace:
                self.ui.removeMaterialFromStack()
            elif key == QtCore.Qt.Key_Down:
                idx = self.selectionModel().selectedRows()[0].row()
                self.ui.rearrangeStackTable(idx, idx+1, self.ui.stack)
            elif key == QtCore.Qt.Key_Up:
                idx = self.selectionModel().selectedRows()[0].row()
                self.ui.rearrangeStackTable(idx, idx-1, self.ui.stack)
            event.accept()
         else:
            event.ignore()

    def viewClicked(self, clickedIndex):
        row = clickedIndex.row()
        self.ui.updateStackDetailTable(row, self.ui.stack)
        
    def dropEvent(self, e):
        super().dropEvent(e)
        self.droppedRow = self.rowAt(e.pos().y())
        self.ui.rearrangeStackTable(self.draggedRow, self.droppedRow, self.ui.stack)

    def dragMoveEvent(self, e):
        super().dragMoveEvent(e)

    def dragEnterEvent(self, e):
        super().dragEnterEvent(e)
        self.draggedRow = self.rowAt(e.pos().y())

    def resizeEvent(self, event):
        """ Resize all sections to content and user interactive """
        #super(Table, self).resizeEvent(event)
        super().resizeEvent(event)
        header = self.verticalHeader()
        for column in range(header.count()):
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
            width = header.sectionSize(column)
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
            header.resizeSection(column, width)

class TableModel(QtGui.QStandardItemModel):
    def dragMimeData(self, data, action, row, col, parent):
        """
        Always move the entire row, and don't allow column "shifting"
        """
        return super().dragMimeData(data, action, row, 0, parent)

    def dropMimeData(self, data, action, row, col, parent):
        """
        Always move the entire row, and don't allow column "shifting"
        """
        return super().dropMimeData(data, action, row, 0, parent)

class TableStyle(QtWidgets.QProxyStyle):

    def drawPrimitive(self, element, option, painter, widget=None):
        """
        Draw a line across the entire row rather than just the column
        we're hovering over.  This may not always work depending on global
        style - for instance I think it won't work on OSX.
        """
        if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QtWidgets.QStyleOption(option)
            option_new.rect.setLeft(0)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        super().drawPrimitive(element, option, painter, widget)

class GraphFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(GraphFrame, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.parent = parent
        self.graph_view = GraphView(self)

    def resizeEvent(self, event):
        self.graph_view.setGeometry(self.rect())

class GraphView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)

        #self.name = name
        #self.graph_title = graph_title
        self.parent = parent

        self.dpi = 60
        self.cid = -1 #identification for connection of annotation in graph
        figsize = (self.rect().width(), self.rect().height())
        #figsize = (100,45)
        
        self.fig = Figure(figsize, dpi = self.dpi, facecolor=(1,1,1), edgecolor=(0,0,0))
        self.axes = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        #self.fig.set_facecolor(color) in case needed.
        self.layout = QtWidgets.QVBoxLayout()
        #self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.canvas)
        #self.layout.setStretchFactor(self.canvas, 1)
        self.setLayout(self.layout)
        #self.fig.tight_layout()
        self.canvas.show()
        self.fig.tight_layout(pad=26)
        # ask the canvas to kindly draw it self some time in the future
        # when Qt thinks it is convenient
        self.canvas.draw_idle()
        
    def plot_designGraph(self, x, stack, settings, refresh = True):
        from helperFunctions import is_number
        self.axes.clear()
        error_string = 'Error: -'
        self.annot = self.axes.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        if not x == None:
            xmin = min(settings.standard_wave_list)
            xmax = max(settings.standard_wave_list)
            if not stack.isEmpty() and not len(stack.designT) == 0:
                if is_number(stack.RMSerror):
                    error_string = 'Error: {:5.3f}'.format(stack.RMSerror)

                    self.designT, = self.axes.plot(x, stack.designT, color = 'C0', linewidth=2, linestyle="-", label="$T_{design}$")
                    self.designR, = self.axes.plot(x, stack.designR, color = 'C1', linewidth=2, linestyle="-", label="$R_{design}$")
                    if settings.display_absorbCurve:
                        self.designA, = self.axes.plot(x, stack.designA, color = 'C2', linewidth=2, linestyle="-", label="$A_{design}$")
                    xmin = min(x)
                    xmax = max(x)
                
                if not len(stack.excelT) == 0:
                    self.excelT, = self.axes.plot(stack.excel_wvl, stack.excelT, color = 'C0', linewidth=2, linestyle="--", label="$T_{excel}$")
                    self.excelR, = self.axes.plot(stack.excel_wvl, stack.excelR, color = 'C1', linewidth=2, linestyle="--", label="$R_{excel}$")
                    if settings.display_absorbCurve:
                        self.excelA, = self.axes.plot(stack.excel_wvl, stack.excelA, color = 'C2', linewidth=2, linestyle="--", label="$A_{excel}$")
            
                if min(x) > min(stack.excel_wvl):
                    xmin = min(stack.excel_wvl)
                if max(x) < max(stack.excel_wvl):
                    xmax = max(stack.excel_wvl)

                self.axes.legend(loc="upper right", prop={'size': 14})

                if self.cid == None:
                    self.cid = self.canvas.mpl_connect("motion_notify_event", self.hover_design)
            else:
                self.canvas.mpl_disconnect(self.cid)
                self.cid = None
           
            self.axes.set_xlim(xmin, xmax)
            self.axes.set_ylim(0, 1)
            self.axes.set_xlabel('$Wavelength  (nm)$')
            self.axes.set_ylabel('Ratio')
            #print error string in plot: arg1 and 2 are x,y, transform indicates coordinates are indicated from 0,0 to 1,1.
            self.axes.xmargin = 0
            self.axes.ymargin = 0
            self.canvas.draw()
        

    def plot_fitGraph(self, x, stack, settings, refresh = True):
        from helperFunctions import is_number
        self.axes.clear()
        error_string = 'Error: -'

        refresh = True
        if not x == None:
            xmin = min(settings.standard_wave_list)
            xmax = max(settings.standard_wave_list)
            if not stack.isEmpty() and not len(stack.fitT) == 0:
                if is_number(stack.RMSerror):
                    error_string = 'Error: {:5.3f}'.format(stack.RMSerror)

                if refresh:
                    self.fitT, = self.axes.plot(x, stack.fitT, color = 'C0', linewidth=2, linestyle="-", label="$T_{fit}$")
                    self.fitR, = self.axes.plot(x, stack.fitR, color = 'C1', linewidth=2, linestyle="-", label="$R_{fit}$")
                    if settings.display_absorbCurve:
                        self.fitA, = self.axes.plot(x, stack.fitA, color = 'C2', linewidth=2, linestyle="-", label="$A_{fit}$")
                    xmin = min(x)
                    xmax = max(x)
                else:
                    self.fitT.set_ydata(stack.fitT)
                    self.fitR.set_ydata(stack.fitR)
                    if settings.display_absorbCurve:
                        self.fitA.set_ydata(stack.fitA)
            
                if stack.online and not len(stack.measureT) == 0:
                    if refresh or not hasattr(self,'measureT'):
                        self.measureT, = self.axes.plot(stack.measure_wvl, stack.measureT, color = 'C0', linewidth=2, linestyle="--", label="$T_{online}$")
                        self.measureR, = self.axes.plot(stack.measure_wvl, stack.measureR, color = 'C1', linewidth=2, linestyle="--", label="$R_{online}$")
                        if settings.display_absorbCurve:
                            self.measureA, = self.axes.plot(stack.measure_wvl, stack.measureA, color = 'C2', linewidth=2, linestyle="--", label="$A_{online}$")
                    else:
                        self.measureT.set_ydata(stack.measureT)
                        self.measureR.set_ydata(stack.measureR)
                        if settings.display_absorbCurve:
                            self.measureA.set_ydata(stack.measureA)

                if settings.display_designCurvesInFit:
                    if not (stack.designT == None or len(stack.designT) == 0):
                        if refresh:
                            self.designT, = self.axes.plot(stack.fit_wvl, stack.designT, color = 'C0', linewidth=2, linestyle=":", label="$T_{design}$")
                            self.designR, = self.axes.plot(stack.fit_wvl, stack.designR, color = 'C1', linewidth=2, linestyle=":", label="$R_{design}$")
                            if settings.display_absorbCurve:
                                self.designA, = self.axes.plot(stack.fit_wvl, stack.designA, color = 'C2', linewidth=2, linestyle=":", label="$A_{design}$")
                        else:
                            self.designT.set_ydata(stack.designT)
                            self.designR.set_ydata(stack.designR)
                            if settings.display_absorbCurve:
                                self.designA.set_ydata(stack.designA)

            if refresh:
                self.axes.set_xlim(xmin, xmax)
                self.axes.set_ylim(0, 1)
                self.axes.set_xlabel('$Wavelength  (nm)$')
                self.axes.set_ylabel('Ratio')
                #print error string in plot: arg1 and 2 are x,y, transform indicates coordinates are indicated from 0,0 to 1,1.
                self.axes.xmargin = 0
                self.axes.ymargin = 0
            
                #if title != None:
                #   self.axes.set_title(title)

            system_time_string = 'Sys time: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_time_string = 'DB time:  ' + str(stack.measuredTime)
            txt_error = self.axes.text(0.007, 1.02, error_string, transform = self.axes.transAxes, weight = 'bold', fontsize = 12)
            txt_time = self.axes.text(0.207, 1.02, system_time_string, transform = self.axes.transAxes, weight = 'bold', fontsize = 12)
            txt_msr = self.axes.text(0.407, 1.02, db_time_string, transform = self.axes.transAxes, weight = 'bold', fontsize = 12)  
            
            if refresh:
                self.axes.legend(loc="upper right", prop={'size': 14})
                self.canvas.draw()
            else:
                self.axes.draw_artist(self.axes.patch)
                self.axes.draw_artist(self.fitT)
                self.axes.draw_artist(self.fitR)
                self.axes.draw_artist(self.measureT)
                self.axes.draw_artist(self.measureR)
                if settings.display_designCurvesInFit:
                    self.axes.draw_artist(self.designT)
                    self.axes.draw_artist(self.designR)
                self.axes.draw_artist(txt_error)
                self.axes.draw_artist(txt_time)
                self.axes.draw_artist(txt_msr)

                if settings.display_absorbCurve:
                    self.axes.draw_artist(self.fitA)
                    self.axes.draw_artist(self.measureA)
                    if settings.display_designCurvesInFit:
                        self.axes.draw_artist(self.designA)
                
                self.fig.canvas.update()
                self.fig.canvas.flush_events()
    
    def update_annot_design(self, ind, curveId):
        x,yT = self.designT.get_data()
        x,yR = self.designR.get_data()
        absorbCurve = True
        try:
            x,yA = self.designA.get_data()
        except AttributeError:
            absorbCurve = False
        t = ' '
        r = ' '
        a = ' '
        if curveId == 'T':
            y = yT
            t = '*'
        elif curveId == 'R':
            y = yR
            r = '*'
        elif absorbCurve:
            y = yA
            a = '*'
        self.annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
        #text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), " ".join([names[n] for n in ind["ind"]]))
        if absorbCurve:
            text = 'Wave: {:4.0f}\nT: {:4.2f} {}\nR: {:4.2f} {}\nA: {:4.2f} {}'.format(x[ind["ind"][0]], yT[ind["ind"][0]], t, yR[ind["ind"][0]], r, yA[ind["ind"][0]], a)
        else:
            text = 'Wave: {:4.0f}\nT: {:4.2f} {}\nR: {:4.2f} {}'.format(x[ind["ind"][0]], yT[ind["ind"][0]], t, yR[ind["ind"][0]], r)
        self.annot.get_bbox_patch().set_alpha(0.4)
        if y[ind["ind"][0]] > 0.8:
             self.annot.set_position((20,-20))
        else:
             #self.annot.xytext = (-20,20)
             self.annot.set_position((20,-20))
        self.annot.set_text(text)

    def hover_design(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes:
            cont1, ind1 = self.designT.contains(event)
            cont2, ind2 = self.designR.contains(event)
            try:
                cont3, ind3 = self.designA.contains(event)
            except AttributeError:
                cont3 = False
            if cont1 or cont2 or cont3:
                if cont1:
                    curveId = 'T'
                    ind = ind1
                elif cont2:
                    curveId = 'R'
                    ind = ind2
                else:
                    curveId = 'A'
                    ind = ind3
                self.update_annot_design(ind, curveId)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()