# coding=utf-8
import sys
from PyQt5 import QtCore, QtWidgets, uic
import Resource

# Hiển thị bảng giới thiệu sản phẩm

class MyWindow(QtWidgets.QDialog):

  def __init__(self):
    # Load UI
    super(MyWindow, self).__init__()
    uic.loadUi('About.ui', self)
    # Build form
    self.exec_()

if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MyWindow()
  sys.exit(app.exec_())
