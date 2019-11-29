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
    def test_pass_good_data(self):
        form_data = {'first_name': 'testfirst', 'last_name': 'testlast', 'email': 'testfirst@email.com'}
        form = ChangeUserDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_pass_bad_data(self):
        form_data = {'first_name': 'testfirst', 'last_name': 'testlast', 'email': 'testfirst@incomplete'}
        form = ChangeUserDetailsForm(data=form_data)
        self.assertFalse(form.is_valid())

