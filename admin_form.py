from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlconn as sqc
import os

client_ui, _ = loadUiType(f'{os.getcwd()}\\ui\\admin.ui')

class AdminForm(QDialog,client_ui):
    engine = sqc.Database().engine
    admin = sqc.Database().admin
    conn = engine.connect()

    def __init__(self, parent=None):
        super(AdminForm,self).__init__(parent)
        self.setupUi(self)
        self.cancel_button.clicked.connect(self.cancel_form)

    def cancel_form(self):
        self.close()

    def add_data(self):
        self.admin_label.setText('Add Admin Account')
        self.save_button.clicked.connect(self.add_admin_action)

    def update_data(self,userid):
        s = self.admin.select().where(self.admin.c.userid == int(userid))
        s_value = self.conn.execute(s)
        for val in s_value:
            self.username.setText(str(val[1]))
            self.password.setText(str(val[2]))
        self.admin_label.setText('Update Admin Account')
        self.save_button.clicked.connect(lambda:self.update_admin_action(userid))

    def add_admin_action(self):
        s = self.admin.insert().values(
            username=self.username.text(),
            password=self.password.text(),
        )
        self.conn.execute(s)
        self.parent().show_admin_table()
        self.close()

    def update_admin_action(self,userid):
        s = self.admin.update().where(self.admin.c.userid == int(userid)).\
            values(username=self.username.text(),
                    password=self.password.text(),)
        self.conn.execute(s)
        self.parent().show_admin_table()
        self.close()


