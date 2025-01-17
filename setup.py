from setuptools import setup
from setuptools import find_packages


setup(
    name='automatic_fetching',
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
                automatic_fetching.download_files_using_collection_links:main',
            'fetch_collection_urls = \
                automatic_fetching.fetch_collection_urls:main',
            'get_number_of_files_for_each_collection = \
                automatic_fetching.get_number_of_files_for_each_collection:main',
            'count_total_number_of_options_from_file = \
                automatic_fetching.count_total_number_of_options_from_file:main',
            'check_for_missing_files = \
                automatic_fetching.check_for_missing_files:main',
            'filter_missing_entries = \
                automatic_fetching.filter_missing_entries:main',

        ]
    }
)
