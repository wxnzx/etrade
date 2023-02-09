from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import socket
import logging

logging.basicConfig(level=logging.DEBUG)


class LoginRqstThread(QThread):

    failed = pyqtSignal(str)
    signal_login_status = pyqtSignal(str)
    signal_login_result = pyqtSignal(str)

    def __init__(self, parent=None, address=None, socket=None, rqst_msg=""):
        super(LoginRqstThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.address = address
        self.rqst_msg = rqst_msg
        self._retry_count = 0

    def run(self):
        msg = "Starting login request\n"
        self.signal_login_status.emit(msg)
        logging.info("Starting connecting to server...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(7.0)
        try:
            msg = "正在连接服务器\n"
            logging.info(msg)
            self.signal_login_status.emit(msg)

            self.socket.connect(self.address)
        except ConnectionRefusedError as e:
            msg = "服务器未开启\n"
            logging.info(msg)
            self.signal_login_status.emit(msg)
            self.failed.emit(str(e))
        except socket.gaierror as e:
            msg = "服务器IP有误\n"
            logging.info(msg)
            self.signal_login_status.emit(msg)
            self.failed.emit(str(e))
        except OSError as e:
            msg = "服务器IP有误\n"
            logging.info(msg)
            self.signal_login_status.emit(msg)
            self.failed.emit(str(e))
        except Exception as e:
            logging.error(e, exc_info=True)
            msg = "无法连接服务器\n"
            logging.info(msg)
            self.signal_login_status.emit(msg)
            self.failed.emit(str(e))
        else:
            self.socket.settimeout(None)
            msg = "Successful. TCP client connected to \nIP:%s port:%s\n" % self.address
            logging.info(msg)
            self.signal_login_status.emit(msg)
        logging.info("start login request thread")
        try:
            self.socket.send(self.rqst_msg.encode("utf-8"))
        except Exception as e:
            logging.error(e, exc_info=True)
            self.failed.emit(str(e))
        while True:
            self.socket.settimeout(7.0)
            try:
                recv_msg = self.socket.recv(1024)
            except socket.error as serr:
                logging.error(e, exc_info=True)
                self.socket.close()
                self.failed.emit(str(serr))

            except Exception as e:
                logging.error(e, exc_info=True)
                self.failed.emit(str(e))
            else:
                self.socket.settimeout(None)
                if recv_msg:
                    logging.info(f"receiving msg:{recv_msg}")
                    msg = recv_msg.decode("utf-8")
                    self.signal_login_result.emit(msg)

                else:
                    self.failed.emit("服务器无响应")

    def stop(self):
        self._running = False
        logging.info("Stopping login requst thread...")
        self.terminate()
