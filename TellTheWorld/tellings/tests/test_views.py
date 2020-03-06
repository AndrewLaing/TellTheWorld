"""
# Filename:     test_views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 28/01/2020
# Description:  Test cases for tellings views
"""

import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date, timezone

from tellings.models import *
import json

class SharedVariables:
    errorPage_viewname = 'tellings:errorpage'
    indexPage_viewname = 'tellings:index'
    loginPage_viewname = 'tellings:loginpage'
    credentials1 = { 'username': 'testuser1',
                    'email': 'testUser1@email.com',
                    'pwd': '@myp455w0rd'
    }
    credentials2 = { 'username': 'testuser2',
                     'email': 'testUser2@email.com',
                     'pwd': '@myp455w0rd'
    }
    credentials3 = { 'username': 'testuser3',
                     'email': 'testUse3@email.com',
                     'pwd': '@myp455w0rd'
    }
    invalid_credentials = { 'username': 'fakeuser',
                            'pwd': '@b4dp455w0rd'
    }
    partial_credentials = {'username': 'testuser1'}

    today = date.today()
    test_postDate = django.utils.timezone.now()
    test_postDate = test_postDate.replace(tzinfo=timezone.utc)
    test_postTitle = 'PT_title'
    test_postText = 'PT_text'        
    test_postTitle1 = 'PT_title_1'
    test_postTitle2 = 'PT_title_2'
    test_postText1 = 'PT_text_1'
    test_postText2 = 'PT_text_2'
    test_postTags = ["qwertyuiop","zxcvbnm","this is a test", "still a test"]
    test_reasonForDeletingAccount = "somethingelse"
    test_bannedText = "fucking admins"
    test_censoredText = "****ing admins"
    test_cleanText = "fluffy little bunnies"


class SharedTestMethods(TestCase):
    """ Shared helper functions used by the classes in this file """
    def check_templates_are_included(self, response, template):
        """ Checks that the page and default templates are included
            on the tested page """
        self.assertTemplateUsed(response, template)
        self.assertTemplateUsed(response, 'tellings/base.html')
        self.assertTemplateUsed(response, 'tellings/includes/navbar.html')
        self.assertTemplateUsed(response, 'tellings/includes/footerContents.html')

    def createPostRecord(self, userID, dateOfPost, postTitle, postText):
        """ Creates a new UserPost record """
        return UserPost.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        """ Creates a new Tag record """
        return Tag.objects.create(tagName=tagName)    

    def createTagmapRecord(self, postID=1, tagID=1):
        """ Creates a new Tagmap record """
        return Tagmap.objects.create(postID=postID, tagID=tagID)

    def get_loggedin_tests(self): 
        """ Logs into an account, GETs a page, and tests that the page
            is returned correctly with its template. """
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
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

    def get_login_HTTPResponseNotAllowed_tests(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.get(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 405)

    def post_invalid_login_redirect_tests(self):
        self.client.logout()
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.loginPage_viewname))

    def post_loggedin_not_allowed_tests(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 405)

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
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))

    def post_valid_login_tests(self):
        user = User.objects.get(username=self.credentials1['username'])
        response = self.client.post(reverse(self.viewname), self.credentials1)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertRedirects(response, reverse(self.indexPage_viewname))


