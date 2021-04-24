__version__ = '1.0.1'

try:
    import django
    if django.VERSION < (3, 2):
        default_app_config = 'django_admin_logs.apps.DjangoAdminLogsConfig'
except ModuleNotFoundError:
    pass  # When run from setup.py
