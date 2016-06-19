# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from django.db import connection
from django.core.management.base import BaseCommand
from django_model_documentation.management.commands import get_models_to_doc, get_comment, normalize_comment


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


class Command(BaseCommand):
    help = u'Write comments do tables em fields based on models of applications'
    can_import_settings = True

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout, stderr, no_color)
        self.verbose = False
        self.noexecsql = False
        self.cursor = None

    def handle(self, *args, **options):
        self.verbose = options['verbosity'] == 1
        self.noexecsql = 'noexecsql' in options

        if not self.noexecsql:
            self.cursor = connection.cursor()

        for model in get_models_to_doc():
            try:
                meta = model._meta
                self.write_table_comment(meta)
                self.write_fields_comment(meta)
            except Exception as e:
                print (e)

    def execute_sql(self, sql):
        if self.verbose:
            print (sql)
        if not self.noexecsql:
            self.cursor.execute(sql)

    def write_table_comment(self, meta):
        try:
            comment = normalize_comment(get_comment(meta, '', meta.verbose_name))
            self.execute_sql(u"COMMENT ON TABLE %s IS '%s'" % (meta.db_table, comment))
        except Exception as e:
            print (e)

    def write_fields_comment(self, meta):
        for field in meta.concrete_fields:
            try:
                if str(meta.model) == str(field.model):
                    comment = normalize_comment(get_comment(meta, field.column, field.verbose_name))
                    self.execute_sql(u"COMMENT ON COLUMN %s.%s IS '%s'" % (meta.db_table, field.column, comment))
            except Exception as e:
                print (e)
