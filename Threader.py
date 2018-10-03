import threading
from PyQt5.QtCore import *

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, t1, a1):
        super(StoppableThread, self).__init__(target = t1, args = a1)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

'''
class StoppableQThread(QThread):
    """QThread needs work!!!."""

    def __init__(self):
        #super(StoppableQThread, self).__init__(self)
        QThread.__init__(self)
        self._stop_event = QThread.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
'''

