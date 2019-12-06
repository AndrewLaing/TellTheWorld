"""
# Filename:     test_views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 06/12/2019
# Description:  Test cases for tellings views
"""

import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date, timedelta 

from tellings.models import Posts, Tags, Tagmap


class SharedVariables:
    credentials = { 'username': 'testuser1',
                    'email': 'testUser1@email.com',
                    'pwd': '@myp455w0rd'
    }
    credentials2 = { 'username': 'testuser2',
                     'email': 'testUser2@email.com',
                     'pwd': '@myp455w0rd'
    }


class SharedTestMethods(TestCase):
    """ Shared helper functions used by the classes in this file """
    def check_templates_are_included(self, response, template):
        """ Checks that the page and default templates are included
            on the tested page """
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                         postTitle='Post Title', postText='Post Text'):
        """ Creates a new Posts record """
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        """ Creates a new Tags record """
        return Tags.objects.create(tagName=tagName)    

    def createTagmapRecord(self, postID=1, tagID=1):
        """ Creates a new Tagmap record """
        return Tagmap.objects.create(postID=postID, tagID=tagID)

    def createNewUpdates(self):
        """ Creates the records for two test updates """
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

    def get_loggedin_tests(self): 
        """ Logs into an account, GETs a page, and tests that the page
            is returned correctly with its template. """
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

    def get_loggedout_tests(self):
        """ GETs a page, whilst logged out, and tests that the page
            is returned correctly with its template. """
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

    def get_loggedout_redirect_tests(self):
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.loggedout_redirect_URL)

    def get_loggedin_redirects_to_errorpage_tests(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))

    def post_invalid_login_redirect_tests(self):
        self.client.logout()
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.loginPage_viewname))

    def post_loggedin_tests(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

    def post_loggedout_redirect_tests(self):
        """ Sends a POST request for a page and ensures that it
            receives a redirect to the error page instead """
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.loggedout_redirect_URL)

    def post_missing_data_tests(self):
        response = self.client.post(reverse(self.viewname), 
                                    self.partial_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

    def post_no_data_redirect_to_errorpage_tests(self):
        """ Sends a POST request for a page and ensures that it
            receives a redirect to the error page instead """
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))

    def post_no_results_found_tests(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.test_PostData2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_no_results_HTML)



class LoginpageTests(SharedTestMethods):
    """Tests for the Loginpage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:loginpage'
        cls.templateURL = 'tellings/loginpage.html'

        SV = SharedVariables
        cls.credentials = SV.credentials
        
        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])   
        cls.login_credentials = {
            'username': 'testuser1',
            'password': '@myp455w0rd'}       
        cls.login_credentials_invalid = {
            'username': 'fakeuser',
            'password': '@myp455w0rd'}

    def test_GET_loggedout(self):
        self.get_loggedout_tests()

    def test_GET_loggedin(self):
        # If logged in opens the home page
        self.get_loggedin_tests()

    def test_POST_valid(self):
        response = self.client.post(reverse(self.viewname), self.login_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        # redirects to home page after valid login
        indexpage = IndexPageViewTests()
        self.check_templates_are_included(response, indexpage.templateURL)

    def test_POST_invalid(self):
        response = self.client.post(reverse(self.viewname), self.login_credentials_invalid, follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)


class ChangeUserDetailsPageTests(SharedTestMethods):
    """Tests for the ChangeUserDetails view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:changeuserdetails'
        cls.loggedout_redirect_URL = '/loginpage/?next=/changeuserdetails/' 
        cls.templateURL = 'tellings/changeUserDetails.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()


