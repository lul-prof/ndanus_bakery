import requests
from flask import current_app
from datetime import datetime
import base64

class MPESAPayment:
    def __init__(self):
        self.business_shortcode = "174379"
        self.passkey = current_app.config['MPESA_PASSKEY']
        self.consumer_key = current_app.config['MPESA_CONSUMER_KEY']
        self.consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']
        self.base_url = "https://sandbox.safaricom.co.ke"

    def get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}"}
        
        response = requests.get(url, headers=headers)
        return response.json()['access_token']

    def initiate_payment(self, phone_number, amount, reference):
        access_token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.business_shortcode}{self.passkey}{timestamp}".encode()).decode()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/mpesa/callback",
            "AccountReference": reference,
            "TransactionDesc": "Payment for order"
        }

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

class PayPalPayment:
    def __init__(self):
        self.client_id = current_app.config['PAYPAL_CLIENT_ID']
        self.client_secret = current_app.config['PAYPAL_CLIENT_SECRET']
        self.base_url = "https://api-m.sandbox.paypal.com"

    def get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data)
        return response.json()['access_token']

    def create_order(self, items, total_amount):
        access_token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": str(total_amount)
                }
            }]
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()