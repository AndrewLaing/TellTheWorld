"""
# Filename:     test_forms.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 16/01/2020
# Description:  Test cases for tellings forms
"""

import django
from django.test import TestCase

from tellings.forms import *


class ChangeUserDetailsFormTests(TestCase):
    """Tests for the ChangeUserDetailsForm form."""

    def test_pass_good_data(self):
        form_data = {'first_name': 'testfirst', 'last_name': 'testlast', 'email': 'testfirst@email.com'}
        form = ChangeUserDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        form_data = {'first_name': 'testfirst', 'last_name': 'testlast', 'email': 'testfirst@incomplete'}
        form = ChangeUserDetailsForm(data=form_data)
        self.assertFalse(form.is_valid())


class DeleteAccountFormTests(TestCase):
    """Tests for the DeleteAccountForm form."""

    def test_pass_good_data(self):
        form_data = {'deleted_date': '2019-08-12', 
                     'deleted_reason': 'somethingelse', 
                     'membership_length': 365}
        form = DeleteAccountForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        form_data = {'deleted_date': '2019-08-12', 
                     'deleted_reason': 'somethingelse', 
                     'membership_length': -244}
        form = DeleteAccountForm(data=form_data)
        self.assertFalse(form.is_valid())


class NewUserCreationFormTests(TestCase):
    """Tests for the NewUserCreationForm form."""

    def test_pass_good_data(self):
        form_data = {'username': 'testuser1', 'email': 'testuser@gmail.com', 'password1': '@P455w0rd', 'password2': '@P455w0rd'}
        form = NewUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        form_data = {'username': 'testuser1', 'email': 'testuser@incomplete', 'password1': '@P455w0rd', 'password2': '@P455w0rd'}
        form = ChangeUserDetailsForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserPostFormTests(TestCase):
    """Tests for the UserPostForm form."""

    @classmethod
    def setUpTestData(cls):        
        """ Creates the test data used by the methods within this class. """
        cls.credentials = { 'username': 'testuser1',
                            'email': 'testUser1@email.com',
                            'pwd': '@myp455w0rd'
        }
        cls.user1 = User.objects.create_user(cls.credentials['username'], 
                                             cls.credentials['email'],
                                             cls.credentials['pwd'])   

    def test_pass_good_data(self):
        form_data = {'user': self.user1.id, 
                     'dateOfPost': '2020-01-01', 
                     'postTitle': 'Another post', 
                     'postText': 'Text for another post'}
        form = UserPostForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        form_data = {'user': self.user1.id, 
                     'dateOfPost': 'yesterday', 
                     'postTitle': 'Another post', 
                     'postText': 'Text for another post'}
        form = UserPostForm(data=form_data)
        self.assertFalse(form.is_valid())