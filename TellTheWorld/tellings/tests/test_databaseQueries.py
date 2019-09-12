"""
# Filename:     test_databaseQueries.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 23/08/2019
# Description:  Tests the functions in databaseQueries.py
"""
from django.test import TestCase
from django.contrib.auth.models import User
from tellings.models import Posts, Tags, Tagmap
from datetime import datetime, date, timedelta 
import tellings.databaseQueries as DBQ


class DatabaseQueriesTests(TestCase):
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
     
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')

        today = date.today()
        cls.test_todaysDate = today.strftime("%Y-%m-%d")

        cls.test_single_postDetails = {
            'userID': cls.user1.id,
            'dateOfPost': '2019-08-02',
            'postTitle': 'PT_title_1',
            'postText': 'PT_text_1',
            'postTags': ['post1','user1','common', 'testTag1']
            }

        cls.testTag1 = 'testTag1'
        cls.testTag2 = 'testTag2'

        cls.test_multiple_postDetails = {
            'post1': {
                'userID': cls.user1.id,
                'dateOfPost': '2019-08-02',
                'postTitle': 'PT_title_1',
                'postText': 'PT_text_1',
                'postTags': ['post1','user1', cls.testTag1]
            },
            'post2': {
                'userID': cls.user1.id,
                'dateOfPost': '2019-08-03',
                'postTitle': 'PT_title_2',
                'postText': 'PT_text_2',
                'postTags': ['post2','user1', cls.testTag1]
            },
            'post3': {
                'userID': cls.user2.id,
                'dateOfPost': '2019-08-02',
                'postTitle': 'PT_title_3',
                'postText': 'PT_text_3',
                'postTags': ['post3', 'user2', cls.testTag1]
            },
            'post4': {
                'userID': cls.user2.id,
                'dateOfPost': '2019-08-04',
                'postTitle': 'PT_title_4',
                'postText': 'PT_text_4',
                'postTags': ['post4', 'user2', cls.testTag1, cls.testTag2]
            },
            'post5': {
                'userID': cls.user2.id,
                'dateOfPost': '2019-08-07',
                'postTitle': 'PT_title_5',
                'postText': 'PT_text_5',
                'postTags': ['post5', 'user2', cls.testTag2]
            }
        }


    def createPostRecord(self, userID=1, dateOfPost='2019-08-02', 
                         postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def createTagRecord(self, tagName='Tag1'):
        return Tags.objects.create(tagName=tagName)

    def createTagmapRecord(self, postID=1, tagID=1):
        return Tagmap.objects.create(postID=postID, tagID=tagID)


    def createSinglePostRecord(self):
        return self.createPostRecord(self.test_single_postDetails['userID'], 
                                     self.test_single_postDetails['dateOfPost'], 
                                     self.test_single_postDetails['postTitle'], 
                                     self.test_single_postDetails['postText'])


    def createSinglePostRecordForToday(self):
        return self.createPostRecord(self.test_single_postDetails['userID'], 
                                     self.test_todaysDate, 
                                     self.test_single_postDetails['postTitle'], 
                                     self.test_single_postDetails['postText'])


    def createMultiplePostRecords(self):
        for key in self.test_multiple_postDetails.keys():
            post = self.createPostRecord(self.test_multiple_postDetails[key]['userID'], 
                                      self.test_multiple_postDetails[key]['dateOfPost'], 
                                      self.test_multiple_postDetails[key]['postTitle'], 
                                      self.test_multiple_postDetails[key]['postText'])
        return post

    def createSingleUpdate(self):
        post = self.createSinglePostRecord()
        for tag in self.test_single_postDetails['postTags']:
            tg = self.createTagRecord(tag)
            self.createTagmapRecord(post, tg)
        return post
         
    def createMultipleUpdates(self):
        for key in self.test_multiple_postDetails.keys():
            post = self.createPostRecord(self.test_multiple_postDetails[key]['userID'], 
                                  self.test_multiple_postDetails[key]['dateOfPost'], 
                                  self.test_multiple_postDetails[key]['postTitle'], 
                                  self.test_multiple_postDetails[key]['postText'])

            for tag in self.test_multiple_postDetails[key]['postTags']:
                tg = self.createTagRecord(tag)
                self.createTagmapRecord(post, tg)

    def test_sanitise_xss_string(self):
        result = DBQ.sanitiseString(self.xss_string)
        for c in self.blocked_chars:
            self.assertTrue((c not in result), "'%c' found in sanitised string" % c)

    def test_sanitise_clean_string(self):
        result = DBQ.sanitiseString(self.clean_string)
        self.assertTrue((len(result) == len(self.clean_string)), "Clean string has been shortened!")

    def test_getAllTagNames(self):
        testData = self.test_single_postDetails['postTags']
        for tag in testData:
            tg = self.createTagRecord(tag)

        result = DBQ.getAllTagNames()
        self.assertTrue((len(result)==len(testData)), "Test data and result lengths do not match")
        self.assertTrue((testData[0] in result), "'%s' not found in returned data." % testData[0])

    def test_getTagNamesByPostID(self):
        testData = self.test_single_postDetails['postTags']
        post = self.createSingleUpdate()
        result = DBQ.getTagNamesByPostID(post.postID)
        self.assertTrue((len(result)==len(testData)), "Test data and result lengths do not match")
        self.assertTrue((testData[0] in result), "'%s' not found in returned data." % testData[0])

    def test_getAllPostDetails(self):
        self.createMultiplePostRecords()
        result = DBQ.getAllPostDetails()
        testDictLen = len(self.test_multiple_postDetails)
        resultLen = len(result)    
        
        self.assertTrue(isinstance(result, list), "Did not return a list.")
        self.assertTrue((resultLen==testDictLen), "Added %d records and %d records were returned." % (testDictLen, resultLen))

        # create a flat list of the results list to make it easier to search through
        flat_list = [item for sublist in result for item in sublist]
        for key in self.test_multiple_postDetails.keys():
            testData = self.test_multiple_postDetails[key]['postTitle']
            self.assertTrue((testData in flat_list), "Post with title '%s' not found in Posts table." % testData)

    def test_getAllPostsByUserID(self):
        self.createMultiplePostRecords()
        result = DBQ.getAllPostsByUserID(self.user1.id)
        resultLen = len(result)   

        #get number of records added by user1
        userRecords = 0
        for key in self.test_multiple_postDetails.keys():
            if(self.test_multiple_postDetails[key]['userID'] == self.user1.id):
                userRecords+=1

        self.assertTrue((resultLen==userRecords), "Added %d records for user and %d records were returned." % (userRecords, resultLen))

    def test_getAllPostsByTagname(self):
        self.createMultipleUpdates()
        result = DBQ.getAllPostsByTagname(self.testTag1)
        resultLen = len(result)   

        #get number of records containing tag
        userRecords = 0
        for key in self.test_multiple_postDetails.keys():
            if( self.testTag1 in self.test_multiple_postDetails[key]['postTags']):
                userRecords+=1

        self.assertTrue((resultLen==userRecords), "Added %d records containing the tag '%s' and %d records were returned." % (userRecords, self.testTag1, resultLen))


    def test_getAllPostsByTagnameForUserID(self):
        self.createMultipleUpdates()
        result = DBQ.getAllPostsByTagnameForUserID(self.testTag2, self.user2.id)
        resultLen = len(result)   

        #get number of records containing tag
        userRecords = 0
        for key in self.test_multiple_postDetails.keys():
            if( self.testTag2 in self.test_multiple_postDetails[key]['postTags']):
                if(self.test_multiple_postDetails[key]['userID'] == self.user2.id):
                    userRecords+=1

        self.assertTrue((resultLen==userRecords), "Added %d records containing the tag '%s' and %d records were returned." % (userRecords, self.testTag1, resultLen))

    def test_getPostIDFromLastPostRecordAdded(self):
        lastPostID = self.createMultiplePostRecords().postID
        result = DBQ.getPostIDFromLastPostRecordAdded()
        self.assertTrue((result==lastPostID), "Expected postID '%d' does not match returned postID '%d'." % (lastPostID, result))

    def test_getTagIDFromLastTagRecordAdded(self):
        self.createTagRecord(self.testTag1)
        lastTagID = self.createTagRecord(self.testTag2).tagID
        result = DBQ.getTagIDFromLastTagRecordAdded()
        self.assertTrue((result==lastTagID), "Expected tagID '%d' does not match returned tagID '%d'." % (lastTagID, result))

    def test_userHasPostedToday_true(self):
        self.createSinglePostRecordForToday()
        userID = self.test_single_postDetails['userID']
        result = DBQ.userHasPostedToday(userID)
        self.assertTrue(result, "Returned user has not posted today")

    def test_userHasPostedToday_false(self):
        self.createSinglePostRecordForToday()
        userID = self.test_multiple_postDetails['post3']['userID']
        result = DBQ.userHasPostedToday(userID)
        self.assertFalse(result, "Returned user has posted today")

    def test_postTitleExists_true(self):
        self.createSinglePostRecordForToday()
        postTitle = self.test_single_postDetails['postTitle']
        result = DBQ.postTitleExists(postTitle)
        self.assertTrue(result, "Returned user has not posted today")

    def test_postTitleExists_false(self):
        self.createSinglePostRecordForToday()
        postTitle = self.test_multiple_postDetails['post3']['postTitle']
        result = DBQ.postTitleExists(postTitle)
        self.assertFalse(result, "Returned user has posted today")

    def test_addTagRecord(self):
        tag = self.test_single_postDetails['postTags'][0]
        DBQ.addTagRecord(tag)
        result = Tags.objects.get(tagName=tag)
        result_tagName = str(result)
        self.assertTrue((result_tagName==tag), "Tag with tagName '%s' not found in Tags table." % tag)
        self.assertTrue(isinstance(result, Tags), "Did not return a Tags object.")

    def test_addPostRecord(self):
        testData = self.test_single_postDetails['postTitle']
        DBQ.addPostRecord(self.test_single_postDetails['userID'], 
                          self.test_todaysDate, 
                          self.test_single_postDetails['postTitle'], 
                          self.test_single_postDetails['postText'])
        result = Posts.objects.get(postTitle=testData)
        result_postTitle = str(result)
        self.assertTrue((result_postTitle==testData), "Post with title '%s' not found in Posts table." % testData)
        self.assertTrue(isinstance(result, Posts), "Did not return a Posts object.")

    def test_addTagmapRecord(self):
        tagName = self.test_single_postDetails['postTags'][0]
        post = self.createSinglePostRecord()
        tag = self.createTagRecord(tagName)
        DBQ.addTagmapRecord(post.postID, tag.tagID)
        result = Tagmap.objects.get(postID=post.postID)
        self.assertTrue(isinstance(result, Tagmap), "Did not return a Tagmap object.")