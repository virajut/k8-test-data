
from .base import BaseScraper
import urllib.request, urllib.error, urllib.parse
from time import sleep
from urllib.error import URLError
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException




class Scraper(BaseScraper):
    def __init__(self):

        self.base_url = "https://cloud.corvusforensics.com"
        self.url = 'https://cloud.corvusforensics.com/s/HDcCHLnQTGBnYBN'



    def scrape_file(self):
        cwd = os.getcwd()
        download_path = cwd + "/test"
        isFile = os.path.isdir(download_path)
        if (not isFile):
            os.mkdir(download_path, 0o777);
        newfile = open('zipfiles.txt', 'w')
        print("Running script.. ")
        extension = ".zip"
        html = None

        browser = webdriver.Chrome()
        browser.get(self.url)
        try:
            sleep(10);
        except TimeoutException:
            print('Loading took too much time!')
        else:
            html = browser.page_source
        finally:
            browser.quit()

        soup = BeautifulSoup(html, features="lxml")
        soup.prettify()
        gdp_table = soup.find("table", attrs={"class": "list-container"})
        gdp_table_data = gdp_table.tbody.find_all("tr")  # contains 2 rows

        for td in gdp_table_data:
            x = td.find_all("td")
            zip_url = x[1].find_all("a")[0]['href']
            links = self.base_url + zip_url
            if links.endswith(extension):
                newfile.write(links + '\n')
        newfile.close()

        newfile = open('zipfiles.txt', 'r')
        for line in newfile:
            print(line + '/n')
        newfile.close()
        self.save(download_path)

        return download_path

    def save(self,path):
        with open('zipfiles.txt', 'r') as url:
            for line in url:
                if line:
                    try:
                        ziplink = line
                        # Removes the first 48 characters of the url to get the name of the file
                        zipfile = line[48:]
                        # Removes the last 4 characters to remove the .zip
                        zipfile2 = zipfile[:3]
                        print("Trying to reach " + ziplink)
                        response = urllib.request.urlopen(ziplink)
                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print('We failed to reach a server.')
                            print('Reason: ', e.reason)
                            continue
                        elif hasattr(e, 'code'):
                            print('The server couldn\'t fulfill the request.')
                            print('Error code: ', e.code)
                            continue
                    else:
                        zipcontent = response.read()
                        completeName = os.path.join(path, zipfile2 + ".zip")
                        with open(completeName, 'wb') as f:
                            print("downloading.. " + zipfile)
                            f.write(zipcontent)
                            f.close()
        print("Script completed")

