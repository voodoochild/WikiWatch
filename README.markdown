# WikiWatch

This project comprises two parts; a Chrome browser extension which reports whenever you are viewing an article on Wikipedia, and a Django site which accepts and processes the URLs passed from the Chrome extension. The aim is to keep a log of all articles visited, per user, and then to display that data in an interesting way.

## Server

### Requirements

* [paver](http://pypi.python.org/pypi/Paver/1.0.4)
* [virtualenv](http://pypi.python.org/pypi/virtualenv/1.5.1)
* [RabbitMQ](http://www.rabbitmq.com/)

### Installation

1. `git clone git@github.com:voodoochild/WikiWatch.git`
2. `paver create_bootstrap`
3. `python bootstrap.py`
4. `venv/bin/pip install -e git://github.com/dwaiter/django-bcrypt.git#egg=django-bcrypt`
5. `venv/bin/python manage.py syncdb --noinput`
6. `rabbitmqctl add_user <username> <password>`
7. `rabbitmqctl add_vhost <vhost>`
8. `rabbitmqctl set_permissions -p <vhost> <username> ".*" ".*" ".*"`

### Notes

* Add a timestamp to show when the page was last visited and only revisit after a set period of time
* Try to think of a way to reduce SQL queries when importing links in visit_article()

## Chrome extension

### Notes

* Remove anchors from URLs before sending to the server
* Add a config screen to specify upload URL and auth details
* Which method of auth: oAuth, unique upload URL, or "something else"
* Add a popup.html which shows all articles logged in the current session
