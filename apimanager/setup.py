import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apipkg",
    version="0.0.1",
    author="Socle technique SIGL 2020",
    author_email="brandonquinne@hotmail.fr",
    description="Package for api manager kong service wrapper ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ursi-2020/technical-base",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)