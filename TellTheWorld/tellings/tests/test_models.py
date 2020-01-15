"""
# Filename:     test_models.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 15/01/2020
# Description:  Test cases for tellings models.
"""

import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from tellings.models import *

class TagModelTests(TestCase):
    """Tests for the Tag model."""

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def createTag(self, tagName='MyTag'):
        return Tag.objects.create(tagName=tagName)

    def test_tag_creation(self):
        tag = self.createTag()
        self.assertTrue(isinstance(tag, Tag))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Tag._meta.verbose_name_plural), "Tags")

    def test_string_representation(self):
        tag = self.createTag("Tag1")
        self.assertEqual(str(tag), tag.tagName)

    def test_tagName_max_length(self):
        tag = self.createTag()
        max_length = tag._meta.get_field('tagName').max_length
        self.assertEquals(max_length, 15)


class UserPostModelTests(TestCase):
    """Tests for the UserPost model."""

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')

    def setUp(self):
        pass

    def createPost(self, userID=1, dateOfPost='2019-08-12', 
                   postTitle='Post Title', postText='Post Text'):
        return UserPost.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def test_verbose_name_plural(self):
        self.assertEqual(str(UserPost._meta.verbose_name_plural), "UserPosts")

    def test_post_creation(self):
        post = self.createPost()
        self.assertTrue(isinstance(post, UserPost))

    def test_string_representation(self):
        post = self.createPost(self.user1.id, '2019-08-12', 'postTitle 2', 'postText 2')
        self.assertEqual(str(post), post.postTitle)

    def test_postTitle_max_length(self):
        post = self.createPost()
        max_length = post._meta.get_field('postTitle').max_length
        self.assertEquals(max_length, 35)

    def test_postText_max_length(self):
        post = self.createPost()
        max_length = post._meta.get_field('postText').max_length
        self.assertEquals(max_length, 255)


class TagmapModelTests(TestCase):
    """Tests for the Tagmap model."""

    @classmethod
    def setUpTestData(cls):
        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')
        cls.testtag = Tag(tagName='testtag')
        cls.testpost = UserPost(cls.user2.id, '2019-08-12', 'postTitle 3', 'postText 3')

    def setUp(self):
        pass    
    
    def createTagmap(self, postID=1, tagID=1):
        return Tagmap(postID_id=postID, tagID_id=tagID)

    def test_tagmap_creation(self):
        tagmap = self.createTagmap(self.testtag.tagID, self.testpost.postID)
        self.assertTrue(isinstance(tagmap, Tagmap))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Tagmap._meta.verbose_name_plural), "Tagmaps")


class DeletedAccountModelTests(TestCase):
    """Tests for the DeletedAccount model."""

    def setUp(self):
        pass

    def createRecord(self, deleted_date='2019-08-12', 
                     deleted_reason='somethingelse', membership_length=365):
        return DeletedAccount.objects.create(deleted_date=deleted_date, 
                     deleted_reason=deleted_reason, membership_length=membership_length)

    def test_verbose_name_plural(self):
        self.assertEqual(str(DeletedAccount._meta.verbose_name_plural), "DeletedAccounts")

    def test_record_creation(self):
        record = self.createRecord()
        self.assertTrue(isinstance(record, DeletedAccount))

    def test_deleted_reason_max_length(self):
        record = self.createRecord()
        max_length = record._meta.get_field('deleted_reason').max_length
        self.assertEquals(max_length, 15)