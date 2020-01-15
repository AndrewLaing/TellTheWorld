"""
# Filename:     test_forms.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 29/11/2019
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