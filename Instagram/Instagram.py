from Instagram.Constraints import *
from Instagram.download_post import DownloadPost
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random as rand
import time


class Instagram(webdriver.Chrome):
    def __init__(self, driver_path=chrome_path):
        self.target = None
        self.photoNumber = 0
        self.links = []
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super(Instagram, self).__init__()
        # self.implicitly_wait(15)
        self.cnt = 0
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
        print(f"{self.cnt } posts downloaded with {self.photoNumber }photos")
        print(GREEN + "Time elapsed: {} minutes {} seconds".format(elapsed_minutes, elapsed_seconds))

    @staticmethod
    def typing(container, string: str, speed: float = .05):
        for char in string:
            container.send_keys(char)
            sleep(speed)

    def get_land_page(self):
        self.get(BASE_URL)

    def login_with_account(self, user, pas):
        user_input = WebDriverWait(self, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Phone number, username, or email']"))
        )
        password_input = self.find_element(By.CSS_SELECTOR, "input[aria-label='Password']")
        login_btn = self.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.typing(user_input, user)
        self.typing(password_input, pas)
        # user_input.send_keys(user)
        # password_input.send_keys(pas)
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
        # facebook_user.send_keys(user)
        self.typing(facebook_user, user)
        # sleep(1)
        facebook_password = self.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        self.typing(facebook_password, pas)
        # facebook_password.send_keys(pas)
        # sleep(1)
        facebook_login_btn = self.find_element(By.ID, 'loginbutton')
        facebook_login_btn.click()

    def login(self, way, user, password):
        if way == 1:
            self.login_with_account(user, password)
        elif way == 2:
            self.login_with_facebook(user=user, pas=password)

    def move_to_profile(self, target):
        self.target = target
        try:
            save_data_btn = WebDriverWait(self, 3).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, '_a9_1'), "Not Now")
            )
            save_data_btn.click()
        except Exception as e:
            print("move to profile error :", end=' ')
            print(e.args)

            WebDriverWait(self, 180).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'button[type="button"]'), "Save Info")
            )
        search_btn = WebDriverWait(self, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'svg[aria-label="Search"]')
            )
        )

        search_btn.click()
        search_input = WebDriverWait(self, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[aria-label="Search input"]')
            )
        )
        self.typing(search_input, target, 0.1)
        # search_input.send_keys(target)
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
                except Exception as e:
                    print("follow error", ": ", end=' ')
                    print(e.args)
                    pass
        # self.refresh()
        # sleep(5)

    def get_first_photo(self):
        sleep(3)
        try:
            first_photo = WebDriverWait(self, 15).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, '_aagu')
                )
            )

            first_photo.click()
        except Exception as e:
            print('account is private', ": ", end=' ')
            print(e.args)

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
                self.typing(activated_comment_section, rand.choice(comments))
                # activated_comment_section.send_keys(rand.choice(comments))
                activated_comment_section.send_keys(Keys.ENTER)
            except Exception as e:
                print("can't add comment", ": ", end=' ')
                print(e.args)
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
            except Exception as e:
                print("can't dislike", ": ", end=' ')
                print(e.args)
                pass

    def handle_like(self, choice: int):
        if choice == 1:
            self.like()
        elif choice == 2:
            self.dislike()
        else:
            pass

    def next_post(self):
        try:
            nxt = WebDriverWait(self, 3).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'svg[aria-label="Next"]')
                )
            )
            nxt.click()
        except Exception as e:
            print("can't find next photo", ": ", end=' ')
            print(e.args)
            return False
        return True

    def close_img(self):
        try:
            close_btn = self.find_element(By.CSS_SELECTOR, 'svg[aria-label="Close"]')
            close_btn.click()
            print("closed")
        except Exception as e:
            print("can't close the image", ": ", end=' ')
            print(e.args)

    def do_work(self, like: int, comment: bool, prev: bool, download: bool):
        try:
            if not prev:
                self.close_img()
                return
            sleep(2)
            self.add_comment(choice=comment)
            self.handle_like(choice=like)
            if download:
                download_post = DownloadPost(driver=self, cnt=self.cnt, target=self.target,
                                             photoNumber=self.photoNumber)
                self.cnt ,self.photoNumber= download_post.execute_process()
            sleep(2)
            return self.do_work(like=like, comment=comment, prev=self.next_post(), download=download)
        except Exception as e:
            print("work is not done", ": ", end=' ')
            print(e.args)
