# SMS
-- by rtzs-cell </br>
An easy Student Management System by Django framework

# How to start?
<code>python manage.py runserver localhost:8000 </code>

# How to change the DB?

In SMS->settings, you can modify this part of code</br>
<code>DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'StudentManagement',
	        'USER': 'root',
	        'PASSWORD': '',
	        'HOST': '127.0.0.1',
	        'PORT': '3306',
	    }
	}</code>
