from setuptools import setup, find_packages

setup(
    name='globeexplorer',
    version='1.0',
    description='Tool for automating penetration tests',
    author='@gpiechnik2',
    packages=find_packages(
        exclude=[
            "*tmp.*",
            "*tmp",
            "*modules.*",
            "*modules",
            "script.py",
        ]),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'globeexplorer = cli:cli',
        ],
    },
)
