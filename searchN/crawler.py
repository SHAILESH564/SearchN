from time import time
import re
import os
from urllib.parse import urlencode
from dotenv import load_dotenv
from fake_useragent import UserAgent

from .models import SearchN

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Crawler:
    def __init__(self, tags):
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        # set up ScrapOps proxy URL
        # scrapeops_proxy = f"https://proxy.scrapeops.io/v1/?api_key={self.api_key}"
        # scrapeops_proxy = f"http://scrapeops.headless_browser_mode=true:{self.api_key}@proxy.scrapeops.io:5353"

        self.tags = [tag.strip().replace(' ','-') for tag in tags.split(',')]
        ua = UserAgent()

        options = Options()
        options.binary_location = os.getenv("CHROME_BIN", "/opt/render/project/src/chrome/opt/google/chrome/google-chrome")
        options.add_argument("--headless=new")
        # options.add_argument(f"--proxy-server={scrapeops_proxy}")
        options.add_argument("--no-sandbox")
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)

    def get_scrapeops_url(self, target_url):
        if "proxy.scrapeops.io" in target_url:
            url = target_url.replace("proxy.scrapeops.io", "nhentai.net")
            payload = {'api_key': self.api_key, 'url': url}
            new_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
            return [new_url, url]
             
        payload = {'api_key': self.api_key, 'url': target_url}
        return 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)

    def convert_to_int(self, count_element):
        # Convert the string to int eg. 1K to 1000
        regex_pattern = re.match(r'([\d.]+)([KM]?)', count_element)
        if 'K' in count_element:
            return int(float(regex_pattern.group(1)) * 1000)
        elif 'M' in count_element:
            return int(float(regex_pattern.group(1)) * 1000000)
        else:
            return int(count_element.replace(',', ''))

    # Smallest count of a tag among the given tags
    # Returns the tag with the smallest count
    def returnSmallestCountTag(self):
        if not self.tags:
            return None
        count = float('inf')
        smallest_tag = None
        print(f"Tags to search: {self.tags}")
        for tag in self.tags:
            try:
                target_url = f"https://nhentai.net/tag/{tag}/"
                proxy_url = self.get_scrapeops_url(target_url)
                # self.driver.get(f"https://nhentai.net/tag/{tag}/")
                self.driver.get(proxy_url)
                # Get the count of the tag in String
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.tag span.count"))
                )
                count_element = self.driver.find_element(By.CSS_SELECTOR, "a.tag span.count")
                # Convert the count to an integer
                tag_count = self.convert_to_int(count_element.text)
                if tag_count is not None and tag_count < count:
                    count = tag_count
                    smallest_tag = tag
            
            except Exception as e:
                print(f"Error fetching tag {tag}: {str(e)}")
                continue
        return smallest_tag
                
    def get_last_pageNumber(self):
        try:
            # self.driver.get(f"https://nhentai.net/tag/{tag}/")
            # Wait for the page to load and find the last page number
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "last"))
            )
            last_page_element = self.driver.find_element(By.CLASS_NAME, "last").get_attribute("href")
            last_page_number_re =  re.search(r"page=(\d+)", last_page_element)

            last_page_number = int(last_page_number_re.group(1)) if last_page_number_re else 1
        except Exception as e:
            last_page_number = 1
        print(f"Last page number: {last_page_number}")
        return last_page_number

        

    def search_main_tag(self, tag):
        page = 1
        result = {}
        # self.driver.get(f"https://nhentai.net/tag/{tag}/?page={page}")
        target_url = f"https://nhentai.net/tag/{tag}/?page={page}"
        proxy_url = self.get_scrapeops_url(target_url)
        self.driver.get(proxy_url)
        last_page_number = self.get_last_pageNumber()
        while page <= last_page_number:
            try:
                # self.driver.get(f"https://nhentai.net/tag/{tag}/?page={page}")
                target_url = f"https://nhentai.net/tag/{tag}/?page={page}"
                proxy_url = self.get_scrapeops_url(target_url)
                self.driver.get(proxy_url)
                WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,".container .gallery a.cover"))
                )
            
            except Exception as e:
                print(f"⚠️ Timeout waiting for galleries on page {page}")
                page += 1
                continue

            # All the photos urls
            urls = self.driver.find_elements(By.CSS_SELECTOR, ".container .gallery a.cover")
            for url in urls:
                try:
                    name = url.find_element(By.CLASS_NAME, "caption").text
                    link = url.get_attribute("href")
                    src = url.find_element(By.TAG_NAME, "img").get_attribute("data-src")
                    manga_id = re.search(r'(\d+)', link).group(1)
                    # Open a new tab
                    scraped_link, link = self.get_scrapeops_url(link)
                    self.driver.execute_script("window.open(arguments[0]);", scraped_link)
                    self.driver.switch_to.window(self.driver.window_handles[1])

                    # Wait for the image to load
                    WebDriverWait(self.driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#tags .tag-container")))
                    # Contains all tags eg. language, paradies, translated, etc.
                    tag_container = self.driver.find_elements(By.CSS_SELECTOR, "#tags .tag-container")
                    # temptag = self.tags[:]  #Create a deep copy
                    found_tags = set()  # Create a set for faster lookup

                    for tag_element in tag_container:
                        if "Tags:" in tag_element.text:
                            tags_found = tag_element.find_elements(By.CSS_SELECTOR, "span.tags a.tag .name")
                            for tag_el in tags_found:
                                # tag_text = tag_el.text.strip().replace(" ",'-')
                                found_tags.add(tag_el.text.strip().replace(" ", "-"))
                        # if empty means all the tags are present as intended
                    if not set(self.tags) - found_tags:
                        result[manga_id] = [name, link, src]
                        SearchN.objects.create(
                            name=name,
                            link=link,
                            url=src,
                            is_remote=src.startswith('http')
                        )
                        print(f"Found: {name} - {link} - {src}")
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                except Exception as e:
                    print(f"⚠️ Error fetching gallery details on page {page}: {e}")
                    page += 1
                    continue
            page += 1
        # return result
        