from django.db import models

# Create your models here.

class stocklist(models.Model):
    Sno      = models.AutoField(primary_key=True)
    title    = models.CharField(max_length=100)
    desc  = models.TextField(max_length=1000)
    date     = models.DateTimeField(blank=True, auto_now_add=True)
    file = models.FileField(upload_to='files')

    def __str__(self):
        return self.title

class Query(models.Model):
    Sno = models.AutoField(primary_key=True)
    stockname = models.CharField(max_length=50)
    query = models.CharField(max_length=200)

    def __str__(self):
        return self.stockname
