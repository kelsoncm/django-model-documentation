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
from importlib import import_module
from django.conf import settings
from django.db.models.base import ModelBase
from django.apps.registry import Apps


__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


def get_models():
    result = []
    apps = Apps(settings.INSTALLED_APPS)
    for app_config in apps.get_app_configs():
        try:
            import_module('%s.comments' % app_config.module.__name__)
        except ImportError:
            pass
        except Exception as e:
            raise e

        for attr_name in dir(app_config.models_module):
            attr = getattr(app_config.models_module, attr_name)
            if isinstance(attr, ModelBase) and attr.__module__ == '%s.models' % app_config.module.__name__:
                result.append(attr)
    return result


def get_metas():
    return [getattr(x, '_meta') for x in get_models_to_doc()]


def get_models_to_doc():
    return [x for x in get_models() if not skip_model(getattr(x, '_meta'))]


def skip_model(meta):
    return meta.abstract or (meta.db_table == 'auth_user' and 'AUTH_USER_MODEL' in dir(settings))


def normalize_comment(clear_comment):
    return clear_comment.replace("'", "''")


def get_comment(meta, name, verbose_name):
    if 'comments' in dir(meta) and name in meta.comments:
        return u'%s' % meta.comments[name]
    elif 'id' == name:
        if 'DJANGO_COMMENT_DOCUMENTATION_DEFAULT_ID_COMMENT' in dir(settings):
            if callable(settings.DJANGO_COMMENT_DOCUMENTATION_DEFAULT_ID_COMMENT):
                return u'%s' % settings.DJANGO_COMMENT_DOCUMENTATION_DEFAULT_ID_COMMENT()
            else:
                return u'%s' % settings.DJANGO_COMMENT_DOCUMENTATION_DEFAULT_ID_COMMENT
        else:
            return u"Identificador único"
    else:
        return u'%s' % verbose_name
