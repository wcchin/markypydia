from setuptools import setup
import os

pkgfiles = os.listdir('core/')

setup(
    name="markypydia",
    version="0.0.1",
    author="Benny Chin",
    author_email="wcchin.88@gmal.com",
    packages=pkgfiles,
    include_package_data=True,
    #url="https://github.com/wcchin/markypydia",
    license="LICENSE.txt",
    description="Taiwan Geographic Open Data",
    long_description=open("README.md").read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Documentation',
         'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='markdown, personal wikipedia, documentation, website',

    install_requires=[
        "jinja",
        "beautifulsoup4",
        "docdata",
        "yaml",
    ],
)
