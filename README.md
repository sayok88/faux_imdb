# faux_imdb

A RESTful API for movies (something similar to IMDB).

**Local setup**

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py loadfixture
    
you can use sqlite in database if you face any issues

**Heroku Deployement**


    heroku login
    git add -A .
    git commit -m "deploy"
    heroku create
    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py loadfixture
    heroku run python manage.py createsuperuser
    heroku ps:scale web=1
    heroku open

