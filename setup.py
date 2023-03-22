import os

from setuptools import setup

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name="reed_scraper",
    version="0.0.1",
    description="A python program that Scrapes job information from Reed.co.uk",
    install_requires=install_requires,
    package_dir={"": "src"},
    packages=[""],
    url="https://github.com/aaFurze/Reed-Scraper",

)