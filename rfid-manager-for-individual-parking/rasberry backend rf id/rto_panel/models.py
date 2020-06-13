from run import db,db_new 
import bcrypt
from flask import jsonify
import bson.json_util as bsj
from bson.objectid import ObjectId
import datetime
'''
import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()
def read():
    try:
        id, text = reader.read()
        return([id,text])
    finally:
        GPIO.cleanup()

def rWrite(text):
    try:
        reader.write(text)
        print("Written")
    finally:
        GPIO.cleanup()

def getParkingName():
    return "Ghatkopar West"
    '''
class InsertVehicle():
    def __init__(self,rfid,vehicle,ISOtime):
        self.rfid = rfid
        self.vehicle = vehicle
        self.ISOtime = datetime.datetime.now()

    # def insert_data_in_localdb(self):
    #     x = db.fpp.find_one({"rfid":self.rfid})
    #     if not x:
    #         db.fpp.insert_one({'rid':self.rfid,'rfid':[{'vehicle':self.vehicle,'ISOtime': self.ISOtime}] ,'status':1})
    #     elif x:
    #         db.fpp.update_one ({})

    def handleRfid(self):
        x = db_new.lotstats.find_one_and_delete({"rfid":self.rfid})
        if not x:
            db_new.lotstats.insert_one({"vehicle_no": self.vehicle,"intime" : datetime.datetime.now()})  #rdecode tb defined
            rWrite(self.vehicle)
        else:
            db_1.lotstats.update({"vehicle_no": self.rfid}, { "$push": { "lots": [ {"name":getParkingName()},{"inTime": getIntime()},{"outTime" : datetime.datetime.now()} ] }} ,{upsert:True}) 
            rWrite("")