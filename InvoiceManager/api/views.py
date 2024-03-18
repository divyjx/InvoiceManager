# invoices_app/views.py
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    def get(self, request):
        output = [{'username':output.username,
                   'card':output.card,
                   'password':output.password,
                   'balance': output.balance}
                  for output in Invoice.objects.all()]
        return Response(output)
    def post(self, request):
        serializer = InvoiceSerializer(data = request.data)
        if (serializer.is_valid(raise_exception = True)):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors) 