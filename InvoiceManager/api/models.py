# invoices_app/models.py

from django.db import models

class Invoice(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    customer_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Invoice {self.id} - {self.date} - {self.customer_name}"

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='details', on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail of Invoice {self.invoice.id} - {self.description}"
