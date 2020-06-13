from flask import Flask,request,render_template
from flask_restful import Api
import pymongo as pm
import mongoengine as me
import RPi.GPIO as GPIO
import SimpleMFRC522
import datetime
from flaskext.mysql import MySQL
import mysql.connector as mariadb
import json
from bson import json_util
import requests
app = Flask(__name__)
api = Api(app)


#from flask_jwt_extended import JWTManager

#client = pm.MongoClient("mongodb+srv://dharmin_chothani:nokia5800@parkinglots-tqjoh.mongodb.net/parkinglots?retryWites=true")
#client = me.connect(host="mongodb://127.0.0.1", port = 27017)
#collname = client["lotstats"]
#print(client)
#client.lotstats(name="test", loc=[-87, 101]).save()
#print(client.lotstats.find())
#db = client.parkinglots
#db_new = client.rto
#db_new.lotstats.insert_one({"vehicle_no": "mh03db0939","intime" : datetime.datetime.now()})
#print(db_new.lotstats.find({}))


# write
def write(data):
    out = open("datafile.json", "w")
    json_out_data = json.dumps(data, indent=4, sort_keys=True, default=str)
    out.write(json_out_data)
    out.close()

def read():
    input = open("datafile.json", "r+")
    ifZero = len(input.read())
    print(ifZero)
    if (ifZero == 0):
        return(None)
    input.seek(0)
    data = json.loads(input.read())
    input.close()
    return(data)
#parkingid, no. of cars
#car, intime, outtime for history


app.config['JWT_SECRET_KEY'] = 'This-is-a-JWT-Secret-Key'
kk = app.config['JWT_SECRET_KEY'] = 'This-is-a-JWT-Secret-Key'

def readrfid():
    reader = SimpleMFRC522.SimpleMFRC522()
    try:
        return reader.read()
    finally:
        GPIO.cleanup()
def writerfid(text):
    try:
        writer = SimpleMFRC522.SimpleMFRC522()
        writer.write(text)
        return 1
    finally:
        GPIO.cleanup()

#jwt = JWTManager(app)

#import resources,write,read



@app.route("/test", methods = ['POST','GET'])
def test():
    readdata = read()
    print(readdata)
    if readdata is None:
        readdata = { "count" : 0, "vehicles" : []}
        print("readdata is blank")
    id,rawtext = readrfid()
#    z = list(x)
    text = rawtext.strip()
#    print(''.format(x,'b') for x in bytearray(text.encode('utf-8')))
#    print(type(z[0]),type(z[1]))
    blankStr = 'blank';
#    blankStr = '                                                ';
#    if request.method == "POST":
    vehNo =  request.form.get('vehi_no')
#    vehNo = "mh03db0939"
    if(vehNo =="" or vehNo is None):
        vehNo = "blank"
        print("veh no is now blankStr")
    print(type(vehNo))
    
    if text != blankStr:
        action = text + " is leaving."
        resp = writerfid(blankStr)
        print(blankStr+" written" + str(resp))
        #sendToDB()    
        vehicles=list()
        vehicles[:] = [d for d in readdata["vehicles"] if d.get('no') != text]
        print(readdata["count"])
        print("beforedecrementing")
        if readdata["count"] is not 0:
            readdata["count"] -= 1
        tbw = {"count" : readdata["count"], "vehicles":  vehicles}
        write(tbw)
       # sendData(readdata["count"],0,text)
        
    else:
        print(vehNo)
        writerfid(vehNo)        
        if vehNo is "blank":
            action = "Card is blank please enter the license number of vehicle entering"
            
        else:        
            action = vehNo + " is entering."
            readdata["vehicles"].append({"no": vehNo,"intime" : datetime.datetime.now()})
            readdata["count"]+=1
            write(readdata)
         #   sendData(readdata["count"],1,vehNo)
    return render_template("test.html",data=id,action=action,count=readdata["count"])


def sendData(count,inout,veh_no):
    parkingId = "5c746156038f338820f0ac4e"
    if inout ==  0:
        vehinouttime = "veh_out_time"
    else:
        vehinouttime = "veh_in_time"        
    data = json.dumps({ "id_of_lot" : parkingId,
             "veh_count" : count,
             vehinouttime : str(datetime.datetime.now()),"veh_no" : veh_no         
        })
    
    #r = requests.post(url="http://169.254.21.68:5000/capi", data = data)
    r = requests.post(url="http://192.168.137.216:5000/",data = data)
#192.168.137.122

#@app.route("/test", methods = ["POST","GET"])
#def test():
    
           

#if __name__ == "__main__":
#    app.run(debug=True,host='0.0.0.0')
