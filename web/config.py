import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="newpostgresserver.postgres.database.azure.com"  # Update value
    POSTGRES_USER="newadmin" # Update value
    POSTGRES_PW="Test12345"   # Update value
    POSTGRES_DB="techconfdb"   # Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}?sslmode=require'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL

    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://thirdprojectnamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=cOr5Kca2ae0aztU5nLp3tMyzErm/CKgl8+ASbAA/KF0=' # Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'aditivkulkarni5@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
