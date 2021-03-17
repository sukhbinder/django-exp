# Django Exp
A django app i developved for maintaining household expenses. I have primariliy used it to maintain and record expenses for my housing society.

# Install
pip install django-exp

# How to use

Create a new django project

```bash

django-admin startproject expensesite

```

In the **settings.py**

```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add these two lines
    'rest_framework',
    'exp',
]

```



# Demo

![](img/expense_slow.gif)


