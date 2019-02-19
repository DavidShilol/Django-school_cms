from django.db import models
from dorm.abstract_model import NewUser
from dorm.models import Building

# Create your models here.
class DormAdminUser(NewUser):
    permission = models.IntegerField('Permission', default=0)
    incharge = models.ForeignKey(Building, on_delete=models.SET_NULL, related_name='admins', verbose_name='Charge Building', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-permission']
        unique_together = ('workid', 'incharge')

