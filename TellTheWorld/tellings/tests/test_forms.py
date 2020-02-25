"""
# Filename:     test_forms.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 13/02/2020
# Description:  Test cases for tellings forms
"""

import django
from django.test import TestCase

from tellings.forms import *
from datetime import date, timezone

class ChangeUserDetailsFormTests(TestCase):
    """Tests for the ChangeUserDetailsForm form."""

    def test_pass_good_data(self):
        valid_data = {'first_name': 'testfirst', 'last_name': 'testlast', 'email': 'testfirst@email.com'}
        form = ChangeUserDetailsForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'first_name': 'testfirst', 'last_name': 'testlast', 'email': 'testfirst@incomplete'}
        form = ChangeUserDetailsForm(data=invalid_data)
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
        form = DeleteAccountForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'deleted_date': self.test_postDate, 
                     'deleted_reason': 'somethingelse', 
                     'membership_length': -244}
        form = DeleteAccountForm(data=invalid_data)
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
        valid_data = {'username': 'testuser1', 'email': 'testuser@gmail.com', 'password1': '@P455w0rd', 'password2': '@P455w0rd'}
        form = NewUserCreationForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'username': 'testuser1', 'email': 'testuser@incomplete', 'password1': '@P455w0rd', 'password2': '@P455w0rd'}
        form = ChangeUserDetailsForm(data=invalid_data)
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
        form = UserCommentForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'postID': self.testpost.postID, 
                       'user': self.user2.id, 
                       'dateOfComment': 'yesterday',
                       'commentText': 'Text for another post'}
        form = UserCommentForm(data=invalid_data)
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
                     'postText': 'Text for another post'}
        form = UserPostForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        invalid_data = {'user': self.user1.id, 
                     'dateOfPost': 'yesterday', 
                     'postTitle': 'Another post', 
                     'postText': 'Text for another post'}
        form = UserPostForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = UserPostForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'dateOfPost': ['This field is required.'],
            'postTitle': ['This field is required.'],
            'user': ['This field is required.'],
            'postText': ['This field is required.']
        })

