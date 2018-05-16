# coding=utf-8
import sys
from PyQt5 import QtCore, QtWidgets, uic
from module import Database, TableModel, Camera
from datetime import datetime


class MyWindow(QtWidgets.QMainWindow):
    dataInvoiceCustomer = []
    customerFoundList = []

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('Main.ui', self)
        # self.setWindowState(QtCore.Qt.WindowMaximized) #Set maxwindow
        self.show()
        # Load event items
        self.Database_1 = Database.Server_1('10.228.112.112')

        # Link menu
        self.actionConfig_Customer.triggered.connect(self.showConfigCustomer)
        self.actionConfig_Item.triggered.connect(self.showConfigItem)
        self.actionConfig_Invoice.triggered.connect(self.showConfigInvoice)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionConfig_Employee.triggered.connect(self.showConfigEmployee)

        # Load Camera
        self.initializationCam()

    #Connect camera
    def initializationCam(self):
        self.video = Camera.Video(0)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.loadCamera)
        self.loadCamera()

    #Load camera
    def loadCamera(self):
        self._timer.start(27)
        try:
            defect_out = []
            names = self.customer_GetList()

            #Nhân diện khách hàng sử dụng hàm recogitionFace trong Class Camera.py
            self.video.recogitionFace(names, defect_out)

            self.label_videoFrame.setPixmap(self.video.convertFrame())
            self.label_videoFrame.setScaledContents(True)
            self.loadTableView_Data(defect_out)
        except TypeError:
            print("No frame")

    #getList customer
    def customer_GetList(self):
        rows = self.Database_1.execute('EXECUTE [dbo].[customer_GetList]').fetchall()
        data = []
        for row in rows:
            try:
                data.append({'id': row.cmtnd, 'name': row.customer_name})
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, 'Error', str(e))
        return data

    # Load dữ liệu thông tin khách hàng lên hệ thống
    def loadTableView_Data(self, data_list):
        header = ['Invoice ID', 'Invoice Code', 'Customer Name', 'Date', 'Money', 'Item List','Employee']
        # data = []

        for customer in data_list:
            if customer not in self.customerFoundList:
                rows = self.Database_1.execute('EXECUTE [dbo].[invoiceHeader_GetList_ByCMTND] ''?''',
                                               (customer['id'])).fetchall()
                for row in rows:
                    # data.append([str(i) for i in row])
                    self.dataInvoiceCustomer.insert(0,[str(i) for i in row])

                # Code gui email tạm thời chưa thực hiện được !


                self.customerFoundList.append(customer)

        # Xuat file txt
        if self.dataInvoiceCustomer != []:
            theFile = open('file/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.txt', 'w')
            for item in self.dataInvoiceCustomer:
                theFile.write('\n'.join(str(x) for x in item) + '\n')
            theFile.close()


        model = TableModel.TableModel(self, header, self.dataInvoiceCustomer)
        self.tableView_Data.setModel(model)
        self.tableView_Data.resizeRowsToContents()


    #show các Button ra hệ thống

    def showConfigCustomer(self):
        self._timer.stop()
        # self.video.quit()
        del self._timer
        del self.video
        import ConfigCustomer
        ConfigCustomer.MyWindow()
        self.initializationCam()

    def showConfigEmployee(self):
        # self._timer.stop()
        self._timer.stop()
        # self.video.quit()
        del self._timer
        del self.video
        import ConfigEmployee
        ConfigEmployee.MyWindow()
        self.initializationCam()
        # self._timer.start(27)

    def showConfigItem(self):
        # self._timer.stop()
        self._timer.stop()
        # self.video.quit()
        del self._timer
        del self.video
        import ConfigItem
        ConfigItem.MyWindow()
        self.initializationCam()
        # self._timer.start(27)

    def showConfigInvoice(self):
        # self._timer.stop()
        self._timer.stop()
        # self.video.quit()
        del self._timer
        del self.video
        import ConfigInvoice
        ConfigInvoice.MyWindow()
        self.initializationCam()
        # self._timer.start(27)

    def showAbout(self):
        self._timer.stop()
        import About
        About.MyWindow()
        self._timer.start(27)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
