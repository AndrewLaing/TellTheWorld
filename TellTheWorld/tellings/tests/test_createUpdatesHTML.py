"""
# Filename:     test_createUpdatesHTML.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 22/08/2019
# Description:  Tests the functions in createTagLinksHTML.py
"""
from django.test import TestCase
from django.contrib.auth.models import User
from tellings.models import Posts, Tags, Tagmap

import tellings.createUpdatesHTML as CU
import tellings.databaseQueries as DBQ

class CreateUpdatesHTMLTests(TestCase):
    """Tests the functions in createTagLinksHTML.py"""

    @classmethod
    def setUpTestData(cls):
        """ Creates the test data used by the methods within this class. """
        cls.xss_string = '<script>alert("XSS");</script>'
        cls.clean_string = 'This is a clean string.'
        cls.blocked_chars = '<>&'

        cls.test_postDetails = [ 'tag1', 'tag2' ]
        cls.test_postDetails_empty = [ ]
        cls.no_results_text = '<h1>No results found!</h1>'

        # create a user update       
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.test_postTitle1 = 'PT_title_1'
        cls.test_postText1 = 'PT_text_1'
        cls.test_postTags = ["qwertyuiop","zxcvbnm","this is a test", "still a test"]


    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                   postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        return Tags.objects.create(tagName=tagName)

    def createTagmapRecord(self, postID=1, tagID=1):
        return Tagmap.objects.create(postID=postID, tagID=tagID)
         
    def createNewUpdate(self):
        post1 = self.createPostRecord(userID=self.user1.id, dateOfPost='2019-08-02', 
                              postTitle=self.test_postTitle1, postText=self.test_postText1)

        for tag in self.test_postTags:
            tg = self.createTagRecord(tag)
            self.createTagmapRecord(post1, tg)

    def test_sanitise_xss_string(self):
        result = CU.sanitiseString(self.xss_string)
        for c in self.blocked_chars:
            self.assertTrue((c not in result), "'%c' found in sanitised string" % c)

    def test_sanitise_clean_string(self):
        result = CU.sanitiseString(self.clean_string)
        self.assertTrue((len(result) == len(self.clean_string)), "Clean string has been shortened!")

    def test_createInnerHTML(self):
        self.createNewUpdate()
        postDetails = DBQ.getAllPostDetails()
        result = CU.createInnerHTML(postDetails)
        self.assertTrue((self.user1.username in result), "Username '%s' not found in HTML" % self.user1.username)
        self.assertTrue((self.test_postTitle1 in result), "Post title '%s' not found in HTML" % self.test_postTitle1)
        self.assertTrue((self.test_postText1 in result), "Post text '%s' not found in HTML" % self.test_postText1)
        for tag in self.test_postTags:
            self.assertTrue((tag in result), "Tag '%s' not found in HTML" % tag)

    def test_createInnerHTML_without_postDetails(self):
        result = CU.createInnerHTML(self.test_postDetails_empty)
        self.assertTrue((self.no_results_text in result), "'%s' not found in HTML" % self.no_results_text)
























