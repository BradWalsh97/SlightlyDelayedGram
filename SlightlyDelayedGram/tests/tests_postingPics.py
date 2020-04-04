from django.test import TestCase
from users.models import Picture, Profile
from PIL import Image
from django.utils import timezone
from django.contrib.auth.models import User
import base64
import io


class TestPostPic(TestCase):
    def setUp(self):

        #Create a user to assign the photo to as owner
        self.user = User.objects.create_user('bob')
        self.user.save()

        #Create reference to pic we want to upload
        self.pic = 'media/italy-landscape.png'

        #create reference upload time
        self.uploadTime = timezone.now()

        #Create a valid picture object in the DB
        self.validPicture = Picture.objects.create(
            owner=self.user,
            picture_object=self.pic,
            post_date=self.uploadTime
        )

        #Create a picture object that has no path to the file
        self.emptyPicture = Picture.objects.create(
            owner = self.user,
            picture_object = "",
            post_date = self.uploadTime
        )
        #Create a picture object that is not given a picture
        self.noPicGiven = Picture.objects.create(
            owner = self.user,
            picture_object = None,
            post_date = self.uploadTime
        )

        #Create a picture object that is to have its picture deleted
        self.pictureToDelete = self.validPicture

    #test if a valid picture is stored in the model correctly
    def test_upload_pic(self): 
        self.assertEquals(self.validPicture.owner, self.user)
        self.assertEquals(self.validPicture.picture_object, self.pic)
        self.assertEquals(self.validPicture.post_date, self.uploadTime)

    #test if an empty picture (no pic referenced) is stored
    def test_upload_empty_pic(self): 
        self.assertEquals(self.emptyPicture.picture_object, "")

    #tests if image is properly deleted
    def test_delete_pic(self): 
        self.pictureToDelete.picture_object.delete()
        self.assertEquals(self.pictureToDelete.picture_object, None)

    #tests when no image path is provided
    def test_upload_no_pic(self): #tests when no image path is provided
        self.assertEquals(self.noPicGiven.picture_object, None)
