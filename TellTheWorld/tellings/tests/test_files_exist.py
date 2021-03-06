﻿"""
# Filename:     test_files_exist.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 19/03/2020
# Description:  Tests that files used by the site are accessible.
"""

import django
from django.test import SimpleTestCase, TestCase
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template

import os

class tellingsFilesExistTests(TestCase):
    """Tests that tellings folder files are available."""

    @classmethod
    def setUpTestData(cls):
        """ Creates the test data used by the methods within this class. """
        cls.path = os.path.join(settings.BASE_DIR, 'tellings/')
        cls.tellings_files = [ 'admin.py',
                               'apps.py',
                               'forms.py',
                               'models.py',
                               'page_extras.py',
                               'urls.py',
                               'views.py',
                               'templatetags\my_tags.py' ]

    def test_file_exists(self):
        for filename in self.tellings_files:
            fullpath = self.path+filename
            self.assertTrue(os.path.isfile(fullpath), "File %s not found " % (fullpath))

class TemplatesExistTests(TestCase):
    """Tests that included template files are available."""

    @classmethod
    def setUpTestData(cls):
        cls.template_files = [ 'tellings/about.html',
                               'tellings/acceptableusage.html',
                               'tellings/accountDeleted.html',
                               'tellings/base.html',
                               'tellings/changePassword.html',
                               'tellings/changeUserDetails.html',
                               'tellings/errorPage.html',
                               'tellings/index.html',
                               'tellings/loginpage.html',
                               'tellings/missionstatement.html',
                               'tellings/myupdates_list.html',
                               'tellings/newupdates_list.html',
                               'tellings/privacypolicy.html',
                               'tellings/signup.html',
                               'tellings/tag_list.html',
                               'tellings/termsandconditions.html',
                               'tellings/usercomment_list.html' ]

    def setUp(self):
        pass

    def test_template_files_are_accessible(self):
        for filename in self.template_files:
            self.assertIsNotNone(get_template(filename))


class IncludedFilesExistTests(TestCase):
    """Tests that included files are available."""

    @classmethod
    def setUpTestData(cls):
        cls.base_html_files = [ 'tellings/includes/addUpdate_modal.html',
                                'tellings/includes/deleteAccount_modal.html',
                                'tellings/includes/editComment.html',
                                'tellings/includes/editPost.html',
                                'tellings/includes/footerContents.html',
                                'tellings/includes/formErrors.html',
                                'tellings/includes/JSMessagePopup.html',
                                'tellings/includes/login_modal.html',
                                'tellings/includes/navbar.html',
                                  ]

    def setUp(self):
        pass


    def test_base_html_include_files_are_accessible(self):
        for filename in self.base_html_files:
            self.assertIsNotNone(get_template(filename))
        

class StaticFilesExistTests(TestCase):
    """Tests that included static files are available."""

    @classmethod
    def setUpTestData(cls):
        cls.bootstrap_files = ['tellings/css/bootstrap-tagsinput.css',
                               'tellings/css/bootstrap.min.css',
                               'tellings/css/bootstrap.min.css.map',
                               'tellings/js/bootstrap.min.js',
                               'tellings/js/bootstrap-tagsinput.js']
        cls.jquery_files =    ['tellings/js/jquery.min.js',
                               'tellings/js/jquery.redirect.js']
        cls.other_js_files =  ['tellings/js/typeahead.bundle.js',
                               'tellings/js/JQScripts.js']
        cls.other_css_files = ['tellings/css/style.css',
                               'tellings/css/typeaheadjs.css']
        cls.image_files = ['tellings/imgs/bgimage.jpg',
                           'tellings/imgs/settings_cog.png',
                           'tellings/imgs/settings_medium_cog.png',
                           'tellings/imgs/ttwLogo.jpg']
        
    def setUp(self):
        pass

    def test_bootstrap_files_are_accessible(self):
        for filename in self.bootstrap_files:
            absolute_path = finders.find(filename)
            self.assertNotEquals(absolute_path, None, "File missing=%s" % filename)

    def test_jquery_files_are_accessible(self):
        for filename in self.jquery_files:
            absolute_path = finders.find(filename)
            self.assertNotEquals(absolute_path, None, "File missing=%s" % filename)

    def test_other_js_files_are_accessible(self):
        for filename in self.other_js_files:
            absolute_path = finders.find(filename)
            self.assertNotEquals(absolute_path, None, "File missing=%s" % filename)

    def test_other_css_files_are_accessible(self):
        for filename in self.other_css_files:
            absolute_path = finders.find(filename)
            self.assertNotEquals(absolute_path, None, "File missing=%s" % filename)

    def test_image_files_are_accessible(self):
        for filename in self.image_files:
            absolute_path = finders.find(filename)
            self.assertNotEquals(absolute_path, None, "File missing=%s" % filename)
