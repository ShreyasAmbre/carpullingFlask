import datetime
from email.policy import default
from carpulling import db, ma
from os import path


class DriverUsers(db.Model):

    __tablename__ = "DriverUsers"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    aadharno = db.Column(db.String(30), nullable=False)
    carname = db.Column(db.String(30), nullable=False)
    carnoplate = db.Column(db.String(30), nullable=False)
    carlicenseno = db.Column(db.String(30), nullable=False)
    aadharfile = db.Column(db.String(30), nullable=False)
    licensefile = db.Column(db.String(30), nullable=False)
    carfile = db.Column(db.String(30), nullable=False)
    ratings = db.Column(db.Integer, default=2)
    driver_rides = db.relationship('DriverRides', backref='driverusers', lazy=True)
    fid = db.Column(db.String(50), nullable=False)
    

    def getallusers(self):
        return DriverUsers.query.all()

    def adduser(self, fullname, email, contact, role, password, aadharno, carname, carnoplate, carlicenseno, aadharfile, licensefile, carfile, fid):
        user = DriverUsers(fullname=fullname, email=email, contact=contact, role=role, password=password,
        aadharno=aadharno, carname=carname, carnoplate=carnoplate, carlicenseno=carlicenseno, aadharfile=aadharfile, 
        licensefile=licensefile, carfile=carfile, fid=fid)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def checkuser(self, email):
        user = DriverUsers.query.filter_by(email=email).first()
        return user

    def getuser(self, fid):
        user = DriverUsers.query.filter_by(fid=fid).first()
        data = [user]
        return data
    
    def updatedriverdetails(self, data):
        driver_details_updated = DriverUsers.query.filter_by(fid=data["fid"]).update(
            {
                "fullname": data["fullname"],
                "email": data["email"],
                "contact": data["contact"],
                "carname": data["carname"],
                "carnoplate": data["carnoplate"],
            }
        )
        db.session.commit()
        
        return driver_details_updated, 201

    def updatedriverratings(self, data):
        driver_details_updated = DriverUsers.query.filter_by(id=data["driver_id"]).update(
            {
                "ratings": data["ratings"],
            }
        )
        db.session.commit()
        
        return driver_details_updated, 201

class DriverUsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fullname', 'email', 'contact', 'role','aadharno', 'carname', 'carnoplate', 'carlicenseno', 'ratings', 'fid')

class PassangerUsers(db.Model):

    __tablename__ = "PassangerUsers"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    fid = db.Column(db.String(50), nullable=False)

    def getallusers(self):
        return PassangerUsers.query.all()

    def adduser(self, fullname, email, contact, role, password, fid):
        user = PassangerUsers(fullname=fullname, email=email, contact=contact, role=role, password=password, fid=fid)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def checkuser(self, email):
        user = PassangerUsers.query.filter_by(email=email).first()
        return user

    def getuser(self, fid):
        user = PassangerUsers.query.filter_by(fid=fid).first()
        data = [user]
        return data

    def updatepassangerdetails(self, data):
        passanger_details_updated = PassangerUsers.query.filter_by(fid=data["fid"]).update(
            {
                "fullname": data["fullname"],
                "email": data["email"],
                "contact": data["contact"],
            }
        )
        db.session.commit()
        return passanger_details_updated, 201

class PassangerUsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fullname', 'email', 'contact', 'role',)

class DriverRides(db.Model):

    __tablename__ = "DriverRides"
    id = db.Column(db.Integer, primary_key=True)
    sources = db.Column(db.String(30), nullable=False)
    destination = db.Column(db.String(30), nullable=False)
    passanger_required = db.Column(db.Integer, nullable=False)
    ride_fare = db.Column(db.String(10), nullable=False)
    date_of_ride = db.Column(db.String(20), nullable=False)
    time_of_ride = db.Column(db.String(20), nullable=False)
    car_name = db.Column(db.String(20), nullable=False)
    car_number_plate = db.Column(db.String(20), nullable=False)
    ride_status = db.Column(db.String(20), nullable=False)
    fid = db.Column(db.Integer, db.ForeignKey('DriverUsers.fid'), nullable=False)

    def getallrides(self):
        return DriverRides.query.all()

    def getallridesofdriver(self, fid):
        rides = DriverRides.query.filter_by(fid=fid).all()
        return rides

    def addride(self, source, destination, passanger_required, ride_fare, date_of_ride, time_of_ride, car_name, car_number_plate, ride_status, fid):
        ride = DriverRides(sources=source, destination=destination, passanger_required=passanger_required, 
        ride_fare=ride_fare, date_of_ride=date_of_ride, time_of_ride=time_of_ride, car_name=car_name, 
        car_number_plate=car_number_plate, ride_status=ride_status, fid=fid)
        db.session.add(ride)
        db.session.commit()
        return ride, 201

    def updaterideofdriver(self, data):
        ride_updated = DriverRides.query.filter_by(id=data["ride_id"], fid=data["fid"]).update(
            {
                "ride_status": data["ride_status"],
            }
        )
        db.session.commit()
        return ride_updated, 201

    def updatepassangerrequiredcount(self,data):
        ride_updated = DriverRides.query.filter_by(id=data["ride_id"]).update(
            {
                "passanger_required": data["passanger_required"],
            }
        )
        db.session.commit()
        return ride_updated, 201

class DriverRidesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sources', 'destination', 'passanger_required', 'ride_fare', 'date_of_ride', 'time_of_ride', 'car_name', 'car_number_plate', 'ride_status', 'driver_id', 'fid')

class PassangerBookedRides(db.Model):

    __tablename__ = "PassangerBookedRides"
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, nullable=False)
    passanger_id = db.Column(db.Integer, nullable=False)
    ride_id = db.Column(db.Integer, nullable=False)
    driver_fullname = db.Column(db.String(30), nullable=False)
    driver_email = db.Column(db.String(30), nullable=False)
    driver_contact = db.Column(db.String(15), nullable=False)
    passanger_fullname = db.Column(db.String(30), nullable=False)
    passanger_email = db.Column(db.String(30), nullable=False)
    passanger_contact = db.Column(db.String(15), nullable=False)
    sources = db.Column(db.String(30), nullable=False)
    destination = db.Column(db.String(30), nullable=False)
    ride_fare = db.Column(db.String(10), nullable=False)
    date_of_ride = db.Column(db.String(20), nullable=False)
    time_of_ride = db.Column(db.String(20), nullable=False)
    car_name = db.Column(db.String(20), nullable=False)
    car_number_plate = db.Column(db.String(20), nullable=False)
    booked_ride_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ride_status = db.Column(db.String(20), default="pending")
    last_update_ride = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def checkride(self, passanger_id, driver_id, ride_id):
        ride = PassangerBookedRides.query.filter_by(passanger_id=passanger_id, driver_id=driver_id, ride_id=ride_id).first()
        return ride

    def getallconfirmridesofpassanger(self, passanger_id):
        confirm_rides = PassangerBookedRides.query.filter_by(passanger_id=passanger_id).all()
        return confirm_rides

    def addbookedride(self, driver_id, passanger_id, ride_id, driver_fullname, driver_email, driver_contact, passanger_fullname, passanger_email, passanger_contact, sources, destination, ride_fare, date_of_ride, time_of_ride, car_name, car_number_plate):
        booked_ride = PassangerBookedRides (driver_id=driver_id, passanger_id=passanger_id, ride_id=ride_id, driver_fullname=driver_fullname, 
        driver_email=driver_email, driver_contact=driver_contact, passanger_fullname=passanger_fullname, passanger_email=passanger_email, 
        passanger_contact=passanger_contact, sources=sources, destination=destination, ride_fare=ride_fare, date_of_ride=date_of_ride,
        time_of_ride=time_of_ride, car_name=car_name, car_number_plate=car_number_plate)

        db.session.add(booked_ride)
        db.session.commit()
        return booked_ride, 201

    def updatepassangerride(self, data):
        if data["ride_status"] == 'completed':
            ride_updated = PassangerBookedRides.query.filter_by(ride_id=data["ride_id"], driver_id=data["driver_id"], passanger_id=data["passanger_id"]).update(
                {
                    "ride_status": data["ride_status"],
                }
            )
            db.session.commit()
            return ride_updated, 201
        if data["ride_status"] == 'cancelled':
            ride_updated = PassangerBookedRides.query.filter_by(ride_id=data["ride_id"], driver_id=data["driver_id"], passanger_id=data["passanger_id"]).update(
                {
                    "ride_status": data["ride_status"],
                }
            )
            db.session.commit()
            return ride_updated, 201

    def getpassangerlistofrides(self, driver_id, ride_id):
        rides = PassangerBookedRides.query.filter_by(driver_id=driver_id, ride_id=ride_id).all()
        return rides
  
class PassangerBookedRidesSchema(ma.Schema):

    class Meta:
        fields = ('id', 'driver_id', 'passanger_id', 'ride_id', 'driver_fullname', 'driver_email', 'driver_contact', 
        'passanger_fullname', 'passanger_email', 'passanger_contact', 'sources', 'destination', 'ride_fare', 'date_of_ride', 
        'time_of_ride', 'car_name', 'car_number_plate', 'booked_ride_at', 'ride_status')


if path.exists("carpulling.db") == False:
    db.create_all()