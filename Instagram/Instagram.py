from Instagram.Constraints import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium import webdriver
import os
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random as rand
import time
# from bs4 import BeautifulSoup
# import requests
import urllib.request


class Instagram(webdriver.Chrome):
    def __init__(self, driver_path=chrome_path):
        self.links = []
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super(Instagram, self).__init__()
        self.implicitly_wait(15)
        self.cnt = 1
        self.maximize_window()
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        sleep(5)
        self.quit()
        self.end_time = time.time()
        elapsed_time_seconds = self.end_time - self.start_time
        elapsed_minutes = int(elapsed_time_seconds // 60)
        elapsed_seconds = int(elapsed_time_seconds % 60)
        GREEN = '\033[32m'
        print(GREEN + "Time elapsed: {} minutes {} seconds".format(elapsed_minutes, elapsed_seconds))

    def get_land_page(self):
        self.get(BASE_URL)

    def login_with_account(self, user, pas):
        user_input = WebDriverWait(self, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Phone number, username, or email']"))
        )
        password_input = self.find_element(By.CSS_SELECTOR, "input[aria-label='Password']")
        login_btn = self.find_element(By.CSS_SELECTOR, "button[type='submit']")
        user_input.send_keys(user)
        password_input.send_keys(pas)
        sleep(1)
        login_btn.click()

    def login_with_facebook(self, user, pas):
        login_with_facebook_btn = WebDriverWait(self, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, '_ab37'))
        )
        # sleep(1)
        login_with_facebook_btn.click()
        #
        facebook_user = WebDriverWait(self, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]'))
        )
        # sleep(1)
        facebook_user.send_keys(user)
        # sleep(1)
        facebook_password = self.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        facebook_password.send_keys(pas)
        # sleep(1)
        facebook_login_btn = self.find_element(By.ID, 'loginbutton')
        facebook_login_btn.click()

    def login(self, way, user, password):
        if way == 1:
            self.login_with_account(user, password)
        elif way == 2:
            self.login_with_facebook(user=user, pas=password)

    def move_to_profile(self, target):
        try:
            save_data_btn = WebDriverWait(self, 3).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'yWX7d'), "Not Now")
            )
            save_data_btn.click()
        except Exception as e:
            print("not now didn't appear")

        WebDriverWait(self, 180).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'button[type="button"]'), "Save Info")
        )
        search_btn = self.find_element(
            By.CSS_SELECTOR, 'svg[aria-label="Search"]'
        )
        search_btn.click()
        sleep(1)
        search_input = self.find_element(
            By.CSS_SELECTOR, 'input[aria-label="Search input"]'
        )
        search_input.send_keys(target)
        sleep(3)
        choose_account = self.find_element(
            By.CSS_SELECTOR, f'a[href="/{target}/"]'
        )
        choose_account.click()
        sleep(5)

    def follow_account(self, choice):
        sleep(5)
        if choice == 3:
            return
        follow_btn = self.find_element(
            By.CSS_SELECTOR, 'button[type="button"]'
        ).find_element(
            By.CLASS_NAME, 'x9f619'
        ).find_element(
            By.CLASS_NAME, '_aacl'
        )
        if follow_btn.text == "Follow" and choice == 1:
            follow_btn.click()
        elif follow_btn.text == "Following" and choice == 2:
            follow_btn.click()
            sleep(5)
            tmp = self.find_elements(
                By.CLASS_NAME, 'xuxw1ft'
            )
            sleep(2)
            for i in tmp:
                try:
                    if i.text == 'Unfollow':
                        i.click()

                        break
                except:
                    pass
        self.refresh()

    def get_first_photo(self):
        try:
            first_photo = self.find_element(By.CLASS_NAME, '_aagu')
            first_photo.click()
        except:
            print('account is private')

    def add_comment(self, choice: bool):
        if choice:
            try:
                active_comment_section = self.find_element(
                    By.CLASS_NAME, '_akhn'
                ).find_element(
                    By.CSS_SELECTOR, 'textarea[placeholder="Add a comment…"]'
                )
                active_comment_section.click()
                sleep(1)
                activated_comment_section = self.find_element(
                    By.CLASS_NAME, '_akhn'
                ).find_element(
                    By.CSS_SELECTOR, 'textarea[placeholder="Add a comment…"]'
                )
                activated_comment_section.clear()
                activated_comment_section.send_keys(rand.choice(comments))
                activated_comment_section.send_keys(Keys.ENTER)
            except:
                pass

    def like(self):
        img_loc = self.find_element(By.CLASS_NAME, '_aatl')
        actions = ActionChains(self)
        actions.double_click(img_loc).perform()

    def dislike(self):
        btns = self.find_element(
            By.CSS_SELECTOR, 'span[class="_aamw"]'
        ).find_elements(By.TAG_NAME, 'svg')
        for btn in btns:
            try:
                txt = btn.get_attribute('aria-label')
                if txt == 'Unlike':
                    btn.click()
                    break
            except:
                pass

    def handle_like(self, choice: int):
        if choice == 1:
            self.like()
        elif choice == 2:
            self.dislike()
        else:
            pass

    def get_next(self):
        try:
            tmp1 = self.find_element(By.CSS_SELECTOR, 'svg[aria-label="Next"]')
            tmp1.click()
        except:
            return False
        return True

    def close_img(self):
        try:
            close_btn = self.find_element(By.CSS_SELECTOR, 'svg[aria-label="Close"]')
            close_btn.click()
            print("closed")
        except:
            print("close not found")

    def do_work(self, like: int, comment: bool, prev: bool):
        if not prev:
            self.close_img()
            return
        sleep(2)
        self.download()
        self.add_comment(choice=comment)
        self.handle_like(choice=like)
        sleep(2)
        return self.do_work(like=like, comment=comment, prev=self.get_next())

    def next_photo(self, element):
        sleep(5)
        try:
            nxt = element.find_elements(
                By.CSS_SELECTOR, 'button[aria-label="Next"]'
            )
            print(len(nxt))
            nxt[0].click()
            return True
        except:
            print("failed")
            return False

    def download(self):
        is_multiple = self.find_element(
            By.CLASS_NAME, '_aatk'
        ).find_elements(
            By.CSS_SELECTOR, 'div[role="button"]'
        )
        print(len(is_multiple))
        if len(is_multiple) == 1:
            img = is_multiple[0].find_element(
                By.TAG_NAME, 'img'
            )
            img_url = img.get_attribute('src')
            file_name = f"image{self.cnt}.jpeg"
            self.cnt += 1
            urllib.request.urlretrieve(img_url, file_name)
            print("Image downloaded successfully as:", file_name)
            print("src : ", img.get_attribute('src'))
            # self.links.append(img.get_attribute('src'))

        else:
            try:
                while True:
                    # while next page
                    find_box = self.find_element(
                        By.CLASS_NAME, '_aatk'
                    )
                    print("here0")
                    find_the_list = find_box.find_element(
                        By.TAG_NAME, 'ul'
                    )
                    print("here1")
                    find_list_elements = find_the_list.find_elements(
                        By.TAG_NAME, 'img'
                    )
                    print("here2")
                    for img in find_list_elements:
                        print("src : ", img.get_attribute('src'))
                        self.links.append(img.get_attribute('src'))
                        print("int the loop\n\n")
                    if not self.next_photo(element=find_box):
                        break
                    sleep(5)
                    print(len(self.links))
            except:
                print("out")

    def process_download(self):
        for link in set(self.links):
            file_name = f"image{self.cnt}.jpeg"
            self.cnt += 1
            urllib.request.urlretrieve(link, file_name)
            print("Image downloaded successfully as:", file_name)
