from sqlalchemy import create_engine
from sqlalchemy import Table, Column,VARCHAR,INTEGER,Float,String, MetaData,ForeignKey,DateTime,Text,DECIMAL,Boolean
from sqlalchemy.sql import exists
import os
class Database():
    engine = create_engine('sqlite:///{}/db/data.sql'.format(os.getcwd()))
    meta = MetaData()

    admin = Table('admin',meta,
                    Column('userid',INTEGER,primary_key=True),
                    Column('username',VARCHAR(50)),
                    Column('password',VARCHAR(50)),)

    client = Table('client',meta,
                  Column('clientid',INTEGER,primary_key=True),
                  Column('clientname',VARCHAR(50)),
                  Column('licenseno',VARCHAR(50)),
                  Column('plateno', VARCHAR(50)),
                  Column('carmodel', VARCHAR(50)),
                  Column('carcolor', VARCHAR(50)))

    parking = Table('parking',meta,
                  Column('parkingid',INTEGER,primary_key=True),
                  Column('clientid',INTEGER),
                  Column('parkinglotid',INTEGER),
                  Column('timein',DateTime),
                  Column('timeout',DateTime),
                  Column('ratehr', Float,default=50),
                  Column('balance', Float,default=0),
                  Column('overdue', Float,default=0),
                  Column('total', Float,default=0),
                  Column('vacant',Boolean,default=True))


    meta.create_all(engine)
    conn = engine.connect()

    ##adding default values to admin
    s = admin.select()
    s_value = conn.execute(s)
    z = 0
    for val in s_value:
        z += 1

    if z == 0:
        ins = admin.insert().values(username = 'admin',password = 'admin')
        result = conn.execute(ins)