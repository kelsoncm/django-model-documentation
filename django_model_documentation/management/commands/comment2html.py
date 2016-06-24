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
from __future__ import unicode_literals
import sys
import codecs
from django.core.management.base import BaseCommand
from django_model_documentation.management.commands import get_metas
from django.template import loader


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


class Command(BaseCommand):
    help = u'Output as HTML models documentations'
    can_import_settings = True

    def __init__(self):
        super(Command, self).__init__(**{})
        self.verbose = False

    def handle(self, *args, **options):
        sys.stdout = codecs.open("result.html", "w", "utf-16")
        metas = get_metas()
        print loader.render_to_string('django_model_documentation/documentation_local.html', locals())
