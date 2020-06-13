import json


class MakeJSON():
    def __init__(self,longitude,latitude):
        self.longitude = longitude
        self.latitude = latitude
    def mJSON(self):
        mydata = { 
            "type": "Feature",
            "properties": {
                "name": "",
                "description": "",
                "parkingId": "",
                "city": "",
                "road": "",
                "landmark": "",
                "address": "",
                "latitude": self.latitude,
                "longitude": self.longitude,
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
                "vehicleTypeId": ""
            },
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude,self.latitude]
            }
}
        print(type(json.dumps(mydata)))
        return json.dumps(mydata)


# keval = MakeJSON(72,56)
# print(keval.mJSON())
# print(type(keval.mJSON))


