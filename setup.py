# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='Tougou',
    version='0.1.0',
    author='Gonzalo Martinez',
    author_email='gonzalo@deploshark.com.ar',
    package_dir={'tougou': 'lib/tougou'},
    packages=['tougou'],
    scripts=['bin/tougou'],
    url='http://pypi.python.org/pypi/Tougou/',
    license='LICENSE.txt',
    description='Herramienta de integración de monitoreos',
    long_description=open('README.md').read(),
)
