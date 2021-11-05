import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from client_form import ClientForm
from parking_form import ParkingForm
from admin_form import AdminForm
import sqlconn as sqc
import os
import subprocess

ui, _ = loadUiType('main2.ui')
monthly_report_ui, _ = loadUiType('monthly_report.ui')


class MonthlyReportDialog(QDialog,monthly_report_ui):
    def __init__(self,parent=None):
        super(MonthlyReportDialog,self).__init__(parent)
        self.setupUi(self)

class MainApp(QMainWindow, ui):
    engine = sqc.Database().engine
    client = sqc.Database().client
    admin = sqc.Database().admin
    parking = sqc.Database().parking
    conn = engine.connect()

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()


    def Handle_UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.widget_dashboard.setVisible(False)
        self.Handle_Tables(self.parking_table)
        self.Handle_Tables(self.parking_record)
        self.Handle_Tables(self.client_table)
        self.Handle_Tables(self.admin_table)
        self.show_parking_buttons()
        self.show_parking_data()
        self.show_admin_table()
        self.show_client_data()
        self.parking_tab.setCurrentIndex(0)

    def Handle_Buttons(self):
        self.login_button.clicked.connect(self.login_button_action)
        self.widget_map_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.widget_parking_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.widget_client_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(3))
        self.widget_settings_button.clicked.connect(lambda: self.tabWidget.setCurrentIndex(4))
        self.widget_logout_button.clicked.connect(self.widget_logout_button_action)
        self.client_add_button.clicked.connect(lambda: self.add_data_action(ClientForm))
        self.client_update_button.clicked.connect(lambda: self.update_data_action(self.client_table,ClientForm))
        self.client_search.textChanged.connect(self.client_search_action)
        self.admin_add_button.clicked.connect(lambda: self.add_data_action(AdminForm))
        self.admin_update_button.clicked.connect(lambda: self.update_data_action(self.admin_table,AdminForm))


    def Handle_Tables(self,table_widget):
        table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        table_widget.resizeColumnsToContents()
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        table_widget.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        table_widget.setColumnHidden(0, True)



    def login_button_action(self):
        username = self.login_username.text()
        password = self.login_password.text()
        s = self.admin.select().where(self.admin.c.username == username)
        s_value = self.conn.execute(s)

        for val in s_value:
            if val[1] == username and val[2] == password:
                self.tabWidget.setCurrentIndex(1)
                self.widget_dashboard.setVisible(True)
            else:
                self.error_popup('Incorrect Password!')

        self.login_username.setText('')
        self.login_password.setText('')

    def show_admin_table(self):
        tableWidget = self.admin_table
        tableWidget.setRowCount(0)
        s = self.admin.select()
        s_value = self.conn.execute(s)

        for val in s_value:
            row_position = tableWidget.rowCount()
            tableWidget.insertRow(row_position)
            for i in range(0, 3):
                tableWidget.setItem(row_position, i, QTableWidgetItem(str(val[i])))


    def show_parking_buttons(self):
        occupied_list = []
        s = self.parking.select().where(self.parking.c.vacant == False)
        s_value = self.conn.execute(s)
        for val in s_value:
            occupied_list.append(val[2])

        for i in reversed(range(self.ParkingLot.count())):
            self.ParkingLot.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.ParkingLot2.count())):
            self.ParkingLot2.itemAt(i).widget().setParent(None)


        for i in range(50):
            current_num = i + 1
            color = 'white'
            vacant = True
            self.btn = QPushButton('{}'.format(current_num), self)
            if current_num in occupied_list:
                color = 'yellow'
                vacant = False
            if vacant == True:
                self.btn.clicked.connect(lambda checked, text=current_num:self.parking_slot_add(text))
            else:
                self.btn.clicked.connect(lambda checked, text=current_num:self.parking_slot_release(text))

            self.btn.setFont(QtGui.QFont('Segoe UI Black', 9))

            self.btn.setStyleSheet("border :2px solid ;"
                                   f"background-color: {color};"
                                 "border-top-color : black; "
                                 "border-left-color :black;"
                                 "border-right-color :black;"
                                 "border-bottom-color : black")

            self.btn.setMinimumSize(0,24)
            if current_num <= 25:
                self.ParkingLot.addWidget(self.btn)
            else:
                self.ParkingLot2.addWidget(self.btn)

    def show_parking_data(self):
        tableWidget = self.parking_table
        tableWidget.setRowCount(0)
        s = self.parking.select().where(self.parking.c.vacant == False)
        s_value = self.conn.execute(s)

        for val in s_value:
            row_position = tableWidget.rowCount()
            tableWidget.insertRow(row_position)
            for i in range(0, 10):
                tableWidget.setItem(row_position, i, QTableWidgetItem(str(val[i])))

        tableWidget = self.parking_record
        tableWidget.setRowCount(0)
        s = self.parking.select().where(self.parking.c.vacant == True)
        s_value = self.conn.execute(s)

        for val in s_value:
            row_position = tableWidget.rowCount()
            tableWidget.insertRow(row_position)
            for i in range(0, 10):
                tableWidget.setItem(row_position, i, QTableWidgetItem(str(val[i])))

    def parking_slot_add(self,lotid):
        data = ParkingForm(self)
        data.show()
        data.add_data(int(lotid))

    def parking_slot_release(self,lotid):
        data = ParkingForm(self)
        data.show()
        data.update_data(int(lotid))


    def error_popup(self,error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(error_message)
        msg.setWindowTitle("Error")
        msg.exec_()




    def widget_logout_button_action(self):
        self.tabWidget.setCurrentIndex(0)
        self.widget_dashboard.setVisible(False)

    def client_search_action(self):
        tableWidget = self.client_table
        tableWidget.setRowCount(0)
        current_text = self.client_search.text()
        engine = sqc.Database().engine
        client = sqc.Database().client
        conn = engine.connect()
        print(current_text)
        s = client.select().where(client.c.clientname.contains(current_text))
        s_value = conn.execute(s)

        for val in s_value:
            row_position = tableWidget.rowCount()
            tableWidget.insertRow(row_position)
            for i in range(0, 6):
                tableWidget.setItem(row_position, i, QTableWidgetItem(str(val[i])))
        conn.close()

    def show_client_data(self):
        tableWidget = self.client_table
        tableWidget.setRowCount(0)
        s = self.client.select()
        s_value = self.conn.execute(s)

        for val in s_value:
            row_position = tableWidget.rowCount()
            tableWidget.insertRow(row_position)
            for i in range(0, 6):
                tableWidget.setItem(row_position, i, QTableWidgetItem(str(val[i])))

    def add_data_action(self,Form):
        data = Form(self)
        data.show()
        data.add_data()

    def update_data_action(self,tableWidget,Form):
        try:
            r = tableWidget.currentRow()
            id = tableWidget.item(r, 0).text()
            data = Form(self)
            data.show()
            data.update_data(id)
        except Exception as e:
            self.error_popup(f"{e}")

    def settings_monthly_report_action(self):
        monthly_report_dialog = MonthlyReportDialog(self)
        monthly_report_dialog.show()

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
