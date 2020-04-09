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
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('picture_detail', args=[str(self.id)])

    def delete(self, *args, ** kwargs):
        self.picture_object.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.pk)


class Comment(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name="Add your Comment")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}'.format(self.text, str(self.author.username))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    followed = models.ManyToManyField(User, related_name='followed', blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('peer_profile', args=[str(self.id)])

    def __str__(self):
        return f'{self.user.username} Profile'
