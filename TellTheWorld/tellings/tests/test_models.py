"""
# Filename:     test_models.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 28/01/2020
# Description:  Test cases for tellings models.
"""

import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timezone
from tellings.models import *

class DeletedAccountModelTests(TestCase):
    """Tests for the DeletedAccount model."""

    def setUp(self):
        test_postDate = django.utils.timezone.now()
        self.test_postDate = test_postDate.replace(tzinfo=timezone.utc)        

    def createRecord(self, deleted_date, deleted_reason, membership_length):
        return DeletedAccount.objects.create(deleted_date=deleted_date, 
                     deleted_reason=deleted_reason, membership_length=membership_length)

    def test_verbose_name_plural(self):
        self.assertEqual(str(DeletedAccount._meta.verbose_name_plural), "DeletedAccounts")

    def test_record_creation(self):
        record = self.createRecord(self.test_postDate, "something else", 365)
        self.assertTrue(isinstance(record, DeletedAccount))

    def test_deleted_reason_max_length(self):
        max_length = DeletedAccount._meta.get_field('deleted_reason').max_length
        self.assertEquals(max_length, 15)
                

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
        max_length = Tag._meta.get_field('tagName').max_length
        self.assertEquals(max_length, 15)


class TagmapModelTests(TestCase):
    """Tests for the Tagmap model."""

    @classmethod
    def setUpTestData(cls):
        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')
        cls.testtag = Tag(tagName='testtag')
        test_postDate = django.utils.timezone.now()
        cls.test_postDate = test_postDate.replace(tzinfo=timezone.utc)
        cls.testpost = UserPost(cls.user2.id, test_postDate, 'postTitle 3', 'postText 3')

    def setUp(self):
        pass    
    
    def createTagmap(self, postID=1, tagID=1):
        return Tagmap(postID_id=postID, tagID_id=tagID)

    def test_tagmap_creation(self):
        tagmap = self.createTagmap(self.testtag.tagID, self.testpost.postID)
        self.assertTrue(isinstance(tagmap, Tagmap))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Tagmap._meta.verbose_name_plural), "Tagmaps")


class UserCommentModelTests(TestCase):
    """Tests for the UserComment model."""

    @classmethod
    def setUpTestData(cls):
        test_postDate = django.utils.timezone.now()
        cls.test_postDate = test_postDate.replace(tzinfo=timezone.utc)
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')
        cls.testpost = UserPost.objects.create(user_id=cls.user2.id, dateOfPost=cls.test_postDate, 
                                               postTitle='postTitle 1', postText='postText 1') 

    def setUp(self):
        pass


    def createComment(self, postID, userID, dateOfComment, commentText):
    
        return UserComment.objects.create(postID=postID, user_id=userID, 
                                          dateOfComment=dateOfComment, 
                                          commentText=commentText)

    def test_verbose_name_plural(self):
        self.assertEqual(str(UserComment._meta.verbose_name_plural), "UserComments")

    def test_comment_creation(self):
        comment = self.createComment(self.testpost, self.user2.id, self.test_postDate, 'comment text 1')
        self.assertTrue(isinstance(comment, UserComment))

    def test_string_representation(self):
        comment = self.createComment(self.testpost, self.user2.id, self.test_postDate, 'comment text 2')
        self.assertEqual(str(comment), comment.commentText)

    def test_commentText_max_length(self):
        max_length = UserComment._meta.get_field('commentText').max_length
        self.assertEquals(max_length, 255)


class UserPostModelTests(TestCase):
    """Tests for the UserPost model."""

    @classmethod
    def setUpTestData(cls):
        test_postDate = django.utils.timezone.now()
        cls.test_postDate = test_postDate.replace(tzinfo=timezone.utc)
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')

    def setUp(self):
        pass

    def createPost(self, userID, dateOfPost, postTitle, postText):
        return UserPost.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def test_verbose_name_plural(self):
        self.assertEqual(str(UserPost._meta.verbose_name_plural), "UserPosts")

    def test_post_creation(self):
        post = self.createPost(1, self.test_postDate, 'postTitle 2', 'postText 2')
        self.assertTrue(isinstance(post, UserPost))

    def test_string_representation(self):
        post = self.createPost(self.user1.id, self.test_postDate, 'postTitle 2', 'postText 2')
        self.assertEqual(str(post), post.postTitle)

    def test_postTitle_max_length(self):
        max_length = UserPost._meta.get_field('postTitle').max_length
        self.assertEquals(max_length, 35)

    def test_postText_max_length(self):
        max_length = UserPost._meta.get_field('postText').max_length
        self.assertEquals(max_length, 255)
