"""
# Filename:     test_createTagLinksHTML.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last Updated: 21/08/2019
# Description:  Tests the functions in createTagLinksHTML.py
"""
from django.test import TestCase
import tellings.createTagLinksHTML as CTL

class CreateTagLinksHTMLTests(TestCase):
    """Tests the functions in createTagLinksHTML.py"""

    @classmethod
    def setUpTestData(cls):
        """ Creates the test data used by the methods within this class. """
        cls.test_tags = [ 'tag1', 'tag2' ]
        cls.test_tags_empty = [ ]
        cls.no_results_text = '<h1>No results found!</h1>'

    def test_createInnerHTML_with_tagnames(self):
        result = CTL.createInnerHTML(self.test_tags)
        for tag in self.test_tags:
            self.assertTrue((tag in result), "%s not found in HTML" % tag)

    def test_createInnerHTML_without_tagnames(self):
        result = CTL.createInnerHTML(self.test_tags_empty)
        self.assertTrue((self.no_results_text in result), "%s not found in HTML" % self.no_results_text)