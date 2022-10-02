Django Application on Local Machines


This Django app has features ... 


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
           
To run your app:
           
           python3 manage.py runserver

__Building the Application__

Django is now installed. To build the application, run
            
            cd ~//path/to/django
            django-admin startproject MyDjSite
            
Edit the file `~//path/to/django/MyDjSite/MyDjSite/settings.py` by changing this line:
            
            ALLOWED_HOSTS = ['*']
            
__Adding Ads appllication__
Go to the root directory of your project:

            cd ~//path/to/django/MyDjSite
            python3 manage.py startapp ads

            


