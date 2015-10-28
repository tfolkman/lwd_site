import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)

# Redis connection
REDIS_SERVER = os.environ.get('REDIS_SERVER', None)
REDIS_PORT = os.environ.get('REDIS_PORT', None)
REDIS_DB = os.environ.get('REDIS_DB', None)
