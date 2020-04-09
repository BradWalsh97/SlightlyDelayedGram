from django.test import TestCase
from users.models import Picture, Profile, Comment
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count

class TestTrendingPage(TestCase):
    def setUp(self):
        self.postPicUser1 = User.objects.create_user('bob')
        self.postPicUser2 = User.objects.create_user('bobbert')
        self.likePicUser1 = User.objects.create_user('tim')
        self.likePicUser2 = User.objects.create_user('jim')
        self.likePicUser3 = User.objects.create_user('jimbo')

        self.picture1 = Picture.objects.create(
            owner = self.postPicUser1,
            picture_object = 'media/italy-landscape.png',
            post_date = timezone.now()
        )

        self.picture2 = Picture.objects.create(
            owner = self.postPicUser1,
            picture_object = 'media/italy-landscape.png',
            post_date = timezone.now()
        )

    #trending page with a simple order where one pic has no likes and the other has one
    def test_simple_order(self):
        self.picture1.likes.add(self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all().count(), 1)
        self.assertEquals(self.picture2.likes.all().count(), 0)

        pics = Picture.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        self.assertEquals(pics[0].likes.all().count(), 1)
        self.assertEquals(pics[1].likes.all().count(), 0)

    def test_like_then_unlike(self):
        self.picture1.likes.add(self.likePicUser1)
        self.picture1.likes.add(self.likePicUser2)
        self.picture2.likes.add(self.likePicUser1)        
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[1], self.likePicUser2)
        self.assertEquals(self.picture2.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all().count(), 2)
        self.assertEquals(self.picture2.likes.all().count(), 1)

        pics = Picture.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        self.assertEquals(pics[0].likes.all().count(), 2)
        self.assertEquals(pics[1].likes.all().count(), 1)

        self.picture1.likes.remove(self.likePicUser1)
        self.picture1.likes.remove(self.likePicUser2)

        pics = Picture.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        self.assertEquals(pics[0].likes.all().count(), 1)
        self.assertEquals(pics[1].likes.all().count(), 0)

    def test_changing_order(self):
        self.picture1.likes.add(self.likePicUser1)
        self.picture1.likes.add(self.likePicUser2)
        self.picture2.likes.add(self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[1], self.likePicUser2)
        self.assertEquals(self.picture2.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all().count(), 2)
        self.assertEquals(self.picture2.likes.all().count(), 1)

        pics = Picture.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        self.assertEquals(pics[0].likes.all().count(), 2)
        self.assertEquals(pics[1].likes.all().count(), 1)

        self.picture2.likes.add(self.likePicUser2, self.likePicUser3)
        self.assertEquals(self.picture2.likes.all().count(), 3)
        pics = Picture.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        self.assertEquals(pics[0].likes.all().count(), 3)
        self.assertEquals(pics[1].likes.all().count(), 2)