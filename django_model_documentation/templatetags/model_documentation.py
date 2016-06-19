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
from django import template
from django.db import connection
from django.utils.safestring import mark_safe
from django_model_documentation.management.commands import get_comment
from django_model_documentation.templatetags import render_default, render_constraints


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


register = template.Library()


@register.simple_tag
def table_comment(meta):
    return get_comment(meta, '', meta.verbose_name)


@register.simple_tag
def table_verbose_name(meta):
    return meta.verbose_name


@register.simple_tag
def field_type(field):
    return field.db_type(connection)


@register.simple_tag
def field_default(field):
    return mark_safe(render_default(field))


@register.simple_tag
def field_constraints(field):
    return mark_safe(render_constraints(field))


@register.simple_tag
def field_comment(meta, field):
    return mark_safe(get_comment(meta, field.column, field.verbose_name))
