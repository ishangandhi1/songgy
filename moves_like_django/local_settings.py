
import os

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "songgy_deploy",
        "USER": "heroku7692",
        "PASSWORD": "Okhli123!",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
