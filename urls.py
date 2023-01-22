from django.urls import path
from Paypal.views import *

urlpatterns = [
   path("checkout/<str:typeofaccount>", PaypalViews.as_view()),
   path('paypal/order_id/confirmation/', authentication_paypal),
   path("prices/", prices),
]

