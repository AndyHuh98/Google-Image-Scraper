# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020
Forked on Sat Jul 1 20:10:25 2023

@author: OHyic
@modified-by: AndyHuh98

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
from GoogleImageScraperCommandParser import *
from patch import webdriver_executable
import subprocess

def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        image_path, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed,
        is_colabs)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)

    #Release resources
    del image_scraper

def initialize_colabs_webdriver(webdriver_path, is_colabs):
    if not is_colabs:
        print("[INFO] Environment is not colabs, initializing webdriver following normal procedure and not using Colabs compatible distribution at {}.".format(webdriver_path))
        return
    
    try:
        if not os.path.exists(webdriver_path):
            webdriver_init_script_path = './initialize-webdriver.sh'
            os.chmod(webdriver_init_script_path, 0o111)
            subprocess.run(webdriver_init_script_path, shell=True, check=True)
            print(f"Webdriver initialized at webdriver_path: {webdriver_path}")
        else:
            print("[INFO] Webdriver already exists at {}".format(webdriver_path))
    except Exception as e:
        print("[ERROR] Error when attempting to initialize webdriver.")

if __name__ == "__main__":
    #Get arguments from CLI
    parser = initialize_parser()
    args = parse_args(parser)

    #Define file path
    is_colabs = args.colabs
    if is_colabs:
        webdriver_path = "/usr/bin/chromedriver"
    else:
        webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    initialize_colabs_webdriver(webdriver_path, is_colabs)

    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys = list(set(args.searchkeys))

    #Parameters
    number_of_images = args.imagecount               # Desired number of images
    headless = args.headless                     # True = No Chrome GUI
    min_resolution = (int(args.minres[0]), int(args.minres[1]))             # Minimum desired image resolution
    max_resolution = (int(args.maxres[0]), int(args.maxres[1]))       # Maximum desired image resolution
    max_missed = 10                   # Max number of failed images before exit
    number_of_workers = args.numworkers               # Number of "workers" used
    keep_filenames = args.keepfilename            # Keep original URL image filenames

    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    #Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)
