# coding=utf-8
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import operator

# Kết nối cơ sở dữ liệu với các table

class TableModel(QAbstractTableModel):

  def __init__(self, parent, header, mylist, *args):
    QAbstractTableModel.__init__(self, parent, *args)
    super(TableModel, self).__init__()
    self.header = header
    self.mylist = mylist
    self.data = pd.DataFrame(self.mylist, columns=self.header)

  def update(self, in_data):
    self.data = in_data

  def rowCount(self, parent=None):
    return len(self.data.index)

  def columnCount(self, parent=None):
    return len(self.data.columns.values)

  def setData(self, index, value, role=None):
    if role == Qt.EditRole:
      row = index.row()
      col = index.column()
      column = self.data.columns.values[col]
      self.data.set_value(row, column, value)
      self.update(self.data)
      return True

  def data(self, index, role=None):
    if role == Qt.DisplayRole:
      row = index.row()
      col = index.column()
      value = self.data.iloc[row, col]
      return value

  def headerData(self, section, orientation, role=None):
    if role == Qt.DisplayRole:
      if orientation == Qt.Horizontal:
        return self.data.columns.values[section]

  # sắp xếp theo thứ tự
  def sort(self, Ncol, order):
    self.layoutAboutToBeChanged.emit()
    self.data = self.data.sort_values(self.header[Ncol],
                                      ascending=order == Qt.AscendingOrder)
    self.layoutChanged.emit()