class AboutPageViewTests(SharedTestMethods):
    """Tests for the AboutPage view."""
   
    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:about'
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/about.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.invalid_credentials = SV.invalid_credentials
        cls.partial_credentials = SV.partial_credentials

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
        self.post_valid_login_tests()

    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class AcceptableUsagePageViewTests(SharedTestMethods):
    """Tests for the AcceptableUsagePage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:acceptableusage'
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/acceptableusage.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.invalid_credentials = SV.invalid_credentials
        cls.partial_credentials = SV.partial_credentials

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
        self.post_valid_login_tests()

    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class AccountDeletedPageTests(SharedTestMethods):
    """Tests for the AccountDeletedPage view."""

    @classmethod
    def setUpTestData(cls):      
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables  
        cls.viewname = 'tellings:accountdeleted'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/accountdeleted/'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.test_reasonForDeletingAccount = SV.test_reasonForDeletingAccount

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()    

    def test_POST_validDeleteAccount(self):
        test_deleteAccount = {
            'reason': self.test_reasonForDeletingAccount
        }

        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_deleteAccount, follow=True)
        userStillExists = User.objects.filter(username=self.credentials1['username']).exists()    

        self.assertEqual(response.status_code, 200)
        self.assertFalse(userStillExists)


class AddUserCommentViewTests(SharedTestMethods):
    """Tests for the AddUserComment view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:addusercomment'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/addusercomment/'
        
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        
        cls.credentials2 = SV.credentials2
        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

        cls.test_postDate = SV.test_postDate
        cls.test_postTitle1 = SV.test_postTitle1
        cls.test_postText1 = SV.test_postText1   
        cls.test_bannedText = SV.test_bannedText 
        
        cls.test_valid_commentData = { 'postID': 1, 'commentText': 'test comment' }      
        cls.test_banned_commentData = { 'postID': 1, 'commentText': cls.test_bannedText }        
        cls.test_invalid_commentData = { 'postID': 1, 'commentText': '' }

    def add_valid_postID_to_commentData(self, in_postTitle, commentData):
        """ Note in_postTitle is used because postTitles must be unique """
        post = self.createPostRecord(userID=self.user1.id, 
                                     dateOfPost=self.test_postDate, 
                                     postTitle=in_postTitle, 
                                     postText=self.test_postText1)   
        post = UserPost.objects.latest('postID')
        test_postID = post.postID
        commentData['postID'] = test_postID
        return commentData

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_success(self):
        self.test_valid_commentData = self.add_valid_postID_to_commentData('post success', 
                                                                           self.test_valid_commentData)
        
        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
                    
        response = self.client.post(reverse(self.viewname), 
                                    self.test_valid_commentData, follow=True)                    
                          
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "true")

    def test_POST_failure(self):
        self.test_invalid_commentData = self.add_valid_postID_to_commentData('post failure', 
                                                                             self.test_invalid_commentData)
        
        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
                    
        response = self.client.post(reverse(self.viewname), 
                                    self.test_invalid_commentData, follow=True)                    
                          
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "false")

    def test_POST_censored(self):
        self.test_banned_commentData = self.add_valid_postID_to_commentData('post censored',
                                                                            self.test_banned_commentData)
        
        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
                    
        response = self.client.post(reverse(self.viewname), 
                                    self.test_banned_commentData, follow=True)                    
                          
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "censored")


