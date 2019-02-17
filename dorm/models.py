from django.db import models
from teacher.models import TeacherUser

# Create your models here.
class Building(models.Model):
    number = models.IntegerField('Building Number', unique=True)
    build_date = models.DateField('Build Date')
    floor = models.IntegerField('Number of Floor', default=0)
    volume = models.IntegerField('Number of Rooms')
    sex = models.CharField('Who lives here?', max_length=100)

    def __str__(self):
        return '{}'.format(self.number)

    class Meta:
        ordering = ['number']

class Room(models.Model):
    number = models.IntegerField('Room Number')
    volume = models.IntegerField('Room Volume')
    free = models.IntegerField('Spare Bed')
    building = models.ForeignKey('Building', on_delete=models.CASCADE, related_name='rooms', verbose_name='Building Number')

    class Meta:
        unique_together = ('number', 'building',)

    def __str__(self):
        return '{}#{}'.format(self.building.number, self.number)

class Student(models.Model):
    name = models.CharField('Student Name', max_length=200)
    idcard = models.CharField('ID Card', max_length=200, null=True, blank=True, unique=True)
    sex = models.CharField('Sex', max_length=10)
    info = models.CharField('Student Info', max_length=200)
    number = models.CharField('Student ID', max_length=200, default='', unique=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='students', verbose_name='Room_number', blank=True, null=True)
    teacher = models.ForeignKey(TeacherUser, null=True, blank=True, on_delete=models.CASCADE, related_name='students', verbose_name='Student\'s Teacher')

    def __str__(self):
        return '{}#{}'.format(self.info, self.name)

    class Meta:
        ordering = ['number']

