"""
# Filename:     test_urls.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 29/11/2019
# Description:  Test cases for tellings urls
"""

import django
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.views import LoginView
from tellings.views import *


class URLTests(SimpleTestCase):
    """Tests for urls."""

    def test_changeuserdetails_url_resolves(self):
        url = reverse('tellings:changeuserdetails')
        self.assertEquals(resolve(url).func.view_class, ChangeUserDetailsPage)

    def test_changepassword_url_resolves(self):
        url = reverse('tellings:changepassword')
        self.assertEquals(resolve(url).func.view_class, ChangePasswordPage)

    def test_signup_url_resolves(self):
        url = reverse('tellings:signup')
        self.assertEquals(resolve(url).func.view_class, SignUpPage)

    def test_loginpage_url_resolves(self):
        url = reverse('tellings:loginpage')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_index_url_resolves(self):
        url = reverse('tellings:index')
        self.assertEquals(resolve(url).func.view_class, IndexPage)

    def test_newupdates_url_resolves(self):
        url = reverse('tellings:newupdates')
        self.assertEquals(resolve(url).func.view_class, NewUpdatesPage)

    def test_tags_url_resolves(self):
        url = reverse('tellings:tags')
        self.assertEquals(resolve(url).func.view_class, TagsPage)

    def test_myupdates_url_resolves(self):
        url = reverse('tellings:myupdates')
        self.assertEquals(resolve(url).func.view_class, MyUpdatesPage)

    def test_errorpage_url_resolves(self):
        url = reverse('tellings:errorpage')
        self.assertEquals(resolve(url).func.view_class, ErrorPage)

    def test_haspostedtoday_url_resolves(self):
        url = reverse('tellings:haspostedtoday')
        self.assertEquals(resolve(url).func.view_class, HasPostedToday)

    def test_titleexists_url_resolves(self):
        url = reverse('tellings:titleexists')
        self.assertEquals(resolve(url).func.view_class, TitleExists)

    def test_addnewupdate_url_resolves(self):
        url = reverse('tellings:addnewupdate')
        self.assertEquals(resolve(url).func.view_class, AddNewUpdate)

    def test_addupdatesfortag_url_resolves(self):
        url = reverse('tellings:addupdatesfortag')
        self.assertEquals(resolve(url).func.view_class, AddUpdatesForTag)

    def test_addupdatesfortagbyloggedinuser_url_resolves(self):
        url = reverse('tellings:addupdatesfortagbyloggedinuser')
        self.assertEquals(resolve(url).func.view_class, AddUpdatesForTagByLoggedInUser)

    def test_addupdatesforusername_url_resolves(self):
        url = reverse('tellings:addupdatesforusername')
        self.assertEquals(resolve(url).func.view_class, AddUpdatesForUsername)

    def test_accountdeleted_url_resolves(self):
        url = reverse('tellings:accountdeleted')
        self.assertEquals(resolve(url).func.view_class, AccountDeletedPage)

    def test_changeuserdetails_url_resolves(self):
        url = reverse('tellings:changeuserdetails')
        self.assertEquals(resolve(url).func.view_class, ChangeUserDetailsPage)

    def test_checkuserpassword_url_resolves(self):
        url = reverse('tellings:checkuserpassword')
        self.assertEquals(resolve(url).func.view_class, CheckUserPassword)

    def test_deleteuserpost_url_resolves(self):
        url = reverse('tellings:deleteuserpost')
        self.assertEquals(resolve(url).func.view_class, DeleteUserPost)

    def test_edituserpost_url_resolves(self):
        url = reverse('tellings:edituserpost')
        self.assertEquals(resolve(url).func.view_class, EditUserPost)
