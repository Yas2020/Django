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

            


