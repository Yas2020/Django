Django App.


This web site is a classified ad web site. People can view ads without logging in and if they log in, they can create their own ads. It uses a social login 
that allows logging in using github accounts. Database for this app is set to be MySQL.


Setting up the enviornment:

          mkdir ~/path/to/django
          cd ~/path/to/django
          python3 -m venv Dj
          source Dj/bin/activate
          #python -m pip freeze > requirements.txt
          #pip3 install Django

Install the application:

           pip3 install -r requirements.txt
           python3 manage.py check

If no error, then

           python3 manage.py makemigrations
           python3 manage.py migrate
           
To run your apps:
           
           python3 manage.py runserver

__Building the Application__

Django is now installed. To build your project, run
            
            cd ~//path/to/django
            django-admin startproject MyDjSite
            
Edit the file `~//path/to/django/MyDjSite/MyDjSite/settings.py` by changing this line:
            
            ALLOWED_HOSTS = ['*']
            
__Adding Ads appllication to your project__
Go to the root directory of your project:

            cd ~//path/to/django/MyDjSite
            python3 manage.py startapp ads
Then add this app to `MyDjSite/MyDjSite/settings.py` and `MyDjSite/MyDjSite/urls.py`. The tables and their schema in the data base is defined 
in `ads/model.py`. There are differen types of field in tables such as _Char_, _Integer_, _Binary_, _text_ etc. Both _one-to-many_ and _many-to-many_ data models exist in the table designs. Many-to-many models are done through a third table delared by a keyword arg "through" in Django.

Different users own each row in a data model and we only allow a user to edit/modify the rows that belong to them. Any user can see all rows but can only 
edit their owns. To do this, we create a new module `owner.py` in which we overwrite some generic view methods (ListView, UpdateView, CreateView etc.) in 
django.

Django has an admin feature that helps building users table for login/logout feature. One can create supersuer acccount to login to /admin page and control 
other users (create new users, delete them or give them permissions of various types, associate them wiht groups etc.) To do this, run

             python3 manage.py createsuperuser 

Login functionality is built into Django and included in your `setting.py` by default (`django.contib.auth`). Also one has to add a path to the `url.py`
(`path('accounts/', include('django.contrib.auth.urls`) inside the project.
To allow the control the look and feel of login page, we must provide a template called `registration/login.html`. This is a global template and will be 
found by django anywhere. So we can put this in any of our application template folder. In our case, this is placed in _home_ application.

`crispy_forms` library is used to shape some forms to make them look slightly better, instead of the boring default look.

In `forms.py`, the _clean_ and _save_ methods of standard model form is overwritten to handle optional pictures for ads. Picture file is recieved as 
"InMemoryUploadedFile" from user, its size is checked and after its _content type_ extracted, the picture file is saved as binary type 
(bytearray).

Make your favicon and place it in `home/static/favicon.ico`.

The python module `github_settings-dist.py` make social login work. You need to insert your own client ID and secret you get from 
github, and also you can register your app with github (on your localhost, for example).

A search feature is added to ad_list page, in addition to favorite star icons. These are integrated features in the front-end that either query(in the case 
of search) or save data (in the case of favourites) in the back-end. There is also support for tags that are displayed in details page for each ad.

Finally, the simple app called `rest` is a simple REST API app using Django. Its contains very simple model Cat, Breed (many-to-many). Using 
`serializers.py` and `rest_framework` library of Django, a web application can be turned into REST API. one can send POST, GET requests through a web 
browsable API or other tools.

The projects are parts of the assignments of courses in a great Django specialization [here]{https://www.coursera.org/specializations/django#courses}. 
            


