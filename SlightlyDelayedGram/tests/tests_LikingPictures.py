from django.test import TestCase
from users.models import Picture, Profile, Comment
from django.utils import timezone
from django.contrib.auth.models import User

class TestLikePictures(TestCase):

    def setUp(self):
        #Create the users who will post/like pics
        self.postPicUser = User.objects.create_user('bob')
        self.likePicUser1 = User.objects.create_user('tim')
        self.likePicUser2 = User.objects.create_user('jim')

        #Create the picture which will be posted/liked
        self.picture1 = Picture.objects.create(
            owner = self.postPicUser,
            picture_object = 'media/italy-landscape.png',
            post_date = timezone.now()
        )

    #test if user can like a pic
    def test_single_like_a_picture(self):
        self.picture1.likes.add(self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)

    #test if multiple users can like a pic
    def test_multiple_like_a_picture(self):
        self.picture1.likes.add(self.likePicUser1, self.likePicUser2)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[1], self.likePicUser2)

    #test flag stopping user from liking pic twice
    def test_stop_one_user_from_liking_twice(self):
        self.picture1.likes.add(self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)

        #since pic has already been liked, the following line should say so (true).
        #this check is used to stop a user from double liking 
        self.assertEquals(self.picture1.likes.\
            filter(id=self.likePicUser1.id).exists(), True)

    #test if user cna unlike if they're the only to like
    def test_unlike_if_single_like(self):
        self.picture1.likes.add(self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)
        self.picture1.likes.remove(self.likePicUser1)
        self.assertNotEquals(self.picture1.likes.all(), self.likePicUser1)

    #test if one user unlikes pic, the others stay there
    def test_unlike_if_multiple_user_likes(self):
        self.picture1.likes.add(self.likePicUser1)
        self.picture1.likes.add(self.likePicUser2)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[1], self.likePicUser2)
        self.picture1.likes.remove(self.likePicUser1)
        self.assertNotEquals(self.picture1.likes.all()[0], self.likePicUser1)
        self.assertEquals(self.picture1.likes.all()[0], self.likePicUser2)