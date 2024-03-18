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

    

    def list(self, request, *args, **kwargs):
        print("LIST")
        data = []
        for invoice in self.get_queryset():
            invoice_data = self.get_serializer(invoice).data
            invoice_detail = InvoiceDetail.objects.filter(invoice=invoice).first()
            if invoice_detail:
                details_ser = InvoiceDetailSerializer(instance=invoice_detail)
                details_data = details_ser.data

                data.append({
                    "invoice": invoice_data,
                    "details": details_data
                })
            else :
                data.append({
                    "invoice": invoice_data,
                    "details": None
                })
        return Response(data)
    
    def create(self, request):
        print("CREATE")
        serializer = self.get_serializer(data=request.data)
        details_data = request.data.get('details', None)
        if serializer.is_valid():
            if details_data:
                invoice = serializer.save()
                details_data["invoice"] = invoice.id
                invoice_detail_serializer = InvoiceDetailSerializer(data = details_data)
                if invoice_detail_serializer.is_valid():
                    invoice_detail_serializer.save()
                    return Response({
                        "invoice":serializer.data,
                        "details":invoice_detail_serializer.data
                    })
                else:
                    return Response(invoice_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
        print("RETRIEVE")
        queryset = self.get_queryset()  
        instance = get_object_or_404(queryset, pk=pk)  
        serializer = self.get_serializer(instance)  # Serialize instance
        invoice_data = serializer.data
        invoice_detail = InvoiceDetail.objects.filter(invoice=instance).first()
        if invoice_detail:
            details_ser = InvoiceDetailSerializer(instance=invoice_detail)
            details_data = details_ser.data

            data = {
                "invoice": invoice_data,
                "details": details_data
            }
        else:
            data = {
                "invoice": invoice_data,
                "details": None
            }
        return Response(data)    
    
    def update(self, request, pk=None):
        print("UPDATE")
        instance = self.get_object()  
        serializer = self.get_serializer(instance, data=request.data)  
        if serializer.is_valid():
            serializer.save()
            invoice_detail = InvoiceDetail.objects.filter(invoice=pk).first()
            
            data = request.data.get('details')
            data["invoice"] = pk
            if invoice_detail:
                detail_serializer = InvoiceDetailSerializer(instance=invoice_detail, 
                                                            data=data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            invoice_data = serializer.data
            details_data = None
            if invoice_detail:
                details_data = detail_serializer.data
            
            data = {
                "invoice": invoice_data,
                "details": details_data
            }
            
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
    
    def partial_update(self, request, pk=None):
        print("PARTIAL_UPDATE")
        instance = self.get_object()  
        serializer = self.get_serializer(instance, data=request.data)  
        if serializer.is_valid():
            serializer.save()
            invoice_detail = InvoiceDetail.objects.filter(invoice=pk).first()
            
            data = request.data.get('details')
            data["invoice"] = pk
            if invoice_detail:
                detail_serializer = InvoiceDetailSerializer(instance=invoice_detail, 
                                                            data=data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            invoice_data = serializer.data
            details_data = None
            if invoice_detail:
                details_data = detail_serializer.data
            
            data = {
                "invoice": invoice_data,
                "details": details_data
            }
            
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        print("DESTROY")
        instance = self.get_object()  # Get the instance to be deleted
        instance.delete()  # Delete the instance
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return 204 status code for successful deletion
