from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import time
import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)


class QuoteThread(QThread):

    failed = pyqtSignal()
    signal_quote = pyqtSignal(pd.DataFrame)

    def __init__(
        self,
        parent=None,
        quote_broker_obj=None,
        symbol=None,
    ):
        super(QuoteThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.quote_broker_obj = quote_broker_obj
        self.symbol = symbol

    def run(self):
        logging.info("Start quote thread...")
        while True:
            try:
                quote = self.yahoo_quote()
            except Exception as e:
                self.failed.emit()
            else:
                self.signal_quote.emit(quote)
            time.sleep(3)

    def stop(self):
        self._running = False
        logging.info("Stop quote thread...")
        self.terminate()

    def yahoo_quote(self):
        url = f"https://finance.yahoo.com/quote/{self.symbol}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        header_id = "Lead-5-QuoteHeader-Proxy"
        price = soup.find("div", {"id": header_id}).find("fin-streamer").text
        quote_id = "quote-summary"
        prev_close = (
            soup.find("div", {"id": quote_id})
            .find("td", {"data-test": "PREV_CLOSE-value"})
            .text
        )
        open = (
            soup.find("div", {"id": quote_id})
            .find("td", {"data-test": "OPEN-value"})
            .text
        )
        bid = (
            soup.find("div", {"id": quote_id})
            .find("td", {"data-test": "BID-value"})
            .text
        )
        ask = (
            soup.find("div", {"id": quote_id})
            .find("td", {"data-test": "ASK-value"})
            .text
        )
        volume = (
            soup.find("div", {"id": quote_id})
            .find("td", {"data-test": "TD_VOLUME-value"})
            .find("fin-streamer")
            .text
        )

        return pd.DataFrame(
            {
                "symbol": self.symbol,
                "price": price,
                "prev_close": prev_close,
                "open": open,
                "bid": bid,
                "ask": ask,
                "volume": volume,
            },
            index=[0],
        )

    def xueqiu_quote(self):

        url = f"https://stock.xueqiu.com/v5/stock/quote.json?symbol={self.symbol}&extend=detail"
        response = requests.get(url)


if __name__ == "__main__":
    quote_obj = QuoteThread(symbol="CJJD")
    quote_obj.xueqiu_quote()
