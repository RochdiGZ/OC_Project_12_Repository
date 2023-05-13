from django.conf import settings
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"role": "sales"},
    )
    is_prospect = models.BooleanField(blank=False, default=True)

    class Meta:
        ordering = ['-date_updated']
        verbose_name = 'client'

    def __str__(self):
        return f"Customer {id} : {self.first_name} {self.last_name}, Company : #{self.company_name}"