class AddNewUpdateViewTests(SharedTestMethods):
    """Tests for the AddNewUpdate view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:addnewupdate'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/addnewupdate/'
        
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        
        cls.credentials2 = SV.credentials2
        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

        cls.test_postTags_json = json.dumps(SV.test_postTags)
        cls.test_bannedText = SV.test_bannedText 

        cls.test_postData1 = { 'postTitle': SV.test_postTitle1,
                              'postText': SV.test_postText1,
                              'postTags': cls.test_postTags_json, }

        cls.test_postData2 = { 'postTitle': SV.test_postTitle2,
                              'postText': SV.test_postText2,
                              'postTags': cls.test_postTags_json, }
        
        cls.test_duplicate_title_postData = { 'postTitle': SV.test_postTitle1,
                              'postText': SV.test_postText2,
                              'postTags': cls.test_postTags_json, }
        
        cls.test_banned_postData = { 'postTitle': SV.test_postTitle1,
                              'postText': SV.test_bannedText,
                              'postTags': cls.test_postTags_json, }

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_success(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.test_postData1, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "true")

    def test_POST_censored(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.test_banned_postData, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "censored")

    def test_POST_fail_title_exists(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
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
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        self.client.post(reverse(self.viewname), 
                         self.test_postData1, follow=True)

        response = self.client.post(reverse(self.viewname), 
                         self.test_postData2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))


class AddUpdateModalTests(SharedTestMethods):
    """ Tests for the AddUpdateModal view. """

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addupdatemodal'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addupdatemodal/'
        cls.templateURL = 'tellings/includes/addUpdate_modal.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])                                           

        cls.test_postDate = SV.test_postDate
        cls.test_postTitle1 = SV.test_postTitle1
        cls.test_postText1 = SV.test_postText1                                             
        cls.test_newPostText = SV.test_postText2

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin_hasNotExceededMaxPosts(self):
        """ Tests the behaviour if the user has NOT already posted
            an update today. """
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_GET_loggedin_hasExceededMaxPosts(self):
        """ Tests the behaviour if the user has already posted
            an update today. """
        pass
"""         self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1, 
                              postText=self.test_postText1)

        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("false", content) """

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin_hasNotExceededMaxPosts(self):
        """ Tests the behaviour if the user has NOT already posted
            an update today. """
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedin_hasExceededMaxPosts(self):
        """ Tests the behaviour if the user has already posted
            an update today. """
        pass
"""         self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1, 
                              postText=self.test_postText1)

        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post((reverse(self.viewname)), follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("false", content) """


class CensorTextViewTests(SharedTestMethods):
    """Tests for the CensorText view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:censortext'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/censortext/'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.test_cleanText = SV.test_cleanText
        cls.test_bannedText = SV.test_bannedText 
        cls.test_censoredText = SV.test_censoredText 
                                             

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_textCensored(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        data_with_bannedWords = {'textToCensor': self.test_bannedText}
        response = self.client.post(reverse(self.viewname), 
                                    data_with_bannedWords, follow=True)
                                    
        content = response.content.decode("utf-8")
                                    
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.test_censoredText, content)

    def test_POST_textUncensored(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        data_without_bannedWords = {'textToCensor': self.test_cleanText}
        response = self.client.post(reverse(self.viewname), 
                                    data_without_bannedWords, follow=True)
                                    
        content = response.content.decode("utf-8")
                                    
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.test_cleanText, content)


class ChangePasswordPageTests(SharedTestMethods):
    """Tests for the ChangePassword view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:changepassword'
        cls.loggedout_redirect_URL = '/loginpage/?next=/changepassword/'
        cls.templateURL = 'tellings/changePassword.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
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


class ChangeUserDetailsPageTests(SharedTestMethods):
    """Tests for the ChangeUserDetails view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:changeuserdetails'
        cls.loggedout_redirect_URL = '/loginpage/?next=/changeuserdetails/' 
        cls.templateURL = 'tellings/changeUserDetails.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()


class CheckUserPasswordViewTests(SharedTestMethods):
    """Tests for the CheckUserPassword view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:checkuserpassword'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/checkuserpassword/'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
                                             
        cls.valid_password = {'pwd': cls.credentials1['pwd']}
        cls.invalid_password = {'pwd': cls.credentials1['username']}

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_validPassword(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.valid_password, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "true")

    def test_POST_invalidPassword(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_password, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "false")


class DeleteAccountModalTests(SharedTestMethods):
    """ Tests for the DeleteAccountModal view. """

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:deleteaccountmodal'
        cls.loggedout_redirect_URL = '/loginpage/?next=/deleteaccountmodal/'
        cls.templateURL = 'tellings/includes/deleteAccount_modal.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)


class DeleteUserCommentViewTests(SharedTestMethods):
    """Tests for the DeleteUserComment view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:deleteusercomment'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/deleteusercomment/'
        
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        
        cls.credentials2 = SV.credentials2
        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

        cls.credentials3 = SV.credentials3
        cls.user3 = User.objects.create_user(cls.credentials3['username'], 
                                             cls.credentials3['email'],
                                             cls.credentials3['pwd'])

        cls.test_postDate = SV.test_postDate
        cls.test_postTitle1 = SV.test_postTitle1
        cls.test_postText1 = SV.test_postText1      


    def createSinglePostRecord(self, in_postTitle):
        """ Note in_postTitle is used because postTitles must be unique """
        return self.createPostRecord(userID=self.user1.id, 
                                     dateOfPost=self.test_postDate, 
                                     postTitle=in_postTitle, 
                                     postText=self.test_postText1)   

    
    def createComment(self, postTitle, commentText):
        post = self.createSinglePostRecord(postTitle)
        return UserComment.objects.create(postID=post, user=self.user2, 
                     dateOfComment=self.test_postDate, commentText=commentText)    

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_validDelete_commenter(self):
        """ Tests that the user who made the comment can delete it
        """
        self.createComment('valid delete comment', 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID
        test_validDelete = {
            'commentID': test_commentID,
        }

        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        content = response.content.decode("utf-8")
        commentStillExists = UserComment.objects.filter(pk=test_commentID).exists()

        self.assertEqual(response.status_code, 200)
        self.assertIn("true", content)
        self.assertFalse(commentStillExists)


    def test_POST_validDelete_poster(self):
        """ Tests that the user who made the post being commented
            upon can delete comments attached to it.
        """
        self.createComment('valid delete post', 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID
        test_validDelete = {
            'commentID': test_commentID,
        }

        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        content = response.content.decode("utf-8")
        commentStillExists = UserComment.objects.filter(pk=test_commentID).exists()

        self.assertEqual(response.status_code, 200)
        self.assertIn("true", content)
        self.assertFalse(commentStillExists)


    def test_POST_invalidDelete_data(self):
        """ Tests trying to delete a non-existing comment.
        """
        test_invalidDelete = {
            'commentID': 999,
        }

        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidDelete, follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("YOU CANNOT DELETE", content)


    def test_POST_invalidDelete_user(self):
        """ Tests that a comment cannot be deleted by a user who did
            not post it or the post that was commented upon .
        """
        self.createComment('valid delete post', 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID
        test_validDelete = {
            'commentID': test_commentID,
        }

        self.client.login(username=self.credentials3['username'], 
                          password=self.credentials3['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        content = response.content.decode("utf-8")
        commentStillExists = UserComment.objects.filter(pk=test_commentID).exists()

        self.assertEqual(response.status_code, 200)
        self.assertIn("YOU CANNOT DELETE", content)
        self.assertTrue(commentStillExists)


class DeleteUserPostViewTests(SharedTestMethods):
    """Tests for the DeleteUserPost view."""

    @classmethod
    def setUpTestData(cls):      
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables  
        cls.viewname = 'tellings:deleteuserpost'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/deleteuserpost/'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

        cls.credentials2 = SV.credentials2
        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])
        
        cls.test_postDate = SV.test_postDate
        cls.test_postTitle1 = SV.test_postTitle1
        cls.test_postText1 = SV.test_postText1
                                
    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_validDelete(self):
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1, 
                              postText=self.test_postText1)
        post = UserPost.objects.latest('postID')
        test_postID = post.postID
        test_validDelete = {
            'postID': test_postID,
        }

        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        content = response.content.decode("utf-8")
        postStillExists = UserPost.objects.filter(pk=test_postID).exists()

        self.assertEqual(response.status_code, 200)
        self.assertIn("true", content)
        self.assertFalse(postStillExists)

    def test_POST_invalidDelete(self):
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1, 
                              postText=self.test_postText1)
        post = UserPost.objects.latest('postID')
        test_postID = post.postID
        test_invalidDelete = {
            'postID': test_postID,
        }

        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidDelete, follow=True)
        content = response.content.decode("utf-8")
        postStillExists = UserPost.objects.filter(pk=test_postID).exists()

        self.assertEqual(response.status_code, 200)
        self.assertIn("YOU CANNOT DELETE", content)
        self.assertTrue(postStillExists)


class EditUserCommentViewTests(SharedTestMethods):
    """Tests for the EditUserComment view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:editusercomment'
        cls.templateURL = 'tellings/includes/editComment.html'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/editusercomment/'
        
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        
        cls.credentials2 = SV.credentials2
        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])

        cls.test_postDate = SV.test_postDate
        cls.test_postTitle1 = SV.test_postTitle1
        cls.test_postText1 = SV.test_postText1 
        cls.test_bannedText = SV.test_bannedText  
        
        cls.test_newCommentText = 'Edited comment'   


    def createSinglePostRecord(self, in_postTitle):
        """ Note in_postTitle is used because postTitles must be unique """
        return self.createPostRecord(userID=self.user1.id, 
                                     dateOfPost=self.test_postDate, 
                                     postTitle=in_postTitle, 
                                     postText=self.test_postText1)   

    
    def createComment(self, postTitle, commentText):
        post = self.createSinglePostRecord(postTitle)
        return UserComment.objects.create(postID=post, user=self.user2, 
                     dateOfComment=self.test_postDate, commentText=commentText)   

    def getTestURL(self, commentText): 
        self.createComment(commentText, 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID   
        return reverse(self.viewname) + str(test_commentID)  

    def test_GET_loggedout(self):
        url = self.getTestURL('get_loggedOut')
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        url = self.getTestURL('get_loggedIn')
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests() 

    def test_POST_validEdit(self):
        self.createComment('post_validEdit', 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID  

        test_validEdit = {
            'commentID': test_commentID,
            'commentText': self.test_newCommentText
        }

        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)
        content = response.content.decode("utf-8")

        editedComment = UserComment.objects.get(pk=test_commentID)
        editedField = editedComment.commentText
        self.assertEqual(response.status_code, 200)
        self.assertIn("true", content)
        self.assertEqual(self.test_newCommentText, editedField)

    def test_POST_censored(self):
        self.createComment('post_validEdit', 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID  

        test_validEdit = {
            'commentID': test_commentID,
            'commentText': self.test_bannedText
        }

        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)
        content = response.content.decode("utf-8")

        editedComment = UserComment.objects.get(pk=test_commentID)
        editedField = editedComment.commentText
        self.assertEqual(response.status_code, 200)
        self.assertIn("censored", content)
        self.assertNotEqual(self.test_newCommentText, editedField)

    def test_POST_invalidEdit_user(self):
        """ Tests that a user cannot edit another user's comments.
        """
        self.createComment('post_invalidEdit_user', 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID  

        test_validEdit = {
            'commentID': test_commentID,
            'commentText': self.test_newCommentText
        }

        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)
        content = response.content.decode("utf-8")

        editedComment = UserComment.objects.get(pk=test_commentID)
        editedField = editedComment.commentText

        self.assertEqual(response.status_code, 200)
        self.assertIn("YOU CANNOT EDIT", content)
        self.assertNotEqual(self.test_newCommentText, editedField)


class EditUserPostViewTests(SharedTestMethods):
    """Tests for the EditUserPost view."""

    @classmethod
    def setUpTestData(cls):      
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables  
        cls.viewname = 'tellings:edituserpost'
        cls.testGETURL = '/edituserpost/1'
        cls.templateURL = 'tellings/includes/editPost.html'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/edituserpost/'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

        cls.credentials2 = SV.credentials2
        cls.user2 = User.objects.create_user(cls.credentials2['username'], 
                                             cls.credentials2['email'],
                                             cls.credentials2['pwd'])                                             

        cls.test_postDate = SV.test_postDate
        cls.test_postTitle1 = SV.test_postTitle1
        cls.test_postText1 = SV.test_postText1                                             
        cls.test_newPostText = SV.test_postText2
        cls.test_bannedText = SV.test_bannedText

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1, 
                              postText=self.test_postText1)
        response = self.client.get(self.testGETURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()
 
    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()       

    def test_POST_validEdit(self):
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1, 
                              postText=self.test_postText1)
        post = UserPost.objects.latest('postID')
        test_postID = post.postID
        test_validEdit = {
            'postID': test_postID,
            'postText': self.test_newPostText
        }
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])

        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)
        content = response.content.decode("utf-8")

        editedPost = UserPost.objects.get(pk=test_postID)
        editedField = editedPost.postText
        self.assertEqual(response.status_code, 200)
        self.assertIn("true", content)
        self.assertEqual(self.test_newPostText, editedField)   

    def test_POST_censored(self):
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1, 
                              postText=self.test_postText1)
        post = UserPost.objects.latest('postID')
        test_postID = post.postID
        test_validEdit = {
            'postID': test_postID,
            'postText': self.test_bannedText
        }
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])

        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)
        content = response.content.decode("utf-8")

        editedPost = UserPost.objects.get(pk=test_postID)
        editedField = editedPost.postText
        self.assertEqual(response.status_code, 200)
        self.assertIn("censored", content)
        self.assertNotEqual(self.test_bannedText, editedField)

    def test_POST_invalidEdit(self):
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle1,
                              postText=self.test_postText1)
        post = UserPost.objects.latest('postID')
        test_postID = post.postID
        test_invalidEdit = {
            'postID': test_postID,
            'postText': self.test_newPostText
        }

        self.client.login(username=self.credentials2['username'], 
                          password=self.credentials2['pwd'])
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidEdit, follow=True)
        content = response.content.decode("utf-8")

        editedPost = UserPost.objects.get(pk=test_postID)
        editedField = editedPost.postText

        self.assertEqual(response.status_code, 200)
        self.assertIn("YOU CANNOT EDIT", content)
        self.assertNotEqual(self.test_newPostText, editedField)


class ErrorPageViewTests(SharedTestMethods):
    """Tests for the ErrorPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:errorpage'
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/errorPage.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.invalid_credentials = SV.invalid_credentials
        cls.partial_credentials = SV.partial_credentials

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
        self.post_valid_login_tests()

    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class HasExceededMaxPostsTests(SharedTestMethods):
    """Tests for the HasExceededMaxPosts view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:hasexceededmaxposts'
        cls.loggedout_redirect_URL = '/loginpage/?next=/hasexceededmaxposts/'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        
        cls.test_postDate = SV.test_postDate
        cls.test_postTitle = SV.test_postTitle
        cls.test_postText = SV.test_postText

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_has_not_posted(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "false")

    def test_GET_has_posted(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        self.createPostRecord(self.user1.id, 
                              self.test_postDate, 
                              self.test_postTitle, 
                              self.test_postText)
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "true")

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        self.createPostRecord(self.user1.id, 
                              self.test_postDate, 
                              self.test_postTitle, 
                              self.test_postText)
        response = self.client.post((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "true")


class IndexPageViewTests(SharedTestMethods):
    """Tests for the IndexPage view."""

    @classmethod
    def setUpTestData(cls):
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:index'
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/index.html'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.invalid_credentials = SV.invalid_credentials
        cls.partial_credentials = SV.partial_credentials

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
        self.post_valid_login_tests()
        
    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class LoginModalTests(SharedTestMethods):
    """ Tests for the LoginModal view. """

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:loginmodal'
        cls.templateURL = 'tellings/includes/login_modal.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

    def test_GET_loggedout(self):
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_GET_loggedin(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedin(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.post(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)


class LoginPageTests(SharedTestMethods):
    """Tests for the Loginpage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:loginpage'
        cls.templateURL = 'tellings/loginpage.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])   
        cls.login_credentials = {
            'username': 'testuser1',
            'password': '@myp455w0rd'}   

        cls.invalid_credentials = SV.invalid_credentials    

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
        response = self.client.post(reverse(self.viewname), self.invalid_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)


class MissionStatementPageViewTests(SharedTestMethods):
    """Tests for the MissionStatementPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:missionstatement'
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/missionstatement.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.invalid_credentials = SV.invalid_credentials
        cls.partial_credentials = SV.partial_credentials

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
        self.post_valid_login_tests()

    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class MyUpdatesListViewTests(SharedTestMethods):
    """Tests for the MyUpdatesList view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:myupdates'
        cls.loggedout_redirect_URL = '/loginpage/?next=/myupdates/'
        cls.templateURL = 'tellings/myupdates_list.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.post_loggedin_not_allowed_tests()


class NewUpdatesListViewTests(SharedTestMethods):
    """Tests for the NewUpdatesListView view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:newupdates'
        cls.loggedout_redirect_URL = '/loginpage/?next=/newupdates/'
        cls.templateURL = 'tellings/newupdates_list.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.post_loggedin_not_allowed_tests()


class PrivacyPolicyPageViewTests(SharedTestMethods):
    """Tests for the PrivacyPolicyPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:privacypolicy'
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/privacypolicy.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.invalid_credentials = SV.invalid_credentials
        cls.partial_credentials = SV.partial_credentials

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
        self.post_valid_login_tests()

    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class SignUpPageTests(SharedTestMethods):
    """Tests for the SignUpPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:signup'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/signup.html'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

        cls.invalid_credentials = SV.invalid_credentials
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
        self.assertEqual(response.status_code, 200)

    def test_POST_invalid(self):
        response = self.client.post(reverse(self.viewname), self.registration_data_invalid)
        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)
        
    def test_POST_valid_login(self):
        self.post_valid_login_tests()
        
    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()
        

class TagListViewTests(SharedTestMethods):
    """Tests for the TagListView view."""

    @classmethod
    def setUpTestData(cls):
        cls.viewname = 'tellings:tags'
        cls.loggedout_redirect_URL = '/loginpage/?next=/tags/'
        cls.templateURL = 'tellings/tag_list.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

    def setUp(self):
        pass

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.post_loggedin_not_allowed_tests()


class TermsAndConditionsPage(SharedTestMethods):
    """Tests for the TermsAndConditionsPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:termsandconditions'
        cls.indexPage_viewname = SV.indexPage_viewname
        cls.loginPage_viewname = SV.loginPage_viewname
        cls.templateURL = 'tellings/termsandconditions.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])
        cls.invalid_credentials = SV.invalid_credentials
        cls.partial_credentials = SV.partial_credentials

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
        self.post_valid_login_tests()

    def test_POST_invalid_login(self):
        self.post_invalid_login_redirect_tests()


class TitleExistsViewTests(SharedTestMethods):
    """Tests for the TitleExists view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        SV = SharedVariables
        cls.viewname = 'tellings:titleexists'
        cls.errorPage_viewname = SV.errorPage_viewname
        cls.loggedout_redirect_URL = '/loginpage/?next=/titleexists/'

        cls.credentials1 = SV.credentials1
        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

        cls.test_postDate = SV.test_postDate
        cls.test_postTitle = SV.test_postTitle
        cls.test_postText = SV.test_postText

        cls.test_notexists = { 'title': 'Not exists'}
        cls.test_exists = { 'title': cls.test_postTitle }

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_login_HTTPResponseNotAllowed_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.post_no_data_redirect_to_errorpage_tests()

    def test_POST_title_not_exists(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle, 
                              postText=self.test_postText)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_notexists, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "false")

    def test_POST_title_exists(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        self.createPostRecord(userID=self.user1.id, 
                              dateOfPost=self.test_postDate, 
                              postTitle=self.test_postTitle, 
                              postText=self.test_postText)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_exists, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "true")


class UserCommentListViewTests(SharedTestMethods):
    """Tests for the UserCommentList view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:usercomments'
        cls.loggedout_redirect_URL = '/loginpage/?next=/usercomments/'
        cls.templateURL = 'tellings/usercomment_list.html'

        SV = SharedVariables
        cls.credentials1 = SV.credentials1

        cls.user1 = User.objects.create_user(cls.credentials1['username'], 
                                             cls.credentials1['email'],
                                             cls.credentials1['pwd'])

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.client.login(username=self.credentials1['username'], 
                          password=self.credentials1['pwd'])
        response = self.client.get((reverse(self.viewname)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):
        self.post_loggedin_not_allowed_tests()
