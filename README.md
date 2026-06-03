# Supermarche-Prix-Scraper

A Python-based supermarket scraper designed to collect product data from French online supermarkets using Playwright, SeleniumBase, and BeautifulSoup.

The project focuses on handling modern anti-bot protections (such as Cloudflare), infinite scrolling pages, and large product catalogs while maintaining good scraping performance.


## Current Supported Supermarkets
- Super U (coursesu.com)
- Intermarche (in progress)


## Python libraries used
- Playwright
- SeleniumBase
- BeautifulSoup4


## Usage

Run the scraper:

- python main.py

The scraper will:

- Open a Chromium browser
- Connect Playwright through CDP
- Accept cookies automatically
- Scroll through supermarket categories
- Extract product information
- Save data to CSV

## Performance Optimizations

This scraper includes several optimizations for large supermarket pages:

- Blocking unnecessary assets (images/fonts/media)
- Incremental infinite scrolling
- Partial DOM cleanup
- Fast extraction using BeautifulSoup instead of repeated Playwright locator calls

## Disclaimer

This project is intended for:

- educational purposes
- research
- price analysis
- personal use

Please respect the target website's terms of service and local laws regarding web scraping.

## Future Improvements

Planned improvements include:

- SQLite database support
- Multi-supermarket support
- Parallel scraping
- Creation of a UI 

## Licence
MIT License
