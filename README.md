# Google Image Scraper
NOTE: This is a fork of ohciyong's Google Image Scraper, designed to make it easier to run in Colabs and other notebooks.

A library created to scrape Google Images.<br>
If you are looking for other image scrapers, JJLimmm has created image scrapers for Gettyimages, Shutterstock, and Bing. <br>
Visit their repo here: https://github.com/JJLimmm/Website-Image-Scraper

## Pre-requisites:
1. Google Chrome
2. Python3 packages (Pillow, Selenium, Requests)
3. Windows OS (Other OS is not tested)

## Setup:
1. Open command prompt
2. Clone this repository (or [download](https://github.com/AndyHuh98/Google-Image-Scraper/archive/refs/heads/master.zip))
    ```
    git clone https://github.com/AndyHuh98/Google-Image-Scraper
    ```
3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```
4. Run the program
    ```
    python main.py
    ```

## Usage:
This project was created to bypass Google Chrome's new restrictions on web scraping from Google Images. 
To use it, define your desired parameters in main.py and run through the command line:

### Running the script with default parameters:
```
python main.py
```

Default arguments will be of the form: 
````
searchkeys=['cat', 'dog'] 
imagecount=5 
headless=True 
minres=(0, 0) 
maxres=(9999, 9999) 
numworkers=1 
keepfilename=False
````

### Running the script through CLI:
*replace these arguments with your own preferences*
```
python3 main.py \
    --searchkeys "cat houses" "doll houses" \
    --imagecount 50 \
    --minres 0 0 \
    --maxres 9999 9999 \
    --numworkers 1 \
    --headless
```
* `--keepfilename` can be added to keep the original URL image filenames
* `--headless` can be added to disable Chrome GUI

## Youtube Video:
[![IMAGE ALT TEXT](https://github.com/ohyicong/Google-Image-Scraper/blob/master/youtube_thumbnail.PNG)](https://youtu.be/QZn_ZxpsIw4 "Google Image Scraper")


## IMPORTANT:
Although it says so in the video, this program will not run through VSCode. It must be run in the command line.

This program will install an updated webdriver automatically. There is no need to install your own.

### Please like, subscribe, and share if you found my project helpful! 
