from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = router.urls

"""
allowed methods and urls

GET      /invoices     
POST     /invoices     
GET      /invoices/<pk>
PUT      /invoices/<pk>
PATCH    /invoices/<pk>
DELETE   /invoices/<pk>
"""