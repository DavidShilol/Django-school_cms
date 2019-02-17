from django.db import models

# Create your models here.
class NewUser(models.Model):
    name = models.CharField('Name', max_length=200)
    sex = models.CharField('Sex', max_length=10)
    phone = models.CharField('Phone', max_length=200)
    workid = models.CharField('Work Id', max_length=200)
    idcard = models.CharField('ID Card', max_length=200, default='')
    password = models.CharField('Password', max_length=200, default='')

    class Meta:
        abstract = True

