# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:01:02 2020

@author: OHyic
"""
#import selenium drivers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#import helper libraries
import time
from urllib.parse import urlparse
import os
import requests
import io
from PIL import Image
import re

#custom patch libraries
import patch

class GoogleImageScraper():
    def __init__(self, webdriver_path, image_path, search_key="cat", number_of_images=1, headless=True, min_resolution=(0, 0), max_resolution=(1920, 1080), max_missed=10, is_colabs=False):
        #check parameter types
        image_path = os.path.join(image_path, search_key)
        if (type(number_of_images)!=int):
            print("[Error] Number of images must be integer value.")
            return
        if not os.path.exists(image_path):
            print("[INFO] Image path not found. Creating a new folder.")
            os.makedirs(image_path)
            
        #check if chromedriver is installed and install it if not (this is the normal, non Colabs procedure)
        if (not os.path.isfile(webdriver_path) and not is_colabs):
            print("[INFO] Downloading latest chromedriver as part of normal, non Colabs execution.")
            is_patched = patch.download_lastest_chromedriver()
            if (not is_patched):
                exit("[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

        for i in range(1):
            try:
                options = Options()
                if(headless):
                    print("Adding --headless option")
                    options.add_argument('--headless')
                # Fixes `unknown error: DevToolsActivePort file doesn't exist`.
                # https://stackoverflow.com/questions/50642308/webdriverexception-unknown-error-devtoolsactiveport-file-doesnt-exist-while-t
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--remote-debugging-port=9222')
                driver = webdriver.Chrome(executable_path=webdriver_path, chrome_options=options)
                driver.set_window_size(1400,1050)
                #try going to www.google.com
                driver.get("https://www.google.com")
                try:
                    print("Trying WebDriverWait...")
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()
                except Exception as e:
                    print(f"Exception waiting for element to be clickable: {e}")
                    continue
            except Exception as e:
                print(f"Exception initializing chrome driver: {e}")
                #update chromedriver
                pattern = '(\d+\.\d+\.\d+\.\d+)'
                version = list(set(re.findall(pattern, str(e))))[0]
                is_patched = patch.download_lastest_chromedriver(version)
                if (not is_patched):
                    exit("[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.webdriver_path = webdriver_path
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
        self.headless=headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.max_missed = max_missed

    def find_image_urls(self):
        """
            This function search and return a list of image urls based on the search key.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls = google_image_scraper.find_image_urls()

        """
        print("[INFO] Gathering image links")
        self.driver.get(self.url)
        image_urls=[]
        missed_count = 0
        indx_1 = 0
        indx_2 = 0
        xpath_expression = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'
        time.sleep(1)
        while self.number_of_images > len(image_urls) and missed_count < self.max_missed:
            print("------------------------------------")
            element_found = False
            if indx_2 == 0:
                try:
                    print("[INFO] Attempting to find element using regular xpath_expression.")
                    img_element = self.driver.find_element(By.XPATH, xpath_expression%(indx_1+1))
                    img_element.click()
                    missed_count = 0
                    indx_1 = indx_1 + 1    
                    element_found = True
                except Exception as e:
                    print(f"[ERROR] Exception finding image element using xpath_expression, structure of page may have changed: {e}")
                    try:
                        print("[INFO] Attempting to find image using an extra nested div child. If successful, set xpath_expression to contain the extra nested child for future searches.")
                        img_element = self.driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'%(indx_1,indx_2+1))
                        img_element.click()
                        missed_count = 0
                        indx_2 = indx_2 + 1
                        xpath_expression = '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                        element_found = True
                    except Exception as e:
                        print(f"[ERROR] Exception finding image element using xpath_expression with an extra nested div child. Adding to miss count. {e}")
                        indx_1 = indx_1 + 1
                        missed_count = missed_count + 1
            else:
                try:
                    print("[INFO] Attempting to find element using modified xpath_expression with an extra nested div child.")
                    img_element = self.driver.find_element(By.XPATH, xpath_expression%(indx_1, indx_2))
                    img_element.click()
                    indx_2 = indx_2 + 1
                    missed_count = 0
                    element_found = True
                except Exception as e:
                    print(f"[ERROR] Exception finding image element using modified xpath_expression: {e}")
                    try:
                        print("[INFO] Attempting to get the next image element in the results instead using modified xpath_expression.")
                        img_element = self.driver.find_element(By.XPATH, xpath_expression%(indx_1+1, indx_2))
                        img_element.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                        element_found = True
                    except Exception as e:
                        print(f"[ERROR] Failed to get the next image element as well. Skipping this iteration and adding to the miss count: {e}")
                        indx_2 = indx_2 + 1
                        missed_count = missed_count + 1
            if element_found:
                try:
                    print("[INFO] Attempting to select image from popup after clicking.")
                    #select image from the popup
                    time.sleep(0.1)
                    class_names = ["iPVvYb","r48jcc","pT0Scc"]
                    images = []
                    for class_name in class_names:
                        elements = self.driver.find_elements(By.CLASS_NAME, class_name)
                        if elements:
                            images = elements
                            break

                    for image in images:
                        src_link = image.get_attribute("src")
                        if src_link.startswith("http") and "encrypted" not in src_link:
                            print(f"[INFO] {self.search_key} \t #{len(image_urls)} \t {src_link}")
                            image_urls.append(src_link)
                            print("[INFO] Image found.")
                            break
                except Exception as e:
                    print(f"[ERROR] Exception getting link from image popup: {e}")

                try:
                    #scroll page to load next image
                    if(len(image_urls)%15==0):
                        self.driver.execute_script("window.scrollTo(0, "+str(indx_1*60)+");")
                        print("[INFO] Loading next page")
                        time.sleep(0.1)
                except Exception as e:
                    print(f"[ERROR] Exception when scrolling: {e}")
                    time.sleep(0.1)
            else:
                print("[INFO] Element not found, skipping iteration.")

        self.driver.quit()
        print("[INFO] Google search ended")
        print("\n\n\n\n")
        return image_urls

    def save_images(self,image_urls, keep_filenames):
        #save images into file directory
        """
            This function takes in an array of image urls and save it into the given image path/directory.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls=["https://example_1.jpg","https://example_2.jpg"]
                google_image_scraper.save_images(image_urls)

        """
        print("[INFO] Saving images, please wait...")
        for indx,image_url in enumerate(image_urls):
            try:
                print("------------------------------------")
                print("[INFO] Image url:%s"%(image_url))
                filename_base = self.search_key.replace(' ', '_')
                image = requests.get(image_url,timeout=5)
                if image.status_code == 200:
                    print("[INFO] Image retrieved for {}_{}".format(self.search_key, indx))
                    try:
                        with Image.open(io.BytesIO(image.content)) as image_from_web:
                            try:
                                print("[INFO] Generating local filename...")
                                if (keep_filenames):
                                    #extact filename without extension from URL
                                    parsed_url = urlparse(image_url)
                                    image_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                                    name = os.path.splitext(os.path.basename(image_url))[0]
                                    #join filename and extension
                                    filename = "%s.%s"%(name,image_from_web.format.lower())
                                else:
                                    try:
                                        filename = "%s_%s.%s"%(filename_base,str(indx),image_from_web.format.lower())
                                        print("[INFO] Generated filename as:", filename)
                                    except Exception as e:
                                        print("[ERROR] error generating local filename:", e)

                                print("[INFO] Generating local path for file...")
                                image_path = os.path.join(self.image_path, filename)
                                print(
                                    f"[INFO] {self.search_key} \t {indx} \t Image saved at: {image_path}")
                                try:
                                    image_from_web.save(image_path)
                                except Exception as e:
                                    print("[ERROR] Saving image failed: ", e)
                            except Exception as e:
                                print(f"[ERROR] Exception encountered while extraction or saving image: {e}")
                                rgb_im = image_from_web.convert('RGB')
                                rgb_im.save(image_path)
                            image_resolution = image_from_web.size
                            if image_resolution != None:
                                if image_resolution[0]<self.min_resolution[0] or image_resolution[1]<self.min_resolution[1] or image_resolution[0]>self.max_resolution[0] or image_resolution[1]>self.max_resolution[1]:
                                    image_from_web.close()
                                    os.remove(image_path)

                            image_from_web.close()
                    except Exception as e:
                        print("[ERROR] Opening image file failed: ", e)
                else:
                    print("[INFO] Image request failed with status code {} and reason {}".format(image.status_code, image.reason))
            except Exception as e:
                print("[ERROR] Download failed: ", e)
                pass
        print("--------------------------------------------------")
        print("[INFO] Downloads completed. Please note that some photos were not downloaded as they were not in the correct format (e.g. jpg, jpeg, png)")
