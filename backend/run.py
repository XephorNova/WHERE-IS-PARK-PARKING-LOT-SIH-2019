from flask import Flask
from flask_restful import Api
import pymongo as pm 
from flask_jwt_extended import JWTManager
import os

#print(os.environ['MONGODB_URI'])

#client = pm.MongoClient(os.environ['MONGODB_URI'])
client = pm.MongoClient("mongodb://localhost:27017")
db = client.parkinglots



app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'This-is-a-JWT-Secret-Key'
kk = app.config['JWT_SECRET_KEY'] = 'This-is-a-JWT-Secret-Key'

jwt = JWTManager(app)

import views,resources,models

api.add_resource(resources.UserLoginPage,'/login')
api.add_resource(resources.UserRegistration,'/register')
api.add_resource(resources.Getlocation,'/Getlocation')
api.add_resource(resources.AddLocation,'/addlocation')
api.add_resource(resources.PollingSystem,'/pol')
api.add_resource(resources.GetCapacity,'/capi')
api.add_resource(resources.Booking,'/book')

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=5000)