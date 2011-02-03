from paver.easy import *

generic_cmdopts = [('pathtoenv=', 'p', 'path to generate env in (e.g. for \
    virtualbox shared folder symlink issues, ~/virtual-env will install a \
    virtual env in your home dir)'),]

def get_env_path(localopts):
    if localopts.get('pathtoenv'):
        return localopts.get('pathtoenv')
    else:
        return './venv'

@task
@cmdopts(generic_cmdopts)
def create_bootstrap():
	from paver.virtual import _create_bootstrap

	localopts = options.create_bootstrap
	pathtoenv = get_env_path(localopts)

	_create_bootstrap('bootstrap.py', [
	    'Django==1.2.4',
	    'Jinja2==2.5.5',
	    'DjanJinja==0.8',
	    'celery==2.2.1',
	    'django-celery==2.2.1',
	    'BeautifulSoup==3.2.0',
	], '', dest_dir=pathtoenv, no_site_packages=True)

