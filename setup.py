# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import pagseguro

version = pagseguro.__version__

requires = [
    'Django>=1.8',
    'six',
    'requests',
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
    long_description=io.open('docs/index.rst', 'rt', encoding='UTF-8').read(),
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
