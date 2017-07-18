# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.management import call_command
from django.utils.text import slugify

from survey.tests.management.test_management import TestManagement


class TestSurvey2CSV(TestManagement):

    """ Permit to check if export result is working as intended. """

    def test_handle(self):
        """ The custom command export result create the right csv file. """
        call_command("exportresult")
        csv_name = u'{}.csv'.format(slugify(self.test_managament_survey_name))
        file_ = open(os.path.join(settings.CSV_DIR, csv_name))
        self.assertEqual(self.expected_content.encode("utf8"), file_.read())
        file_.close()
        csv_name = u'{}.csv'.format(slugify('Test survëy'))
        file_ = open(os.path.join(settings.CSV_DIR, csv_name))
        expected = u"""\
user,Lorem ipsum dolor sit amët; <strong> consectetur </strong> adipiscing \
elit.,Ipsum dolor sit amët; <strong> consectetur </strong> adipiscing elit.,\
Dolor sit amët; <strong> consectetur</strong> adipiscing elit.,Lorem ipsum\
 dolor sit amët; consectetur<strong> adipiscing </strong> elit.,Ipsum dolor \
sit amët; consectetur <strong> adipiscing </strong> elit.,Dolor sit amët; \
consectetur<strong> adipiscing</strong> elit.
pierre,Yës | Maybe,,Text for a response,,1,No | Whatever
ps250112,Yës,,,,1,Yës
"""
        self.assertMultiLineEqual(expected.encode("utf8"), file_.read())
