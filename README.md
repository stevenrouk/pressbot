# pressbot

An app to analyze relationships among text articles (news articles, blogs, etc.) on the web.

[Heroku Application: pressbotcity](https://pressbotcity.herokuapp.com/)

(Note: The Heroku app doesn't have the sentiment analysis capabilities yet because of a package issue.)

---

### To install and run locally for Mac / Linux

Install [Anaconda](https://www.continuum.io/downloads) for Python 3.x.

Clone the directory to your computer.
```bash
git clone https://github.com/stevenrouk/pressbot.git
```

Create and activate a conda virtual environment named 'pressbot-env' from the environment.yml file.
```bash
cd pressbot/
conda env create
source activate pressbot-env
```

Create settings_secret.py, and add a secret key for Django.
```bash
echo "SECRET_KEY = 'my-secret-key'" > pressbot/settings_secret.py
```

Make database migrations, then create the database.
```bash
python manage.py makemigrations
python manage.py migrate
```

Collect static files.
```bash
python manage.py collectstatic
```

Create an admin user.
```bash
python manage.py createsuperuser
```

Run the application server! In order to add text articles, you'll need to login as admin first by navigating to http://127.0.0.1:8000/admin, then go back to the index page and click the "Add Press Release" button.
```bash
python manage.py runserver
```

Or, to explore the Jupyter notebooks under the 'research' folder:
```bash
jupyter notebook
```
