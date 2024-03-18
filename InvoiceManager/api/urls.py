# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'invoices/<int:pk>', InvoiceViewSet)

urlpatterns = router.urls
