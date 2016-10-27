# press-analytics

A web app to analyze relationships among press releases.

[Heroku Application: pressbotcity](https://pressbotcity.herokuapp.com/)

---

### To install and run locally for Mac / Linux

Install Anaconda for Python 3.x.
[Anaconda](https://www.continuum.io/downloads)

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

Run the application server!
```bash
python manage.py runserver
```

Or, to explore the Jupyter notebooks under the 'research' folder:
```bash
jupyter notebook
```
