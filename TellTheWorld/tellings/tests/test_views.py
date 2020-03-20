"""
# Filename:     test_views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 20/03/2020
# Description:  Test cases for tellings views
"""

import django
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timezone, timedelta

from tellings.models import *
from tellings.views import maxPostsPerDay, adminNameList, StatusCode
from tellings.views import contains_banned_word, has_exceeded_max_posts
import enum, json


class SharedTestMethods(TestCase):
    """ Common functions used by the classes in this file """

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

    test_reasonForDeletingAccount = "somethingelse"
    test_bannedText = "fucking admins"
    test_censoredText = "****ing admins"
    test_cleanText = "fluffy little bunnies"

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

    common_templates = ['tellings/base.html',
                        'tellings/includes/navbar.html',
                        'tellings/includes/footerContents.html']

    def user_login(self, credentials):
        self.client.login(username=credentials['username'], 
                          password=credentials['pwd'])

    def check_templates_are_included(self, response, template):
        """ Checks that the page and default templates are included in the response """
        self.assertTemplateUsed(response, template)

        for ct in self.common_templates:
            self.assertTemplateUsed(response, ct)

    def createPostRecord(self, userID, dateOfPost, postTitle, postText):
        """ Creates a new UserPost record. """
        return UserPost.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        """ Creates a new Tag record """
        return Tag.objects.create(tagName=tagName)     

    def createTagmapRecord(self, in_post, in_tag):
        """ Creates a new Tagmap record """
        return Tagmap.objects.create(postID=in_post, tagID=in_tag)

    def createUserRecord(self, credentials):
        """ Creates a new User record """
        return User.objects.create_user(credentials['username'], 
                                        credentials['email'],
                                        credentials['pwd'])

    def create_n_UserPosts(self, n, userList):
        """ Creates n UserPost objects for each user in the user list supplied. """
        tag = self.createTagRecord(self.test_postTags[0])
        posts = []

        for user in userList:
            for i in range(0, n):
                post = self.createPostRecord(userID=user.id, 
                                             dateOfPost=self.test_postDate, 
                                             postTitle=(self.test_postTitle1 + str(i) ), 
                                             postText=self.test_postText1) 
                posts.append(post)
                tagmap = self.createTagmapRecord(post, tag) 

                post.save()
                tagmap.save()

        return posts

    def create_UserPost_for_yesterday(self):
        """ Creates and returns a UserPost object for yesterday. """
        yesterday = django.utils.timezone.now() + timedelta(days=-1)  
        yesterday = yesterday.replace(tzinfo=timezone.utc)

        tag = self.createTagRecord(self.test_postTags[1])
        post = self.createPostRecord(userID=self.user1.id, 
                                     dateOfPost=yesterday, 
                                     postTitle=(self.test_postTitle1 + "yesterday" ), 
                                     postText=self.test_postText1) 
        tagmap = self.createTagmapRecord(post, tag)

        post.save()
        tagmap.save()

        return post

    def http_method_not_allowed_tests(self, http_method):  
        response = http_method(reverse(self.viewname), follow=True)
        self.assertEqual(response.status_code, 405)

    def get_loggedin_tests(self): 
        """ Logs into an account, GETs a page, and tests that the page
            is returned correctly with its template. """
        self.user_login(self.credentials1)
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

    def post_invalid_login_redirect_tests(self):
        self.client.logout()
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_credentials, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.loginPage_viewname))

    def post_loggedout_redirect_tests(self):
        """ Sends a POST request for a page and ensures that it
            receives a redirect instead """
        response = self.client.post(reverse(self.viewname), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.loggedout_redirect_URL)

    def post_missing_data_tests(self):
        response = self.client.post(reverse(self.viewname), 
                                    self.partial_credentials, follow=True)

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

    def post_redirects_to_errorpage_tests(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.errorPage_viewname))

    def post_valid_login_tests(self):
        user = User.objects.get(username=self.credentials1['username'])
        response = self.client.post(reverse(self.viewname), self.credentials1)

        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertRedirects(response, reverse(self.indexPage_viewname))

    def response_contains_status_code(self, response, status_code):
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content["status"], status_code)


class AboutPageViewTests(SharedTestMethods):
    """Tests for the AboutPage view."""
   
    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:about'
        cls.templateURL = 'tellings/about.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_GET_loggedout(self):
        self.get_loggedout_tests()

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
        cls.viewname = 'tellings:acceptableusage'
        cls.templateURL = 'tellings/acceptableusage.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

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
        cls.viewname = 'tellings:accountdeleted'
        cls.loggedout_redirect_URL = '/loginpage/?next=/accountdeleted/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

        max_reason_len = DeletedAccount._meta.get_field('deleted_reason').max_length
        cls.test_invalidReason = "@" * (max_reason_len + 10)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)        
        self.post_redirects_to_errorpage_tests(response)    

    def test_POST_validDeleteAccount(self):
        test_deleteAccount = {
            'reason': self.test_reasonForDeletingAccount
        }

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_deleteAccount, follow=True)
        userStillExists = User.objects.filter(username=self.credentials1['username']).exists()    

        self.assertEqual(response.status_code, 200)
        self.assertFalse(userStillExists)

    def test_POST_invalidDeleteAccount(self):
        test_deleteAccount = {
            'reason': self.test_invalidReason
        }
        self.user_login(self.credentials2)

        response = self.client.post(reverse(self.viewname), 
                                    test_deleteAccount, follow=True)
        userStillExists = User.objects.filter(username=self.credentials2['username']).exists()    

        self.post_redirects_to_errorpage_tests(response)
        self.assertTrue(userStillExists)


