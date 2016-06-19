# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='django_model_documentation',
    packages=['django_model_documentation',
              'django_model_documentation.management',
              'django_model_documentation.management.commands',
              'django_model_documentation.templatetags',
              'django_model_documentation.templates',
              'django_model_documentation.templates.django_model_documentation', ],
    package_dir={'django_model_documentation': 'django_model_documentation'},
    package_data={'django_model_documentation': ['templates/django_model_documentation/*',
                                                 'static/js/*',
                                                 'static/css/*', ],},
    version='0.7.0',
    download_url='https://github.com/kelsoncm/django_model_documentation/releases/tag/0.7.0',
    description='Django Application for output a documentation of apps models',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@gmail.com',
    url='https://github.com/kelsoncm/django_model_documentation',
    keywords=['django', 'model', 'documentation', ],    
    classifiers=[]
)
