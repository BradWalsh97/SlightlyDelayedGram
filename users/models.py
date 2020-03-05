from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Picture(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture_object = models.ImageField(upload_to='photos/', blank=True)
    post_date = models.DateTimeField(default=timezone.now)

    def delete(self, *args, ** kwargs):
        self.picture_object.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.picture_object


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

class peer_profile(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'
