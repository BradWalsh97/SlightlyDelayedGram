from django.test import TestCase
from users.models import Picture, Profile, Comment
from django.utils import timezone
from django.contrib.auth.models import User
import time, re

class TestPostComment(TestCase):

    def setUp(self):       
        #create the user who will post the picture
        self.pictureUser = User.objects.create_user('bob')
        self.pictureUser.save()

        #create users who will comment on the picture
        self.comment1User = User.objects.create_user('joe')
        self.comment1User.save()
        self.comment2User = User.objects.create_user('billy')
        self.comment2User.save()
        self.comment3User = User.objects.create_user('mary')
        self.comment3User.save()

        #Create reference to pic we want to upload
        self.pic = 'media/italy-landscape.png'

        #create reference times
        self.pictureUploadTime = timezone.now()
        time.sleep(0.5)
        self.commentTime = timezone.now()

        #Create the picture to be posted
        self.validPicture = Picture.objects.create(
            owner=self.pictureUser,
            picture_object=self.pic,
            post_date=self.pictureUploadTime
        )

        #create the text to be added to the comment
        self.commentText = "Wow bob, thats so funny. AhaHA! Love Joe <3"

        #create the first comment
        self.comment1 = Comment.objects.create(
            picture = self.validPicture,
            author = self.comment1User,
            text = self.commentText,
            created_date = self.commentTime,
            approved_comment = True
        )

        #create a second comment
        self.comment2 = Comment.objects.create(
            picture = self.validPicture,
            author = self.comment2User,
            text = self.commentText,
            created_date = self.commentTime,
            approved_comment = True
        )

        #create a third comment
        self.comment3 = Comment.objects.create(
            picture = self.validPicture,
            author = self.comment3User,
            text = self.commentText,
            created_date = self.commentTime,
            approved_comment = True
        )

    #test if the comment text matches and it was uploaded at the correct time
    def test_post_comment(self):
        self.assertEquals(self.comment1.text, self.commentText)
        self.assertEquals(self.comment1.created_date, self.commentTime)
        self.assertNotEquals(self.comment1.text, "")
        self.assertNotEquals(self.comment1.text, None)

    #test if all three comments exist
    def test_comment_count(self):
        comments = Comment.objects.filter(picture = self.validPicture)
        self.assertEquals(len(comments), 3)

    #now we check to see if the comment is actually in the picture
    def test_check_comment_on_photo(self):

        #get the comments on the picture
        comments = Comment.objects.filter(picture = self.validPicture)

        #now for each comment in the list of comments, we extract the comment itself
        #and assert if it does not match the correct commentText
        for unfilteredComment in comments:
            #we can split on the '-' since we know they wont be present
            #in the comments made for the test
            filteredComment = unfilteredComment.text.split('-')
            self.assertEquals(filteredComment[0], self.commentText)



