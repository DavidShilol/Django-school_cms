from django.db import models
from dorm.abstract_model import NewUser

# Create your models here.
class TeacherUser(NewUser):
    def __str__(self):
        return self.name

