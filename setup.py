import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pynosql",
    version = "1.0",
    author = "John Andersen",
    author_email = "johnandersenpdx@gmail.com",
    description = ("Socket and webserver with client connecters and console for json storage"),
    license = "MIT",
    keywords = "python nosql json",
    url = "https://github.com/pdxjohnny/PyNoSQL/",
    packages=['pynosql'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: Utilities",
        "License :: MIT License",
    ],
)
