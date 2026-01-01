import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from azure.servicebus import ServiceBusClient

app = Flask(__name__)
# app.config.from_object('config.DevelopmentConfig')
app.config.from_object('config.ProductionConfig')

app.secret_key = app.config.get('SECRET_KEY')

servicebus_client = ServiceBusClient.from_connection_string(
    app.config.get('SERVICE_BUS_CONNECTION_STRING')
)

queue_client = servicebus_client.get_queue_sender(
    queue_name=app.config['SERVICE_BUS_QUEUE_NAME']
)

db = SQLAlchemy(app)

from . import routes
