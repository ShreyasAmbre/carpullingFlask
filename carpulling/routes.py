from carpulling import api
from carpulling.resources import HelloWorld, DriverSignUp, PassangerSignUp, Login, BookDriverRide, GetDriverRides, DriverUpdateProfile, PassangerUpdateProfile, DriverProfileDetails, PassangerProfileDetails, UpdateRideStatus,PassangerBookRide, GetPassangerBookedRides, UpdateRatingsAndRides, PassangerListOnRides, GetDriverAllRides

api.add_resource(HelloWorld, "/hello")
api.add_resource(DriverSignUp, "/driversignup")
api.add_resource(PassangerSignUp, "/passangersignup")
api.add_resource(Login, "/login")
api.add_resource(BookDriverRide, "/bookdriverride")
api.add_resource(GetDriverRides, "/getdriverrides")
api.add_resource(DriverUpdateProfile, "/driverupdateprofile")
api.add_resource(PassangerUpdateProfile, "/passangerupdateprofile")
api.add_resource(DriverProfileDetails, "/getdriverprofile")
api.add_resource(PassangerProfileDetails, "/getpassangerprofile")
api.add_resource(UpdateRideStatus, "/updateridestatus")
api.add_resource(PassangerBookRide, "/passangerbookride")
api.add_resource(GetPassangerBookedRides, "/getpassangerbookedrides")
api.add_resource(UpdateRatingsAndRides, "/updateratingsandridestatus")
api.add_resource(PassangerListOnRides, "/passangerlistofrides")
api.add_resource(GetDriverAllRides, "/allrides")
