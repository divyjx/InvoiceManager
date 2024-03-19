from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def fill_response(self, invoice_data, detail_data = None):
        return {
                    "invoice": invoice_data,
                    "details": detail_data
                }
    
    def list(self, request, *args, **kwargs):
        print("LIST")
        data = []
        for invoice in self.get_queryset():
            invoice_data = self.get_serializer(invoice).data
            invoice_detail = InvoiceDetail.objects.filter(invoice=invoice).first()
            details_data = None
            if invoice_detail:
                details_ser = InvoiceDetailSerializer(instance=invoice_detail)
                details_data = details_ser.data
        
            data.append(self.fill_response(invoice_data, details_data))
        return Response(data)
    
    def create(self, request):
        print("CREATE")
        serializer = self.get_serializer(data=request.data)
        details_data = request.data.get('details', None)
        if serializer.is_valid():
            invoice = serializer.save()
            if details_data:
                details_data["invoice"] = invoice.id
                detail_serializer = InvoiceDetailSerializer(data = details_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                    return Response(self.fill_response(serializer.data, detail_serializer.data)
                        , status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
        print("RETRIEVE")
        queryset = self.get_queryset()  
        instance = get_object_or_404(queryset, pk=pk)  
        serializer = self.get_serializer(instance)  # Serialize instance
        invoice_data = serializer.data
        invoice_detail = InvoiceDetail.objects.filter(invoice=pk).first()
        detail_data = None
        if invoice_detail:
            details_ser = InvoiceDetailSerializer(instance=invoice_detail)
            detail_data = details_ser.data

        return Response(self.fill_response(invoice_data, detail_data))    
    
    def update_or_partial_update(self, request, pk=None, partial=False):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()

            invoice_detail = InvoiceDetail.objects.filter(invoice=pk).first()
            detail_data = None
            if invoice_detail:
                data = request.data.get('details')
                data["invoice"] = pk
                detail_serializer = InvoiceDetailSerializer(instance=invoice_detail, data=data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                    detail_data = detail_serializer.data
            
            return Response(self.fill_response(serializer.data, detail_data))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        print("UPDATE")
        return self.update_or_partial_update(request, pk=pk)

    def partial_update(self, request, pk=None):
        print("PARTIAL_UPDATE")
        return self.update_or_partial_update(request, pk=pk, partial=True)
   
    def destroy(self, request, pk=None):
        print("DESTROY")
        instance = self.get_object()  
        instance.delete()  
        return Response(status=status.HTTP_204_NO_CONTENT)
