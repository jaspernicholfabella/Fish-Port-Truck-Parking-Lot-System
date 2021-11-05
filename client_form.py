from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlconn as sqc
import os

client_ui, _ = loadUiType(f'{os.getcwd()}\\ui\\client.ui')

class ClientForm(QDialog,client_ui):
    engine = sqc.Database().engine
    client = sqc.Database().client
    conn = engine.connect()

    def __init__(self, parent=None):
        super(ClientForm,self).__init__(parent)
        self.setupUi(self)
        self.cancel_button.clicked.connect(self.cancel_form)

    def cancel_form(self):
        self.close()

    def add_data(self):
        self.client_label.setText('Add Client')
        self.save_button.clicked.connect(self.add_client_action)

    def update_data(self,clientid):
        s = self.client.select().where(self.client.c.clientid == int(clientid))
        s_value = self.conn.execute(s)
        for val in s_value:
            self.client_name.setText(str(val[1]))
            self.client_license_no.setText(str(val[2]))
            self.car_plate_no.setText(str(val[3]))
            self.car_model.setText(str(val[4]))
            self.car_color.setText(str(val[5]))

        self.client_label.setText('Update Client')
        self.save_button.clicked.connect(lambda: self.update_client_action(clientid))

    def add_client_action(self):
        s = self.client.insert().values(
            clientname=self.client_name.text(),
            licenseno=self.client_license_no.text(),
            plateno = self.car_plate_no.text(),
            carmodel = self.car_model.text(),
            carcolor = self.car_color.text()
        )
        self.conn.execute(s)
        self.parent().show_client_data()
        self.close()

    def update_client_action(self,clientid):
        s = self.client.update().where(self.client.c.clientid == clientid).\
            values(clientname=self.client_name.text(),
                    licenseno=self.client_license_no.text(),
                    plateno = self.car_plate_no.text(),
                    carmodel = self.car_model.text(),
                    carcolor = self.car_color.text())
        self.conn.execute(s)
        self.parent().show_client_data()
        self.close()


