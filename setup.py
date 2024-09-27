from setuptools import setup


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-hx711-loadcell',
      version='0.1.0.a4',
      description='CraftBeerPi 4 Plugin for hx711 loadcell',
      author='Alexander Vollkopf',
      author_email='avollkopf@web.de',
      url='https://github.com/PiBrewing/cbpi4-hx711-loadcell',
      license='GPLv3',
      keywords='globalsettings',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-hx711-loadcell': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-hx711-loadcell'],
      install_requires=["hx711-rpi-py"],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
