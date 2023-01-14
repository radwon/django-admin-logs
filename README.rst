=================
Django Admin Logs
=================

.. image:: https://img.shields.io/pypi/v/django-admin-logs.svg
   :target: https://pypi.python.org/pypi/django-admin-logs

.. image:: https://img.shields.io/codecov/c/github/radwon/django-admin-logs.svg
   :target: https://codecov.io/gh/radwon/django-admin-logs

Log entries are automatically created by the Django framework whenever a user
adds, changes or deletes objects through the admin interface.

**Django Admin Logs** is a package that allows you to either view the admin
log entries from within the admin interface, or to disable them entirely.


Requirements
============

* Python 3.6+
* Django 3.2+


Installation
============

Install the package from PyPI:

.. code-block:: bash

    pip install django-admin-logs

Then add it to your ``INSTALLED_APPS`` in the ``settings`` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_admin_logs',
        ...
    )


Configuration
=============

By default, **Django Admin Logs** enables log entries to be viewed from within
the admin interface but does not allow them to be deleted. Either of these
options can be configured by adding the following to your ``settings`` file.

.. code-block:: python

    DJANGO_ADMIN_LOGS_DELETABLE = True

This allows super users, or any staff users with the delete_logentry
permission, to delete log entries from within the admin interface.

.. code-block:: python

    DJANGO_ADMIN_LOGS_ENABLED = False

This disables admin log entries so that they are no longer created by the
Django framework or viewable from within the admin interface.

By default, Django creates log entries with the message "No fields changed"
when an unchanged object is saved in the admin interface. To prevent such log
entries from being created use the following setting:

.. code-block:: python

    DJANGO_ADMIN_LOGS_IGNORE_UNCHANGED = True


Development
===========

From the local project directory, activate the virtual environment and install the development requirements:

.. code-block:: bash

    pip install -e .[dev]

To run tests for the installed version of Python and Django using pytest:

.. code-block:: bash

    pytest

To run tests for all supported Python and Django versions using tox:

.. code-block:: bash

    tox

To run tests for specific versions e.g. Python 3.9 and Django 3.2:

.. code-block:: bash

    tox -e py39-django32
