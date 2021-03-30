# Qtech

## Heroku

Click here to see the deployed site

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://qtectask.herokuapp.com/)

## Running

Use the python `virtualenv` tool to build locally:

```sh
$ virtualenv-3.8 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
```

Then visit `http://localhost:8000` to view the app.

