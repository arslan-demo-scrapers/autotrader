# Web Scraper Usage Guide

**Author:** Arslan Shakar\
**Python Version:** 3.x (Recommended: Latest Stable Version)

## Overview

This web scraper searches and extracts vehicles from [autotrader.co.uk](https://www.autotrader.co.uk). The scraper
extracts vehicle data, downloads the listed images for each vehicle, creates a **separate unique folder** for each
vehicle, and stores the images under the `autotrader/autotrader/images` directory.

It is integrated with **Gemini AI** to extract vehicle registration numbers from the images.

---

## Download

You can download the scraper project [here](https://github.com/arslan-demo-scrapers/autotrader.git)

---

## How to Setup Documentation

### Prerequisites

- **Python Version:** Ensure you have Python 3 installed.
- **IDE Recommendation:** Download and install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/).
- **Virtual Environment Setup:** Follow this [guide](https://www.geeksforgeeks.org/python-virtual-environment/) for
  installation.

---

## Step 1: Install Dependencies

1. Open PyCharm and ensure `pip` is updated to the latest version.
2. Open the terminal in PyCharm and run the following commands:

```shell
pip install Scrapy==2.5.1
pip install pillow
pip install google-generativeai
```

4. Set your project interpreter to the one where Scrapy is installed.

---

## Step 2: Running the Script

### Before Running

- Make sure you are in the correct directory:

> cd autotrader/autotrader/spiders

- Run the spider script using:

> scrapy crawl autotrader_spider

### Notes

- autotrader_spider is the name of the spider that scrapes data.
- If any library is missing, you can download and install them
  from [Here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted).

---

## Step 3: Output Location

- Scraped results will be stored in a CSV file named: `autotrader_cars.csv`
- The CSV file will be located in the output folder.
- Downloaded images will be stored in `autotrader/autotrader/images` with **unique folders for each vehicle**.

---

## Need Help?

For any queries, feel free to send me a message.

Kind regards,  
Arslan Shakar
