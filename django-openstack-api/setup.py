import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django_open",
    version = "0.0.1",
    author = "Jeff Wilcox",
    author_email = "jeffjapan@gmail.com",
    description = ( "An initial attempt at an openstack API version of django-nova" ),
    license = 'Apache 2.0',
    url = "https://code.launchpad.net/~jeffjapan/openstack-dashboard/openstackAPI",
    packages = ['django_open'],
    long_description = read('README'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Django",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    test_suite = 'tests',
)

