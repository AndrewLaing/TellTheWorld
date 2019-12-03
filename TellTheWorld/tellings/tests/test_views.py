"""
# Filename:     test_views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 03/12/2019
# Description:  Test cases for tellings views
"""

import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date, timedelta 

from tellings.models import Posts, Tags, Tagmap


class LoginpageTests(TestCase):
    """Tests for the Loginpage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}        
        cls.login_credentials = {
            'username': 'testuser1',
            'password': '@myp455w0rd'}       
        cls.login_credentials_invalid = {
            'username': 'fakeuser',
            'password': '@myp455w0rd'}

    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_loginpage_GET_loggedout(self):
        response = self.client.get((reverse('tellings:loginpage')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/loginpage.html')

    def test_loginpage_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:loginpage')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/loginpage.html')

    def test_signup_POST_valid(self):
        response = self.client.post(reverse('tellings:loginpage'), self.login_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/index.html')

    def test_signup_POST_invalid(self):
        response = self.client.post(reverse('tellings:loginpage'), self.login_credentials_invalid, follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/loginpage.html')

class ChangeUserDetailsPageTests(TestCase):
    """Tests for the ChangeUserDetails view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}

    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_changeuserdetails_GET_loggedout(self):
        response = self.client.get((reverse('tellings:changeuserdetails')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/changeuserdetails/')

    def test_changeuserdetails_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:changeuserdetails')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/changeUserDetails.html')

    def test_changeuserdetails_POST_loggedout(self):
        response = self.client.post(reverse('tellings:changeuserdetails'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/changeuserdetails/')

class ChangePasswordPageTests(TestCase):
    """Tests for the ChangePassword view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'
        }
        cls.change_data = {
            'old_password': '@myp455w0rd',
            'new_password1': 'ch@n63d70n3w',
            'new_password1': 'ch@n63d70n3w'
        }
        cls.new_credentials = {
            'username': 'testuser1',
            'pwd': 'ch@n63d70n3w'
        }
        cls.change_data_invalid1 = {
            'old_password': '@myp455w0rd',
            'new_password1': 'ch@n63d70n3w',
            'new_password1': 'ch@n63wr0n6'
        }
        cls.change_data_invalid2 = {
            'old_password': '@mywr0n6p455w0rd',
            'new_password1': 'ch@n63d70n3w',
            'new_password1': 'ch@n63d70n3w'
        }

    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_changepassword_GET_loggedout(self):
        response = self.client.get((reverse('tellings:changepassword')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/changepassword/')

    def test_changepassword_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:changepassword')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/changePassword.html')

    def test_changepassword_POST_loggedout(self):
        response = self.client.post(reverse('tellings:changepassword'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/changepassword/')

class SignUpPageTests(TestCase):
    """Tests for the SignUpPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}
        cls.invalid_credentials = {
            'username': 'fakeuser',
            'pwd': '@b4dp455w0rd'}
        cls.registration_data = {
            'username': 'testuser2',
            'password1': '@myp455w0rd',
            'password2': '@myp455w0rd'}
        cls.registration_data_invalid = {
            'username': 'testuser2',
            'password1': '@myp455w0rd',
            'password2': '@myp455'}

    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_signup_GET_loggedout(self):
        response = self.client.get((reverse('tellings:changepassword')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/changepassword/')

    def test_signup_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:signup')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/signup.html')

    def test_signup_POST_no_data(self):
        response = self.client.post(reverse('tellings:signup'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_signup_POST_valid(self):
        response = self.client.post(reverse('tellings:signup'), self.registration_data)
        self.assertRedirects(response, reverse('tellings:index'))

    def test_signup_POST_invalid(self):
        response = self.client.post(reverse('tellings:signup'), self.registration_data_invalid)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/signup.html')
        
    def test_signup_POST_valid_login(self):
        user = User.objects.get(username=self.credentials['username'])
        response = self.client.post(reverse('tellings:signup'), self.credentials)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertRedirects(response, reverse('tellings:index'))
        
    def test_signup_POST_invalid_login(self):
        self.client.logout()
        response = self.client.post(reverse('tellings:signup'), 
                                    self.invalid_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:loginpage'))

class IndexPageViewTests(TestCase):
    """Tests for the IndexPage view."""

    @classmethod
    def setUpTestData(cls):
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}
        cls.invalid_credentials = {
            'username': 'fakeuser',
            'pwd': '@b4dp455w0rd'}
        cls.partial_credentials = {'username': 'testuser1'}

    def setUp(self):
        pass

    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_index_GET_loggedout(self):
        response = self.client.get(reverse('tellings:index'))
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/index.html')

    def test_index_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:index')))
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/index.html')
 
    def test_index_POST_no_data(self):
        response = self.client.post(reverse('tellings:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/index.html')

    def test_index_POST_missing_data(self):
        response = self.client.post(reverse('tellings:index'), 
                                    self.partial_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/index.html')
        
    def test_index_POST_valid_login(self):
        user = User.objects.get(username=self.credentials['username'])
        response = self.client.post(reverse('tellings:index'), self.credentials)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertRedirects(response, reverse('tellings:index'))
        
    def test_index_POST_invalid_login(self):
        self.client.logout()
        response = self.client.post(reverse('tellings:index'), 
                                    self.invalid_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:loginpage'))

class NewUpdatesViewTests(TestCase):
    """Tests for the NewUpdates view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}


    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_newupdates_GET_loggedout(self):
        response = self.client.get((reverse('tellings:newupdates')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/newupdates/')

    def test_newupdates_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:newupdates')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/newupdates.html')

    def test_newupdates_POST_loggedout(self):
        response = self.client.post(reverse('tellings:newupdates'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/newupdates/')

    def test_newupdates_POST_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:newupdates'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/newupdates.html')
        
class TagsViewTests(TestCase):
    """Tests for the Tags view."""

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}


    def setUp(self):
        pass

    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')


    def test_tags_GET_loggedout(self):
        response = self.client.get((reverse('tellings:tags')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/tags/')

    def test_tags_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:tags')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/tags.html')

    def test_tags_POST_loggedout(self):
        response = self.client.post(reverse('tellings:tags'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/tags/')

    def test_tags_POST_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:tags'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/tags.html')

class MyUpdatesViewTests(TestCase):
    """Tests for the NewUpdates view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}


    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_myupdates_GET_loggedout(self):
        response = self.client.get((reverse('tellings:myupdates')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/myupdates/')

    def test_myupdates_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:myupdates')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/myupdates.html')

    def test_myupdates_POST_loggedout(self):
        response = self.client.post(reverse('tellings:myupdates'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/myupdates/')

    def test_myupdates_POST_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:myupdates'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/myupdates.html')

class ErrorPageViewTests(TestCase):
    """Tests for the ErrorPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}
        cls.invalid_credentials = {
            'username': 'fakeuser',
            'pwd': '@b4dp455w0rd'}
        cls.partial_credentials = {'username': 'testuser3'}

    def check_templates_are_included(self, response, template):
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def test_errorpage_GET(self):
        response = self.client.get((reverse('tellings:errorpage')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, 'tellings/errorPage.html')

    def test_errorpage_POST_no_data(self):
        response = self.client.post(reverse('tellings:errorpage'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_errorpage_POST_missing_data(self):
        response = self.client.post(reverse('tellings:errorpage'), 
                                    self.partial_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_errorpage_POST_valid_login(self):
        user = User.objects.get(username=self.credentials['username'])
        response = self.client.post(reverse('tellings:errorpage'), 
                                    self.credentials, follow=True)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:index'))
        
    def test_errorpage_POST_invalid_login(self):
        self.client.logout()
        response = self.client.post(reverse('tellings:errorpage'), 
                                    self.invalid_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/')

class HasPostedTodayViewTests(TestCase):
    """Tests for the HasPostedToday view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}
        
        today = date.today()
        cls.test_postDate = today.strftime("%Y-%m-%d")
        cls.test_postTitle = 'PT_title'
        cls.test_postText = 'PT_text'

    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                   postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def test_haspostedtoday_GET_loggedout(self):
        response = self.client.get((reverse('tellings:haspostedtoday')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/haspostedtoday/')

    def test_haspostedtoday_GET_has_not_posted(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse('tellings:haspostedtoday')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "False")

    def test_haspostedtoday_GET_has_posted(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(self.user1.id, dateOfPost=self.test_postDate)
        response = self.client.get((reverse('tellings:haspostedtoday')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")

    def test_haspostedtoday_POST_loggedout(self):
        response = self.client.post(reverse('tellings:haspostedtoday'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/haspostedtoday/')

    def test_haspostedtoday_POST_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(self.user1.id, dateOfPost=self.test_postDate)
        response = self.client.post((reverse('tellings:haspostedtoday')), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")

class TitleExistsViewTests(TestCase):
    """Tests for the HasPostedToday view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}
        
        cls.test_postTitle = 'PT_title'
        cls.test_postText = 'PT_text'

        cls.test_notexists = { 'title': 'Not exists'}
        cls.test_exists = { 'title': cls.test_postTitle }


    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                   postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def test_titleexists_GET_loggedout(self):
        response = self.client.get(reverse('tellings:titleexists'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/titleexists/')

    def test_titleexists_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get(reverse('tellings:titleexists'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_titleexists_POST_loggedout(self):
        response = self.client.post(reverse('tellings:titleexists'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/titleexists/')

    def test_titleexists_POST_no_data(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:titleexists'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_titleexists_POST_title_not_exists(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                        postTitle=self.test_postTitle, postText=self.test_postText)
        response = self.client.post(reverse('tellings:titleexists'), 
                                    self.test_notexists, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "False")

    def test_titleexists_POST_title_exists(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                        postTitle=self.test_postTitle, postText=self.test_postText)
        response = self.client.post(reverse('tellings:titleexists'), 
                                    self.test_exists, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")

class AddNewUpdateViewTests(TestCase):
    """Tests for the AddNewUpdate view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser3@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}

        cls.user2 = User.objects.create_user('testuser2', 'testUser4@email.com', '@myp455w0rd')
        cls.credentials2 = {
            'username': 'testuser2',
            'pwd': '@myp455w0rd'}

        today = date.today()
        cls.test_postDate = today.strftime("%Y-%m-%d")
        cls.test_postTitle1 = 'PT_title_1'
        cls.test_postTitle2 = 'PT_title_2'
        cls.test_postText1 = 'PT_text_1'
        cls.test_postText2 = 'PT_text_2'
        cls.test_postTags = '["test","testing","this is a test"]'

        cls.test_postData1 = { 'postTitle': cls.test_postTitle1,
                              'postText': cls.test_postText1,
                              'postTags': cls.test_postTags, }

        cls.test_postData2 = { 'postTitle': cls.test_postTitle2,
                              'postText': cls.test_postText2,
                              'postTags': cls.test_postTags, }
        
        cls.test_duplicate_title_postData = { 'postTitle': cls.test_postTitle1,
                              'postText': cls.test_postText2,
                              'postTags': cls.test_postTags, }


    def test_addnewupdate_GET_loggedout(self):
        response = self.client.get(reverse('tellings:addnewupdate'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addnewupdate/')

    def test_addnewupdate_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get(reverse('tellings:addnewupdate'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addnewupdate_POST_loggedout(self):
        response = self.client.post(reverse('tellings:addnewupdate'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addnewupdate/')

    def test_addnewupdate_POST_no_data(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addnewupdate'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addnewupdate_POST_success(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addnewupdate'), 
                                    self.test_postData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")

    def test_addnewupdate_POST_fail_title_exists(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.client.post(reverse('tellings:addnewupdate'), 
                         self.test_postData1, follow=True)
        self.client.logout()

        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
        response = self.client.post(reverse('tellings:addnewupdate'), 
                          self.test_duplicate_title_postData, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))


    def test_addnewupdate_POST_fail_already_posted_today(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.client.post(reverse('tellings:addnewupdate'), 
                         self.test_postData1, follow=True)

        response = self.client.post(reverse('tellings:addnewupdate'), 
                         self.test_postData2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

class AddUpdatesForTagViewTests(TestCase):
    """Tests for the AddUpdatesForTag view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser3@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}

        cls.user2 = User.objects.create_user('testuser2', 'testUser4@email.com', '@myp455w0rd')
        cls.credentials2 = {
            'username': 'testuser2',
            'pwd': '@myp455w0rd'}

        cls.test_postTitle1 = 'PT_title_1'
        cls.test_postTitle2 = 'PT_title_2'
        cls.test_postText1 = 'PT_text_1'
        cls.test_postText2 = 'PT_text_2'
        cls.test_postTags = ["qwertyuiop","testing","this is a test", "still a test"]
        cls.test_goodTag = cls.test_postTags[0]
        cls.test_badTag = "NotATag"

        cls.test_PostData1 = {
            'postTag': cls.test_goodTag,
        }
        cls.test_PostData2 = {
            'postTag': cls.test_badTag,
        }

        cls.test_no_results_HTML = '<h1>No results found!</h1>'

        
    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                   postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        return Tags.objects.create(tagName=tagName)

    def createTagmapRecord(self, postID=1, tagID=1):
        return Tagmap.objects.create(postID=postID, tagID=tagID)

    def createNewUpdates(self):
        post1 = self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                              postTitle=self.test_postTitle1, postText=self.test_postText1)
        post2 = self.createPostRecord(userID=self.user2.id, dateOfPost='2019-08-02', 
                              postTitle=self.test_postTitle2, postText=self.test_postText2)

        skipCreate = True
        for tag in self.test_postTags:
            tg = self.createTagRecord(tag)
            if skipCreate:
                self.createTagmapRecord(post2, tg)
                skipCreate = False
            else:
                self.createTagmapRecord(post1, tg)
                self.createTagmapRecord(post2, tg)

    def test_addupdatesfortag_GET_loggedout(self):
        response = self.client.get(reverse('tellings:addupdatesfortag'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addupdatesfortag/')

    def test_addupdatesfortag_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get(reverse('tellings:addupdatesfortag'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addupdatesfortag_POST_loggedout(self):
        response = self.client.post(reverse('tellings:addupdatesfortag'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addupdatesfortag/')

    def test_addupdatesfortag_POST_no_data(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesfortag'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addupdatesfortag_POST_contents_contains_tag(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesfortag'), 
                                    self.test_PostData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_goodTag)

    def test_addupdatesfortag_POST_no_results_found(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesfortag'), 
                                    self.test_PostData2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_no_results_HTML)
       
class AddUpdatesForTagByLoggedInUserViewTests(TestCase):
    """Tests for the AddUpdatesForTagByLoggedInUser view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}

        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')
        cls.credentials2 = {
            'username': 'testuser2',
            'pwd': '@myp455w0rd'}

        cls.test_postTitle1 = 'PT_title_1'
        cls.test_postTitle2 = 'PT_title_2'
        cls.test_postText1 = 'PT_text_1'
        cls.test_postText2 = 'PT_text_2'
        cls.test_postTags = ["qwertyuiop","zxcvbnm","this is a test", "still a test"]
        cls.test_tag1 = cls.test_postTags[1]
        cls.test_tag2 = cls.test_postTags[0]
        cls.test_badtag = "NotATag"

        cls.test_PostData1 = {
            'postTag': cls.test_tag1,
        }
        cls.test_PostData2 = {
            'postTag': cls.test_tag2,
        }
        cls.test_no_results_HTML = '<h1>No results found!</h1>'

    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                   postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        return Tags.objects.create(tagName=tagName)

    def createTagmapRecord(self, postID=1, tagID=1):
        return Tagmap.objects.create(postID=postID, tagID=tagID)

    def createNewUpdates(self):
        post1 = self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                              postTitle=self.test_postTitle1, postText=self.test_postText1)
        post2 = self.createPostRecord(userID=self.user2.id, dateOfPost='2019-08-02', 
                              postTitle=self.test_postTitle2, postText=self.test_postText2)

        skipCreate = True
        for tag in self.test_postTags:
            tg = self.createTagRecord(tag)
            if skipCreate:
                self.createTagmapRecord(post2, tg)
                skipCreate = False
            else:
                self.createTagmapRecord(post1, tg)
                self.createTagmapRecord(post2, tg)

    def test_addupdatesfortagbyloggedinuser_GET_loggedout(self):
        response = self.client.get(reverse('tellings:addupdatesfortagbyloggedinuser'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addupdatesfortagbyloggedinuser/')

    def test_addupdatesfortagbyloggedinuser_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get(reverse('tellings:addupdatesfortagbyloggedinuser'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addupdatesfortagbyloggedinuser_POST_loggedout(self):
        response = self.client.post(reverse('tellings:addupdatesfortagbyloggedinuser'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addupdatesfortagbyloggedinuser/')

    def test_addupdatesfortagbyloggedinuser_POST_no_data(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesfortagbyloggedinuser'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addupdatesfortagbyloggedinuser_POST_contents(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesfortagbyloggedinuser'), 
                                    self.test_PostData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_tag1)
        self.assertNotContains(response, self.test_tag2)
        self.assertNotContains(response, self.credentials2['username'])

    def test_addupdatesfortag_POST_no_results_found(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesfortagbyloggedinuser'), 
                                    self.test_PostData2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_no_results_HTML)       

class AddUpdatesForUsernameViewTests(TestCase):
    """Tests for the AddUpdatesForUsername view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.credentials = {
            'username': 'testuser1',
            'pwd': '@myp455w0rd'}

        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')
        cls.credentials2 = {
            'username': 'testuser2',
            'pwd': '@myp455w0rd'}

        cls.test_postTitle1 = 'PT_title_1'
        cls.test_postTitle2 = 'PT_title_2'
        cls.test_postText1 = 'PT_text_1'
        cls.test_postText2 = 'PT_text_2'
        cls.test_postTags = ["qwertyuiop","zxcvbnm","this is a test", "still a test"]
        cls.test_tag1 = cls.test_postTags[1]
        cls.test_tag2 = cls.test_postTags[0]
        cls.test_badTag = "NotATag"

        cls.test_PostData1 = {
            'username': cls.credentials['username'],
        }
        cls.test_PostData2 = {
            'username': 'NotAUsername'
        }
        cls.test_no_results_HTML = '<h1>No results found!</h1>'

    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                   postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        return Tags.objects.create(tagName=tagName)

    def createTagmapRecord(self, postID=1, tagID=1):
        return Tagmap.objects.create(postID=postID, tagID=tagID)
         
    def createNewUpdates(self):
        post1 = self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                              postTitle=self.test_postTitle1, postText=self.test_postText1)
        post2 = self.createPostRecord(userID=self.user2.id, dateOfPost='2019-08-02', 
                              postTitle=self.test_postTitle2, postText=self.test_postText2)

        skipCreate = True
        for tag in self.test_postTags:
            tg = self.createTagRecord(tag)
            if skipCreate:
                self.createTagmapRecord(post2, tg)
                skipCreate = False
            else:
                self.createTagmapRecord(post1, tg)
                self.createTagmapRecord(post2, tg)
                
    def test_addupdatesforusername_GET_loggedout(self):
        response = self.client.get(reverse('tellings:addupdatesforusername'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addupdatesforusername/')
                
    def test_addupdatesforusername_GET_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get(reverse('tellings:addupdatesforusername'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addupdatesforusername_POST_loggedout(self):
        response = self.client.post(reverse('tellings:addupdatesforusername'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/loginpage/?next=/addupdatesforusername/')

    def test_addupdatesforusername_POST_no_data(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesforusername'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tellings:errorpage'))

    def test_addupdatesforusername_POST_contents(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesforusername'), 
                                    self.test_PostData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.credentials['username'])
        self.assertNotContains(response, self.credentials2['username'])

    def test_addupdatesfortag_POST_no_results_found(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse('tellings:addupdatesforusername'), 
                                    self.test_PostData2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_no_results_HTML)
