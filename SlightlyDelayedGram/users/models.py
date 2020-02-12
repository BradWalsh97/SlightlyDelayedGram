from django.db import models
from django.contrib.auth.models import User
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

# Create your models here.

class Picture(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture_object = models.ImageField(upload_to='photos/', blank=True)
    post_date = models.DateTimeField('Date Posted')
