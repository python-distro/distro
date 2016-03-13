from setuptools import setup
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='ld',
    version="0.5.0",
    url='https://github.com/nir0s/ld',
    author='Nir Cohen',
    author_email='nir36g@gmail.com',
    license='Apache License, Version 2.0',
    platforms='All',
    description='Linux OS Platform Information API',
    long_description=read('README.rst'),
    packages=['ld'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Operating System',
    ]
)
