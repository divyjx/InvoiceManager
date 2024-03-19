from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Invoice, InvoiceDetail
import random
from datetime import datetime


class TestInvoiceViewSet(APITestCase):
    """
    From test_list_invoices all functions are called sequentially, performing tests on given url     
    
    """
    def setUp(self):
        """
        Creating a invoice object and invoice detail object
        """
        rn = random.randint(10000, 100000)
        self.invoice = Invoice.objects.create(**{
            "id": rn,
            "date": datetime.now(),
            "customer_name": "test_customer"+str(rn)
        })
        self.invoice_details = InvoiceDetail.objects.create(**{
            "invoice":self.invoice,
            "description":"test decription "+str(rn),
            "quantity": 100,
            "price":90
        })

    def test_list_invoices(self):
        """
        GET      /invoices       verifies the amount of rows recieved are same as in database
        """
        url = reverse('invoice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Invoice.objects.all()), len(response.data))

    def test_create_invoice(self):
        """
        POST     /invoices       verifies that the sent invoice data is same in responce and created object
        """
        url = reverse('invoice-list')
        data = {
            "customer_name": "test_create_customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(data, response.data["invoice"])

    def test_create_invoice_with_details(self):
        """
        POST     /invoices       verifies that the sent invoice data and details is same in responce and created object
        """
        url = reverse('invoice-list')
        data = {
            "customer_name": "test_create_customer_with_details",
        }
        details= {
                "description":"test decription",
                "quantity": 100,
                "price":90
        }
        combined = data.copy()
        combined["details"] = details
        keys = ["invoice", "details"]
        response = self.client.post(url, combined, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertListEqual(keys, list(response.data.keys()))
        self.assertDictContainsSubset(data, response.data["invoice"])
        self.assertDictContainsSubset(details, response.data["details"])

    def test_retrieve_invoice(self):
        """
        GET      /invoices/<pk>  retrieves and checks invoice object feilds
        """
        url = reverse('invoice-detail', args=[self.invoice.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invoice_dict = self.invoice.__dict__.copy()
        invoice_dict.pop("_state")
        invoice_dict.pop("date")
        response.data["invoice"].pop("date")

        self.assertDictContainsSubset(invoice_dict, response.data["invoice"])

    def test_retrieve_invoice_with_details(self):
        """
        GET      /invoices/<pk>  retrieves and checks invoice object and invoice details feilds
        """
        url = reverse('invoice-detail', args=[self.invoice.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(["invoice", "details"], list(response.data.keys()))
        invoice_dict = self.invoice.__dict__.copy()
        invoice_dict.pop("_state")
        invoice_dict.pop("date")
        response.data["invoice"].pop("date")

        self.assertDictContainsSubset(invoice_dict, response.data["invoice"])

        invoice_detail_dict = self.invoice_details.__dict__
        invoice_detail_dict.pop("_state")
        invoice_detail_dict["invoice"] = invoice_detail_dict.pop("invoice_id")
        
        self.assertDictContainsSubset(invoice_detail_dict, response.data["details"])



    def test_update_invoice(self):
        """
        PUT      /invoices/<pk>  verifies update in objects
        """
        url = reverse('invoice-detail', args=[self.invoice.pk])
        new_data = {
            "customer_name":"test customer",
            "details":{
                "description":"new desription",
                "price":10000
            }
        }  
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_invoice(self):
        """
        PATCH    /invoices/<pk>  verifies partial update in objects
        """
        url = reverse('invoice-detail', args=[self.invoice.pk])
        partial_data= {
            "details":{
                "description":"partial desription",
            }
        }  
        response = self.client.patch(url, partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_invoice(self):
        """
        DELETE   /invoices/<pk>  checks whether object is deleted from database
        """
        url = reverse('invoice-detail', args=[self.invoice.pk])
        pk = self.invoice.pk
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerySetEqual(Invoice.objects.filter(pk = pk), Invoice.objects.none())
        self.assertQuerySetEqual(InvoiceDetail.objects.filter(invoice = pk), InvoiceDetail.objects.none())