class AddUserCommentViewTests(SharedTestMethods):
    """Tests for the AddUserComment view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addusercomment'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addusercomment/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)
        
        cls.test_valid_commentData = { 'postID': 1, 'commentText': 'test comment' }      
        cls.test_banned_commentData = { 'postID': 1, 'commentText': cls.test_bannedText }        
        cls.test_invalid_commentData1 = { 'postID': 1, 'commentText': '' }      
        cls.test_invalid_commentData2 = { 'postID': 1999, 'commentText': '' }

    def add_valid_postID_to_commentData(self, commentData):
        posts = self.create_n_UserPosts(1, [self.user1])
        test_postID = posts[0].postID
        commentData['postID'] = test_postID
        return commentData

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials2)       
        response = self.client.post(reverse(self.viewname), follow=True)    

        self.response_contains_status_code(response, StatusCode.ERROR.value) 

    def test_POST_success(self):
        self.test_valid_commentData = self.add_valid_postID_to_commentData(self.test_valid_commentData)
        
        self.user_login(self.credentials2)                    
        response = self.client.post(reverse(self.viewname), 
                                    self.test_valid_commentData, follow=True)                    
                          
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_failure(self):
        self.test_invalid_commentData1 = self.add_valid_postID_to_commentData(self.test_invalid_commentData1)
        
        self.user_login(self.credentials2)           
        response = self.client.post(reverse(self.viewname), 
                                    self.test_invalid_commentData1, follow=True)                    
                          
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_invalid_postID(self):
        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_invalid_commentData2, follow=True)                    
                          
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_censored(self):
        self.test_banned_commentData = self.add_valid_postID_to_commentData(self.test_banned_commentData)   
        self.user_login(self.credentials2)

        response = self.client.post(reverse(self.viewname), 
                                    self.test_banned_commentData, follow=True)                    
                          
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.CENSORED.value)


class AddNewUpdateViewTests(SharedTestMethods):
    """Tests for the AddNewUpdate view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addnewupdate'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addnewupdate/'
        
        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

        cls.test_postTags_json = json.dumps(cls.test_postTags)

        cls.test_postData1 = { 'postTitle': cls.test_postTitle1,
                              'postText': cls.test_postText1,
                              'postTags': cls.test_postTags_json, }

        cls.test_postData2 = { 'postTitle': cls.test_postTitle2,
                              'postText': cls.test_postText2,
                              'postTags': cls.test_postTags_json, }

        max_postTitle_len = UserPost._meta.get_field('postTitle').max_length
        invalid_postTitle = "@" * (max_postTitle_len + 10)
        
        cls.test_invalid_postData = { 'postTitle': invalid_postTitle,
                              'postText': cls.test_postText2,
                              'postTags': cls.test_postTags_json, }

        cls.test_duplicate_title_postData = { 'postTitle': cls.test_postTitle1,
                              'postText': cls.test_postText2,
                              'postTags': cls.test_postTags_json, }
        
        cls.test_banned_postData = { 'postTitle': cls.test_postTitle1,
                              'postText': cls.test_bannedText,
                              'postTags': cls.test_postTags_json, }

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)    

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_success(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_postData1, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_exceed_MaxPosts(self):
        self.user_login(self.credentials1)
        self.create_n_UserPosts(maxPostsPerDay, [self.user1])

        response = self.client.post(reverse(self.viewname), 
                                    self.test_postData1, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_invalidData(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_invalid_postData, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_censored(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.test_banned_postData, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.CENSORED.value)


class AddUpdateModalTests(SharedTestMethods):
    """ Tests for the AddUpdateModal view. """

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:addupdatemodal'
        cls.loggedout_redirect_URL = '/loginpage/?next=/addupdatemodal/'
        cls.templateURL = 'tellings/includes/addUpdate_modal.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)                                      

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin_hasNotExceededMaxPosts(self):
        """ Tests the behaviour if the user has NOT already posted
            an update today. """
        self.user_login(self.credentials1)
        response = self.client.get((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_GET_exceed_MaxPosts(self):
        self.user_login(self.credentials1)
        self.create_n_UserPosts(maxPostsPerDay, [self.user1])

        response = self.client.get(reverse(self.viewname),  follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn(content, 'false')


class BlockedUserListViewTests(SharedTestMethods):
    """Tests for the BlockedUserListView."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:blockedusers'
        cls.loggedout_redirect_URL = '/loginpage/?next=/blockedusers/'
        cls.templateURL = "tellings/blockeduser_list.html"

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.user_login(self.credentials1)
        blocked = BlockedUser.objects.create(blockedUser=self.user2, blockedBy=self.user1)
        blocked_username = self.user2.username
        blocked.save()

        response = self.client.get((reverse(self.viewname)), follow=True)
        content = response.content.decode("utf-8")

        self.assertIn(blocked_username, content, msg="Blocked user '%s' not found." % blocked_username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()


class BlockUserTests(SharedTestMethods):
    """Tests for the BlockUser view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:blockuser'
        cls.loggedout_redirect_URL = '/loginpage/?next=/blockuser/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)                             
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)
        
        cls.valid_data = {
            'username': cls.credentials2['username']
        }        
        cls.invalid_data1 = {
            'username': "nonexistantuser"
        }       
        cls.invalid_data2 = {
            'username': cls.credentials1['username']
        }       
        cls.invalid_data3 = {
            'username': adminNameList[0] 
        }

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)
        
    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)   

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validData(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.valid_data, follow=True)
        isblocked = BlockedUser.objects.filter(blockedUser=self.user2, blockedBy=self.user1).exists()

        self.assertTrue(isblocked)
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_invalidData(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_invalidData(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_data1, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_cannot_block_self(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_data2, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_cannot_block_admin(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_data3, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class CensorTextViewTests(SharedTestMethods):
    """Tests for the CensorText view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """

        cls.viewname = 'tellings:censortext'
        cls.loggedout_redirect_URL = '/loginpage/?next=/censortext/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
                                             
    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)  

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_textCensored(self):
        data_with_bannedWords = {'textToCensor': self.test_bannedText}
        self.user_login(self.credentials1)

        response = self.client.post(reverse(self.viewname), 
                                    data_with_bannedWords, follow=True)
        content = response.content.decode("utf-8")
                                    
        self.assertEqual(response.status_code, 200)      
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)


class ChangePasswordPageTests(SharedTestMethods):
    """Tests for the ChangePassword view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:changepassword'
        cls.loggedout_redirect_URL = '/loginpage/?next=/changepassword/'
        cls.templateURL = 'tellings/changePassword.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

        cls.valid_data = {
            'old_password': cls.credentials1['pwd'],
            'new_password1': 'ch@n63d70n3w',
            'new_password2': 'ch@n63d70n3w'
        }
        cls.invalid_data = {
            'old_password': '@mywr0n6p455w0rd',
            'new_password1': 'ch@n63d70n3w',
            'new_password2': 'ch@n63d70n3w'
        }

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)       
        response = self.client.post(reverse(self.viewname), follow=True)   

        self.post_redirects_to_errorpage_tests(response)

    def test_POST_validData(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.valid_data, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_POST_invalidOldPassword(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_data, follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Old password error", content, msg="Invalid old_password error not found.")


class ChangeUserDetailsPageTests(SharedTestMethods):
    """Tests for the ChangeUserDetails view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:changeuserdetails'
        cls.loggedout_redirect_URL = '/loginpage/?next=/changeuserdetails/' 
        cls.templateURL = 'tellings/changeUserDetails.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

        cls.valid_data = {
            'first_name': 'Robert', 
            'last_name': 'Robot', 
            'email': 'r_robot@bot.com'
        }
        cls.success_message = 'Your details have been updated'

        cls.invalid_data = {
            'first_name': 'Robert', 
            'last_name': 'Robot', 
            'email': 'notavalidemail'
        }
        cls.fail_message = 'Email error: Enter a valid email address'


    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)       
        response = self.client.post(reverse(self.viewname), follow=True)   

        self.post_redirects_to_errorpage_tests(response)

    def test_POST_validData(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.valid_data, follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.success_message, content, msg="Details updated message not found.")

    def test_POST_invalidData(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_data, follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.fail_message, content, msg="Invalid details message not found.")


class CheckUserPasswordViewTests(SharedTestMethods):
    """Tests for the CheckUserPassword view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:checkuserpassword'
        cls.loggedout_redirect_URL = '/loginpage/?next=/checkuserpassword/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
                                             
        cls.valid_password = {'pwd': cls.credentials1['pwd']}
        cls.invalid_password = {'pwd': cls.credentials1['username']}

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)      
        response = self.client.post(reverse(self.viewname), follow=True)  

        self.response_contains_status_code(response, StatusCode.ERROR.value) 

    def test_POST_validPassword(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.valid_password, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_invalidPassword(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    self.invalid_password, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.INVALIDPASSWORD.value)


class DeleteAccountModalTests(SharedTestMethods):
    """ Tests for the DeleteAccountModal view. """

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:deleteaccountmodal'
        cls.loggedout_redirect_URL = '/loginpage/?next=/deleteaccountmodal/'
        cls.templateURL = 'tellings/includes/deleteAccount_modal.html'
        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.user_login(self.credentials1)
        response = self.client.get((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)


class DeleteUserCommentViewTests(SharedTestMethods):
    """Tests for the DeleteUserComment view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:deleteusercomment'
        cls.loggedout_redirect_URL = '/loginpage/?next=/deleteusercomment/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)
        cls.user3 = cls.createUserRecord(cls, cls.credentials3)
     
    def createComment(self, postTitle, commentText):
        posts = self.create_n_UserPosts(1, [self.user1])
        return UserComment.objects.create(postID=posts[0], user=self.user2, 
                     dateOfComment=self.test_postDate, commentText=commentText)    

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)   

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validDelete_comment(self):
        """ Tests that the user who made the comment can delete it
        """
        self.createComment('valid delete comment', 'test comment')
        comment = UserComment.objects.latest('commentID')
        test_commentID = comment.commentID
        test_validDelete = {
            'commentID': test_commentID,
        }

        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        commentStillExists = UserComment.objects.filter(pk=test_commentID).exists()

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)
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

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        commentStillExists = UserComment.objects.filter(pk=test_commentID).exists()

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)
        self.assertFalse(commentStillExists)


    def test_POST_invalidDelete_data(self):
        """ Tests trying to delete a non-existing comment.
        """
        test_invalidDelete = {
            'commentID': 999,
        }

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidDelete, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


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

        self.user_login(self.credentials3)
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        commentStillExists = UserComment.objects.filter(pk=test_commentID).exists()

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)
        self.assertTrue(commentStillExists)


