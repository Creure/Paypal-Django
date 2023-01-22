from django.db import models

# Create your models here.
class PaypalData(models.Model):

    order_id = models.CharField(primary_key=True,max_length=30)
    email = models.EmailField()
    id_information = models.CharField(max_length=30)
    full_name = models.CharField(max_length=30)
    status = models.CharField(max_length=13)
    description = models.CharField(max_length=3)
    value = models.FloatField()

    class Meta:
        verbose_name = 'PaypalData'
        verbose_name_plural = 'PaypalData'
        ordering = ['email']

    def __str__(self):
        return f"{self.email}"
    
