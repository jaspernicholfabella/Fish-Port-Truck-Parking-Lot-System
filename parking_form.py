from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlconn as sqc
import os
import datetime

parking_ui, _ = loadUiType(f'{os.getcwd()}\\ui\\parking.ui')

class ParkingForm(QDialog,parking_ui):
    engine = sqc.Database().engine
    client = sqc.Database().client
    admin = sqc.Database().admin
    parking = sqc.Database().parking
    conn = engine.connect()

    def __init__(self, parent=None):
        super(ParkingForm,self).__init__(parent)
        self.setupUi(self)
        self.Occupied.setVisible(False)
        self.OccupiedButtons.setVisible(False)
        self.Vacant.setVisible(False)
        self.VacantButtons.setVisible(False)
        self.cancel_button.clicked.connect(self.cancel_form)
        self.HandleUIChanges()

    def HandleUIChanges(self):
        s = self.client.select().order_by(self.client.c.clientname)
        s_value = self.conn.execute(s)
        for val in s_value:
            self.comboBox.addItem(f"{val[1]} - {val[0]}")


    def cancel_form(self):
        self.close()

    def add_data(self,lotid):
        self.Vacant.setVisible(True)
        self.VacantButtons.setVisible(True)
        self.parking_label.setText(f'Parking Lot # {lotid} (Vacant)')
        self.save_button.clicked.connect(lambda: self.add_data_action(lotid))


    def update_data(self,lotid):
        self.Occupied.setVisible(True)
        self.OccupiedButtons.setVisible(True)
        s = self.parking.select().where(self.parking.c.parkinglotid == int(lotid))
        s_value = self.conn.execute(s)

        for val in s_value:
            self.balance.setText(str(val[6]))
            self.overdue.setText(str(val[7]))
            self.timestarted.setText(str(val[3]))
            t = self.client.select().where(self.client.c.clientid == val[1])
            t_value = self.conn.execute(t)
            for tval in t_value:
                self.clientname.setText(str(tval[1]))

        self.parking_label.setText(f'Parking Lot # {lotid} (Occupied)')
        self.release_button.clicked.connect(lambda: self.update_data_action(lotid))

    def add_data_action(self,lotid):
        try:
            clientid = int(self.comboBox.currentText().split('-')[1].strip())
            print(lotid)
            s = self.parking.insert().values(
                clientid=clientid,
                parkinglotid=int(lotid),
                timein = datetime.datetime.utcnow(),
                ratehr = float(self.rate.text()),
                balance = float(self.payment.text()),
                vacant = False
            )
            self.conn.execute(s)
        except Exception as e:
            print(e)
        self.parent().show_parking_buttons()
        self.parent().show_parking_data()
        self.close()

    def update_data_action(self,lotid):
        try:
            parkid = 0
            t = self.parking.select().where(self.parking.c.parkinglotid==lotid).where(self.parking.c.vacant == False)
            t_value = self.conn.execute(t)
            for tval in t_value:
                parkid = tval[0]
                balance = tval[6]

            overdue = float(str(self.overdue.text()).replace("php",""))
            total = overdue + balance

            s = self.parking.update().where(self.parking.c.parkingid == parkid).\
            values(
                overdue = overdue,
                timeout = datetime.datetime.utcnow(),
                total=float(total),
                vacant = True
            )
            print('parkid')
            self.conn.execute(s)
            self.parent().show_parking_buttons()
            self.parent().show_parking_data()
            self.close()
        except Exception as e:
            self.print(e)
            self.parent().error_popup(e)


