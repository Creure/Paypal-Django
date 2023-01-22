from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from .Paypal import Paypal
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.models import User

import pdb, base64



def prices(request):
    return render(request, 'prices.html')
def successfully(request, id_order):
    return render(request, 'thanks_you.html', {'order_id': id_order})




class PaypalViews(View):
    def get(self,request,typeofaccount):
        
        return render(request, 'checkout.html', {'cedula' :'', 'message':''})

    def post(self,request, typeofaccount):
        if User.objects.filter(username=request.POST['id_cedula']).values_list('username', flat=True).first() == None:
            if request.POST['id_cedula'].isnumeric():
                price = { '30D':31.99, '60D':51.99 ,'90D':71.99}
                
                #a = 3.4 * price /100
                #b = 1.9 *price /100
                #Comision =price +  a + b +0.35 + 1
                #Comision = round(Comision, 2)
                return render(request, 'checkout.html', {'description':typeofaccount , 'price': price[typeofaccount ], 'cedula':request.POST['id_cedula'] ,'client_id': settings.CLIENT_ID})
            else:
                return render(request, 'checkout.html', {'cedula' :'', 'error': True,'message':'Cedula no debe contener letras ni guines, solo numeros'})
        else:
            return render(request, 'checkout.html', {'cedula' :'','error': True,'message':f'Ya existe un usuario con esta cedula de identidad <{request.POST["id_cedula"]}>, esta opción es para cliente que nunca se han registrado'})
def authentication_paypal(request):

    if request.method == 'POST':
        data = base64.b64decode(request.POST['8ba1f7908']).decode("utf-8")
        id = base64.b64decode(request.POST['15ac18a2']).decode("utf-8")
        if Paypal().valid_order(data, id):
            return HttpResponse(200)
        else:
            return HttpResponse(500) #some happening and the information isn't save
    else:
        return HttpResponse(404)
