from PyQt5.QtCore import QThread, pyqtSignal, QMutex

import logging


logging.basicConfig(level=logging.DEBUG)


class AuthThread(QThread):
    authenticated = pyqtSignal(dict)
    failed = pyqtSignal(dict)

    def __init__(self, parent=None, broker_obj=None, id=None):
        super(AuthThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_obj = broker_obj
        self.id = id

    def run(self):
        logging.info("Start auth thread")
        try:
            ret, data = self.broker_obj.authenticate()
        except Exception as e:
            logging.error(e, exc_info=True)
        else:
            if ret == "OK":
                msg = {"id": self.id, "broker_obj": self.broker_obj}
                self.authenticated.emit(msg)
            else:
                msg = {"id": self.id, "content": data}
                self.failed.emit(msg)

    def stop(self):
        self._running = False
        logging.info("Stop auth thread...")
        self.terminate()
