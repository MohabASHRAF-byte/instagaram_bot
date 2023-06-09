from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import os


class DownloadPost:
    def __init__(self, driver: webdriver, cnt: int, target, photoNumber):
        self.links = []
        self.target = target
        self.driver = driver
        self.cnt = cnt + 1
        self.download()
        self.idx = photoNumber

    def next_photo(self, element):
        try:
            nxt = WebDriverWait(element, 0).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'button[aria-label="Next"]')
                )
            )
            nxt.click()
            return True
        except Exception as e:
            print(f"{self.cnt - 1}'s post done", end='\n')
            e.args = "-1"
            return False

    def download_img(self, link):
        try:
            self.idx += 1
            indexed_name = f"post {self.cnt} - image {self.idx}"
            file_name = os.path.join(os.getcwd(), self.target, f"{indexed_name}.jpeg")
            print("Image downloaded successfully as:", f"{indexed_name}.jpeg")
            urllib.request.urlretrieve(link, file_name)

        except Exception as e:
            print("couldn't download the photo : ", end=' ')
            print(e.args)
            pass

    def download_single(self, is_multiple):
        try:
            img = is_multiple[0].find_element(
                By.TAG_NAME, 'img'
            )
            img_url = img.get_attribute('src')
            self.links.append(img_url)
        except Exception as e:
            print("ERROR :: it might contains video ", ": ", end=' ')
            e.args = " "
            pass

    def download_multiple(self, first_box):
        try:
            while self.next_photo(element=first_box):
                sleep(1)
                find_box = self.driver.find_element(
                    By.CLASS_NAME, '_aatk'
                )
                find_the_list = find_box.find_element(
                    By.TAG_NAME, 'ul'
                )
                find_list_elements = find_the_list.find_elements(
                    By.TAG_NAME, 'img'
                )
                for img in find_list_elements:
                    self.links.append(img.get_attribute('src'))
        except Exception as e:
            print("mul download", ": ", end=' ')
            print(e.args)
            pass

    def download(self):
        find_box = self.driver.find_element(
            By.CLASS_NAME, '_aatk'
        )
        is_multiple = find_box.find_elements(
            By.CSS_SELECTOR, 'div[role="button"]'
        )
        self.download_single(is_multiple)
        if len(is_multiple) != 1:
            self.download_multiple(first_box=find_box)

    def execute_process(self):
        if not os.path.isdir(self.target):
            os.mkdir(self.target)
        for link in set(self.links):
            self.download_img(link=link)
        return self.cnt, self.idx
