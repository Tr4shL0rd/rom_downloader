ROM Downloader Script

This Python script is designed to download and manage ROM files for RetroPie emulators. By connecting to a server hosting ROM files, it retrieves a list of available directories and files, allowing the user to download all or specific ROM sets with options for file organization.
Prerequisites

    Python 3.x
    Dependencies:
        requests – for server communication
        BeautifulSoup – for HTML parsing
        wget – for handling downloads with a custom progress bar
        dotenv – for loading environment variables from a .env file
        zipfile – for unzipping ROM archives

Install dependencies with:

bash

pip install requests beautifulsoup4 wget python-dotenv

Setup

    Server Configuration:
        Ensure your server hosts ROM files in an accessible format.
        Place directories inside the ROM directory in the server (e.g., misc/, psx/).

    Environment Variables:
        Create a .env file with the following variables:

        plaintext

        SERVER_IP=your.server.ip.address
        SERVER_PORT=your_server_port

    Set up Directory:
        Specify a download directory for ROM files (default is RetroPie/roms/).

Usage

Run the script with:

bash

python3 rom_downloader.py

The script performs the following tasks:

    Server Connection: Checks connectivity to the server.
    Directory Retrieval: Gets the list of available directories for ROMs on the server.
    File Management:
        Choose a specific directory to download from, or download all available ROMs.
        Files are downloaded and saved in the appropriate subdirectories within the ROM directory.
    Unzipping: Automatically unzips ROM files when needed (e.g., .zip archives).

Key Functions

    test_connect(): Tests server connection.
    get_dirs(): Retrieves directories from the server.
    download_file(files, directory): Downloads a list of files from a given directory.
    bulk_download(dirs): Downloads all files from all available directories.
    dir_choice(directories): Allows the user to select a directory from the list.

Troubleshooting

If the script fails to connect to the server, check:

    Server IP and Port in .env file.
    Internet connection and server accessibility.

Warnings

    Path Issues: If the specified download path (DIST) is not found, you’ll be prompted to continue or exit.
    Compatibility: Certain ROMs (e.g., PSX) may not work on the Arcade.

License

MIT License