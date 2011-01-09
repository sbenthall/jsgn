from setuptools import setup, find_packages

try:
    description = file('README').read()
except IOError: 
    description = ''

dependencies = []
try:
    import json
except:
    dependencies.append('simplejson')

version = "0.0"

setup(name='jsgn',
      version=version,
      description="",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=dependencies,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
      

