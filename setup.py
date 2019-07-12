import codecs
import os
import re

from setuptools import setup, Command

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


def get_version():
    changes_path = os.path.join(BASE_PATH, 'CHANGES.rst')
    regex = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?([a-z])?)$'
    with codecs.open(changes_path, encoding='utf-8') as changes_file:
        for line in changes_file:
            res = re.match(regex, line)
            if res:
                return res.group('version')
    return '0.0.0'


version = get_version()


class VersionCommand(Command):
    description = 'print current library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='pytest-envvars',
    version=version,
    author='Rafael Henrique da Silva Correia',
    author_email='rafael@abraseucodigo.com.br',
    maintainer='Rafael Henrique da Silva Correia',
    maintainer_email='rafael@abraseucodigo.com.br',
    license='MIT',
    url='https://github.com/rafaelhenrique/pytest-envvars',
    description='Pytest plugin to validate use of envvars on your tests ',
    long_description=read('README.rst'),
    packages=['pytest_envvars'],
    install_requires=['pytest>=3.0.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    cmdclass={
        'version': VersionCommand,
    },
    entry_points={
        'pytest11': [
            'envvars = pytest_envvars',
        ],
    },
)
