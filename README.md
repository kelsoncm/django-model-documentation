# Django Model Documentation

This app reads all models in INSTALLED_APPS and generates the app documentation as database script or as HTML. If you don't provide a comment to the model the app will assume the Model's name as comment to the table. If you don't provide a comment to the field the app will assume the verbose_name as comment, if you don't provide a verbose_name the field name will be assumed as comment.


# How to install

```bash
pip install --upgrade django_model_documentation
```

# Example

Don't forget to add (django_model_documentation) to the INSTALLED_APPS in your settings project.

## Comment your model

Comments are a dict where each key is a field name, but if you provide a key '' (empty string) this key will be assumed as a table comment.

To provide a comments open the models.py of the app where you want do to document, so you can do something like that:

```python
from django_model_documentation import load_class_meta

load_class_meta('myapp', 'Foo').comments = {
    '': u'Describe a Foo',
    'bar': u'The bar of this foo',
}
```

You can put this code in your models.py or in a comments.py separated file at same directory of your models.py.



## Generate as HTML file

To generate the documentation as a HTML file named result.html on project root. 

```bash
python manage.py comment2html
```


## Generate as SQL Script

To output the documentation as DBRMS comments.

```bash
python manage.py comment2database
```


## Comment third's model

Do need to create a comments.py file in a app of your choice and put something like this:

```python
from django_model_documentation import load_class_meta
load_class_meta('django.contrib.auth' 'User').comments = {
    '': u'User with administration privileges',
    'username': u'This is the username used to do a login',
}
```


 
# License
 
The MIT License (MIT)

Copyright 2015 KelsonCM.

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
http://peterdowns.com/posts/first-time-with-pypi.html
