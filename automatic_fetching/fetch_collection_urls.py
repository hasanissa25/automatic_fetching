import requests
from bs4 import BeautifulSoup
import logging
import click
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing


#  Sample Call: fetch_urls --cores 16 -p 69


# Configure logging
log_format: str = '%(asctime)s.%(msecs)03d %(levelname)s \
%(module)s %(funcName)s: %(message)s'
log_datefmt: str = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    format=log_format,
    datefmt=log_datefmt,
    level=logging.INFO)


def get_page_links(base_url, page_number):
    """
    Fetch all hrefs from a specific page of the search results.
    """
    url = f"{base_url}{page_number}"
    logging.info(f"Fetching page {page_number}: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Failed to fetch page {page_number}: {response.status_code}")  # noqa
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    # Find all <a> elements within <section class="search-item">
    for section in soup.find_all("section", class_="search-item"):
        link = section.find("a", href=True)
        if link and link["href"].startswith("https://nrcan.canadiana.ca/view/"):
            links.append(link["href"])

    return links


def fetch_pages_concurrently(base_url, max_pages, cores):
    """
    Fetch pages concurrently using multiple threads.
    """
    all_links = []
    page_numbers = range(1, max_pages + 1)

    def fetch_page(page_number):
        return get_page_links(base_url, page_number)

    with ThreadPoolExecutor(max_workers=cores) as executor:
        future_to_page = {executor.submit(
            fetch_page, page): page for page in page_numbers}

        for future in as_completed(future_to_page):
            page = future_to_page[future]
            try:
                links = future.result()
                all_links.extend(links)
                logging.info(f"Page {page} fetched with {len(links)} links.")
            except Exception as e:
                logging.error(f"Error fetching page {page}: {e}")

    return all_links


@click.command()
@click.option(
    '-p',
    type=int,
    required=True,
    help="Maximum number of pages to fetch.")
@click.option(
    '--cores',
    type=int,
    default=multiprocessing.cpu_count(),
    help="Number of CPU cores to use for concurrency.")
def main(p: int, cores: int):
    base_url = "https://nrcan.canadiana.ca/search/"
    logging.info(f"Using {cores} cores to fetch pages concurrently.")

    all_links = fetch_pages_concurrently(base_url, p, cores)

    # Print or save the results
    logging.info(f"Total links found: {len(all_links)}")
    with open("links.txt", "w") as file:
        file.write("\n".join(all_links))
