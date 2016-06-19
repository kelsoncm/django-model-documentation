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
from django.db import connection, models

__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


def render_default(field):
    if field.has_default():
        if 'auto_now' in dir(field) and field.auto_now:
            return u'now() sempre que salvar'
        elif 'auto_now_add' in dir(field) and field.auto_now_add:
            return u'now() apenas ao criar'
        elif field.default:
            if callable(field.default):
                return u'PYTHON: %s' % field.default.__name__
            else:
                return field.default
        else:
            return field.get_default()
    else:
        return u'&nbsp;'


def render_constraints(field):
    result = u''

    if field.primary_key:
        result += u'PK '
    elif field.unique:
        result += u'UK '

    if field.db_index:
        result += u'AK '

    if field.auto_created:
        result += u'AI '

    if not field.empty_strings_allowed:
        if isinstance(field, models.CharField):
            result += u'NB '

    if 'remote_field' in dir(field) and field.remote_field:
        result += u'FK: %s (%s)' % (field.remote_field.model._meta.db_table, field.remote_field.model._meta.pk.column)

    if field.choices:
        result = u'<dt>Check: </dt><dd><table><thead><tr><th>Valor</th><th>Descrição</th></thead><tbody>'
        for item in field.choices:
            result += u'<tr><th>%s</th><td>%s</td><tr>' % (item[0], item[1], )
        result += u'</tbody></table></dd>'

    params = field.db_parameters(connection)
    check = params['check']
    if check is not None and check != []:
        result += u'<dt>Check: </dt><dd>%s</dd>' % check

    # if 'is_relation' in dir(field) and field.is_relation:
    if 'many_to_many' in dir(field) and field.many_to_many:
        result += u'<dt>Chave estrangeira NxN:</dt><dd>%s</dd>' % field.many_to_many
    if 'many_to_one' in dir(field) and field.many_to_one:
        result += u'<dt>Chave estrangeira Nx1:</dt><dd>%s</dd>' % field.many_to_one
    if 'one_to_many' in dir(field) and field.one_to_many:
        result += u'<dt>Chave estrangeira 1xN:</dt><dd>%s</dd>' % field.one_to_many
    if 'one_to_one' in dir(field) and field.one_to_one:
        result += u'<dt>Chave estrangeira 1x1:</dt><dd>%s</dd>' % field.one_to_one

    if field.help_text:
        result += u'<dt>Ajuda oferecida ao cliente:</dt><dd>%s</dd>' % field.help_text

    # if field.default_validators != [] or field.validators != []:
    #     result += u'<dt>Validadores:</dt><dd>%s<br />%s</dd>' % (field.default_validators, field.validators)

    return result


def list_to_str(lst):
    result = u''
    for item in lst:
        if result != u'':
            result += u', '
        result += item
    return result