class DeleteUserPostViewTests(SharedTestMethods):
    """Tests for the DeleteUserPost view."""

    @classmethod
    def setUpTestData(cls):      
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:deleteuserpost'
        cls.loggedout_redirect_URL = '/loginpage/?next=/deleteuserpost/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)
                                
    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)  

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validDelete(self):
        posts = self.create_n_UserPosts(1, [self.user1])
        test_postID = posts[0].postID
        test_validDelete = {
            'postID': test_postID,
        }

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_validDelete, follow=True)
        postStillExists = UserPost.objects.filter(pk=test_postID).exists()

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)
        self.assertFalse(postStillExists)

    def test_POST_invalidUser(self):
        posts = self.create_n_UserPosts(1, [self.user1])
        test_postID = posts[0].postID
        test_invalidDelete = {
            'postID': test_postID,
        }

        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidDelete, follow=True)
        postStillExists = UserPost.objects.filter(pk=test_postID).exists()

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)
        self.assertTrue(postStillExists)

    def test_POST_invalidPostID(self):
        test_invalidDelete = {
            'postID': 99999,
        }

        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidDelete, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class EditUserCommentViewTests(SharedTestMethods):
    """Tests for the EditUserComment view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:editusercomment'
        cls.templateURL = 'tellings/includes/editComment.html'
        cls.loggedout_redirect_URL = '/loginpage/?next=/editusercomment/'
        
        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

        cls.test_newCommentText = 'Edited comment'   

    def createComment(self, commentText):
        posts = self.create_n_UserPosts(1, [self.user1])
        return UserComment.objects.create(postID=posts[0], user=self.user2, 
                     dateOfComment=self.test_postDate, commentText=commentText)   

    def getTestURL(self, commentText): 
        comment = self.createComment(commentText)
        test_commentID = comment.commentID   
        return reverse(self.viewname) + str(test_commentID)  

    def test_GET_loggedout(self):
        url = self.getTestURL('get_loggedOut')
        response = self.client.get((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        url = self.getTestURL('get_loggedIn')
        self.user_login(self.credentials1)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)     

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validEdit(self):
        comment = self.createComment('test comment')
        test_commentID = comment.commentID  

        test_validEdit = {
            'commentID': test_commentID,
            'commentText': self.test_newCommentText
        }

        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)

        editedComment = UserComment.objects.get(pk=test_commentID)
        editedField = editedComment.commentText

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)
        self.assertEqual(self.test_newCommentText, editedField)

    def test_POST_censored(self):
        comment = self.createComment('test comment')
        test_commentID = comment.commentID  

        test_validEdit = {
            'commentID': test_commentID,
            'commentText': self.test_bannedText
        }

        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)

        editedComment = UserComment.objects.get(pk=test_commentID)
        editedField = editedComment.commentText

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.CENSORED.value)
        self.assertNotEqual(self.test_newCommentText, editedField)

    def test_POST_invalidUser(self):
        """ Tests that a user cannot edit another user's comments.
        """
        comment = self.createComment('test comment')
        test_commentID = comment.commentID  

        test_invalidEdit = {
            'commentID': test_commentID,
            'commentText': self.test_newCommentText
        }

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidEdit, follow=True)

        editedComment = UserComment.objects.get(pk=test_commentID)
        editedField = editedComment.commentText

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)
        self.assertNotEqual(self.test_newCommentText, editedField)

    def test_POST_invalidCommentID(self):
        test_commentID = 9999

        test_invalidEdit = {
            'commentID': test_commentID,
            'commentText': self.test_newCommentText
        }

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidEdit, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class EditUserPostViewTests(SharedTestMethods):
    """Tests for the EditUserPost view."""

    @classmethod
    def setUpTestData(cls):      
        """ Creates the test data used by the methods within this class. """ 
        cls.viewname = 'tellings:edituserpost'
        cls.testGETURL = '/edituserpost/1'
        cls.templateURL = 'tellings/includes/editPost.html'
        cls.loggedout_redirect_URL = '/loginpage/?next=/edituserpost/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)                                          
                                          
        cls.test_newPostText = cls.test_postText2

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.user_login(self.credentials1)
        self.create_n_UserPosts(1, [self.user1])
        response = self.client.get(self.testGETURL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()
 
    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)    

        self.response_contains_status_code(response, StatusCode.ERROR.value)    

    def test_POST_validEdit(self):
        posts = self.create_n_UserPosts(1, [self.user1])
        test_postID = posts[0].postID
        test_validEdit = {
            'postID': test_postID,
            'postText': self.test_newPostText
        }
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)
        editedPost = UserPost.objects.get(pk=test_postID)
        editedField = editedPost.postText

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value) 
        self.assertEqual(self.test_newPostText, editedField)   

    def test_POST_censored(self):
        posts = self.create_n_UserPosts(1, [self.user1])
        test_postID = posts[0].postID
        test_validEdit = {
            'postID': test_postID,
            'postText': self.test_bannedText
        }
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    test_validEdit, follow=True)
        editedPost = UserPost.objects.get(pk=test_postID)
        editedField = editedPost.postText

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.CENSORED.value) 
        self.assertNotEqual(self.test_bannedText, editedField)

    def test_POST_invalidUser(self):
        posts = self.create_n_UserPosts(1, [self.user1])
        test_postID = posts[0].postID
        test_invalidEdit = {
            'postID': test_postID,
            'postText': self.test_newPostText
        }

        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidEdit, follow=True)
        editedPost = UserPost.objects.get(pk=test_postID)
        editedField = editedPost.postText

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value) 
        self.assertNotEqual(self.test_newPostText, editedField)

    def test_POST_invalidPostID(self):
        test_postID = 9999
        test_invalidEdit = {
            'postID': test_postID,
            'postText': self.test_newPostText
        }
        self.user_login(self.credentials2)
        response = self.client.post(reverse(self.viewname), 
                                    test_invalidEdit, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value) 


class ErrorPageViewTests(SharedTestMethods):
    """Tests for the ErrorPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:errorpage'
        cls.templateURL = 'tellings/errorPage.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

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

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_has_not_exceeded_maxposts(self):
        self.user_login(self.credentials1)
        response = self.client.get((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_GET_exceed_MaxPosts(self):
        self.user_login(self.credentials1)
        self.create_n_UserPosts(maxPostsPerDay, [self.user1])
        response = self.client.get(reverse(self.viewname),  follow=True)
        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class HiddenPostListViewTests(SharedTestMethods):
    """Tests for the HiddenPostListView view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:hiddenposts'
        cls.loggedout_redirect_URL = '/loginpage/?next=/hiddenposts/'
        cls.templateURL = "tellings/hiddenpost_list.html"

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

        cls.no_results_msg = "You have not hidden any posts"

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_POST_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.post)

    def test_GET_no_hiddenPosts(self):
        self.user_login(self.credentials1)
        self.create_n_UserPosts(2, [self.user2])
        response = self.client.get((reverse(self.viewname)), follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)        
        self.assertIn(self.no_results_msg, content, msg="Message '%s' not found in response." % self.no_results_msg)

    def test_GET_with_hiddenPosts(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(3, [self.user2])
        toHide = posts[0]
        hiddenPost = HiddenPost.objects.create(postID=toHide, hideFrom=self.user1)
        hiddenPost.save()
        hiddenPostTitle = toHide.postTitle

        response = self.client.get((reverse(self.viewname)), follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)        
        self.assertIn(hiddenPostTitle, content, msg="Post title '%s' not found in response." % hiddenPostTitle)

    def test_GET_invalid_username(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(3, [self.user2])
        toHide = posts[0]
        hiddenPost = HiddenPost.objects.create(postID=toHide, hideFrom=self.user1)
        hiddenPost.save()
        hiddenPostTitle = toHide.postTitle
        viewname = reverse(self.viewname) + "?username=nonexistantuser"

        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)        
        self.assertIn(hiddenPostTitle, content, msg="Post title '%s' not found in response." % hiddenPostTitle)

    def test_GET_valid_username(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(3, [self.user2])
        toHide = posts[0]
        hiddenPost = HiddenPost.objects.create(postID=toHide, hideFrom=self.user1)
        hiddenPost.save()
        hiddenPostTitle = toHide.postTitle
        username = self.user2.username
        viewname = reverse(self.viewname) + "?username=" + username

        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)        
        self.assertIn(hiddenPostTitle, content, msg="Post title '%s' not found in response." % hiddenPostTitle)

    def test_GET_with_hiddenPosts_by_blockedUser(self):
        """ Hidden posts by blocked users are not shown!!! """
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(3, [self.user2])
        toHide = posts[0]
        hiddenPost = HiddenPost.objects.create(postID=toHide, hideFrom=self.user1)
        hiddenPost.save()
        blocked = BlockedUser.objects.create(blockedUser=self.user2, blockedBy=self.user1)
        blocked.save()

        response = self.client.get((reverse(self.viewname)), follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)        
        self.assertIn(self.no_results_msg, content, msg="Message '%s' not found in response." % self.no_results_msg)


class HidePostTests(SharedTestMethods):
    """Tests for the HidePost view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:hidepost'
        cls.loggedout_redirect_URL = '/loginpage/?next=/hidepost/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)
                                             
        admin_username = adminNameList[0]        
        cls.admin_user = User.objects.create_superuser(admin_username, 'myemail@test.com', "4un1qu3p4ssw0rd")                                     

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)
        
    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)  

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validData(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(maxPostsPerDay, [self.user2])
        toHide = posts[0]
        valid_data = {'postID': toHide.postID}

        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)
        ishidden = HiddenPost.objects.filter(postID=toHide, hideFrom=self.user1).exists()

        self.assertTrue(ishidden)
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_nonexistant_postID(self):
        self.user_login(self.credentials1)
        invalid_data = {'postID': 9999}
        response = self.client.post(reverse(self.viewname), 
                                    invalid_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_cannot_hide_admin_posts(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(3, [self.admin_user])
        toHide = posts[0]
        valid_data = {'postID': toHide.postID}

        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)
        ishidden = HiddenPost.objects.filter(postID=toHide, hideFrom=self.user1).exists()

        self.assertFalse(ishidden)
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_cannot_hide_hidden_posts(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(3, [self.user2])
        toHide = posts[0]
        valid_data = {'postID': toHide.postID}

        self.client.post(reverse(self.viewname), valid_data, follow=True)
        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class IndexPageViewTests(SharedTestMethods):
    """Tests for the IndexPage view."""

    @classmethod
    def setUpTestData(cls):
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:index'
        cls.templateURL = 'tellings/index.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

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

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

    def test_GET_loggedout(self):
        response = self.client.get((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)

    def test_GET_loggedin(self):
        self.user_login(self.credentials1)
        response = self.client.get((reverse(self.viewname)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)


class LoginPageTests(SharedTestMethods):
    """Tests for the Loginpage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:loginpage'
        cls.templateURL = 'tellings/loginpage.html'
        
        cls.user1 = cls.createUserRecord(cls, cls.credentials1) 
        cls.login_credentials = {
            'username': cls.credentials1['username'],
            'password': cls.credentials1['pwd']}   

    def test_GET_loggedout(self):
        self.get_loggedout_tests()

    def test_GET_loggedin(self):
        # If logged in opens the home page
        self.get_loggedin_tests()

    def test_POST_valid(self):
        indexpage = IndexPageViewTests()
        response = self.client.post(reverse(self.viewname), self.login_credentials, follow=True)

        self.assertEqual(response.status_code, 200)
        # redirects to home page after valid login
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
        cls.viewname = 'tellings:missionstatement'
        cls.templateURL = 'tellings/missionstatement.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

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

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

    def test_POST_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.post)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.user_login(self.credentials1)
        self.create_n_UserPosts(maxPostsPerDay, [self.user1])

        response = self.client.get((reverse(self.viewname)), follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

        for i in range(0, maxPostsPerDay):
            toCheck = self.test_postTitle1 + str(i)
            self.assertIn(toCheck, content, msg="%s not found in response." % toCheck)

    def test_GET_filteredByTag(self):
        valid_tag = self.test_postTags[0]
        invalid_tag = self.test_postTags[1]

        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1])

        viewname = reverse(self.viewname) + "?tagName=" + self.test_postTags[0]
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_tag, content, msg="Tag '%s' not found in response." % valid_tag)
        self.assertNotIn(invalid_tag, content, msg="Tag '%s' found in response." % invalid_tag)

    def test_GET_filteredByNonExistantTag(self):
        valid_tag = self.test_postTags[0]
        invalid_tag = self.test_postTags[1]

        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1])

        viewname = reverse(self.viewname) + "?tagName=unusedtag"
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_tag, content, msg="Tag '%s' not found in response." % valid_tag)
        self.assertIn(invalid_tag, content, msg="Tag '%s' found in response." % invalid_tag)


class NewUpdatesListViewTests(SharedTestMethods):
    """Tests for the NewUpdatesListView view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:newupdates'
        cls.loggedout_redirect_URL = '/loginpage/?next=/newupdates/'
        cls.templateURL = 'tellings/newupdates_list.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

        cls.no_results_msg = "No results found"

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.user_login(self.credentials1)
        self.create_n_UserPosts(maxPostsPerDay, [self.user1])

        response = self.client.get((reverse(self.viewname)), follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.check_templates_are_included(response, self.templateURL)

        for i in range(0, maxPostsPerDay):
            toCheck = self.test_postTitle1 + str(i)
            self.assertIn(toCheck, content, msg="%s not found in response." % toCheck)

    def test_GET_filteredByTag(self):
        valid_tag = self.test_postTags[0]
        invalid_tag = self.test_postTags[1]

        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1])

        viewname = reverse(self.viewname) + "?tagName=" + self.test_postTags[0]
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_tag, content, msg="Tag '%s' not found in response." % valid_tag)
        self.assertNotIn(invalid_tag, content, msg="Tag '%s' found in response." % invalid_tag)

    def test_GET_filteredByNonExistantTag(self):
        valid_tag = self.test_postTags[0]
        invalid_tag = self.test_postTags[1]

        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1])

        viewname = reverse(self.viewname) + "?tagName=unusedtag"
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_tag, content, msg="Tag '%s' not found in response." % valid_tag)
        self.assertIn(invalid_tag, content, msg="Tag '%s' found in response." % invalid_tag)

    def test_GET_filteredByUsername(self):
        valid_user = self.user2.username
        invalid_user = self.user1.username

        self.user_login(self.credentials1)
        self.create_n_UserPosts(2, [self.user1, self.user2])
        
        blocked = BlockedUser.objects.create(blockedUser=self.user2, blockedBy=self.user1)
        blocked.save()
        uname = self.user2.username
        viewname = reverse(self.viewname) + "?userName=" + uname
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_user, content, msg="Posts by valid user '%s' not found in response." % valid_user)
        self.assertNotIn(invalid_user, content, msg="Posts by BlockedUser '%s' found in response." % invalid_user)

    def test_GET_postsByBlockingUser(self):
        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1])

        blocked = BlockedUser.objects.create(blockedUser=self.user1, blockedBy=self.user2)
        blocked.save()
        blocked_username = self.user2.username

        viewname = reverse(self.viewname) + "?userName=" + blocked_username
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.no_results_msg, content, msg="Message '%s' not found in response." % self.no_results_msg)

    def test_GET_filteredByNonExistantUsername(self):
        valid_username = self.user1.username
        invalid_username = "notarealuser"

        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1])

        viewname = reverse(self.viewname) + "?userName=" + invalid_username
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_username, content, msg="Posts by '%s' not found in response." % valid_username)
        self.assertNotIn(invalid_username, content, msg="Invalid username '%s' found in response." % invalid_username)

    def test_GET_filteredByTagAndUsername(self):
        valid_user = self.user2.username
        invalid_user = self.user1.username
        valid_tag = self.test_postTags[0]
        invalid_tag = self.test_postTags[1]

        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1, self.user2])
        
        uname = self.user2.username
        viewname = reverse(self.viewname) + "?userName=" + uname + "&tagName=" + self.test_postTags[0]
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_tag, content, msg="Tag '%s' not found in response." % valid_tag)
        self.assertNotIn(invalid_tag, content, msg="Tag '%s' found in response." % invalid_tag)
        self.assertIn(valid_user, content, msg="Posts by valid user '%s' not found in response." % valid_user)
        self.assertNotIn(invalid_user, content, msg="Posts by BlockedUser '%s' found in response." % invalid_user)

    def test_GET_blockedUserNotPresent(self):
        valid_user = self.user1.username
        invalid_user = self.user2.username

        self.user_login(self.credentials1)
        self.create_UserPost_for_yesterday()
        self.create_n_UserPosts(2, [self.user1, self.user2])

        blocked = BlockedUser.objects.create(blockedUser=self.user2, blockedBy=self.user1)
        blocked.save()

        response = self.client.get(reverse(self.viewname), follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(valid_user, content, msg="Posts by valid user '%s' not found in response." % valid_user)
        self.assertNotIn(invalid_user, content, msg="Posts by BlockedUser '%s' found in response." % invalid_user)

    def test_GET_hiddenPostNotPresent(self):
        self.user_login(self.credentials2)
        toHide = self.create_UserPost_for_yesterday()
        toShow = self.create_n_UserPosts(2, [self.user1, self.user2])

        hiddenPost = HiddenPost.objects.create(postID=toHide, hideFrom=self.user2)
        hiddenPost.save()

        response = self.client.get(reverse(self.viewname), follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)

        hiddenTitle = toHide.postTitle
        self.assertNotIn(hiddenTitle, content, msg="HiddenPost '%s' found in response." % hiddenTitle)

        # Ensure that non-hidden posts are still present
        for post in toShow:
            postTitle = post.postTitle
            self.assertIn(postTitle, content, msg="Post '%s' not found in response." % postTitle)


class PrivacyPolicyPageViewTests(SharedTestMethods):
    """Tests for the PrivacyPolicyPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:privacypolicy'
        cls.templateURL = 'tellings/privacypolicy.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

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
        cls.viewname = 'tellings:signup'
        cls.templateURL = 'tellings/signup.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.test_username = 'testuser2'
        cls.registration_data = {
            'username': cls.test_username,
            'email': 'test@test.com',
            'password1': '@myp455w0rd',
            'password2': '@myp455w0rd'}
        cls.registration_data_invalid = {
            'username': cls.test_username,
            'email': 'test@test.com',
            'password1': '@myp455w0rd',
            'password2': '@myp455'}

    def test_GET_loggedout(self):
        self.get_loggedout_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_no_data(self):
        response = self.client.post(reverse(self.viewname), follow=True)
        self.post_redirects_to_errorpage_tests(response)

    def test_POST_valid(self):
        response = self.client.post(reverse(self.viewname), self.registration_data, follow=True)
        user = User.objects.get(username=self.registration_data['username'])

        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse(self.indexPage_viewname))

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

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

    def setUp(self):
        pass

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):
        self.get_loggedin_tests()

    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.post)


class TermsAndConditionsPage(SharedTestMethods):
    """Tests for the TermsAndConditionsPage view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:termsandconditions'
        cls.templateURL = 'tellings/termsandconditions.html'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)

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


