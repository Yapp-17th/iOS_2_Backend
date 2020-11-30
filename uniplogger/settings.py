import json
import os
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open(os.path.join(BASE_DIR, 'secrets.json'), 'rb') as secret_file:
    secrets = json.load(secret_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'users',
    'accounts',
    'quests',
    'planets',
    'trashcans',

    'drf_yasg',
    'django_crontab',
    'django_mysql',
    "push_notifications",
]

AUTH_USER_MODEL = 'users.CustomUser'

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_EMAIL_VERIFICATION = 'none'

SITE_ID = 1

REST_USE_JWT = True

# Email 전송
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 메일을 호스트하는 서버
EMAIL_HOST = 'smtp.gmail.com'
# gmail과의 통신하는 포트
EMAIL_PORT = 587
# 발신할 이메일
EMAIL_HOST_USER = secrets["EMAIL_HOST_USER"]
# 발신할 메일의 비밀번호
EMAIL_HOST_PASSWORD = secrets["EMAIL_HOST_PASSWORD"]
# TLS 보안 방법
EMAIL_USE_TLS = True
# 사이트와 관련한 자동응답을 받을 이메일 주소
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}

JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uniplogger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uniplogger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : secrets["DATABASES_NAME"],
        'USER' : secrets["DATABASES_USER"],
        'PASSWORD' : secrets["DATABASES_PASSWORD"],
        'HOST' : secrets["DATABASES_HOST"],
        'PORT' : secrets["DATABASES_PORT"]
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
         'jwt': {
             'type': 'apiKey',
             'description': 'jwt Token ***** format: JWT {your JWT} *****',
             'name': 'Authorization',
             'in': 'header'
         }
    },
    'USE_SESSION_AUTH': False
}

CRONJOBS = [
    # 매주 일요일 11:59 행성 삭제 / 월요일 0:0 행성 생성
    ('59 23 * * 0', 'planets.cron.delete_planet'),
    ('0 0 * * 1', 'planets.cron.create_planet'),
    # 매일 0시 0분 미접속자 판별 ( N-> D )
    ('0 0 * * *', 'users.cron.check_3days'),
    # ('0 0 * * *', 'users.cron.check_7days'),
    ('0 0 * 1 *', 'users.cron.monthly_stats'),
    ('0 0 * * 1', 'users.cron.weekly_stats'),
    #('* * * * *', 'users.cron.weekly_stats','>> /Users/guinness/Uniplogger/iOS_2_Backend/users/cronlog.log'),
]
#rest-auth/logout 시 로그아웃 
ACCOUNT_LOGOUT_ON_GET = True


PUSH_NOTIFICATIONS_SETTINGS = {
    "APNS_CERTIFICATE": secrets["APNS_CERTIFICATE"],
    "APNS_AUTH_KEY_PATH" : secrets["APNS_AUTH_KEY_PATH"],
    "APNS_AUTH_KEY_ID" : secrets["APNS_AUTH_KEY_ID"],
    "APNS_TEAM_ID" : secrets["APNS_TEAM_ID" ],
    "APNS_TOPIC": secrets["APNS_TOPIC"],
    #"APNS_USE_ALTERNATIVE_PORT": 443 대신 포트 2197 사용
    #"APNS_USE_SANDBOX" : api.push.apple.com 대신 api.development.push.apple.com 사용
}