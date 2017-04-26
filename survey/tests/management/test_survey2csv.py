# -*- coding: utf-8 -*-

from mock.mock import patch

from survey.management.survey2csv import Survey2CSV
from survey.tests.management.test_management import TestManagement


@staticmethod
def raise_io_exc(survey):
    raise IOError("msg")


class TestSurvey2CSV(TestManagement):

    """ Permit to check if export result is working as intended. """

    def test_get_header_and_order(self):
        """ The header and order of the question is correct. """
        header, order = Survey2CSV.get_header_and_order(self.survey)
        self.assertEqual(header, self.expected_header)
        self.assertEqual(len(order), 4)

    def test_get_survey_as_csv(self):
        """ The content of the CSV is correct. """
        self.assertEqual(Survey2CSV.survey_to_csv(self.survey),
                         self.expected_content)

    @patch.object(Survey2CSV, "file_name", raise_io_exc)
    def test_dir_not_exists(self):
        """ We raise an IoError if the directory does not exists. """
        self.assertRaises(IOError, Survey2CSV.generate_file, self.survey)

    def test_not_a_survey(self):
        """ TypeError raised when the object is not a survey. """
        self.assertRaises(TypeError, Survey2CSV.survey_to_csv, "Not a survey")
        self.assertRaises(TypeError, Survey2CSV.generate_file, "Not a survey")
