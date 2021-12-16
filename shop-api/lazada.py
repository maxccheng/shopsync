from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoAlertPresentException, TimeoutException

import os
import time
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

        btn_login = helper.click_element("//span[normalize-space()='Login']/..")

        time.sleep(2)

        profile = helper.find_element_presence("//div[contains(@class,'asc-profile-info')]/a", 10)
        print("Login success shop name={0}".format(profile.get_attribute('title')))




        #### list products
        print("LIST PRODUCT:")
        driver.get("https://sellercenter.lazada.com.my/product/portal/index")


        product_name = helper.find_elements_presence("//*[@class='item-detail-name']")
        for p in product_name:
            print("Product name={0}".format(p.text))




        #### add product
        print("ADD PRODUCT:")

        file_product = open("test_product_lazada.json", "r")
        json_product = file_product.read()
        products = json.loads(json_product)
        file_product.close()

        for p in products:
            print("p.name={0} p.category={1}".format(p['name'], p['category']))

            driver.get("https://sellercenter.lazada.com.my/product/publish/index")
            time.sleep(1)

            f_name = p['name']
            product_name = helper.find_element("//text()[normalize-space()='Product Name']//ancestor::div[contains(@class,'next-form-item')]//input")
            product_name.send_keys(f_name)

            cat_full = p['category']
            cat_split = cat_full.split(" > ")

            cat_input = helper.click_element("//input[@id='category-input']")
            for i,x in enumerate(cat_split):
                xpath = "(//div[@class='category-list'])[" + str(i+1) + "]//p[normalize-space()='" + x + "']/.."
                cat_list = helper.click_element(xpath)
                next_status = helper.find_element("//button[normalize-space()='Confirm']").get_attribute("disabled")
                if next_status == None:
                    print("next button status {0}={1}".format(i, next_status))
                    next_btn = helper.click_element("//button[normalize-space()='Confirm']")
                    break




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

