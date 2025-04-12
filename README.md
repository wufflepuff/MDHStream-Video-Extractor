# MDHStream Video Extractor

This Python script uses Selenium and yt-dlp to search for videos on `mdhstream.cc` and download them. It allows downloading all videos from a search result, a specific range, or individually selected videos.

## Features

*   Search for videos by actor or title on `mdhstream.cc`.
*   Scrape video titles and page URLs from search results across multiple pages.
*   Multiple download modes:
    *   Download all found videos.
    *   Download a specific range of videos (e.g., 10-25).
    *   Download specific videos by their index number (e.g., 1, 5, 12).
*   Extracts the direct video URL from the video page using various methods.
*   Uses `yt-dlp` for downloading the videos, showing progress percentage.
*   Checks if a video file (based on title) already exists in the target directory to avoid re-downloads.
*   Saves downloads into a subdirectory named after the (sanitized) search term within the configured base download path.
*   Configuration file (`config.json`) for persistent settings:
    *   Interface language (English/German).
    *   Base download path.
    *   Optional path to uBlock Origin extension.
*   Supports English and German languages for the user interface.
*   Optionally uses uBlock Origin (if path provided) to potentially block ads during scraping in the headless browser.
*   Interactive command-line menu for searching, settings, and exiting.

## Requirements

*   **Python 3:** Make sure Python 3 is installed and added to your system's PATH. You can download it from [python.org](https://www.python.org/).
*   **Selenium:** Install the Python package using pip:
    ```sh
    pip install selenium
    ```
*   **Mozilla Firefox:** The script is configured to use Firefox via Selenium WebDriver (geckodriver). Ensure Firefox is installed. `geckodriver` usually comes with the `selenium` package or can be installed separately and added to your PATH if needed (see [geckodriver releases](https://github.com/mozilla/geckodriver/releases)).
*   **yt-dlp:** A powerful command-line video downloader.
    *   Download the latest release executable (`yt-dlp.exe` for Windows, `yt-dlp` for Linux/macOS) from the [yt-dlp GitHub repository](https://github.com/yt-dlp/yt-dlp/releases).
    *   Ensure the executable is placed either:
        *   In the same directory as the `main.py` script.
        *   In a directory listed in your system's PATH environment variable.

## Configuration

The script uses a `config.json` file in the same directory to store settings. If the file doesn't exist, it will be created with default values when you first run the script.

```json
// filepath: config.json
{
    "language": "en",
    "download_path": ".",
    "ublock_path": ""
}
```

*   **`language`**: Sets the interface language. Can be `"en"` for English or `"de"` for German. If `null` or missing on the first run, you will be prompted to choose.
*   **`download_path`**: The base directory where search-term-specific subfolders will be created for downloads. Defaults to the current directory (`.`) where the script is run. Use absolute paths for clarity (e.g., `"C:\\Users\\YourUser\\Downloads\\MDHStream"` or `"/home/youruser/videos/mdhstream"`).
*   **`ublock_path`**: Optional. Provide the full path to a uBlock Origin `.xpi` file (e.g., `"C:\\Path\\To\\ublock_origin-1.xx.x.xpi"`). If set and the file exists, the script will attempt to load it into the headless browser instance. This might help prevent ads from interfering with scraping but is not guaranteed to work perfectly in all headless environments. Leave empty (`""`) if not used.

## Usage

1.  Ensure all requirements listed above are installed and configured (Python, Selenium, Firefox, yt-dlp in PATH or script directory).
2.  Place the `main.py` script in a directory.
3.  (Optional) Create a `config.json` file in the same directory or let the script create it on first run. Edit it to set your preferred download path.
4.  Open a terminal or command prompt, navigate to the directory containing `main.py`, and run the script:
    ```sh
    python main.py
    ```
5.  **First Run:** If no language is set in `config.json`, you'll be prompted to choose between English and German. This choice will be saved.
6.  **Main Menu:** You will see the main menu:
    *   Choose `1` to start a search and the download process.
    *   Choose `2` to access the settings menu (change language, download path, uBlock path).
    *   Choose `3` to exit the script.
7.  **Search & Download (Option 1):**
    *   Enter your search term (e.g., an actor's name or video title).
    *   The script will connect to the site and fetch the total number of videos found for your search.
    *   Choose a download mode:
        *   `1`: Download all videos found.
        *   `2`: Download a range (e.g., `10-25`). Enter the start and end numbers.
        *   `3`: Download specific videos (e.g., `1, 5, 12`). Enter the numbers separated by commas.
    *   The script will scrape the necessary video metadata (titles and page URLs). This might take some time, especially for a large number of videos.
    *   The download process will begin for the selected videos:
        *   It checks if a file with a similar name already exists in the target folder (`your_download_path/your_search_term/`). If found, it skips the download.
        *   It extracts the video URL from the video's page.
        *   It uses `yt-dlp` to download the video, showing the progress percentage.
        *   A summary of successful, skipped, and failed downloads is shown at the end.
    *   Press Enter to return to the main menu after the process finishes.
8.  **Settings (Option 2):**
    *   Allows you to change the interface language, the base download path, and the path to the uBlock Origin `.xpi` file.
    *   Changes are saved to `config.json`.
    *   Choose `4` to return to the main menu.

## Notes

*   **Website Changes:** Web scraping scripts are sensitive to changes in the target website's structure (`mdhstream.cc`). If the site updates its layout, the script might stop working correctly and will need to be updated.
*   **yt-dlp Updates:** Keep `yt-dlp` updated to ensure compatibility with video streaming formats and site changes. You can usually update it by running `yt-dlp -U` in your terminal.
*   **Headless Browser:** The script uses Firefox in headless mode, meaning you won't see the browser window.
*   **Legality:** Be aware of the copyright laws in your country. Downloading copyrighted material without permission may be illegal. Use this script responsibly and at your own risk.
