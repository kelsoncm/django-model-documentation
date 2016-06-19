#!/usr/bin/env python
import argparse
import os


parser = argparse.ArgumentParser(description='release project')
parser.add_argument('version')
args = parser.parse_args()

with open('setup.py', 'w') as f:
    f.write("""# -*- coding: utf-8 -*-
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
    version='%s',
    download_url='https://github.com/kelsoncm/django_model_documentation/releases/tag/%s',
    description='Django Application for output a documentation of apps models',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@gmail.com',
    url='https://github.com/kelsoncm/django_model_documentation',
    keywords=['django', 'model', 'documentation', ],    
    classifiers=[]
)
""" % (args.version, args.version,))

os.system("git add setup.py")
os.system("git commit -m 'Release %s'" % args.version)
os.system("git tag %s" % args.version)
os.system("git push --tags origin master")
os.system("python setup.py sdist")
os.system("twine upload dist/django_model_documentation-%s.tar.gz" % args.version)
# os.system("python setup.py sdist upload -r pypi")
