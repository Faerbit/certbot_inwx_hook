import subprocess
from setuptools import setup, find_packages
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'Readme.md')

# Convert the README to reStructuredText for PyPI if pandoc is available.
# Otherwise, just read it.
try:
    readme = subprocess.check_output(['pandoc', '-f', 'markdown',
        '-t', 'rst', readme]).decode('utf-8')
except:
    with open(readme, encoding='utf-8') as f:
        readme = f.read()


setup(
    name = 'certbot_inwx_hook',
    version = "v1.0",

    license = 'MIT',
    description = "Hook for certbot manual mode and the INWX API",
    long_description = readme,
    url = 'https://github.com/faerbit/certbot_inwx_hook',
    author = "Faerbit",
    author_email = 'faerbit at gmail dot com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],

    packages = ['certbot_inwx_hook'],
    install_requires = [
        'dnspython',
    ],

    entry_points = {
        'console_scripts': [
            'certbot_inwx_hook_deploy = certbot_inwx_hook.main:deploy',
            'certbot_inwx_hook_cleanup = certbot_inwx_hook.main:cleanup',
        ],
    },

    package_data = {
        "/etc/certbot_inwx_hook.sample.ini": [ "certbot_inwx_hook.sample.ini" ],
    },
)
