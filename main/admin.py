from django.contrib import admin
from .models import stocklist, Query

# Register your models here.

admin.site.register(stocklist)
admin.site.register(Query)
