import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd


class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class OrderModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role == Qt.BackgroundRole:
            row = index.row()
            col = index.column()
            open_order_status = [
                "NONE",
                "WAITING_SUBMIT",
                "SUBMITTING",
                "SUBMITTED",
                "FILLED_PART",
                "Submitted", 
                "PreSubmitted"
            ]
            if col == 2:
                if self._data.iloc[row, col] == "BUY":
                    return QVariant(QBrush(QColorConstants.Svg.lightgreen))
                elif self._data.iloc[row, col] == "SELL":
                    return QVariant(QBrush(QColorConstants.Svg.lightcoral))
            elif col == 8:
                if self._data.iloc[row, col] in open_order_status:
                    if self._data.iloc[row, 2] == "BUY":
                        return QVariant(QBrush(QColorConstants.Svg.lightgreen))
                    elif self._data.iloc[row, 2] == "SELL":
                        return QVariant(QBrush(QColorConstants.Svg.lightcoral))
                elif self._data.iloc[row, col] == "FILLED_ALL":
                    return QVariant(QBrush(QColorConstants.Svg.lightskyblue))
                elif self._data.iloc[row, col] == "CANCELLED_ALL":
                    return QVariant(QBrush(QColorConstants.Svg.lightgrey))
                elif self._data.iloc[row, col] == "CANCELLED_PART":
                    return QVariant(QBrush(QColorConstants.Svg.mediumpurple))

        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
