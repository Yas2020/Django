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
in `ads/model.py`. 
Different users own each row in a data model and we only allow a user to edit/modify the rows that belong to them. Any user can see all rows but can only edit their owns. To do this, we create a new module `owner.py` in which we overwrite some generic view methods (ListView, UpdateView, CreateView etc.) in django.

Django has an admin feature that helps building users table for login/logout feature. One can create supersuer acccount to login to /admin page and control other users (create new users, delete them or give them permissions of various types, associate them wiht groups etc.) To do this, run

             python3 manage.py createsuperuser 

Login functionality is built into Django and included in your `setting.py` by default (`django.contib.auth`). Also one has to add a path to the `url.py`
(`path('accounts/', include('django.contrib.auth.urls`) inside the project.
To allow the control th elook and feel of login page, we must provide a template called `registration/login.html`. This is a global template and will be 
found by django anywhere. So we can put htis in any of our application template folder. In our case, this is placed in home application.

`crispy_forms` library is used to shape some forms to make them look slightly better, instead of the boring default look. 

            


