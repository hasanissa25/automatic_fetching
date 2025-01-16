# Define file paths
real_file = "./number_of_files_in_download_directory_pc_21.txt"
expected_file = "./expected_number_of_files_per_collection.txt"


def parse_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # Parse lines into a dictionary with "ooga.NRCan_#" as key and number of options as value
    return {line.split(":")[0].strip(): int(line.split(":")[1].split()[0]) for line in lines}


def main():
    # Parse the files
    real_data = parse_file(real_file)
    expected_data = parse_file(expected_file)

    # Find discrepancies and calculate total missing
    missing_or_mismatched = []
    total_missing = 0

    for key, expected_value in expected_data.items():
        real_value = real_data.get(key)
        if real_value is None:
            # Entire entry is missing
            total_missing += expected_value
            missing_or_mismatched.append(
                f"{key}: Missing ({expected_value} expected)")
        elif real_value != expected_value:
            # Calculate the difference
            difference = expected_value - real_value
            total_missing += difference
            missing_or_mismatched.append(f"{key}: {difference} incomplete (expected {expected_value}, found {real_value})")  # noqa

    # Output the results
    output_file = "missing_or_mismatched.txt"
    with open(output_file, "w") as f:
        for entry in missing_or_mismatched:
            f.write(f"{entry}\n")
        f.write(f"\nTotal missing elements: {total_missing}\n")
