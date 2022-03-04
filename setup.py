from setuptools import setup, find_packages

setup(
    name='globeexplorer',
    version='1.0',
    description='Framework for automating penetration tests',
    author='@gpiechnik2',
    packages=find_packages(
        exclude=[
            "*tmp.*",
            "*tmp",
            "*modules.*",
            "*modules",
            "*example.*",
            "*example",
            "globeexplorerdb",
            "script.json"
        ]
    ),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'bs4',
    ],
    entry_points={
        'console_scripts': [
            'globeexplorer = globecli:cli',
        ],
    },
)
