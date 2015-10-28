from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from lwd.config import REDIS_SERVER, REDIS_PORT, REDIS_DB

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
redis_db = redis.StrictRedis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB)

from . import views, models
from . import nfl_views
