from setuptools import setup, find_packages

setup(
    name="picolab-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "picolab=picolab.main:main",
        ],
    },
)
