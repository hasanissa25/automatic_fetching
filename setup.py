from setuptools import setup
from setuptools import find_packages


setup(
    name='stationverification',
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'beautifulsoup4',
        "pydantic_settings",
        "requests",
        "click"
    ],
    entry_points={
        'console_scripts': [
            'fetch_images = \
                automatic_fetching.command_line:main',
            'fetch_urls = \
                automatic_fetching.fetch_urls:main',
            'file_count = \
                automatic_fetching.file_count:main',
        ]
    }
)
