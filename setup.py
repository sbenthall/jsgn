from setuptools import setup, find_packages

try:
    description = file('README.txt').read()
except IOError: 
    description = ''

version = "0.0"

setup(name='jsgn',
      version=version,
      description="",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='',
      author_email='',
      url='',
      license='See http://www.python.org/2.6/license.html'
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
      
