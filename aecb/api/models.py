from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def upload_to(instance, filename):
    return "cards/{filename}".format(filename=filename)


class Client(models.Model):
    name = models.CharField(max_length=60)
    rfc = models.CharField(max_length=13, unique=True)
    curp = models.CharField(max_length=18, unique=True)
    email = models.CharField(max_length=60, primary_key=True)
    birthdate = models.DateField()
    income = models.IntegerField()
    has_credit = models.BooleanField()
    active = models.BooleanField()
    address = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    last_update = models.DateTimeField(auto_now=True)


class Employee(models.Model):
    name = models.CharField(max_length=60)
    rfc = models.CharField(max_length=13, unique=True)
    email = models.CharField(max_length=60, primary_key=True)
    last_update = models.DateTimeField(auto_now=True)


class Account(models.Model):
    role = models.CharField(max_length=60)
    token = models.CharField(max_length=1200)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_email = models.CharField(max_length=60)
    last_signin = models.DateTimeField(auto_now=True)
    user = GenericForeignKey("content_type", "user_email")


class Insurance(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=256)
    max_protection = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)


class Promotion(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=256)
    valid_until = models.DateField()
    last_update = models.DateTimeField(auto_now=True)


class CreditCard(models.Model):
    name = models.CharField(max_length=60, unique=True)
    min_credit = models.IntegerField()
    max_credit = models.IntegerField()
    tier = models.SmallIntegerField()
    image = models.ImageField(upload_to=upload_to)
    cat = models.SmallIntegerField()
    annual_fee = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    promotions = models.ManyToManyField(Promotion, blank=True)
    insurances = models.ManyToManyField(Insurance, blank=True)


class PreapprovalRequest(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, default=None, null=True)
    last_update = models.DateTimeField(auto_now=True)


class Report(models.Model):
    requests = models.ManyToManyField(PreapprovalRequest)
    employees = models.ManyToManyField(Employee, blank=True)
    clients = models.ManyToManyField(Client, blank=True)
    active_ratio = models.FloatField(default=0.0)
    approval_ratio = models.FloatField(default=0.0)
    most_requested = models.CharField(max_length=60, default=None)
    most_approved = models.CharField(max_length=60, default=None)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="generated_by")
    file = models.CharField(max_length=128, null=True)
