from django.conf import settings


def pytest_configure():
    settings.configure(
        SECRET_KEY="TEST_KEY",
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=[
            "django.contrib.sessions",
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.admin",
            "django_admin_logs",
        ],
        MIDDLEWARE_CLASSES=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
        ],
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.contrib.auth.context_processors.auth",
                    ],
                },
            }
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
    )
