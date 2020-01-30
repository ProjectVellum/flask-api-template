#/usr/lib/python3
"""
    Packaging guide: https://packaging.python.org/tutorials/packaging-projects/

    To build rpm package:
    https://docs.python.org/2.0/dist/creating-rpms.html
"""
import setuptools

long_dsc = ''
with open('README.md', 'r') as file_obj:
    long_dsc = file_obj.read()

# Get dependencies from the requirements.txt and set it to install_requires prop.
#This will help resolve dependencies recursively when this package added as such
#by outside world.
requirements = []
with open('requirements.txt', 'r') as file_obj:
    requirements = file_obj.read().split('\n')

setuptools.setup(
    name='flask-fat',
    version='0.1.2',
    license='GPLv2',
    author='Zach Volchak',
    author_email='zakhar.volchak@hpe.com',
    description='A Python3 netlink handler.',
    long_description=long_dsc,
    long_description_content_type='text/markdown',
    url='https://github.com/ProjectVellum/flask-api-template',
    package_data = {
        # include none .py project artifacts (e.g. cfg files)
        '': ['*.yaml', '*.cfg'],
    },
    packages=setuptools.find_packages(),

    install_requires=requirements,

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6'
)