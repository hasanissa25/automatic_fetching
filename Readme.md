# Find the collection links, which we will download images from. 

`fetch_collection_urls --cores 16 -p 69`
  
Output file:
-       https://nrcan.canadiana.ca/view/ooga.NRCan_211
        https://nrcan.canadiana.ca/view/ooga.NRCan_201
        https://nrcan.canadiana.ca/view/ooga.NRCan_204
        https://nrcan.canadiana.ca/view/ooga.NRCan_210
    

# Get expected number of files for each collection

`clear && get_number_of_files_for_each_collection --urls_file links_to_collections.txt --cores 16`


# Download files using the collection links file

`nohup fetch_images --urls_file missing_links.txt --cores 16 &> fetching_images.log &`

Output file:
    downloads/*


# Find the actual number of files in the directory
    run this where the download directory is
    `find . -type d -exec sh -c 'echo "{}: $(find "{}" -maxdepth 1 -type f | wc -l) option elements"' \; >> number_of_files_in_download_directory.txt`
# Iterate over the number of files output file, and see if there is duplicated downloads (You want to combine all download directories outputs from the command above first)
    awk -F':' '{print $1}' number_of_files_in_download_directory_combined.txt | sort | uniq -d > duplicates.txt




# run check_for_missing_files comparing expected_number_of_files_per_collection vs number_of_files_in_download_directory_combined