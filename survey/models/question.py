# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from .category import Category
from .survey import Survey


CHOICES_HELP_TEXT = _(u"""The choices field is only used if the question type
if the question type is 'radio', 'select', or
'select multiple' provide a comma-separated list of
options for this question .""")


def validate_choices(choices):
    """  Verifies that there is at least two choices in choices
    :param String choices: The string representing the user choices.
    """
    values = choices.split(',')
    empty = 0
    for value in values:
        if value.replace(" ", '') == '':
            empty += 1
    if len(values) < 2 + empty:
        msg = "The selected field requires an associated list of choices."
        msg += " Choices must contain more than one item."
        raise ValidationError(msg)


class Question(models.Model):
    TEXT = 'text'
    SHORT_TEXT = 'short-text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_IMAGE = 'select_image'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, _(u'text (multiple line)')),
        (SHORT_TEXT, _(u'short text (one line)')),
        (RADIO, _(u'radio')),
        (SELECT, _(u'select')),
        (SELECT_MULTIPLE, _(u'Select Multiple')),
        (SELECT_IMAGE, _(u'Select Image')),
        (INTEGER, _(u'integer')),
    )

    text = models.TextField()
    order = models.IntegerField()
    required = models.BooleanField()
    category = models.ForeignKey(Category, blank=True, null=True,
                                 related_name="related_questions")
    survey = models.ForeignKey(Survey, related_name="related_questions")
    type = models.CharField(max_length=200, choices=QUESTION_TYPES,
                            default=TEXT)
    choices = models.TextField(blank=True, null=True,
                               help_text=CHOICES_HELP_TEXT)

    class Meta(object):
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ('survey', 'order')

    def save(self, *args, **kwargs):
        if self.type in [Question.RADIO, Question.SELECT,
                         Question.SELECT_MULTIPLE]:
            validate_choices(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_clean_choices(self):
        if self.choices is None:
            return []
        try:
            choices = unicode(self.choices).split(',')
        except UnicodeDecodeError:
            choices = unicode(self.choices.decode("utf8")).split(',')
        choices_list = []
        for choice in choices:
            choice = choice.strip()
            if choice:
                choices_list.append(choice)
        return choices_list

    @property
    def answers_as_text(self):
        """ Return answers as a list of text.

        :rtype: List """
        return self.answers_cardinality.keys()

    @property
    def answers_cardinality(self):
        """ Return a dictionary with answers as key and cardinality as value

        :rtype: Dict """
        cardinality = {}
        for answer in self.answers.all():
            try:
                cardinality[answer.body] += 1
            except KeyError:
                cardinality[answer.body] = 1
        return cardinality

    def get_choices(self):
        """
        Parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.
        """
        choices_list = []
        for choice in self.get_clean_choices():
            choices_list.append((slugify(choice), choice))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __unicode__(self):
        msg = u"Question '{}' ".format(self.text)
        if self.required:
            msg += u"(*) "
        msg += u"{}".format(self.get_clean_choices())
        return msg
