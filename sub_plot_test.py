import sys
import time

import numpy as np
import pyodbc

from Settings import Settings
from Stack import Stack as stack


from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        self.setting=Settings()
        self.stack = stack()
        

        #spec_canvas = FigureCanvas(Figure(figsize=None))
        #layout.addWidget(dynamic_canvas)

        dynamic_canvas = FigureCanvas(Figure(figsize=(8, 5)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

    def liveSpec(self):
        stack = self.stack

        connect_string = "Driver={" + self.settings.SQL_driver + "};\
                        Server=" + self.settings.SQL_server + ";\
                        Database=" + self.settings.SQL_DB + ";\
                        Trusted_Connection=yes;"

        conn = pyodbc.connect(connect_string)
        cursor = conn.cursor()

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
        

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.array(self.setting.standard_wave_list)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, t)
        ttt = np.linspace(0,300, 1110, 2501)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(ttt, 1000*np.sin(ttt + time.time()))
        #self._dynamic_ax.plot(t,np.cos(t+time.time()))
        #print(type(self.spectrum))
        self._dynamic_ax.figure.canvas.draw()
        

if __name__ == "__main__":
    
    qapp = QtWidgets.QApplication(sys.argv)
    #stack = Stack()
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