class UnblockUserTests(SharedTestMethods):
    """Tests for the UnblockUser view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:unblockuser'
        cls.loggedout_redirect_URL = '/loginpage/?next=/unblockuser/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)                     
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)
        
    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)  

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validData(self):
        valid_data = {'username': self.credentials2["username"]}

        self.user_login(self.credentials1)
        blocked = BlockedUser.objects.create(blockedUser=self.user2, blockedBy=self.user1)
        blocked.save()

        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)
        isblocked = BlockedUser.objects.filter(blockedUser=self.user2, blockedBy=self.user1).exists()

        self.assertFalse(isblocked)
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_userNotBlocked(self):
        valid_data = {'username': self.credentials2["username"]}

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_nonexistant_username(self):
        valid_data = {'username': "nonexistantuser"}

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class UnhidePostTests(SharedTestMethods):
    """Tests for the UnhidePost view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:unhidepost'
        cls.loggedout_redirect_URL = '/loginpage/?next=/unhidepost/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)
        
    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)  

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validData(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(2, [self.user2])
        toHide = posts[0]
        hiddenPost = HiddenPost.objects.create(postID=toHide, hideFrom=self.user1)
        hiddenPost.save()
        valid_data = {'postID': toHide.postID}

        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)
        ishidden = HiddenPost.objects.filter(postID=toHide, hideFrom=self.user1).exists()

        self.assertFalse(ishidden)
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_nonexistant_postID(self):
        self.user_login(self.credentials1)
        invalid_data = {'postID': 9999}
        response = self.client.post(reverse(self.viewname), 
                                    invalid_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_nonhidden_post(self):
        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(2, [self.user2])
        toUnhide = posts[0]
        invalid_data = {'postID': toUnhide.postID}

        response = self.client.post(reverse(self.viewname), 
                                    invalid_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class UnhideUserPostsTests(SharedTestMethods):
    """Tests for the UnhideUserPosts view."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:unhideuserposts'
        cls.loggedout_redirect_URL = '/loginpage/?next=/unhideuserposts/'

        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user2 = cls.createUserRecord(cls, cls.credentials2)

    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.get)
        
    def test_POST_loggedout(self):
        self.post_loggedout_redirect_tests()

    def test_POST_no_data(self):
        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), follow=True)   

        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_validData(self):            
        valid_data = {'user': self.user2.username}

        self.user_login(self.credentials1)
        posts = self.create_n_UserPosts(3, [self.user2])

        for post in posts:
            hiddenPost = HiddenPost.objects.create(postID=post, hideFrom=self.user1)
            hiddenPost.save()

        response = self.client.post(reverse(self.viewname), 
                                    valid_data, follow=True)
                                    
        for post in posts:
            ishidden = HiddenPost.objects.filter(postID=post, hideFrom=self.user1).exists()
            self.assertFalse(ishidden)
            
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.SUCCESS.value)

    def test_POST_nonexistant_username(self):
        invalid_data = {'user': "nonexistantusername"}

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    invalid_data, follow=True)
            
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)

    def test_POST_no_hiddenposts(self):
        invalid_data = {'user': self.user2.username}

        self.user_login(self.credentials1)
        response = self.client.post(reverse(self.viewname), 
                                    invalid_data, follow=True)
            
        self.assertEqual(response.status_code, 200)
        self.response_contains_status_code(response, StatusCode.ERROR.value)


class UserCommentListViewTests(SharedTestMethods):
    """Tests for the UserCommentListView."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.viewname = 'tellings:usercomments'
        cls.loggedout_redirect_URL = '/loginpage/?next=/usercomments/'
        cls.templateURL = "tellings/usercomment_list.html"
        cls.no_results_msg = "Be the first person to make a comment on this post"
        
        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.commentText = "test comment"

    def test_POST_loggedin(self):  
        self.user_login(self.credentials1)
        self.http_method_not_allowed_tests(self.client.post)
        
    def test_GET_loggedout(self):
        self.get_loggedout_redirect_tests()

    def test_GET_nonexistant_postID(self):
        self.user_login(self.credentials1)
        viewname = reverse(self.viewname) + "?postID=9999"
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.no_results_msg, content, msg="Message '%s' not found in response." % self.no_results_msg)

    def test_GET_valid_nocomments(self):
        self.user_login(self.credentials1)
        post = self.create_UserPost_for_yesterday()
        postID = post.postID

        viewname = reverse(self.viewname) + "?postID=" + str(postID)
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)
        self.assertIn(self.no_results_msg, content, msg="Message '%s' not found in response." % self.no_results_msg)

    def test_GET_valid_with_comments(self):
        self.user_login(self.credentials1)
        post = self.create_UserPost_for_yesterday()
        postID = post.postID
        UserComment.objects.create(postID=post, 
                                   user=self.user1, 
                                   dateOfComment=self.test_postDate, 
                                   commentText=self.commentText) 

        viewname = reverse(self.viewname) + "?postID=" + str(postID)
        response = self.client.get(viewname, follow=True)
        content = response.content.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.templateURL)
        self.assertIn(self.commentText, content, msg="Comment '%s' not found in response." % self.commentText)


