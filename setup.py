import codecs
import os

from setuptools import find_packages, setup

import pagseguro

version = pagseguro.__version__
here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'Django>=2.2',
    'requests',
    'python-dateutil',
    'xmltodict'
]

# Get the long description
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-pagseguro2',
    version=version,
    author='Allisson Azevedo',
    author_email='allisson@gmail.com',
    packages=find_packages(),
    license='MIT',
    description='Integração da API v2 do PagSeguro com o Django.',
    long_description=long_description,
    url='https://github.com/allisson/django-pagseguro2',
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
