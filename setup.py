from setuptools import setup

version = '0.9'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'setuptools',
    ],

tests_require = [
    'nose',
    'coverage',
    'mock',
    ]

setup(name='metfilelib',
      version=version,
      description="Library for working with MET files (ingemeten dwarsprofielen)",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords=[],
      author='Remco Gerlich',
      author_email='remco.gerich@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['metfilelib'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
            'metcat = metfilelib.scripts.read_metfile:main',
          ]},
      )
