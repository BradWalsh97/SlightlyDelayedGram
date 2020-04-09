from django.test import TestCase
from users.models import Picture, Profile, Comment
from django.utils import timezone
from django.contrib.auth.models import User



class TestFollowUser(TestCase):

    def setUp(self):
        self.bobUser = User.objects.create_user('bob')
        self.timUser = User.objects.create_user('tim')
        self.jimUser = User.objects.create_user('jim')
        self.bobUser.followed.add(self.timUser.profile)
        self.timUser.following.add(self.bobUser.profile)


    #checks if user shows up in list when following another user
    def test_follow_a_user(self):
        self.assertEquals(self.bobUser.followed.filter(id=2)[0], self.timUser.profile)
        self.assertEquals(self.timUser.following.filter(id=1)[0], self.bobUser.profile)

    #checks if multiple users are shown in list
    def test_followed_by_multiple_users(self):
        self.bobUser.followed.add(self.jimUser.profile)
        followers = self.bobUser.followed.all()
        self.assertEquals(followers[0], self.timUser.profile)
        self.assertEquals(followers[1], self.jimUser.profile)
    
    #check if unfollowing will actually unfollow a user
    def test_unfollow_a_user(self):
        self.bobUser.followed.remove(self.timUser.profile) 
        self.timUser.following.remove(self.bobUser.profile)
        self.assertEquals(self.bobUser.followed.all().count(), 0)
        self.assertEquals(self.timUser.following.all().count(), 0)

    #check if the following list is updated correctly
    def test_following_list_correct(self):
        self.tobyUser = User.objects.create_user('TOBY')
        self.bobUser.followed.add(self.tobyUser.profile)
        self.tobyUser.following.add(self.bobUser.profile)
        self.assertEquals(self.tobyUser.following.all()[0], self.bobUser.profile)