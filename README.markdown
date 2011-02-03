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
4. `venv/bin/python manage.py syncdb --noinput`
5. `rabbitmqctl add_user <username> <password>`
6. `rabbitmqctl add_vhost <vhost>`
7. `rabbitmqctl set_permissions -p <vhost> <username> ".*" ".*" ".*"`

### Notes

* Should Category: namespaces be captured instead of being ignored
* Add a timestamp to show when the page was last visited and only revisit after a set period of time

## Chrome extension

### Notes

* Remove anchors from URLs before sending to the server
* Add a config screen to specify upload URL and auth details
* Which method of auth: oAuth, unique upload URL, or "something else"
