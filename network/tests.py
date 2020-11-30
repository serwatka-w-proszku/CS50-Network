from django.test import TestCase, Client
from django.contrib import auth
from django.conf import settings
from django.db import IntegrityError


from .models import *

# Create your tests here.
#TODO: Models test
#TODO: Post - editied by somebody else test
#TODO: Post - incorrect id test

'''
class TestTest(TestCase):

    def test_sprawdzanie_dzialania(self):
        """ sprawdzam działanie testów """

        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        c = Client()
        # d = Client()
        # d_login = auth.get_user(d)
        # print(d_login.is_authenticated)

        # c_login = auth.get_user(c)
        # print(c_login.is_authenticated)

        # c.login(username='temporary', password="temporary")
        # c_login = auth.get_user(c)
        # print(c_login.is_authenticated)
        # print(c.get('/following'))
        response = c.post('/login', {'username': 'fred', 'password': 'secret'})
        print(response.context["message"])
        self.assertEqual(200, 200, "it is equal")
'''

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.post = Post.objects.create(user=self.user, content="test")
        self.comment = Comment.objects.create(user=self.user, post=self.post, content="test")

    def test_auto_profile_create(self):
        """ Create new user -> create new profile test """
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_default_image_create(self):
        """ New profile created -> create default image test """
        image_path = UserProfile.objects.first().image.path[-11:]
        self.assertEqual(image_path, "default.png")
    
    def test_multiple_likes(self):
        """ Multiple likes on one post by the same user test """
        Like.objects.create(user=self.user, post=self.post, emoji_type=1)

        # Check if IntegrityError raised
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.user, post=self.post, emoji_type=2)

class FormsTestCase(TestCase):
    # TODO
    pass

class ViewsTestCase(TestCase):
    def setUp(self):
        # Force english translation
        settings.LANGUAGE_CODE = 'en'

        self.user = User.objects.create_user(username="test", password="test")
        self.c = Client()

    # Login view - GET
    def test_get_login_status_code(self):
        """ Make sure status code for GET login is 200 """
        response = self.c.get("/login")
        self.assertEqual(response.status_code, 200)
    
    def test_get_login_correct_redirection(self):
        """ Check redirection to index for logged users """
        # Login user
        self.c.login(username='test', password="test")
        # Get response
        response = self.c.get('/login')
        # Check redirect status code and redirection url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    # Login view - POST
    def test_post_login_status_code(self):
        """ 
            Create user and try to login with its data
            * check if user logged out -> login
            * test next redirection 
            * check if user logged in
        """
        # Get user logged out info
        c_logged_out = auth.get_user(self.c)
        # Try to login
        response = self.c.post('/login', {'username': 'test', 'password': 'test'})
        # Get user logged in info
        c_logged_in = auth.get_user(self.c)

        self.assertFalse(c_logged_out.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertTrue(c_logged_in.is_authenticated)

    def test_post_login_invalid_password(self):
        """ Check invalid password login behaviour """
        response = self.c.post('/login', {'username': 'test', 'password': '123'})

        self.assertEqual(response.context["message"], "Invalid username and/or password.")
