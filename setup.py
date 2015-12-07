from setuptools import setup
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='ld',
    version="0.0.4",
    url='https://github.com/nir0s/ld',
    author='nir0s',
    author_email='nir36g@gmail.com',
    license='LICENSE',
    platforms='All',
    description='OS Platform Information API',
    long_description=read('README.rst'),
    packages=['ld'],
    install_requires=[
        "click==6.2",
    ],
)
