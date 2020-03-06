"""
# Filename:     test_urls.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 28/01/2020
# Description:  Test cases for tellings urls
"""

import django
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from django.contrib.auth.views import LoginView
from tellings.views import *


class URLTests(SimpleTestCase):
    """Tests for urls."""

    def test_about_url_resolves(self):
        url = reverse('tellings:about')
        self.assertEquals(resolve(url).func.view_class, AboutPage)

    def test_acceptableusage_url_resolves(self):
        url = reverse('tellings:acceptableusage')
        self.assertEquals(resolve(url).func.view_class, AcceptableUsagePage)

    def test_accountdeleted_url_resolves(self):
        url = reverse('tellings:accountdeleted')
        self.assertEquals(resolve(url).func.view_class, AccountDeletedPage)

    def test_addusercomment_url_resolves(self):
        url = reverse('tellings:addusercomment')
        self.assertEquals(resolve(url).func.view_class, AddUserComment)

    def test_addnewupdate_url_resolves(self):
        url = reverse('tellings:addnewupdate')
        self.assertEquals(resolve(url).func.view_class, AddNewUpdate)

    def test_addupdatemodal_url_resolves(self):
        url = reverse('tellings:addupdatemodal')
        self.assertEquals(resolve(url).func.view_class, AddUpdateModal)

    def test_censortext_url_resolves(self):
        url = reverse('tellings:censortext')
        self.assertEquals(resolve(url).func.view_class, CensorText)

    def test_changepassword_url_resolves(self):
        url = reverse('tellings:changepassword')
        self.assertEquals(resolve(url).func.view_class, ChangePasswordPage)

    def test_changeuserdetails_url_resolves(self):
        url = reverse('tellings:changeuserdetails')
        self.assertEquals(resolve(url).func.view_class, ChangeUserDetailsPage)

    def test_checkuserpassword_url_resolves(self):
        url = reverse('tellings:checkuserpassword')
        self.assertEquals(resolve(url).func.view_class, CheckUserPassword)

    def test_deleteaccountmodal_url_resolves(self):
        url = reverse('tellings:deleteaccountmodal')
        self.assertEquals(resolve(url).func.view_class, DeleteAccountModal)

    def test_deleteusercomment_url_resolves(self):
        url = reverse('tellings:deleteusercomment')
        self.assertEquals(resolve(url).func.view_class, DeleteUserComment)

    def test_deleteuserpost_url_resolves(self):
        url = reverse('tellings:deleteuserpost')
        self.assertEquals(resolve(url).func.view_class, DeleteUserPost)

    def test_editusercomment_url_resolves(self):
        url = reverse('tellings:editusercomment')
        self.assertEquals(resolve(url).func.view_class, EditUserComment)

    def test_edituserpost_url_resolves(self):
        url = reverse('tellings:edituserpost')
        self.assertEquals(resolve(url).func.view_class, EditUserPost)

    def test_errorpage_url_resolves(self):
        url = reverse('tellings:errorpage')
        self.assertEquals(resolve(url).func.view_class, ErrorPage)

    def test_hasexceededmaxposts_url_resolves(self):
        url = reverse('tellings:hasexceededmaxposts')
        self.assertEquals(resolve(url).func.view_class, HasExceededMaxPosts)

    def test_index_url_resolves(self):
        url = reverse('tellings:index')
        self.assertEquals(resolve(url).func.view_class, IndexPage)

    def test_loginmodal_url_resolves(self):
        url = reverse('tellings:loginmodal')
        self.assertEquals(resolve(url).func.view_class, LoginModal)

    def test_loginpage_url_resolves(self):
        url = reverse('tellings:loginpage')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_missionstatement_url_resolves(self):
        url = reverse('tellings:missionstatement')
        self.assertEquals(resolve(url).func.view_class, MissionStatementPage)

    def test_myupdates_url_resolves(self):
        url = reverse('tellings:myupdates')
        self.assertEquals(resolve(url).func.view_class, MyUpdatesListView)

    def test_newupdates_url_resolves(self):
        url = reverse('tellings:newupdates')
        self.assertEquals(resolve(url).func.view_class, NewUpdatesListView)

    def test_privacypolicy_url_resolves(self):
        url = reverse('tellings:privacypolicy')
        self.assertEquals(resolve(url).func.view_class, PrivacyPolicyPage)

    def test_signup_url_resolves(self):
        url = reverse('tellings:signup')
        self.assertEquals(resolve(url).func.view_class, SignUpPage)

    def test_tags_url_resolves(self):
        url = reverse('tellings:tags')
        self.assertEquals(resolve(url).func.view_class, TagListView)

    def test_termsandconditions_url_resolves(self):
        url = reverse('tellings:termsandconditions')
        self.assertEquals(resolve(url).func.view_class, TermsAndConditionsPage)

    def test_titleexists_url_resolves(self):
        url = reverse('tellings:titleexists')
        self.assertEquals(resolve(url).func.view_class, TitleExists)

    def test_usercomments_url_resolves(self):
        url = reverse('tellings:usercomments')
        self.assertEquals(resolve(url).func.view_class, UserCommentListView)
