# WikiWatch

This project comprises two parts; a Chrome browser extension which reports whenever you are viewing an article on Wikipedia, and a Django site which accepts and processes the URLs passed from the Chrome extension. The aim is to keep a log of all articles visited, per user, and then to display that data in an interesting way.

## Server

### Requirements

* [paver](http://pypi.python.org/pypi/Paver/1.0.4)
* [setuptools](http://pypi.python.org/pypi/setuptools)
* [virtualenv](http://pypi.python.org/pypi/virtualenv/1.5.1)
* [RabbitMQ](http://www.rabbitmq.com/)

### Installation

1. `git clone git@github.com:voodoochild/WikiWatch.git`
2. `paver create_bootstrap`
3. `python bootstrap.py`
4. `venv/bin/python manage.py syncdb --noinput`
5. `rabbitmqctl add_user <username> <password>
6. `rabbitmqctl add_vhost <vhost>`
7. `rabbitmqctl set_permissions -p <vhost> <username> ".*" ".*" ".*"`

### Notes

The following namespaces need to be handled in some way:

* Special:
* Help:
* Talk:
* Wikipedia:
* File:
* Category:

Should we strip hashes from the end of urls?

## Chrome extension

### Notes

* Add a config screen to specify upload URL and auth details
* What auth? oAuth, unique upload URL, or something else?
