# lcnet_blog

A django blog system deployed on Sina App Engine (SAE).

* Running on [http://1.lcnet.applinzi.com/](http://1.lcnet.applinzi.com/)
* Based on Django 1.8.3

## Features
* Editing in Markdown
* Code highlighting
* Mobile device friendly
* Search in site
* Archives views
* Article views
* Categories
* Sitemaps
* comments

## Installation on localhost
    git clone git@github.com:jasonlc/lcnet_blog.git
    cd lcnet_blog
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
## Init Database
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

