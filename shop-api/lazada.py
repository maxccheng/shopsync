from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoAlertPresentException, TimeoutException

import os
import json
import urllib.request # python3 std lib
import urllib.error
import traceback
import socket

# custom library
import helper



#### browser session options
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--disable-blink-features")
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
chromeOptions.add_argument("--window-size=1920,1080")

# for urlretrieve() timeout
socket.setdefaulttimeout(12)

MAX_ATTEMPT = 2
attempt = 0
while attempt < MAX_ATTEMPT:
    try:

        driver = Chrome(options=chromeOptions)
        helper.set_driver(driver)
        driver.get("https://sellercenter.lazada.com.my")




        #### sign in process
        print("SIGN IN:")

        str_user ="+60174799829"
        str_password ="popo1234"

        input_user = helper.find_element("//input[@id='account']")
        input_user.send_keys(str_user)
        print("Login user={0}".format(input_user.get_attribute('value')))

        input_password = helper.find_element("//input[@id='password']")
        input_password.send_keys(str_password)
        print("Login password={0}".format(input_password.get_attribute('value')))

        btn_login = helper.click_element("//span[text()='Login']/..")

        profile = helper.find_element_presence("//div[contains(@class,'asc-profile-info')]/a")
        shopname = profile.text # not sure why this is needed
        print("Login success shop name={0}".format(profile.get_attribute('innerHTML')))




        #### list products
        print("LIST PRODUCT:")
        driver.get("https://sellercenter.lazada.com.my/product/portal/index")


        product_name = helper.find_elements_presence("//*[@class='item-detail-name']")
        for p in product_name:
            print("Product name={0}".format(p.text))




        #### logout
        print("LOGOUT:")
        driver.get("https://sellercenter.lazada.com.my")
        profile_icon = helper.click_element("//div[contains(@class,'profile-icon')]/img")
        logout_icon = helper.click_element("//div[contains(@class,'log-out')]")

        input_user = helper.find_element("//input[@id='account']")
        print("Logout ok")

    except Exception as e:
        print("Global exception #{0}/{1}:".format(attempt+1, MAX_ATTEMPT))
        print(traceback.format_exc())
        driver.quit()
        attempt += 1
        continue

    break

