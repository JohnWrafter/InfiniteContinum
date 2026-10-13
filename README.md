# InfiniteContinuum

Form & Field is a neighborhood fitness studio website built with Django. Browse the studio, build a two- or three-day sample training week, and submit a membership enquiry that is saved in the local SQLite database.

## Run locally

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to explore the site. Enquiries are available in Django admin at `/admin/` after creating an administrator with `python manage.py createsuperuser`.
