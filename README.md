# Mindparing-django

https://mindpairing-django.herokuapp.com/

## Deploy to heroku

1. Set Config Vars
* DISABLE_COLLECTSTATIC=1
* DJANGO_SECRET_KEY
* FIREBASE_PRIVATE_KEY
* FIREBASE_PRIVATE_KEY_ID

2. Heroku CLI
```bash
heroku login

heroku git:remote -a mindparing-django
# https://git.heroku.com/mindparing-django.git
git push heroku main

heroku run python manage.py makemigrations
heroku run python manage.py migrate
heroku run python manage.py creatsuperuser
```

## Post
### Community

### Magazine