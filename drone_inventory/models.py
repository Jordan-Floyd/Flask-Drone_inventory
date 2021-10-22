from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

# Adding in Flask Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Creates a hex token for eventual API access.
import secrets

# Importing login manager package and user loader for our db table.
from flask_login import LoginManager, UserMixin

# Import data marshaller
from flask_marshmallow import Marshmallow






db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Drone', backref = 'owner', lazy = True)


    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self,length):
        return secrets.token_hex(length)




class Drone(db.Model):
    id = db.Column(db.String, primary_key= True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    camera_quailty = db.Column(db.Numeric(precision = 10, scale = 2 ))
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision = 10, scale = 2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)



    def __init__(self, name, description, camera_quality, flight_time, max_speed,
                 dimensions, weight, cost_of_prod, series, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.series = series
        self.user_token = user_token

    
    def set_id(self):
        return (secrets.token_urlsafe())


# Creating our marshaller to pull/create k,v pairs out of Drone attributes
class DroneSchema(ma.Schema):
    class Meta:
        # Detailing fields or attributes to be pulled out of our Drone class
        # Instance(s) and sent to API call and vice versa.
        fields = ['id', 'name','description', 'price', 'camera_quality', 'flight_time',
                 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']
        
drone_schema = DroneSchema()
drones_schema = DroneSchema(many = True)

# Takes a python class object like <Drone x982370>
# and iterates through our fields and adds them into a dictionary as k,v pairs.




