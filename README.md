# django-model-documentation
 
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


# Upgrade dependency

```bash
pip install --upgrade django_model_documentation
```

Add the app (django_model_documentation) in INSTALLED_APPS in your settings project.


## Generate documentação em HTML

To generate the documentation as a HTML file named result.html on project root. 

```bash
python manage.py comment2html
```


## Gera a documentação como comentários no banco de dados

To migrate the documentation as DBRMS comments.

```bash
python manage.py comment2database
```


