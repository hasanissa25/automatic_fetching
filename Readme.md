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
# if too much data, move them over from your pc to pc-21
    scp -r ooga.NRCan_390 ooga.NRCan_330 ooga.NRCan_580 ooga.NRCan_674 ooga.NRCan_616 ooga.NRCan_597 ooga.NRCan_561 ooga.NRCan_329 cnsnopr@pc-21:/u01/geomag_archive_ckrn/automatic_fetching/downloads && rm -r ooga.NRCan_390 && rm -r ooga.NRCan_330 && rm -r ooga.NRCan_580 && rm -r ooga.NRCan_674 && rm -r ooga.NRCan_616 && rm -r ooga.NRCan_597 && rm -r ooga.NRCan_561 && rm -r ooga.NRCan_329


# Find the actual number of files in the directory
    run this where the download directory is
    `find . -type d -exec sh -c 'echo "{}: $(find "{}" -maxdepth 1 -type f | wc -l) option elements"' \; >> number_of_files_in_download_directory.txt`
    
    scp cnsnopr@pc-21:/u01/geomag_archive_ckrn/automatic_fetching/downloads/number_of_files_in_download_directory_pc21.txt .

# Iterate over the number of files output file, and see if there is duplicated downloads (You want to combine all download directories outputs from the command above first)
    awk -F':' '{print $1}' number_of_files_in_download_directory_combined.txt | sort | uniq -d > duplicates.txt


# run check_for_missing_files comparing expected_number_of_files_per_collection vs number_of_files_in_download_directory_combined


# run filter_missing_entries to check what is actually missing
    use the above output with number_of_files_in_download_directory_pc_21