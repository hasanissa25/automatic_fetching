import requests
from bs4 import BeautifulSoup
import logging
from automatic_fetching.config import get_app_settings, LogLevels
import click
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

# Sample call: clear && file_count --urls_file links.txt --cores 16


# Configure logging
log_format: str = '%(asctime)s.%(msecs)03d %(levelname)s \
%(module)s %(funcName)s: %(message)s'
log_datefmt: str = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    format=log_format,
    datefmt=log_datefmt,
    level=logging.INFO)


def process_collection(base_url, collection):
    """
    Count the number of option elements in a single collection.

    Args:
        base_url (str): The base URL of the collections.
        collection (str): The collection to process.

    Returns:
        int: The number of option elements in the collection.
    """
    full_url = f"{base_url}{collection}"

    response = requests.get(full_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        select_element = soup.find('select', {'id': 'pvPageSelect'})
        if select_element:
            options = select_element.find_all('option')
            logging.info(f"Found {len(options)} option elements in collection '{
                         collection}'.")
            return len(options)
        else:
            logging.info(f"No select element with id 'pvPageSelect' found in collection '{
                         collection}'.")
    else:
        logging.error(f"Failed to access the URL: {
                      full_url} (status code {response.status_code}).")

    return 0


def process_collections_concurrently(base_url, collections, cores):
    """
    Process collections concurrently using multiple threads to count option elements.

    Args:
        base_url (str): The base URL of the collections.
        collections (list): List of collections to process.
        cores (int): Number of CPU cores to use for concurrency.

    Returns:
        dict: A dictionary mapping collection names to option element counts.
    """
    results = {
        # Initialize all collections with 0 count
        collection: 0 for collection in collections}

    def process_single_collection(collection):
        try:
            return collection, process_collection(base_url, collection)
        except Exception as e:
            logging.error(f"An error occurred while processing collection '{
                          collection}': {e}")
            return collection, 0

    with ThreadPoolExecutor(max_workers=cores) as executor:
        futures = {executor.submit(
            process_single_collection, collection): collection for collection in collections}

        for future in as_completed(futures):
            collection = futures[future]
            try:
                collection_name, count = future.result()
                results[collection_name] = count
                logging.info(f"Finished processing collection '{
                             collection_name}' with {count} option elements.")
            except Exception as e:
                logging.error(f"Error processing collection '{
                              collection}': {e}")

    return results


@click.command()
@click.option(
    '--urls_file',
    type=click.Path(dir_okay=False, file_okay=True, exists=True),
    required=True,
    help="Path to the file containing base URLs.")
@click.option(
    '--cores',
    type=int,
    default=multiprocessing.cpu_count(),
    help="Number of CPU cores to use for concurrency.")
def main(urls_file: str, cores: int):
    """
    Read the URLs file and count the number of option elements in each collection in parallel.
    """
    with open(urls_file, 'r') as f:
        lines = f.readlines()

    collections = [line.strip().split('/')[-1]
                   for line in lines if line.strip()]

    base_url = "https://nrcan.canadiana.ca/view/"

    results = process_collections_concurrently(base_url, collections, cores)

    with open('./number_of_files.txt', 'w') as f:
        for collection in collections:  # Ensure all collections are included
            count = results.get(collection, 0)
            f.write(f"{collection}: {count} option elements\n")

    logging.info("Option element counts written to './number_of_files.txt'.")
