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
import sys
import codecs
from django.core.management.base import BaseCommand
from django.db import connection, models
from django_model_documentation.management.commands import get_models_to_doc, get_comment


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


class Command(BaseCommand):
    help = u'Output as HTML models documentations'
    can_import_settings = True

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(**{})
        self.verbose = False

    def handle(self, *args, **options):
        sys.stdout = codecs.open("result.html", "w", "utf-16")
        self.verbose = options['verbosity'] == 1

        self.write_document_header()

        for model in get_models_to_doc():
            meta = model._meta
            self.write_table_documentation(meta)
            self.write_fields_documentation(meta)

        self.write_document_footer()

    def _write(self, txt):
        sys.stdout.write(u'%s' % txt)

    def write_document_header(self):
        self._write(u'<html><head><style>'
                    u'div {font-weight: 700}'
                    u'label {margin-right: 10px; font-weight: 400}'
                    u'td, th {border: 1px solid #000; margin: 0; padding: 0}'
                    u'table {border-spacing: 0; border-collapse: collapse;}'
                    u'</style></head><body>'
                    u'<h1>Legenda</h1>'
                    u'<div><label>PK</label>Chave primária</div>'
                    u'<div><label>UK</label>Chave única</div>'
                    u'<div><label>AK</label>Chave alternativa (índice não único)</div>'
                    u'<div><label>FK</label>Chave estrangeira</div>'
                    u'<div><label>AI</label>Auto incremento</div>'
                    u'<div><label>NB</label>Branco não permitido</div>')

    def write_document_footer(self):
        self._write(u'</body></html>')

    def write_table_documentation(self, meta):
        """
        # local_concrete_fields, local_fields, local_many_to_many, fields, db_tablespace, swappable, swapped, model, abstract
        db_table, many_to_many, related_objects, unique_together, index_together, fields_map, concrete_fields
        """
        self._write(u'')
        self._write(u'')
        self._write(u'<h1>Tabela: %s</h1>' % meta.db_table)
        self._write(u'<div><label>Comentário:</label>%s</div>' % get_comment(meta, '', meta.verbose_name))
        self._write(u'<div><label>Os usuários conhecem como:</label>%s</div>' % meta.verbose_name)
        # self._write(u'<div><label>Chave primária:</label>%s</div>' % meta.pk)
        # if meta.has_auto_field:
        #     self._write(u'<div><label>Campo gerado automaticamente:</label>%s</div>' % meta.auto_field)
        if meta.ordering:
            self._write(u'<div><label>Normalmente ordenado por:</label>%s</div>' % list_to_str(meta.ordering))

    def write_fields_documentation(self, meta):
        self._write(u'<table>')
        self._write(u'<thead><tr>'
                    u'<th>Coluna</th>'
                    u'<th>Tipo</th>'
                    u'<th>Requerido</th>'
                    u'<th>Padrão</th>'
                    u'<th>Restrições</th>'
                    u'<th>Comentário</th>'
                    u'<th>Conhecido como</th>'
                    u'</tr></thead>')
        self._write(u'<tbody>')
        for field in meta.concrete_fields:
            self._write(u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                        (field.get_attname(),
                         field.db_type(connection),
                         'Sim' if not field.null else '&nbsp;',
                         render_default(field),
                         render_constraints(field),
                         get_comment(meta, field.column, field.verbose_name),
                         field.verbose_name))
        self._write(u'</tbody>')
        self._write(u'</table>')


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

    if 'related' in dir(field) and field.related:
        result += u'FK: %s (%s)' % (field.related.model._meta.db_table, field.related.model._meta.pk.column)

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