class ChangePasswordPageTests(SharedTestMethods):
    """Tests for the ChangePassword view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:changepassword'
        cls.loggedout_redirect_URL = '/loginpage/?next=/changepassword/'
        cls.templateURL = 'tellings/changePassword.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])
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


    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()


class SignUpPageTests(SharedTestMethods):
    """Tests for the SignUpPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:signup'
        cls.errorPage_viewname = 'tellings:errorpage'
        cls.indexPage_viewname = 'tellings:index'
        cls.loginPage_viewname = 'tellings:loginpage'
        cls.templateURL = 'tellings/signup.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])
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


    def test_GET_loggedout(self):
        self.get_loggedout_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_no_data(self):
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))

    def test_POST_valid(self):
        response = self.client.post(reverse(self.viewname), self.registration_data)
        self.assertRedirects(response, reverse(self.indexPage_viewname))

    def test_POST_invalid(self):
        response = self.client.post(reverse(self.viewname), self.registration_data_invalid)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)
        
    def test_POST_valid_login(self):
        user = User.objects.get(username=self.credentials['username'])
        response = self.client.post(reverse(self.viewname), self.credentials)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertRedirects(response, reverse(self.indexPage_viewname))
        
    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class IndexPageViewTests(SharedTestMethods):
    """Tests for the IndexPage view."""

    @classmethod
    def setUpTestData(cls):
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:index'
        cls.loginPage_viewname = 'tellings:loginpage'
        cls.templateURL = 'tellings/index.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])
        cls.invalid_credentials = {
            'username': 'fakeuser',
            'pwd': '@b4dp455w0rd'}
        cls.partial_credentials = {'username': 'testuser1'}

    def setUp(self):
        pass

    def test_GET_loggedout(self):
        self.get_loggedout_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()
 
    def test_POST_no_data(self):
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

    def test_POST_missing_data(self):
        self.post_missing_data_tests()
        
    def test_POST_valid_login(self):
        user = User.objects.get(username=self.credentials['username'])
        response = self.client.post(reverse(self.viewname), self.credentials)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertRedirects(response, reverse(self.viewname))
        
    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class NewUpdatesViewTests(SharedTestMethods):
    """Tests for the NewUpdates view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:newupdates'
        cls.loggedout_redirect_URL = '/loginpage/?next=/newupdates/'
        cls.templateURL = 'tellings/newupdates.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.post_loggedin_tests()
        

class TagsViewTests(SharedTestMethods):
    """Tests for the Tags view."""

    @classmethod
    def setUpTestData(cls):
        cls.viewname = 'tellings:tags'
        cls.loggedout_redirect_URL = '/loginpage/?next=/tags/'
        cls.templateURL = 'tellings/tags.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

    def setUp(self):
        pass

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.post_loggedin_tests()


class MyUpdatesViewTests(SharedTestMethods):
    """Tests for the NewUpdates view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:myupdates'
        cls.loggedout_redirect_URL = '/loginpage/?next=/myupdates/'
        cls.templateURL = 'tellings/myupdates.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.post_loggedin_tests()


