# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='django_model_documentation',
    packages=['django_model_documentation',
              'django_model_documentation.management',
              'django_model_documentation.management.commands'],
    version='0.6.2',
    description='Django Application for output a documentation of apps models',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@gmail.com',
    url='https://github.com/kelsoncm/django_model_documentation',
    download_url='https://github.com/kelsoncm/django_model_documentation/releases/tag/0.6.2',
    keywords=['django', 'model', 'documentation', ],
    classifiers=[]
)