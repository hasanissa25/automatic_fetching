# Extract and sum the numbers
import re
import click
import logging

# Configure logging
log_format: str = '%(asctime)s.%(msecs)03d %(levelname)s \
%(module)s %(funcName)s: %(message)s'
log_datefmt: str = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(
    format=log_format,
    datefmt=log_datefmt,
    level=logging.INFO)


@click.command()
@click.option(
    '--files_count',
    type=click.Path(dir_okay=False, file_okay=True, exists=True),
    required=True,
    help="Path to the file containing base URLs.")
def main(files_count: str):

    # Read the URLs from the file
    with open(files_count, 'r') as f:
        lines = f.readlines()

    # Join all lines into a single string
    content = ''.join(lines)

    # Find all numbers before "option elements"
    numbers = map(int, re.findall(r": (\d+) option elements", content))

    # Calculate the sum
    total = sum(numbers)
    logging.info(f"Total number of files expected: {total}")
