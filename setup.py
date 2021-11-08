from setuptools import find_packages, setup 

setup(
    name='mc-data',
    packages=find_packages(include=["mc-data"]),
    version='0.1.0',
    description='A library which analyzes the stats folder from your Minecraft saves',
    author='Boyan Karakostov',
    install_requires=[
        'requests',
        'matplotlib',
        'numpy',
    ],
    license='MIT',
)