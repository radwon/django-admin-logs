from setuptools import setup

from django_admin_logs import __version__

with open('README.rst') as readme_file:
    README = readme_file.read()
with open('CHANGELOG.rst') as changelog_file:
    CHANGELOG = changelog_file.read()

setup(
    name='django-admin-logs',
    version=__version__,
    author='Adam Radwon',
    author_email='dev@radwon.com',
    url='https://github.com/radwon/django-admin-logs',
    description='View, delete or disable Django admin log entries.',
    long_description=README + '\n\n' + CHANGELOG,
    long_description_content_type='text/x-rst',
    keywords='django admin logs',
    license='MIT',
    packages=[
        'django_admin_logs',
    ],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.5',
    install_requires=[
        'Django>=2.1',
    ],
)
