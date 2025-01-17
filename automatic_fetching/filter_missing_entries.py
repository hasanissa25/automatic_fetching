# Define file paths
missing_file = "missing_or_mismatched.txt"
downloaded_file = "number_of_files_in_download_directory_hasan.txt"
output_file = "need_to_fetch.txt"

# sample call:
# filter_missing_entries


# Read and parse the downloaded files
def parse_file(file_path, has_expected=False):
    data = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split(":", 1)  # Split only on the first colon
            if len(parts) < 2:
                continue  # Skip lines that don't have the expected format
            key = parts[0].strip()
            if has_expected:
                try:
                    value = int(parts[1].split()[0])
                except ValueError:
                    value = None
            else:
                value = None
            data[key] = value
    return data


def main():
    # Parse the files
    missing_data = parse_file(missing_file, has_expected=True)
    downloaded_data = parse_file(downloaded_file)

    # Filter the missing entries
    remaining_missing = []
    for key in missing_data:
        if key not in downloaded_data:
            remaining_missing.append(key)

    # Write the output
    with open(output_file, "w") as f:
        for entry in remaining_missing:
            f.write(f"{entry}\n")
