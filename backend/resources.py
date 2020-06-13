from flask_restful import Resource,request
from flask import jsonify
import models
import bcrypt
import jwt
import datetime
from functools import wraps
import json

def token_required(checkfunc):
    @wraps(checkfunc)
    def decorated(*args, **kwargs):
        token = None
        # print(request.headers)
        if 'Authorization' in request.headers:
            temp = request.headers['Authorization']
            token = temp[7:]
        if not token:
            return jsonify({
                "message" : "token is missing"
            })
        try:
            date = jwt.decode(token,'This-is-a-JWT-Secret-Key')
            checking = models.UserLogin(date["username"],"admin")
            checkuser = checking.checkuser()
        except :
            date = jwt.decode(token,'This-is-a-JWT-Secret-Key')
            return jsonify({"message": "Token is invalid",
            "token" : token,
            "username": "",
            "password": "",
            "datauser":date["username"]
            })
        return checkfunc(checkuser,*args , **kwargs)
    return decorated
class UserRegistration(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        phonenumber = postedData["phonenumber"]
        email = postedData["emailid"]
        hashed = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        todb = models.UserRegister(username,hashed,phonenumber,email)
        print(todb.checkinDB())
        try:
            todb.checkinDB()
             
            return {
                 "Status":200,
                 "Message":"User Register Successfully"

            }
        except :
            return jsonify({
                "Status":301,
                "Message": "Error Occurred while Registration"
            })
        return username,password,email,phonenumber


class UserLoginPage(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        loginob = models.UserLogin(username,password)
        decryptedPassword = loginob.checkpass()
        print(decryptedPassword)
        if decryptedPassword is True:
            token = jwt.encode({'username':username},'This-is-a-JWT-Secret-Key')
            return jsonify({
                'token':token.decode('utf-8'),
                'msg':'User logined and token generated succesfully',
                'Status':200
                
            })
        else:
            return jsonify({
                "Status":500,
                "Message":"Sorry Something went wrong"
            })
    

class Getlocation(Resource):
    #@token_required
    #def get(self,checkuser):
    def post(self):
        print("This is a test log")
        coordinates = request.get_json()
        longitude = coordinates["longitude"]
        latitude = coordinates["latitude"]
        getlocate = models.Nearlocate(longitude,latitude)
        locations = getlocate.locateNearest()
        x = json.loads(locations)
        
        
        return x
        #print(locations)
        


class AddLocation(Resource):
    #@token_required
    #def get(self,checkuser):
    def get(self):
        get_parking_data = request.get_json()
        
        name = get_parking_data["name_of_lot"]
        longitude = get_parking_data["longitude"]
        latitude = get_parking_data["latitude"]

        submit_the_parking_lot = models.SubmitinPark(name,longitude,latitude)
        addparking = submit_the_parking_lot.giveTheParking()

        if addparking :
            return jsonify({
                "status" : 200
            })
        else :
            return jsonify({
                "status" : 500
            })


class PollingSystem(Resource):
    #@token_required
    #def post(self,checkuser):
     def post(self):
        get_lot_data = request.get_json()
        id_lot = get_lot_data["id_lot"]
        id_user = get_lot_data["id_user"]
        like_dislike = bool(get_lot_data["like_dislike"])
        lot = models.PollingModel(id_lot,id_user,like_dislike)
        getdata = lot.updatePol()
        print(getdata)
        return jsonify({
            "message":"Poll added successfully",
            "status code" : 200
        })
class GetCapacity(Resource):
    def get(self):
        get_lot = request.get_json()
        id_of_lot = get_lot["id_of_lot"]
        veh_in = get_lot["veh_count"]
        vehiout = get_lot["veh_out_time"]
        vehiin = get_lot["veh_in_time"]
        vehicaleno = get_lot["veh_no"]
        occupied = models.getCapacity(id_of_lot,veh_in,vehiout,vehiin,vehicaleno)
        op = occupied.insertcapac()
        print(op)
        return jsonify({
            "message":"Occupancy added succesfully",
            "status":200
        })

class Booking(Resource):
    def post(self):
        book = request.get_json()
        cust_name = book["username"]
        booklot_id = book["booklot_id"]
        bookthelot = book["spot_no"]
        ass = models.Booking(cust_name,booklot_id,bookthelot)
        a = ass.bookd()
        return{
            "mesg":"booking successfull"
        }
'''
5c746156038f338820f0ac4e
5c746156038f338820f0ac4f
5c746156038f338820f0ac50
'''