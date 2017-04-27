# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Survey(models.Model):

    name = models.CharField(max_length=400)
    description = models.TextField()
    is_published = models.BooleanField()
    need_logged_user = models.BooleanField()
    display_by_question = models.BooleanField()
    template = models.CharField(max_length=255, null=True, blank=True)

    class Meta(object):
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')

    def __unicode__(self):
        return self.name

    def latest_answer_date(self):
        """ Return the latest answer date. """
        min_ = None
        for response in self.responses.all():
            if min_ is None or min_ < response.updated:
                min_ = response.updated
        return min_

    @models.permalink
    def get_absolute_url(self):
        return ('survey-detail', [self.pk])

    def questions(self):
        """ Return the questions related to a Survey. """
        questions = []
        for question in self.related_questions.all():
            questions.append(question)
        return questions
