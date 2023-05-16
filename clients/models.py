from django.conf import settings
from django.db import models


class Client(models.Model):
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
        default=1,
        null=False,
        blank=False,
        limit_choices_to={"role": "sales"},
    )
    is_prospect = models.BooleanField(blank=False, default=True)

    class Meta:
        ordering = ['-date_updated']
        verbose_name = 'client'

    def __str__(self):
        return f"Client : #{self.first_name} {self.last_name}, Company : #{self.company_name}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'sales'},
        null=True
    )
    client = models.ForeignKey(
        Client,
        related_name="contract",
        on_delete=models.CASCADE,
        null=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    payment_due = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-date_updated']
        verbose_name = 'contract'

    def __str__(self):
        return f"created with {self.sales_contact}"


class ContractStatus(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'True'},
        null=False,
        primary_key=True
    )

    class Meta:
        ordering = ['-contract__id']
        verbose_name = 'contract status'
        verbose_name_plural = 'contracts status'

    def __str__(self):
        return f"Contract : {self.contract}"


class Event(models.Model):
    client = models.ForeignKey(
        Client,
        related_name="event_client",
        on_delete=models.CASCADE,
        null=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'support'},
        null=True
    )
    event_status = models.ForeignKey(
        ContractStatus,
        related_name="event",
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    attendees = models.PositiveIntegerField(blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        ordering = ['-date_updated']
        verbose_name = 'event'
        constraints = [models.UniqueConstraint(fields=['event_status', 'name'], name="unique_event")]

    def __str__(self):
        return f"{self.name}"
