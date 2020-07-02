"""
# Filename:     test_forms.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 02/07/2020
# Description:  Test cases for tellings forms
"""

import django
from django.test import TestCase

from tellings.forms import *
from datetime import date, timezone

class ChangeUserDetailsFormTests(TestCase):
    """Tests for the ChangeUserDetailsForm form."""

    def test_pass_good_data(self):
        valid_data = {'first_name': 'testfirst', 
                      'last_name': 'testlast', 
                      'email': 'testfirst@email.com'}
        form = ChangeUserDetailsForm(valid_data)
        details = form.save()

        self.assertEqual(details.first_name, 'testfirst')
        self.assertEqual(details.last_name, 'testlast')
        self.assertEqual(details.email, 'testfirst@email.com')
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'first_name': 'testfirst', 
                        'last_name': 'testlast', 
                        'email': 'testfirst@incomplete'}
        form = ChangeUserDetailsForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = ChangeUserDetailsForm({})
        self.assertFalse(form.is_valid())


class DeleteAccountFormTests(TestCase):
    """Tests for the DeleteAccountForm form."""
    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        test_postDate = django.utils.timezone.now()
        cls.test_postDate = test_postDate.replace(tzinfo=timezone.utc)


    def test_pass_good_data(self):
        valid_data = {'deleted_date': self.test_postDate, 
                     'deleted_reason': 'somethingelse', 
                     'membership_length': 365}
        form = DeleteAccountForm(valid_data)
        deleted = form.save()

        self.assertEqual(deleted.deleted_date, self.test_postDate)
        self.assertEqual(deleted.deleted_reason, 'somethingelse')
        self.assertEqual(deleted.membership_length, 365)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'deleted_date': self.test_postDate, 
                     'deleted_reason': 'somethingelse', 
                     'membership_length': -244}
        form = DeleteAccountForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = DeleteAccountForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'deleted_date': ['This field is required.'],
            'deleted_reason': ['This field is required.'],
            'membership_length': ['This field is required.']
        })


class NewUserCreationFormTests(TestCase):
    """Tests for the NewUserCreationForm form."""

    def test_pass_good_data(self):
        valid_data = {'username': 'testuser1', 
                      'email': 'testuser@gmail.com', 
                      'password1': '@P455w0rd', 
                      'password2': '@P455w0rd'}
        form = NewUserCreationForm(valid_data)
        newuser = form.save()

        self.assertEqual(newuser.username, 'testuser1')
        self.assertEqual(newuser.email, 'testuser@gmail.com')
        self.assertNotEqual(newuser.password, '@P455w0rd') # password should be encrypted
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'username': 'testuser1', 
                        'email': 'testuser@incomplete', 
                        'password1': '@P455w0rd', 
                        'password2': '@P455w0rd'}
        form = ChangeUserDetailsForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = NewUserCreationForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'password2': ['This field is required.'],
            'password1': ['This field is required.'],
            'email': ['This field is required.']
        })


class UserCommentFormTests(TestCase):
    """Tests for the UserCommentForm form."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.user1 = User.objects.create_user('testuser1', 'testUser1@email.com', '@myp455w0rd')
        cls.user2 = User.objects.create_user('testuser2', 'testUser2@email.com', '@myp455w0rd')
        test_postDate = django.utils.timezone.now()
        cls.test_postDate = test_postDate.replace(tzinfo=timezone.utc)
        cls.testpost = UserPost.objects.create(user_id=cls.user1.id, dateOfPost=cls.test_postDate, 
                                               postTitle='postTitle 1', postText='postText 1')                               

    def test_pass_good_data(self):
        valid_data = {'postID': self.testpost.postID, 
                     'user': self.user2.id, 
                     'dateOfComment': self.test_postDate,
                     'commentText': 'Text for another post'}
        form = UserCommentForm(valid_data)
        comment = form.save()

        self.assertEqual(comment.postID, self.testpost)
        self.assertEqual(comment.user, self.user2)
        self.assertEqual(comment.dateOfComment, self.test_postDate)
        self.assertEqual(comment.commentText, 'Text for another post')
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'postID': self.testpost.postID, 
                       'user': self.user2.id, 
                       'dateOfComment': 'yesterday',
                       'commentText': 'Text for another post'}
        form = UserCommentForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = UserCommentForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'postID': ['This field is required.'],
            'dateOfComment': ['This field is required.'],
            'commentText': ['This field is required.'],
            'user': ['This field is required.']
        })


class UserPostFormTests(TestCase):
    """Tests for the UserPostForm form."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.credentials = { 'username': 'testuser1',
                            'email': 'testUser1@email.com',
                            'pwd': '@myp455w0rd'
        }
        test_postDate = django.utils.timezone.now()
        cls.test_postDate = test_postDate.replace(tzinfo=timezone.utc)
        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])   

    def test_pass_good_data(self):
        valid_data = {'user': self.user1.id, 
                      'dateOfPost': self.test_postDate, 
                      'postTitle': 'Another post', 
                      'postText': 'Text for another post',
                      'postTags': ['["testTag1","testTag2"]']} 
        form = UserPostForm(valid_data)
        userpost = form.save()
        self.assertEqual(userpost.dateOfPost, self.test_postDate)
        self.assertEqual(userpost.postTitle, 'Another post')
        self.assertEqual(userpost.postText, 'Text for another post')
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'user': self.user1.id, 
                        'dateOfPost': 'yesterday', 
                        'postTitle': 'Another post', 
                        'postText': 'Text for another post'}

        form = UserPostForm(invalid_data)
        self.assertFalse(form.is_valid())

    def test_tags_added(self): 
        valid_data = {'user': self.user1.id, 
                      'dateOfPost': self.test_postDate, 
                      'postTitle': 'Another post', 
                      'postText': 'Text for another post',
                      'postTags': ['["testtag1","testtag2","testtag3"]']} 

        form = UserPostForm(valid_data)
        form.save()

        self.assertTrue(Tag.objects.filter(tagName="testtag1").exists())
        self.assertTrue(Tag.objects.filter(tagName="testtag2").exists())
        self.assertTrue(Tag.objects.filter(tagName="testtag3").exists())

    def test_blank_data(self):
        form = UserPostForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'dateOfPost': ['This field is required.'],
            'postTitle': ['This field is required.'],
            'user': ['This field is required.'],
            'postText': ['This field is required.']
        })

