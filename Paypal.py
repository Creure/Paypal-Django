from requests import get, post
from requests.auth import HTTPBasicAuth
from pdb import set_trace
from django.conf import settings
from BackEnd.tools import send_email
from Paypal.models import PaypalData
from django.contrib.auth.models import User
from CustomerManager.models import *
from random import choice

class Paypal:
   
    def __init__(self):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET
        self.api_paypal_url = 'https://api-m.sandbox.paypal.com/'
        self.url_token_api  = self.api_paypal_url + 'v1/oauth2/token'
    

        request_api = post(
            self.url_token_api, data={'grant_type':'client_credentials'}, headers={'Content-Type':'application/x-www-form-urlencoded'}, 
            auth=HTTPBasicAuth(self.client_id, self.client_secret))

        

        #{'error': 'invalid_client', 'error_description': 'Client Authentication failed'}

        self.__token = request_api.json()['access_token']


    def valid_subcription_keto(self, payment_value, description):

        subcription = {
            '30D': 31.99,
            '60D': 51.99,
            '90D': 71.99,
            }

        
        #try:
        return payment_value >= subcription[description]
        #except KeyError:
        #    return 404

    def valid_order(self, id_order, cedula):
        
        order_url = self.api_paypal_url + 'v2/checkout/orders/'+id_order
        req = get(order_url, headers={'Content-Type':'application/json', 'Authorization': f'Bearer '+self.__token} )
        data = req.json()
        password = ''.join(choice('qwertyuioplkjhgfdsazxcvbnm1234567890') for i in range(8))
        
        if req.status_code == 200: 

            #66.99
            #47.99
            #28.99
               
                
            if self.valid_subcription_keto(float(data['purchase_units'][0]['payments']["captures"][0]['amount']["value"]), data['purchase_units'][0]['description']) == True:
                #create all class
                
                
                   #here we gonna crear the table in database
                Paypal_data = PaypalData.objects.create(
                order_id=id_order,
                email=data['payer']['email_address'],
                id_information=data['purchase_units'][0]['payments']['captures'][0]["id"],
                full_name=data['payer']['name']['given_name'] + ' ' + data['payer']['name']['surname'] ,
                status=data['purchase_units'][0]['payments']["captures"][0]['status'],
                description=data['purchase_units'][0]['description'],
                value=float(data['purchase_units'][0]['payments']["captures"][0]['amount']["value"])
                
                )
                user = User.objects.create_user(
                    username=cedula, 
                    password=password, 
                    email=data['payer']['email_address'], 
                    first_name=data['payer']['name']['given_name'],
                    last_name=data['payer']['name']['surname']
                    ) # creating user login
                    
                customerManager = Customer.objects.create(
                    username= user,
                    email=data['payer']['email_address'],
                    name=data['payer']['name']['given_name'],
                    last_name=data['payer']['name']['surname'],
                    type_of_account = data['purchase_units'][0]['description'],
                )
                
                return True
                

                    
                
           
        else:
            print(req)