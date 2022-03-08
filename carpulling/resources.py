from codecs import getencoder
import json
from flask import request, jsonify
from flask_restful import Resource
import uuid
from carpulling.models import DriverRides, DriverUsers, PassangerBookedRides, PassangerBookedRidesSchema, PassangerUsers, DriverRidesSchema, DriverUsersSchema, PassangerUsersSchema

driverrides_schema = DriverRidesSchema()
driverusers_schema = DriverUsersSchema()
passangeruser_schema = PassangerUsersSchema()
passangerbookedrides_schema = PassangerBookedRidesSchema()

class HelloWorld(Resource):
    def get(self):
        return {'msg': 'Hello shreyas!'}

class DriverSignUp(Resource):
    def post(self):
        data = request.get_json()
        user = DriverUsers.checkuser(self, data["email"])
        if user:
            return {"msg": "User Already Present"}
        else:
            DriverUsers.adduser(self, 
            data["fullname"], data["email"], data["contact"], data["role"], data["password"], data["aadharno"], 
            data["carname"], data["carnoplate"], data["carlicenseno"], data["aadharfile"], data["licensefile"], data["carfile"], data["fid"])

            return {"msg": "Account Created"}, 200

class PassangerSignUp(Resource):
    def post(self):
        data = request.get_json()
        # print("PASSANGER USER ==>", data)
        user = PassangerUsers.checkuser(self, data["email"])
        if user:
            return {"msg": "User Already Present"}
        else:
            PassangerUsers.adduser(self, 
            data["fullname"], data["email"], data["contact"], data["role"], data["password"], data["fid"])

            return {"msg": "Account Created"}, 200

class Login(Resource):
    def post(self):
        data = request.get_json()
        print("DATA R==>", data)

        Driveruser = DriverUsers.checkuser(self, data["email"])
        Passangeruser = PassangerUsers.checkuser(self, data["email"])

        if(Driveruser):
            token = str(uuid.uuid4()) 
            print("DRIVER PRESENT")
            dataTest = {"msg": "Driver LoggedIn", "token": token}
            return dataTest, 200
        elif(Passangeruser):
            token = str(uuid.uuid4()) 
            print("PASSANGER PRESENT")
            dataTest = {"msg": "Passanger LoggedIn", "token": token}
            return dataTest, 200
        else:
            print("User Not Found")
            return {"msg": "Login Failed. User not found"}

class BookDriverRide(Resource):
    def post(self):
        data = request.get_json()
        print("DATA RIDE ==>", data)

        ride_status = "pending"
        DriverRides.addride(self, data["sources"], data["destination"], data["passanger_required"], data["ride_fare"], 
        data["date_of_ride"], data["time_of_ride"], data["car_name"], data["car_number_plate"], ride_status, data["fid"])

        return {"msg": "Ride Booked Successfully"}, 200

class GetDriverRides(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA DRIVER ID ==>", data)

        driverrides = DriverRides.getallridesofdriver(self, data["fid"])
        # print("DRIVER RIDES ==>", driverrides, type(driverrides))

        result = driverrides_schema.dumps(driverrides, many=True)

        return result, 202

class DriverUpdateProfile(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA DRIVER UPDATE ==>", data)

        user = DriverUsers.updatedriverdetails(self, data)
        if(user):
            return {"msg": "Driver details updated"}
        else:
            return {"msg": "Driver with this email id not found"}     

class PassangerUpdateProfile(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA PASSANGER UPDATE ==>", data)

        user = PassangerUsers.updatepassangerdetails(self, data)
        if(user):
            return {"msg": "Passanger details updated"}
        else:
            return {"msg": "Passanger with this email id not found"}

class DriverProfileDetails(Resource):
    def post(self):
        data = request.get_json()
        print("DRIVER DETAILS ==>", data)
        user = DriverUsers.getuser(self, data["fid"])
        if user:
            print("DRIVER PROFILE =>", user)
            result = driverusers_schema.dumps(user, many=True)
            return result, 202
        else:
            return {"msg": "User not found"}, 500   

class PassangerProfileDetails(Resource):
    def post(self):
        data = request.get_json()
        # print("DRIVER DETAILS ==>", data)
        user = PassangerUsers.getuser(self, data["fid"])
        if user:
            result = passangeruser_schema.dumps(user, many=True)
            return result, 202
        else:
            return {"msg": "User not found"}, 500   

class UpdateRideStatus(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA OF RIDE STATUS ==>", data)

        ride = DriverRides.updaterideofdriver(self, data)
        if ride:
            return {"msg": "Ride Cancelled"}, 202
        else:
            return {"msg": "Ride  not found"}, 500 

class PassangerBookRide(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA OF BOOK RIDE ==>", data)

        ride = PassangerBookedRides.checkride(self, data["driver_id"], data["passanger_id"], data["ride_id"])
        if ride:
            return {"msg": "Ride Already Confirmed"}
        else:
            DriverRides.updatepassangerrequiredcount(self, data)
            PassangerBookedRides.addbookedride(self, data["driver_id"], data["passanger_id"], data["ride_id"], data["driver_fullname"], 
            data["driver_email"], data["driver_contact"], data["passanger_fullname"], data["passanger_email"], data["passanger_contact"], 
            data["sources"], data["destination"], data["ride_fare"], data["date_of_ride"], data["time_of_ride"], data["car_name"], 
            data["car_number_plate"])

            return {"msg": "Confirmed Rides"}, 200      

class GetPassangerBookedRides(Resource):
    def post(self):
        data = request.get_json()
        print("DATA OF CONFIRM RIDES PASS. ID  ==>", data)

        confirm_rides = PassangerBookedRides.getallconfirmridesofpassanger(self, data["passanger_id"])
        # print("CONFIRM RIDES OF PASSANGER ==>", driverrides, type(driverrides))

        result = passangerbookedrides_schema.dumps(confirm_rides, many=True)

        return result, 202

class UpdateRatingsAndRides(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA DRIVER UPDATE ==>", data)

        if 'ratings' in data:
            user = DriverUsers.updatedriverratings(self, data)
        # driverride = DriverRides.updaterideofdriver(self, data)
        passangerride = PassangerBookedRides.updatepassangerride(self, data)
        if(passangerride):
            return {"msg": "Ride and Rating Updated"}
        else:
            return {"msg": "Something went wrong"}

class PassangerListOnRides(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA DRIVER UPDATE ==>", data)

        passanger_list = PassangerBookedRides.getpassangerlistofrides(self, data["driver_id"], data["ride_id"])

        result = passangerbookedrides_schema.dumps(passanger_list, many=True)

        return result, 202

class GetDriverAllRides(Resource):
    def post(self):
        data = request.get_json()
        # print("DATA DRIVER ID ==>", data)

        driverrides = DriverRides.getallrides(self)
        # print("DRIVER RIDES ==>", driverrides, type(driverrides))

        result = driverrides_schema.dumps(driverrides, many=True)

        return result, 202