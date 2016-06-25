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
from django.utils.translation import ugettext as _


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


def render_default(field):
    if field.has_default():
        if 'auto_now' in dir(field) and field.auto_now:
            return _(u'now() always save')
        elif 'auto_now_add' in dir(field) and field.auto_now_add:
            return _(u'now() only on create')
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
    result = u'<dl>'

    if field.primary_key or field.unique or field.db_index or ('remote_field' in dir(field) and field.remote_field):
        result += '<dt>%s</dt>' % _('Keys')
        result += '<dd>'
        if field.primary_key:
            result += '%s ' % _('PK')
        elif field.unique:
            result += '%s ' % _('UK')
        if field.db_index:
            result += '%s ' % _('AK')
        if 'remote_field' in dir(field) and field.remote_field:
            fk_type = ''
            # if 'is_relation' in dir(field) and field.is_relation:
            if 'many_to_many' in dir(field) and field.many_to_many:
                fk_type += _('NxN')
            if 'many_to_one' in dir(field) and field.many_to_one:
                fk_type += _('Nx1')
            if 'one_to_many' in dir(field) and field.one_to_many:
                fk_type += _('1xN')
            if 'one_to_one' in dir(field) and field.one_to_one:
                fk_type += _('1x1')
            result += '<div>%s <a href="#%s">%s</a>(%s)' % (_(u'FK %s to') % fk_type,
                                                            field.remote_field.model._meta.db_table,
                                                            field.remote_field.model._meta.db_table,
                                                            field.remote_field.model._meta.pk.column)
        result += '</dd>'

    params = field.db_parameters(connection)
    check = params['check']
    nonblank = not field.empty_strings_allowed and isinstance(field, models.CharField)
    hascheck = check is not None and check != []
    if field.choices or field.auto_created or hascheck or nonblank:
        result += '<dt>%s</dt><dd>' % _(u'Checks')
        if field.auto_created:
            result += '%s ' % _('AI')
        if not field.null:
            result += '%s ' % _('NN')
        if nonblank:
            result += '%s ' % _('NB')
        if hascheck:
            result += '<br />%s' % check
        if field.choices:
            result += '<table><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>' % (_('Value'), _('Description'),)
            for item in field.choices:
                result += '<tr><th>%s</th><td>%s</td></tr>' % (item[0], item[1], )
            result += '</tbody></table>'
        result += '</dd>'

    if field.help_text:
        result += _(u'<dt>%s</dt><dd>%s</dd>') % (_('Help message'), field.help_text)

    result += '</dl>'

    return result


def list_to_str(lst):
    result = u''
    for item in lst:
        if result != u'':
            result += u', '
        result += item
    return result
