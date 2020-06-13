from run import db 
import bcrypt
from flask import jsonify
import bson.json_util as bsj
from bson.objectid import ObjectId

users = db["Userinfo"]
PynPa = db["PayandParking"]
insertParking= db["fromUser"]


class UserRegister:
    def __init__(self,username,hashed,phone,email):
        self.username = username
        self.hashed = hashed
        self.phone = phone
        self.email = email
    def checkinDB(self):
        check = users.find({"Username":self.username}).count()
        if not check > 0 :
            uname = self.username
            pwd = self.hashed
            phne = self.phone
            eml = self.email
            users.insert({
                 "Username":uname,
                 "Password": pwd,
                 "phone" : phne,
                 "Emailid":eml
                     })
        else:
            return False

class UserLogin():

    def __init__(self,username,password):
        self.username = username
        self.password = password
    def checkuser(self):
        usname = users.find({
            "Username":self.username,
            })[0]["Username"]
        return usname
    
    def checkpass(self):
        pask = users.find({
            "Username":self.username,
            })[0]["Password"]
    
        
        ps = self.password
        decryptedpass = bcrypt.checkpw(ps.encode(), pask)
        print(bcrypt.checkpw(ps.encode(), pask))
        if decryptedpass is True:

            return decryptedpass
        else:
            return {
                "msg" : "wrong pass"
            }

class Nearlocate():
    def __init__(self,longitude,latitude):
        self.longitude = longitude
        self.latitude = latitude
        # self.lot_id = lot_id
        # self.occupied = occupied

    def locateNearest(self):
        lis_loc = []
        for loaction in db.PayandParking.find({"geometry":{"$near": {"$geometry":{"type": "Point","coordinates":[self.longitude,self.latitude]},"$minDistance":0,"$maxDistance":5000}}}):
            lis_loc.append(loaction)
        x = bsj.dumps(lis_loc)
        return x

class SubmitinPark():
    def __init__(self,name_of_lot,longi,lati):
        self.name_of_lot = name_of_lot
        self.longi = longi
        self.lati= lati
       
    def giveTheParking(self):
        insertParking.insert({
            "type": "Feature",
            "properties": {
                "name": self.name_of_lot,
                "descΩription": "",
                "parkingId": "",
                "city": "",
                "road": "",
                "landmark": "",
                "address": "",
                "latitude": self.lati,
                "longitude": self.longi,
                "capacity": "",
                "days": "",
                "direction": "",
                "restrictions": "",
                "towingStation": "",
                "category": "",
                "status new": "",
                "timing": "",
                "charging_hour": "",
                "vehicalType": "",
                "charges": "",
                "vehicleTypeId": "",
                "dislikes":0,
                "likes":0
            },
            "geometry": {
                "type": "Point",
                "coordinates": [self.longi,self.lati]
            }})
        return {
                "Status" : 200
        }

class PollingModel():
    def __init__(self,parkingObjectId,username,selectedPol):
        self.parkingObjectId = parkingObjectId
        self.username = username
        self.selectedPol = selectedPol
    def updatePol(self):
        # uObj = ObjectId(self.userObjectId)
        pObj = ObjectId(self.parkingObjectId)
        if self.selectedPol is True:
            db.fromUser.update_one({"_id": pObj},{"$inc": {"properties.likes":1}})
            db.Userinfo.update_one({"_id":self.username},{"$push":{"lotslike": { "$each" : [pObj] }}})
            return {
                "msg": "like added successfully",
                "code":200
            }
        elif self.selectedPol is False:
            db.fromUser.update_one({"_id": pObj},{"$inc": {"properties.dislikes":1}})
            db.Userinfo.update_one({"Username":self.username},{"$push":{"lotsdislike": { "$each" : [pObj] }}})
            return {
                "msg": "dislike added successfully",
                "code":200
            }
            
           
        return "done"
        
class getCapacity():
    def __init__(self,lot_id,used_space,vehi_in,vehi_out,vehicleno):
        self.lot_id = lot_id
        self.used_space = used_space
        self.vehicleno = vehicleno
        self.vehi_in = vehi_in
        self.vehi_out = vehi_out
    def insertcapac(self):
        y = ObjectId(self.lot_id)
        q =  db.PayandParking.update_one({"_id":y},{"$set" :{ "properties.occupied":self.used_space,"vehiclethe":self.vehicleno+self.vehi_in+self.vehi_out }})


        print(q)
        return jsonify({
            "status":200
        }) 
class Booking():
    def __init__(self,customer,parkinglot,spotid):
        self.customer = customer
        self.parkinglot = parkinglot
        self.spotid = spotid
    def bookd(self):
        y = ObjectId(self.parkinglot)
        qq = "properties.vacantspots"+self.spotid
        x = self.spotid
        db.PayandParking.update({"_id":y},{"$set" :{qq:"true"}})
        return{
            "msg":"Parking lot booked"
        }







    

"""
\\172.16.22.3
"""