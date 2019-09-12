"""
# Filename:     test_models.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 19/08/2019
# Description:  Test cases for tellings models.
"""

import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from tellings.models import Posts, Tags, Tagmap

class TagsModelTest(TestCase):
    """Tests for the Tags model."""

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def createTag(self, tagName='MyTag'):
        return Tags.objects.create(tagName=tagName)

    def test_tag_creation(self):
        tag = self.createTag()
        self.assertTrue(isinstance(tag, Tags))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Tags._meta.verbose_name_plural), "Tags")

    def test_string_representation(self):
        tag = self.createTag("Tag1")
        self.assertEqual(str(tag), tag.tagName)

    def test_tagName_max_length(self):
        tag = self.createTag()
        max_length = tag._meta.get_field('tagName').max_length
        self.assertEquals(max_length, 15)


class PostsModelTest(TestCase):
    """Tests for the Posts model."""

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')

    def setUp(self):
        pass

    def createPost(self, userID=1, dateOfPost='2019-08-12', 
                   postTitle='Post Title', postText='Post Text'):
        return Posts.objects.create(user_id=userID, dateOfPost=dateOfPost, 
                     postTitle=postTitle, postText=postText)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Posts._meta.verbose_name_plural), "Posts")

    def test_post_creation(self):
        post = self.createPost()
        self.assertTrue(isinstance(post, Posts))

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


class TagmapModelTest(TestCase):
    """Tests for the Tagmap model."""

    @classmethod
    def setUpTestData(cls):
        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')
        cls.testtag = Tags(tagName='testtag')
        cls.testpost = Posts(cls.user2.id, '2019-08-12', 'postTitle 3', 'postText 3')

    def setUp(self):
        pass    
    
    def createTagmap(self, postID=1, tagID=1):
        return Tagmap(postID_id=postID, tagID_id=tagID)

    def test_tagmap_creation(self):
        tagmap = self.createTagmap(self.testtag.tagID, self.testpost.postID)
        self.assertTrue(isinstance(tagmap, Tagmap))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Tagmap._meta.verbose_name_plural), "Tagmaps")