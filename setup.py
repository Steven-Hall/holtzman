from setuptools import setup, find_packages

setup(
        name='holtzman',
        license='MIT',
        author='Steven Hall',
        author_email='steve@fancydash.io',
        version='0.0.1',
        url='https://github.com/steven-hall/holtzman',
        description='simple templating engine',
        long_description=open('README.rst').read(),
        packages=find_packages(exclude=['tests']),
)
