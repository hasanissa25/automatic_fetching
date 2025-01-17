import requests
from bs4 import BeautifulSoup
import os
import logging
import click
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

# Sample call: nohup fetch_images --urls_file links_to_collections_missing.txt --cores 16 &> fetching_images.log &
# Sample call: nohup fetch_images --urls_file missing_collections.txt --cores 16 &> fetching_images.log &
# Parent process: 2124667

# Configure logging
log_format: str = '%(asctime)s.%(msecs)03d %(levelname)s \
%(module)s %(funcName)s: %(message)s'
log_datefmt: str = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    format=log_format,
    datefmt=log_datefmt,
    level=logging.INFO)


def download_image(data_uri, output_dir):
    # Remove /info.json to get the base URL
    base_url = data_uri.replace("/info.json", "")

    # Construct the image URL for the full-size image in JPG format
    image_url = f"{base_url}/full/full/0/default.jpg"

    try:
        logging.info(f"Downloading image from {image_url}...")
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_name = os.path.join(
                output_dir, os.path.basename(base_url) + ".jpg")
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logging.info(f"Saved image to {file_name}.")
        else:
            logging.error(f"Failed to download image from {image_url} (status code {response.status_code}).")  # noqa
    except Exception as e:
        logging.error(f"An error occurred while downloading the image: {e}")


def process_collection(base_url, collection):
    """
    Process a single collection by downloading all relevant files.
    """
    full_url = f"{base_url}{collection}"

    # Directory to store downloaded files
    output_dir = f"./downloads/{collection}"
    os.makedirs(output_dir, exist_ok=True)

    # Send a GET request to the URL
    response = requests.get(full_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the select element with id 'pvPageSelect'
        select_element = soup.find('select', {'id': 'pvPageSelect'})
        if select_element:
            # Find all option elements within the select element
            options = select_element.find_all('option')
            logging.info(f"Found {len(options)} option elements.")

            # Extract URLs from the data-uri property and download files
            for option in options:
                data_uri = option.get('data-uri')
                if data_uri:
                    download_image(data_uri, output_dir)
        else:
            logging.info("No select element with id 'pvPageSelect' found.")
    else:
        logging.info(f"Failed to access the base URL: {full_url} (status code {response.status_code}).")  # noqa


def process_collections_concurrently(base_url, collections, cores):
    """
    Process collections concurrently using multiple threads.
    """
    def process_single_collection(collection):
        try:
            process_collection(base_url, collection)
        except Exception as e:
            logging.error(f"An error occurred while processing collection {collection}: {e}")  # noqa

    with ThreadPoolExecutor(max_workers=cores) as executor:
        futures = {executor.submit(
            process_single_collection, collection): collection
            for collection in collections}

        for future in as_completed(futures):
            collection = futures[future]
            try:
                future.result()
                logging.info(f"Finished processing collection: {collection}")
            except Exception as e:
                logging.error(f"Error processing collection {collection}: {e}")


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
    Read the URLs file and process each collection in parallel.
    """
    # Read the URLs from the file
    with open(urls_file, 'r') as f:
        lines = f.readlines()

    collections = [line.strip().split('/')[-1]
                   for line in lines if line.strip()]

    base_url = "https://nrcan.canadiana.ca/view/"

    process_collections_concurrently(base_url, collections, cores)
