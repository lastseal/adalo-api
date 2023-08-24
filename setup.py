from setuptools import setup

setup(
    name="adalo-api",
    version="1.0.0",
    description="Módulo que permite realizar consultas a las colecciones de Adalo",
    author="Rodrigo Arriaza",
    author_email="hello@lastseal.com",
    url="https://www.lastseal.com",
    packages=['adalo'],
    install_requires=[ 
        i.strip() for i in open("requirements.txt").readlines() 
    ]
)
