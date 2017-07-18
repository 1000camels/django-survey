# -*- coding: utf-8 -*-

import logging

from survey.management.exporter.survey2x import Survey2X

LOGGER = logging.getLogger(__name__)


class Survey2CSV(Survey2X):

    @staticmethod
    def line_list_to_string(line):
        """ Write a line in the CSV. """
        new_line = u""
        for i, cell in enumerate(line):
            try:
                cell = unicode(cell)
            except UnicodeDecodeError:
                cell = unicode(cell.decode("utf8"))
            cell = u" ".join(cell.split())
            new_line += cell.replace(u",", u";")
            if i != len(line) - 1:
                new_line += u","
        return new_line

    @staticmethod
    def get_user_line(question_order, response):
        """ Creating a line for a user """
        not_an_answer = u"NAA"
        LOGGER.debug(u"\tTreating answer from %s", response.user)
        user_answers = {}
        user_answers[u"user"] = unicode(response.user)
        # user_answers[u"entity"] = response.user.entity
        for answer in response.answers.all():
            cell = not_an_answer
            # remove double space, tab, \n...
            answer_body = " ".join(unicode(answer.body).split())
            if "[" in answer_body:
                # Its a select multiple ( [u"Yes", u"Maybe"] )
                answers = eval(answer_body)
                cell = u""
                for i, ans in enumerate(answers):
                    if i < len(answers) - 1:
                        # Separate by a pipe if its not the last
                        cell += ans + u" | "
                    else:
                        cell += ans
            else:
                cell = answer_body
            LOGGER.debug(u"\t\t%s : %s", answer.question.pk, cell)
            user_answers[answer.question.pk] = cell
        user_line = []
        for key_ in question_order:
            try:
                user_line.append(user_answers[key_])
            except KeyError:
                user_line.append(not_an_answer)
        return user_line

    def get_header_and_order(self):
        """ Creating header.

        :param Survey survey: The survey we're treating. """
        header = [u"user"]  # , u"entity"]
        question_order = [u"user"]  # , u"entity" ]
        for question in self.survey.questions.all():
            header.append(unicode(question.text))
            question_order.append(question.pk)
        return header, question_order

    def survey_to_x(self):
        csv = []
        header, question_order = self.get_header_and_order()
        csv.append(Survey2CSV.line_list_to_string(header))
        for response in self.survey.responses.all():
            line = Survey2CSV.get_user_line(question_order, response)
            csv.append(Survey2CSV.line_list_to_string(line))
        return csv
