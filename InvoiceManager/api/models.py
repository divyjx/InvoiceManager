from django.db import models

class Invoice(models.Model):
    
    date = models.DateTimeField(auto_now_add = True)
    customer_name = models.CharField(max_length=100)
    def __str__(self):
        return f"Invoice {self.id} - {self.date} - {self.customer_name}"


class InvoiceDetail(models.Model):
    
    invoice = models.OneToOneField(Invoice, related_name='details', on_delete=models.CASCADE)
    # all these fields are updated later via requests 
    description = models.TextField(blank = True, null = True)
    quantity = models.IntegerField(blank = True, null = True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank = True, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank = True, null = True)

    def __str__(self):
        return f"Detail of Invoice {self.invoice.id} - {self.description} - {self.quantity} - {self.unit_price} - {self.price}"
