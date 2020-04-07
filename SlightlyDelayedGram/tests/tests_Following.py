from django.test import TestCase
from users.models import Picture, Profile, Comment
from django.utils import timezone
from django.contrib.auth.models import User


class TestFollowUser(TestCase):
    def setUp(self):
        #create user who will be followed
        self.followedUser1 = User.objects.create_user('Bob')
        self.followedUser1.save()
        self.followedUser2 = User.objects.create_user('Fred')
        self.followedUser2.save()

        #create users who will follow the followedUser
        self.followingUser1 = User.objects.create_user('jim')
        self.followingUser1.save()
        self.followingUser2 = User.objects.create_user('tim')
        self.followingUser2.save()

    #test to see if followed list changes when user is followed
    def test_follow_a_user(self):
        self.followedUser1.followed = self.followingUser1.username
        self.followingUser1.following = self.followedUser1.username
        self.assertEquals(self.followedUser1.followed, 'jim')
        self.assertEquals(self.followingUser1.following, 'Bob')

    #test to see if multiple users follow a single user, will they all show
    #up in the proper lists
    def test_followed_by_multiple_users(self):
        self.followedUser1.followed = self.followingUser1.username
        self.followedUser1.followed = self.followedUser1.followed + \
         "," + self.followingUser2.username

        self.followingUser1.following = self.followedUser1.username
        self.followingUser2.following = self.followedUser1.username

        self.assertEquals(self.followedUser1.followed, 'jim,tim')
        self.assertEquals(self.followingUser1.following, \
            self.followingUser2.following)
        self.assertEquals(self.followingUser2.following, \
            self.followedUser1.username)

    #if one user follows multiple people, will the people they follow
    #show up in the correct list
    def test_following_multiple_users(self):
        self.followedUser1.followed = self.followingUser1.username
        self.followedUser2.followed = self.followingUser1.username
        self.followingUser1.following = \
            self.followedUser1.username + "," + \
                 self.followedUser2.username

        self.assertEquals(self.followingUser1.following, "Bob,Fred")


