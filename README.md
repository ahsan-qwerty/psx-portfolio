# PSX KSE100 Index Scraper

A Python script to scrape the KSE100 index data from the Pakistan Stock Exchange (PSX) website.

## Features

- Scrapes the current KSE100 index information from the PSX website
- Extracts high, low, current value, change, and percentage change
- Saves data to a CSV file with timestamps
- Appends new data to existing CSV file for historical tracking

## Requirements

- Python 3.6+
- Required packages: requests, beautifulsoup4, pandas

## Installation

1. Clone this repository or download the script files
2. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python psx_scraper.py
```

The script will:

1. Scrape the KSE100 index data from the PSX website
2. Display the data in the console
3. Save the data to a CSV file named `kse100_data.csv`

For automated monitoring, you can set up a scheduled task or cron job to run the script at regular intervals.

## Data Format

The script collects the following information:

- Index: KSE100
- High: Highest value of the day
- Low: Lowest value of the day
- Current: Current index value
- Change: Net change in points
- Percent_Change: Percentage change
- Time: Timestamp when the data was collected

## Disclaimer

This script is for educational and personal use only. Please review the PSX website's terms of service before using the script for any commercial purpose.
