# Google Image Scraper
NOTE: This is a fork of ohciyong's Google Image Scraper, designed to make it easier to run in Colabs and other notebooks.

A library created to scrape Google Images.<br>
If you are looking for other image scrapers, JJLimmm has created image scrapers for Gettyimages, Shutterstock, and Bing. <br>
Visit their repo here: https://github.com/JJLimmm/Website-Image-Scraper

## Setup and Execution
### Pre-requisites:
1. Google Chrome
2. Python3 packages (Pillow, Selenium, Requests)
3. Windows OS (Other OS is not tested)

### Setup:
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

### Usage:
This project was created to bypass Google Chrome's new restrictions on web scraping from Google Images. 
To use it, define your desired parameters in main.py and run through the command line:

#### Running the script with default parameters:
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

#### Running the script through CLI:
*replace these arguments with your own preferences*
```
python3 main.py \
    --searchkeys "cat houses" "doll houses" \
    --imagecount 50 \
    --minres 0 0 \
    --maxres 9999 9999 \
    --numworkers 1 \
    --headless \
    --colabs
```
* `--keepfilename` can be added to keep the original URL image filenames
* `--headless` can be added to disable Chrome GUI

#### Running in Colabs
Add the following cells:

````
# Initialize scraper
!git clone https://github.com/AndyHuh98/Google-Image-Scraper
!pip install -r Google-Image-Scraper/requirements.txt
````

````
# Execute Image Scraper
!cd Google-Image-Scraper/ && git pull && rm -rf photos && python3 main.py \
    --searchkeys "cat houses" "doll houses" \
    --imagecount 15 \
    --minres 0 0 \
    --maxres 9999 9999 \
    --numworkers 1 \
    --headless
````

### Youtube Video:
[![IMAGE ALT TEXT](https://github.com/ohyicong/Google-Image-Scraper/blob/master/youtube_thumbnail.PNG)](https://youtu.be/QZn_ZxpsIw4 "Google Image Scraper")


### IMPORTANT:
Although it says so in the video, this program will not run through VSCode. It must be run in the command line.

This program will install an updated webdriver automatically. There is no need to install your own.

## How does it work?
Somewhat sequential step by step of the key parts of the script execution. Note that some of these functions may change names, and documentation may go out of date - however, this is my best attempt to track what this script is doing (because the code is not clean whatsoever).

### Initializing Colabs Webdriver
The Python script first runs `initialize_colabs_webdriver` to get around Colabs Chromedriver errors. If not a Colabs environment, it downloads the latest Chromedriver later on.

### Scraper execution
After attempting to initialize Colabs webdriver:
* the script creates a `photos` folder within the package itself to hold the scraped images.
* the script takes in the command line arguments parsed (or the default values for the arguments) to initialize the GoogleImageScraper
* begins execution across available threads, of the `worker_threads` method which takes in the `search_keys` from the CLI arguments.
* each function call of `worker_threads`:
  * instantiates a `GoogleImageScraper` using accessible variables assigned in the main method scope, for each `search_key`.
  * finds image URLs using the GoogleImageScraper in one step
  * downloads the full list of image URLs using the GoogleImageScraper in the second step
* releases resources at the end of execution

### GoogleImageScraper internals
If the environment isn't Colabs, during instantiation, the GoogleImageScraper class attempts to initialize the webdriver and download the latest version.

#### Instantiation
Nothing out of the ordinary here, outside of one key part where it sets the base URL to execute the image scraping from. 

````
self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
````

The current query parameters are as follows:
* `q`: This parameter specifies the search query. In this case, the value is "cats", indicating that the search is for images related to cats.
* `source`: This parameter represents the source of the search. In this case, the value is "lnms", which stands for "linked normal search". It indicates that the search was initiated from the normal web search page.
* `tbm`: This parameter specifies the type of search being performed. In this case, the value is "isch", which stands for "image search". It indicates that the search is for images.
* `sa`: This parameter contains additional search parameters or settings. The value "X" in this case doesn't have a specific meaning as it could be a unique identifier or a generic value used by Google's search engine.
* `ved`: This parameter represents a version identifier for tracking purposes. The value "2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw" is specific to the session or request and doesn't have a meaningful interpretation outside of Google's internal systems.
* `biw` and `bih`: These parameters specify the browser window width and height, respectively, in pixels. In this case, the values are "1920" for the browser window width and "947" for the browser window height.

#### `find_image_urls`
This method returns a list of image urls for a search query from Google.

The basis of this method revolves around the following XPath expression: `xpath_expression = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'`. [XPath](https://en.wikipedia.org/wiki/XPath), at least to my understanding, can just be read somewhat like a regular path - each "selector" is separated by a `/` and represents a child node element of the previous element. There are some special specifiers that I'm not familiar with, but this one basically says:

1. `//*` - find any element of any type in the document that matches the subsequent steps of the expression.
2. `[@id="islrg"]` - gets an element with the id `islrg`
   ![](./documentation/isLrg.png)
3. `div[1]` - gets the first child `div` of the element above.
   ![](./documentation/div[1]%20of%20islrg.png)


