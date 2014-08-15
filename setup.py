# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pagseguro

version = pagseguro.__version__

requires = [
    'Django>=1.3',
    'six',
    'requests',
    'httpretty',
    'python-dateutil',
    'xmltodict'
]

setup(
    name='django-pagseguro2',
    version=version,
    author='Allisson Azevedo',
    author_email='allisson@gmail.com',
    packages=find_packages(),
    license='MIT',
    description='Integração da API v2 do PagSeguro com o Django.',
    long_description=open('docs/index.rst').read(),
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
