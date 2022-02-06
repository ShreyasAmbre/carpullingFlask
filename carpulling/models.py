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
    driver_rides = db.relationship('DriverRides', backref='driverusers', lazy=True)
    

    def getallusers(self):
        return DriverUsers.query.all()

    def adduser(self, fullname, email, contact, role, password, aadharno, carname, carnoplate, carlicenseno, aadharfile, licensefile, carfile):
        user = DriverUsers(fullname=fullname, email=email, contact=contact, role=role, password=password,
        aadharno=aadharno, carname=carname, carnoplate=carnoplate, carlicenseno=carlicenseno, aadharfile=aadharfile, 
        licensefile=licensefile, carfile=carfile)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def checkuser(self, email):
        user = DriverUsers.query.filter_by(email=email).first()
        return user

    def getuser(self, id):
        user = DriverUsers.query.filter_by(id=id).first()
        data = [user]
        return data
    
    def updatedriverdetails(self, data):
        driver_details_updated = DriverUsers.query.filter_by(id=data["id"]).update(
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

class DriverUsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fullname', 'email', 'contact', 'role','aadharno', 'carname', 'carnoplate', 'carlicenseno')

class PassangerUsers(db.Model):

    __tablename__ = "PassangerUsers"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def getallusers(self):
        return PassangerUsers.query.all()

    def adduser(self, fullname, email, contact, role, password):
        user = PassangerUsers(fullname=fullname, email=email, contact=contact, role=role, password=password)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def checkuser(self, email):
        user = PassangerUsers.query.filter_by(email=email).first()
        return user

    def getuser(self, id):
        user = PassangerUsers.query.filter_by(id=id).first()
        data = [user]
        return data

    def updatepassangerdetails(self, data):
        passanger_details_updated = PassangerUsers.query.filter_by(id=data["id"]).update(
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
    driver_id = db.Column(db.Integer, db.ForeignKey('DriverUsers.id'), nullable=False)

    def getallridesofdriver(self, driver_id):
        rides = DriverRides.query.filter_by(driver_id=driver_id).all()
        return rides

    def addride(self, source, destination, passanger_required, ride_fare, date_of_ride, time_of_ride, car_name, car_number_plate, ride_status, driver_id):
        ride = DriverRides(sources=source, destination=destination, passanger_required=passanger_required, 
        ride_fare=ride_fare, date_of_ride=date_of_ride, time_of_ride=time_of_ride, car_name=car_name, 
        car_number_plate=car_number_plate, ride_status=ride_status, driver_id=driver_id)
        db.session.add(ride)
        db.session.commit()
        return ride, 201

    def updaterideofdriver(self, data):
        ride_updated = DriverRides.query.filter_by(id=data["ride_id"], driver_id=data["driver_id"]).update(
            {
                "ride_status": data["ride_status"],
            }
        )
        db.session.commit()
        return ride_updated, 201

class DriverRidesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sources', 'destination', 'passanger_required', 'ride_fare', 'date_of_ride', 'time_of_ride', 'car_name', 'car_number_plate', 'ride_status', 'driver_id')



if path.exists("carpulling.db") == False:
    db.create_all()