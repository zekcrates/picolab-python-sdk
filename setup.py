from setuptools import setup, find_packages

setup(
    name='pico-sdk',           
    version='0.1.0',
    packages=find_packages(),  
    install_requires=[
        'typer[all]',          
        'requests',            
        'rich',               
    ],
    entry_points={
        'console_scripts': [
            'picolab=pico.main:app', 
        ],
    },
)