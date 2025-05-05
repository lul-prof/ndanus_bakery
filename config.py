import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bakery.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Payment configurations
    MPESA_CONSUMER_KEY = 'your-mpesa-consumer-key'
    MPESA_CONSUMER_SECRET = 'your-mpesa-consumer-secret'
    PAYPAL_CLIENT_ID = 'your-paypal-client-id'
    PAYPAL_CLIENT_SECRET = 'your-paypal-client-secret'