class ErrorPageViewTests(SharedTestMethods):
    """Tests for the ErrorPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:errorpage'
        cls.indexPage_viewname = 'tellings:index'
        cls.loginPage_viewname = 'tellings:loginpage'
        cls.templateURL = 'tellings/errorPage.html'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])
        cls.invalid_credentials = {
            'username': 'fakeuser',
            'pwd': '@b4dp455w0rd'}
        cls.partial_credentials = {'username': 'testuser3'}

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_GET_loggedout(self):
        self.get_loggedout_tests()

    def test_POST_no_data(self):
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_POST_missing_data(self):
        self.post_missing_data_tests()
        
    def test_POST_valid_login(self):
        user = User.objects.get(username=self.credentials['username'])
        response = self.client.post(reverse(self.viewname), 
                                    self.credentials, follow=True)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertEqual(response.status_code, 200)
        # redirects to home page after valid login
        self.assertRedirects(response, reverse(self.indexPage_viewname))
        
    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class HasPostedTodayViewTests(SharedTestMethods):
    """Tests for the HasPostedToday view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:haspostedtoday'
        cls.loggedout_redirect_URL = '/loginpage/?next=/haspostedtoday/'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])
        
        today = date.today()
        cls.test_postDate = today.strftime("%Y-%m-%d")
        cls.test_postTitle = 'PT_title'
        cls.test_postText = 'PT_text'

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_has_not_posted(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "False")

    def test_GET_has_posted(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(self.user1.id, dateOfPost=self.test_postDate)
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(self.user1.id, dateOfPost=self.test_postDate)
        response = self.client.post((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")


class TitleExistsViewTests(SharedTestMethods):
    """Tests for the TitleExists view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:titleexists'
        cls.errorPage_viewname = 'tellings:errorpage'
        cls.loggedout_redirect_URL = '/loginpage/?next=/titleexists/'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])
        
        cls.test_postTitle = 'PT_title'
        cls.test_postText = 'PT_text'

        cls.test_notexists = { 'title': 'Not exists'}
        cls.test_exists = { 'title': cls.test_postTitle }

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_redirects_to_errorpage_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_title_not_exists(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                        postTitle=self.test_postTitle, postText=self.test_postText)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_notexists, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "False")

    def test_POST_title_exists(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                        postTitle=self.test_postTitle, postText=self.test_postText)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_exists, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")


class AddNewUpdateViewTests(SharedTestMethods):
    """Tests for the AddNewUpdate view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addnewupdate'
        cls.errorPage_viewname = 'tellings:errorpage'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addnewupdate/'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

        cls.credentials2 = SV.credentials2

        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

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

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_redirects_to_errorpage_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_success(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.test_postData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "True")

    def test_POST_fail_title_exists(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.client.post(reverse(self.viewname), 
                         self.test_postData1, follow=True)
        self.client.logout()

        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
        response = self.client.post(reverse(self.viewname), 
                          self.test_duplicate_title_postData, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))

    def test_POST_fail_already_posted_today(self):
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        self.client.post(reverse(self.viewname), 
                         self.test_postData1, follow=True)

        response = self.client.post(reverse(self.viewname), 
                         self.test_postData2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))


class AddUpdatesForTagViewTests(SharedTestMethods):
    """Tests for the AddUpdatesForTag view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addupdatesfortag'
        cls.errorPage_viewname = 'tellings:errorpage'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addupdatesfortag/'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

        cls.credentials2 = SV.credentials2

        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

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

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_redirects_to_errorpage_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_contents_contains_tag(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.test_PostData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_goodTag)

    def test_POST_no_results_found(self):
        self.post_no_results_found_tests()
       

class AddUpdatesForTagByLoggedInUserViewTests(SharedTestMethods):
    """Tests for the AddUpdatesForTagByLoggedInUser view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addupdatesfortagbyloggedinuser'
        cls.errorPage_viewname = 'tellings:errorpage'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addupdatesfortagbyloggedinuser/'

        SV = SharedVariables
        cls.credentials = SV.credentials

        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

        cls.credentials2 = SV.credentials2

        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

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

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_redirects_to_errorpage_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_contents(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.test_PostData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.test_tag1)
        self.assertNotContains(response, self.test_tag2)
        self.assertNotContains(response, self.credentials2['username'])

    def test_POST_no_results_found(self):
        self.post_no_results_found_tests()     


class AddUpdatesForUsernameViewTests(SharedTestMethods):
    """Tests for the AddUpdatesForUsername view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addupdatesforusername'
        cls.errorPage_viewname = 'tellings:errorpage'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addupdatesforusername/'
        cls.credentials = {
            'username': 'testuser1',
            'email': 'testUser1@email.com',
            'pwd': '@myp455w0rd'
        }
        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])

        cls.credentials2 = {
            'username': 'testuser2',
            'email': 'testUser2@email.com',
            'pwd': '@myp455w0rd'
        }
        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

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
                
    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()
                
    def test_GET_loggedin(self):
        self.get_loggedin_redirects_to_errorpage_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_contents(self):
        self.createNewUpdates()
        self.client.login(username=self.credentials['username'], 
                          password=self.credentials['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.test_PostData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.credentials['username'])
        self.assertNotContains(response, self.credentials2['username'])

    def test_POST_no_results_found(self):
        self.post_no_results_found_tests()