class ViewsSharedFunctionsTests(SharedTestMethods):
    """Tests for the share functions in views.py """

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = cls.createUserRecord(cls, cls.credentials1)
        cls.user1.save()
        cls.test_bannedText = "fucking admins"
        cls.test_censoredText = "****ing admins"
        cls.test_cleanText = "fluffy little bunnies"

    def test_contains_banned_word(self):
        toCensor = contains_banned_word(self.test_bannedText)
        clean = contains_banned_word(self.test_cleanText)
        self.assertTrue(toCensor)
        self.assertFalse(clean)

    def test_has_exceeded_max_posts_false(self): 
        test_request = HttpRequest()
        test_request.method = 'GET'
        test_request.user = self.user1
        self.create_UserPost_for_yesterday()
        has_exceeded = has_exceeded_max_posts(test_request)

        self.assertFalse(has_exceeded)

    def test_has_exceeded_max_posts_true(self): 
        test_request = HttpRequest()
        test_request.method = 'GET'
        test_request.user = self.user1
        self.create_n_UserPosts(maxPostsPerDay, [self.user1])
        has_exceeded = has_exceeded_max_posts(test_request)

        self.assertTrue(has_exceeded)

    def test_has_exceeded_max_posts_false_for_Admin(self): 
        admin_username = adminNameList[0]        
        my_admin = User.objects.create_superuser(admin_username, 'myemail@test.com', "4un1qu3p4ssw0rd")
        my_admin.save()

        test_request = HttpRequest()
        test_request.method = 'GET'
        test_request.user = my_admin
        
        number_of_posts = maxPostsPerDay + 1
        self.create_n_UserPosts(number_of_posts, [my_admin])
        has_exceeded = has_exceeded_max_posts(test_request)

        self.assertFalse(has_exceeded)

