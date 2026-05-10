# settings.py 최상단
import os
from pathlib import Path
from dotenv import load_dotenv 

# BASE_DIR 정의 바로 아래나 위에 작성
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env')) # 2. .env 파일 경로를 명시적으로 지정



SECRET_KEY = 'django-insecure-y+cuzqxrsn03)+@yd)o3#5^&ogb2vt)4^)-jmsl-8lu_bc^ai='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver', #네이버 추가
    'allauth.socialaccount.providers.kakao', # 카카오 추가
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'myproject01.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject01.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

AUTH_USER_MODEL = 'user.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# 직접 입력된 값을 아래와 같이 환경 변수에서 가져오도록 수정
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = (os.getenv('DEBUG') == 'True')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# 발신자 기본 이메일 설정도 추가해주면 좋습니다.
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# settings.py 맨 아래에 추가
print(f"CHECK_USER:'{EMAIL_HOST_USER}'")
print(f"CHECK_PWD: '{EMAIL_HOST_PASSWORD}'")

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# 로그인/로그아웃 리다이렉트
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 이메일 필수 등 추가 설정
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False # 이메일 중심 로그인 원할 시

# 어댑터 연결
SOCIALACCOUNT_ADAPTER = 'user.adapter.MySocialAccountAdapter'

# 네이버 데이터 요청 범위 설정
SOCIALACCOUNT_PROVIDERS = {
    'naver': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'name', 'nickname', 'birthday', 'birthyear', 'mobile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    },
    'kakao': {
        'METHOD': 'oauth2',
        'SCOPE': ['profile_nickname', 'profile_image'], 
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    }
    
}