# coding=utf-8
import sys, datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from module import Database, TableModel

class MyWindow(QtWidgets.QDialog):
  f_itemId = 0

  def __init__(self):
    # Load UI
    super(MyWindow, self).__init__()
    uic.loadUi('ConfigInvoice.ui', self)
    # Load button event
    self.Database_1 = Database.Server_1('10.228.112.112')
    self.lineEdit_Quantity.setValidator(QtGui.QIntValidator(0, 999999999, self))
    self.loadcomboBox_Customer()
    self.pushButton_CreateInvoice.clicked.connect(self.createInvoice)
    self.comboBox_Item.currentIndexChanged.connect(self.calculateMoney)
    self.lineEdit_Quantity.textChanged.connect(self.calculateMoney)
    self.pushButton_AddItem.clicked.connect(self.addItem)
    self.pushButton_SaveInvoice.clicked.connect(self.saveInvoice)
    self.pushButton_Clear.clicked.connect(self.clear)

    # Load table list item
    self.tableView_InvoiceHeader.setShowGrid(False)
    self.loadtableView_InvoiceHeader()
    self.tableView_InvoiceHeader.resizeColumnsToContents()
    self.tableView_InvoiceHeader.horizontalHeader().setStretchLastSection(True)
    # self.tableView_InvoiceHeader.clicked.connect(self.rowClick)
    self.tableView_InvoiceHeader.setSelectionBehavior(1);
    self.tableView_InvoiceHeader.sortByColumn(0, QtCore.Qt.AscendingOrder)
    self.tableView_InvoiceHeader.setSortingEnabled(True)
    self.header = ['Item Id', 'Item Name', 'Quantity', 'Money']
    self.data = []

    # Build form
    self.exec_()

  def loadtableView_InvoiceHeader(self):
    header = ['Invoice ID', 'Invoice Code', 'Customer Name', 'Date', 'Total Money']
    model = TableModel.TableModel(self, header, self.item_GetList())
    self.tableView_InvoiceHeader.setModel(model)

  def rowClick(self):
    try:
      for index in self.tableView_InvoiceHeader.selectedIndexes():
        data = index.data()
        if index.column() == 0:
          self.f_itemId = data
        if index.column() == 1:
          self.lineEdit_ItemCode.setText(data)
        elif index.column() == 2:
          self.lineEdit_ItemName.setText(data)
        elif index.column() == 3:
          self.lineEdit_Money.setText(data)
    except Exception as e:
      QtWidgets.QMessageBox.critical(None, 'Error', str(e))

  def item_GetList(self):
    rows = self.Database_1.execute('EXECUTE [dbo].[invoiceHeader_GetList]').fetchall()
    data = []
    for row in rows:
      try:
        data.append([str(i) for i in row]);
      except Exception as e:
        QtWidgets.QMessageBox.critical(None, 'Error', str(e))
    return data

  def loadcomboBox_Customer(self):
    self.comboBox_Customer.clear()
    rows = self.Database_1.execute('EXECUTE [dbo].[customer_GetList]').fetchall()
    self.comboBox_Customer.addItem('', -1)
    for row in rows:
      try:
        self.comboBox_Customer.addItem(row.customer_name, row.customer_id)
      except Exception as e:
        QtWidgets.QMessageBox.critical(None, 'Error', str(e))

  def loadcomboBox_Item(self):
    self.comboBox_Item.clear()
    rows = self.Database_1.execute('EXECUTE [dbo].[item_GetList]').fetchall()
    self.comboBox_Item.addItem('', -1)
    for row in rows:
      try:
        self.comboBox_Item.addItem(row.item_name + ' (' + str(row.money) + ')', row.item_id)
      except Exception as e:
        QtWidgets.QMessageBox.critical(None, 'Error', str(e))

  def createInvoice(self):
    customerId = self.comboBox_Customer.itemData(self.comboBox_Customer.currentIndex())
    if (customerId == -1):
      QtWidgets.QMessageBox.critical(None, 'Error', 'Not enough inputed (*) value')
      return
    self.lineEdit_InvoiceCode.setText(
      'INVOICE_' + str(customerId) + '_' + datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
    self.comboBox_Customer.setEnabled(False)
    self.pushButton_CreateInvoice.setEnabled(False)

    self.tableView_InvoiceHeader.setEnabled(False)
    self.comboBox_Item.setEnabled(True)
    self.lineEdit_Quantity.setEnabled(True)
    self.lineEdit_Money.setEnabled(True)
    self.pushButton_AddItem.setEnabled(True)
    self.loadcomboBox_Item()

  def calculateMoney(self):
    itemId = self.comboBox_Item.itemData(self.comboBox_Item.currentIndex())
    quantity = self.lineEdit_Quantity.text()
    if itemId != -1 and quantity != '':
      price = self.comboBox_Item.currentText()
      price = price[price.rfind('(') + 1:price.rfind(')')]
      self.lineEdit_Money.setText(str(int(price) * int(quantity)))

  def addItem(self):
    itemId = str(self.comboBox_Item.itemData(self.comboBox_Item.currentIndex()))
    itemName = self.comboBox_Item.currentText()
    quantity = self.lineEdit_Quantity.text()
    money = self.lineEdit_Money.text()
    if (itemId == -1 or quantity == ''):
      QtWidgets.QMessageBox.critical(None, 'Error', 'Not enough inputed (*) value')
      return
    self.data.append([itemId, itemName, quantity, money])
    model = TableModel.TableModel(self, self.header, self.data)
    self.tableView_InvoiceDetail.setModel(model)
    self.pushButton_SaveInvoice.setEnabled(True)

  def saveInvoice(self):
    invoiceCode = self.lineEdit_InvoiceCode.text()
    customerId = self.comboBox_Customer.itemData(self.comboBox_Customer.currentIndex())
    result = self.Database_1.execute('EXECUTE [dbo].[invoiceHeader_Insert] ''?'',''?''',
                                     (invoiceCode, customerId)).fetchall()
    for value in result:
      if value[0] == 'O':
        invoiceHeaderId = value[1]
        itemId = ''
        quantity = ''
        model = self.tableView_InvoiceDetail.model()
        for row in range(model.rowCount()):
          for column in range(model.columnCount()):
            if column == 0:
              itemId = model.index(row, column).data()
            if column == 2:
              quantity = model.index(row, column).data()

          self.Database_1.execute('EXECUTE [dbo].[invoiceDetail_Insert] ''?'',''?'',''?''',
                                  (invoiceHeaderId, itemId, quantity)).fetchall()

        QtWidgets.QMessageBox.information(None, 'Susscess', 'Action susscess')
        self.clear()
        self.loadtableView_InvoiceHeader()
      else:
        QtWidgets.QMessageBox.critical(None, 'Error', value[1])
        return

  def clear(self):
    self.tableView_InvoiceHeader.setEnabled(True)
    self.comboBox_Customer.setEnabled(True)
    self.pushButton_CreateInvoice.setEnabled(True)
    self.comboBox_Item.setEnabled(False)
    self.lineEdit_Quantity.setEnabled(False)
    self.lineEdit_Money.setEnabled(False)
    self.pushButton_AddItem.setEnabled(False)
    self.pushButton_SaveInvoice.setEnabled(False)

    self.comboBox_Customer.setCurrentIndex(0)
    self.comboBox_Item.setCurrentIndex(0)
    self.lineEdit_Quantity.setText('')
    self.lineEdit_Money.setText('')
    self.lineEdit_InvoiceCode.setText('')

    self.header = ['Item Id', 'Item Name', 'Quantity', 'Money']
    self.data = []
    model = TableModel.TableModel(self, self.header, self.data)
    self.tableView_InvoiceDetail.setModel(model)


if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MyWindow()
  sys.exit(app.exec_())
