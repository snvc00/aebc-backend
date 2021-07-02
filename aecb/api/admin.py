from django.contrib import admin

from .models import *

admin.site.register([Employee, Report, PreapprovalRequest, Client, CreditCard, Promotion, Insurance])