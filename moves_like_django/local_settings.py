EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

FACEBOOK_APP_ID = '1462424537321539'
FACEBOOK_APP_SECRET = '6c9a1c307b742e8e2ff6da9f8a25e338'
USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ishan.gandhi1@gmail.com'
EMAIL_HOST_PASSWORD = 'okhlikakutta131192'
USERENA_SIGNIN_REDIRECT_URL = '/harmonify/%(username)s/'
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'harmonify.Profile'

FACEBOOK_REGISTRATION_BACKEND = 'django_facebook.registration_backends.UserenaBackend'

FACEBOOK_LOGIN_DEFAULT_REDIRECT = '/'

LOGIN_REDIRECT_URL = '/harmonify/%(username)s/'
LOGIN_URL = '/harmonify/signin/'
logout_URL = '/harmonify/signout/'