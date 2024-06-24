#!/bin/bash

check_package_installed() {
    if ! command -v "$1" &> /dev/null; then
        return 1
    else
        return 0
    fi
}

# Function to install a package
install_package() {
    if [ -n "$(command -v apt-get)" ]; then
        sudo apt-get update
        sudo apt-get install -y "$1"
    elif [ -n "$(command -v yum)" ]; then
        sudo yum install -y "$1"
    else
        echo "Package installation failed. Unsupported package manager."
        exit 1
    fi
}

# Check if unzip is installed, and install it if needed
if ! check_package_installed "unzip"; then
    echo "unzip is not installed. Attempting to install..."
    install_package "unzip"
else
    printf "\n"
    echo "================================="
    echo "unzip is installed. Proceeding..."
fi

# Check if unrar is installed, and install it if needed
if ! check_package_installed "unrar"; then
    echo "unrar is not installed. Attempting to install..."
    install_package "unrar"
else
    echo "unrar is installed. Proceeding..."
    echo "================================="
    printf "\n" 
fi


# Specify the URL of the compressed file you want to download
compressed_url=""
download_type=""

# Function to download and extract a file
download_and_extract() {
    url="$1"
    extension="$2"

    # Extract the filename from the URL
    filename=$(basename "$url").$extension

    # Download the compressed file
    wget "$url" -O "$filename"

    # Check if the download was successful
    if [ $? -eq 0 ]; then
        echo "Download successful!"

        # Extract the downloaded file based on the extension
        if [ "$extension" == "zip" ]; then
            printf "\n"
            echo "Unzipping $filename"
            echo "================================="
            printf "\n"
            unzip "$filename"
            
            printf "\n"
            echo "================================="
            echo "Moving files..."
            mv MiniLibriMix/train/ ./train/ 
            mv MiniLibriMix/val/ ./val/
            echo "Successfully moved files to ./train/ & ./val/"
            echo "================================="
            printf "\n"

        elif [ "$extension" == "rar" ]; then
            printf "\n"
            echo "================================="
            echo "Extracting $filename"
            
            unrar x "$filename" ./test/
            
        else
            echo "Unsupported file format: $extension"
        fi

        # Check if the extraction was successful
        if [ $? -eq 0 ]; then
            echo "Successfully extracted files to ./test/"
            echo "================================="
            printf "\n"

        else
            echo "Extraction failed."
            echo "================================="
            printf "\n"

        fi

        # Clean up the downloaded compressed file
        echo "Deleting $filename"
        rm "$filename"
        printf "\n"
    else
        echo "Download failed."
        print "\n"
    fi
}

# Download and extract RAR file
printf "=====================Getting Libri2Mix (first 250)=====================\n"
compressed_url="https://www.dropbox.com/scl/fi/h4099j5hs9ff6kz4783qs/test-250.rar?rlkey=a5eozcr4sjni6xw58fjirep3r"
download_type="rar"
download_and_extract "$compressed_url" "$download_type"

# Download and extract ZIP file
printf "========================Getting MinLibriMix=======================\n"
printf "=====================NOTE: Zenodo.org is slow=====================\n"
compressed_url="https://zenodo.org/record/3871592/files/MiniLibriMix.zip"
download_type="zip"
download_and_extract "$compressed_url" "$download_type"


