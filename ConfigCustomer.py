# coding=utf-8
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from module import Database, TableModel, Camera

class MyWindow(QtWidgets.QDialog):
  f_customerId = 0

  def __init__(self):
    # Load UI
    super(MyWindow, self).__init__()
    uic.loadUi('ConfigCustomer.ui', self)
    # Load button event
    self.Database_1 = Database.Server_1('10.228.112.112')
    self.pushButton_Insert.clicked.connect(self.insert)
    self.pushButton_Update.clickaed.connect(self.update)
    self.pushButton_Delete.clicked.connect(self.delete)
    self.pushButton_Clear.clicked.connect(self.clear)

    # Load table list customer
    self.tableView_customerList.setShowGrid(False)
    self.loadtableView_CustomerList()
    self.tableView_customerList.resizeColumnsToContents()
    self.tableView_customerList.horizontalHeader().setStretchLastSection(True)
    self.tableView_customerList.clicked.connect(self.rowClick)
    self.tableView_customerList.setSelectionBehavior(1)
    self.tableView_customerList.sortByColumn(0, QtCore.Qt.AscendingOrder)
    self.tableView_customerList.setSortingEnabled(True)

    # Load Camera
    self.initializationCam()

    # Build form
    self.exec_()

  # connect to camera
  def initializationCam(self):
    self.video = Camera.Video(0)
    self._timer = QtCore.QTimer(self)
    self._timer.timeout.connect(self.loadCamera)
    self.loadCamera()

  # load Table View
  def loadtableView_CustomerList(self):
    header = ['Customer ID', 'CMTND', 'Customer Name', 'Phone', 'Address']
    model = TableModel.TableModel(self, header, self.customer_GetList())
    self.tableView_customerList.setModel(model)

  # process Click button
  def rowClick(self):
    try:
      for index in self.tableView_customerList.selectedIndexes():
        data = index.data()
        if index.column() == 0:
          self.f_customerId = data
        if index.column() == 1:
          self.lineEdit_CMTND.setText(data)
          self.loadImageSample(data)
        elif index.column() == 2:
          self.lineEdit_CustomerName.setText(data)
        elif index.column() == 3:
          self.lineEdit_Phone.setText(data)
        elif index.column() == 4:
          self.lineEdit_Address.setText(data)
    except Exception as e:
      QtWidgets.QMessageBox.critical(None, 'Error', str(e))

  # process list customer
  def customer_GetList(self):
    rows = self.Database_1.execute('EXECUTE [dbo].[customer_GetList]').fetchall()
    data = []
    for row in rows:
      try:
        data.append([str(i) for i in row]);
      except Exception as e:
        QtWidgets.QMessageBox.critical(None, 'Error', str(e))
    return data

  def loadCamera(self):
    self._timer.start(27)
    try:
      self.video.captureNextFrame()
      self.label_videoFrame.setPixmap(self.video.convertFrame())
      self.label_videoFrame.setScaledContents(True)
    except TypeError:
      print("No frame")

  def loadImageSample(self, id):
    path = 'image/User.' + id + '.jpg'
    self.graphicsView_Image.setScene(None)
    scene = QtWidgets.QGraphicsScene()
    scene.addPixmap(QtGui.QPixmap(path))
    self.graphicsView_Image.setScene(scene)

  def insert(self):
    CMTND = str(self.lineEdit_CMTND.text())
    customerName = str(self.lineEdit_CustomerName.text())
    phone = str(self.lineEdit_Phone.text())
    address = str(self.lineEdit_Address.text())
    if (CMTND == '' or customerName == ''):
      QtWidgets.QMessageBox.critical(None, 'Error', 'Not enough inputed (*) value')
      return
    result = self.Database_1.execute('EXECUTE [dbo].[customer_Insert] ''?'',''?'',''?'',''?''',
                                     (CMTND, customerName, phone, address)).fetchall()
    for value in result:
      if value[0] == 'O':
        self.video.captureFace(CMTND)
        self.video.trainingFace()
        QtWidgets.QMessageBox.information(None, 'Susscess', 'Action susscess')
        self.loadImageSample(CMTND)
        self.loadtableView_CustomerList()
        self.clear()
      else:
        QtWidgets.QMessageBox.critical(None, 'Error', value[1])
        return

  def update(self):
    customerId = self.f_customerId
    CMTND = str(self.lineEdit_CMTND.text())
    customerName = str(self.lineEdit_CustomerName.text())
    phone = str(self.lineEdit_Phone.text())
    address = str(self.lineEdit_Address.text())
    if customerId == 0 or CMTND == '' or customerName == '':
      QtWidgets.QMessageBox.critical(None, 'Error', 'Not enough inputed (*) value')
      return

    result = self.Database_1.execute('EXECUTE [dbo].[customer_Update] ''?'',''?'',''?'',''?'',''?''',
                                     (customerId, CMTND, customerName, phone, address)).fetchall()
    for value in result:
      if value[0] == 'O':
        # If check Retraining then action
        if self.checkBox_Retraining.isChecked():
          self.video.captureFace(CMTND)
          self.video.trainingFace()
        QtWidgets.QMessageBox.information(None, 'Susscess', 'Action susscess')
        self.loadImageSample(CMTND)
        self.loadtableView_CustomerList()
      else:
        QtWidgets.QMessageBox.critical(None, 'Error', value[1])
        return

  def delete(self):
    customerId = self.f_customerId
    if customerId == 0:
      QtWidgets.QMessageBox.critical(None, 'Error', 'No record need delete')
      return

    confirm = QtWidgets.QMessageBox.question(self, 'Message',
                                             'Are you sure you want to delete ?', QtWidgets.QMessageBox.Yes,
                                             QtWidgets.QMessageBox.No)
    if confirm == QtWidgets.QMessageBox.Yes:
      if len(customerId) > 0:
        result = self.Database_1.execute('EXECUTE [dbo].[customer_Delete] ''?''',
                                         (customerId)).fetchall()
        for value in result:
          if value[0] == 'O':
            QtWidgets.QMessageBox.information(None, 'Susscess', 'Action susscess')
            self.loadtableView_CustomerList()
            self.clear()
          else:
            QtWidgets.QMessageBox.critical(None, 'Error', value[1])
            return
    else:
      return

  def clear(self):
    self.f_customerId = 0
    self.lineEdit_CMTND.setText('')
    self.lineEdit_CustomerName.setText('')
    self.lineEdit_Phone.setText('')
    self.lineEdit_Address.setText('')


if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MyWindow()
  sys.exit(app.exec_())
