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

### Running in Colabs
Colabs has some issues with ChromeDriver as "Ubuntu 20.04+ no longer distributes chromium-browser outside of a snap package, you can install a compatible version from the Debian buster repository". Adding the following to your Colabs notebook
````
# https://github.com/kaliiiiiiiiii/Selenium-Profiles/issues/10#issuecomment-1387618009
%%shell
# Ubuntu no longer distributes chromium-browser outside of snap
#
# Proposed solution: https://askubuntu.com/questions/1204571/how-to-install-chromium-without-snap

# Add debian buster
cat > /etc/apt/sources.list.d/debian.list <<'EOF'
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster.gpg] http://deb.debian.org/debian buster main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster-updates.gpg] http://deb.debian.org/debian buster-updates main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-security-buster.gpg] http://deb.debian.org/debian-security buster/updates main
EOF

# Add keys
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DCC9EFBF77E11517
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A

apt-key export 77E11517 | gpg --dearmour -o /usr/share/keyrings/debian-buster.gpg
apt-key export 22F3D138 | gpg --dearmour -o /usr/share/keyrings/debian-buster-updates.gpg
apt-key export E562B32A | gpg --dearmour -o /usr/share/keyrings/debian-security-buster.gpg

# Prefer debian repo for chromium* packages only
# Note the double-blank lines between entries
cat > /etc/apt/preferences.d/chromium.pref << 'EOF'
Package: *
Pin: release a=eoan
Pin-Priority: 500


Package: *
Pin: origin "deb.debian.org"
Pin-Priority: 300


Package: chromium*
Pin: origin "deb.debian.org"
Pin-Priority: 700
EOF

# Install chromium and chromium-driver
apt-get update
apt-get install chromium chromium-driver

# Install selenium
pip install selenium
````

## Youtube Video:
[![IMAGE ALT TEXT](https://github.com/ohyicong/Google-Image-Scraper/blob/master/youtube_thumbnail.PNG)](https://youtu.be/QZn_ZxpsIw4 "Google Image Scraper")


## IMPORTANT:
Although it says so in the video, this program will not run through VSCode. It must be run in the command line.

This program will install an updated webdriver automatically. There is no need to install your own.

### Please like, subscribe, and share if you found my project helpful! 
