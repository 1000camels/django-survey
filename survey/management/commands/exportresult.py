# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from survey.management.exporter.csv.survey2csv import Survey2CSV
from survey.models import Survey


class Command(BaseCommand):

    """
        See the "help" var.
    """

    requires_system_checks = False

    help = u"""This command permit to export all survey in the database as csv
               and tex."""

    def handle(self, *args, **options):
        for survey in Survey.objects.all():
            exporters = [Survey2CSV(survey)]
            for exporter in exporters:
                if exporter.need_update():
                    exporter.generate_file()
