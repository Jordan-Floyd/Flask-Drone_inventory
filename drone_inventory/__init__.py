from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from flask_migrate import Migrate
from .models import db, login_manager, ma
from flask_cors import CORS



# Instantiating a new flask app.
app = Flask(__name__)
app.config.from_object(Config)

# Registering Blueprints to use within the scope of our whole app.
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)


CORS(app)

# Instantiating db within the scope of our app.
db.init_app(app)


# Instantiating Login Manager within the scope of this app.
login_manager.init_app(app)


# Instantiation Marshmallow
ma.init_app(app)



# Specifies what page to load for protected routed when a user is not logged in.
login_manager.login_view = 'auth.signin'


# Giving Flask migrate access to app ond DB models.
migrate = Migrate(app, db)

