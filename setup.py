from setuptools import setup

setup(name='cbpi4-hx711-loadcell',
      version='0.1.0.a3',
      description='CraftBeerPi Plugin',
      author='Alexander Vollkopf',
      author_email='avollkopf@web.de',
      url='https://github.com/PiBrewing/cbpi4-hx711-loadcell',
      license='GPLv3',
      include_package_data=True,
      keywords='globalsettings',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-hx711-loadcell': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-hx711-loadcell'],
      install_requires=["hx711-rpi-py"],
     )
