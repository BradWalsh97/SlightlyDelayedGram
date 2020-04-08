from django.test import TestCase
from users.models import Picture, Profile, Comment
from django.utils import timezone
from django.contrib.auth.models import User



class TestFollowUser(TestCase):

    def setUp(self):

        #print('.......................0...................')
        self.bobUser = User.objects.create_user('bob')
        self.timUser = User.objects.create_user('tim')
        self.jimUser = User.objects.create_user('jim')
        #print('.......................1...................')
        #print('Bob id: ' + str(self.bobUser.id))
        #print('.......................1-1...................')
        #print('Users: ' + str(User.objects.all()))
        #print('.......................1-2...................')
        #print('Profiles: ' + str(Profile.objects.all()))
        #print('.......................1-3...................')
        #Profile.objects.remove(bobUser)
        #print('Profiles: ' + str(Profile.objects.all()))
        # self.bob = Profile.objects.create(
        #     user = 'bob'
        #      #user = self.bobUser,
        #      #image = 'media/default.jpg'
        #  )
        # print('.......................2...................')
        # #self.bob.save()

        # self.tim = Profile.objects.create(
        #     user = User.objects.create_user('tim'),
        #     #image = 'media/default.jpg'
        # )
        # print('.......................3...................')
        # # self.tim.save()

        # self.jim = Profile.objects.create(
        #     user = User.objects.create_user('jim'),
        #     #image = 'media/default.jpg'
        # )
        # print('.......................4...................')
        # self.jim.save()
        self.bobUser.followed.add(self.timUser.profile)
        self.timUser.following.add(self.bobUser.profile)
        #print('Bob\'s followers:' + str(self.bobUser.followed.all()))


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


    
        






#     def setUp(self):
#         Profile.objects.all().delete()
#         User.objects.all().delete()
#         #os.system('python3 manage.py showmigrations')
#         #create user who will be followed
#         self.followedUser1 = User.objects.create_user(username='jericho', \
#             email='bob@bob.com', password='bob123!@#')
#         self.followedUser1.save()
#         # self.followedUser2 = User.objects.create_user('Fred')
#         # self.followedUser2.save()

#         self.followedProfile1 = Profile.objects.create(
#             user = self.followedUser1, image = 'media/default.jpg'
#             #user = User.objects.create_user('bobby')
#             #image = 'media/default.jpg'
#         )
#         self.followedProfile1.save()
#         # self.followedProfile2 = Profile.objects.create(
#         #     user = self.followedUser2,
#         #     image = 'media/default.jpg'
#         # )

#         #create users who will follow the followedUser
#         self.followingUser1 = User.objects.create_user('jim')
#         self.followingUser1.save()
#         self.followingUser2 = User.objects.create_user('tim')
#         self.followingUser2.save()

#         self.followingProfile1 = Profile.objects.create(
#             user = self.followingUser1, image = 'media/default.jpg'
#         )
#         self.followingProfile1.save()


#         self.followedProfile1.followed.add(self.followingProfile1.user)
#         self.followedProfile1.save()

#         self.followingUser1.following.add(self.followedProfile1.user)
#         self.followingProfile1.save()

#         print(self.followingProfile1.following)
#         # self.followingProfile2 = Profile.objects.create(
#         #     user = self.followingUser2,
#         #     image = 'media/default.jpg'
#         # )
#         # self.followingProfile3 = Profile.objects.create(
#         #     user = self.followingUser3,
#         #     image = 'media/default.jpg'
#         # )

#  #   def tearDown(self):
#         #Profile.objects.all().delete()
#     #     self.followedProfile1.delete()
#     #     self.followedProfile2.delete()
#     #     self.followingProfile1.delete()
#     #     self.followingProfile2.delete()
#     #     self.followingProfile3.delete()
#     #     self.followedUser1.delete()
#     #     self.followedUser2.delete()
#     #     self.followingUser1.delete()
#     #     self.followingUser2.delete()
#     #     self.followingUser3.delete()
        
        

#     #test to see if followed list changes when user is followed
#     def test_follow_a_user(self):
        

#         # self.followedUser1.followed.all().delete()
#         # self.followingUser1.following.all().delete()
#         # self.followedUser1.followed.remove(self.followingProfile1)
#         # self.followedUser1.followed.add(self.followingProfile1.user) 
        
#         self.assertEquals(self.followedUser1.followed, 'jim')
#         self.assertEquals(self.followingUser1.following, 'Bob')

#     #test to see if multiple users follow a single user, will they all show
#     #up in the proper lists
#     # def test_followed_by_multiple_users(self):
#     #     self.followedUser1.followed.add(self.followingUser1)
#     #     # self.followedUser1.followed.set(self.followedUser1.followed + \
#     #     #  "," + self.followingUser2.username)
#     #     self.followedUser1.follwed.add(self.followingUser2.id)

#     #     self.followingUser1.following = self.followedUser1.username
#     #     self.followingUser2.following = self.followedUser1.username

#     #     self.assertEquals(self.followedUser1.followed, 'jim,tim')
#     #     self.assertEquals(self.followingUser1.following, \
#     #         self.followingUser2.following)
#     #     self.assertEquals(self.followingUser2.following, \
#     #         self.followedUser1.username)

#     # #if one user follows multiple people, will the people they follow
#     # #show up in the correct list
#     # def test_following_multiple_users(self):
#     #     self.followedUser1.followed.add(self.followingUser1.id)
#     #     self.followedUser2.followed.add(self.followingUser1.id)
#     #     self.followingUser1.following = \
#     #         self.followedUser1.username + "," + \
#     #              self.followedUser2.username

#     #     self.assertEquals(self.followingUser1.following, "Bob,Fred")

#     # #check to makesure user does not show up as a follower if they
#     # #dont follow a given user
#     # def test_not_following(self):
#     #     self.followingUser3 = User.objects.create_user('toby')
#     #     self.followingUser3.save()

#     #     self.followedUser1.followed.add(self.followingUser1.id)
#     #     # self.followedUser1.followed.set(self.followedUser1.followed + \
#     #     #     ',' + self.followingUser2.username)
#     #     self.followedUser1.followed.add(self.followingUser2.id)

#     #     self.assertEquals(self.followedUser1.followed, 'jim,tim')

#     #     followList = self.followedUser1.followed.split(',')
#     #     #we want to make sure that only jim and tim are in the 
#     #     #follow list
#     #     for follower in followList:
#     #         self.assertNotEquals(follower, 'toby')



