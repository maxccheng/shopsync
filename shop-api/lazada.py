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




starttime = time.time()

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
        product_list = []
        driver.get("https://sellercenter.lazada.com.my/apps/product/list?tab=all")

        product_name = helper.find_elements_presence("//*[@class='item-detail-name']")
        for p in product_name:
            product_list.append(p.text)
            print("Product name={0}".format(p.text))




        #### dump all products info into a json file
        product_info = []

        ### download single product
        print("DOWNLOAD SINGLE PRODUCT:")

        for pname in product_list:
            product = {}
            driver.get("https://sellercenter.lazada.com.my/apps/product/list?tab=all")

            edit_link = helper.find_element("//*[@class='item-detail-name' and normalize-space()='" + pname + "']//ancestor::tr//a[@data-spm='d_action_edit']")
            driver.get(edit_link.get_attribute('href'))

            ## section - Basic Information
            product_name = helper.find_element("//h2[text()='Basic Information']/..//div[@class='next-form-item-label' and normalize-space()='Product Name']/..//input")
            product['name'] = product_name.get_attribute('value')
            print("p.name={0}".format(product['name']))

            product_cat = helper.find_element("//h2[text()='Basic Information']/..//div[@class='next-form-item-label' and normalize-space()='Category']/..//input")
            str_cat  = product_cat.get_attribute('value')
            product['category'] = str_cat.replace("/",">")
            print("p.category={0}".format(product['category']))

            product_video = helper.find_element("//h2[text()='Basic Information']/..//div[@class='next-form-item-label' and normalize-space()='Video URL']/..//input")
            product['video_url'] = product_video.get_attribute('value')
            print("p.video_url={0}".format(product['video_url']))

            ## section - Specification
            product_brand = helper.find_element("//h2[text()='Specification']/..//div[@class='next-form-item-label' and normalize-space()='Brand']/..//span[contains(@class,'next-select-values')]")
            product['brand'] = product_brand.text
            print("p.brand={0}".format(product['brand']))

            ## section - Variants
            product_price = helper.find_element("(//h2[text()='Variants']/..//div[@class='next-table-body']//tr/td)[1]//input")
            product['price'] = product_price.get_attribute('value')
            print("p.price={0}".format(product['price']))

            product_quantity = helper.find_element("(//h2[text()='Variants']/..//div[@class='next-table-body']//tr/td)[3]//input")
            product['quantity'] = product_quantity.get_attribute('value')
            print("p.quantity={0}".format(product['quantity']))

            ## section - Description skip for now

            ## section - Delivery & Warranty
            product_weight = helper.find_element("//h2[text()='Delivery & Warranty']/..//div[@class='next-form-item-label' and normalize-space()='Package Weight (kg)']/..//input")
            product['weight'] = product_weight.get_attribute('value')
            print("p.weight={0}".format(product['weight']))

            package_w = helper.find_element("(//h2[text()='Delivery & Warranty']/..//div[@class='next-form-item-label' and normalize-space()='Package Dimensions (cm)']/..//input)[2]")
            product['parcel_size_w'] = package_w.get_attribute('value')
            print("p.parcel_size_w={0}".format(product['parcel_size_w']))

            package_l = helper.find_element("(//h2[text()='Delivery & Warranty']/..//div[@class='next-form-item-label' and normalize-space()='Package Dimensions (cm)']/..//input)[1]")
            product['parcel_size_l'] = package_l.get_attribute('value')
            print("p.parcel_size_l={0}".format(product['parcel_size_l']))

            package_h = helper.find_element("(//h2[text()='Delivery & Warranty']/..//div[@class='next-form-item-label' and normalize-space()='Package Dimensions (cm)']/..//input)[3]")
            product['parcel_size_h'] = package_h.get_attribute('value')
            print("p.parcel_size_h={0}".format(product['parcel_size_h']))


            product_info.append(product)

        json_data = json.dumps(product_info, indent=4)
        file_handle = open("test_lazada_download.json", "w")
        file_handle.write(json_data)
        file_handle.close()




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

            # fill product name
            f_name = p['name']
            product_name = helper.find_element("//text()[normalize-space()='Product Name']//ancestor::div[contains(@class,'next-form-item')]//input")
            product_name.send_keys(f_name)

            # fill product category
            cat_full = p['category']
            cat_split = cat_full.split(" > ")

            cat_input = helper.click_element("//input[@id='category-input']")
            for i,x in enumerate(cat_split):
                xpath = "(//form//div[@class='cascade-wrap']/div[@class='category-list']/div[@class='list-frame']/ul[@class='list-wrap'])[" + str(i+1) + "]/li[@title='" + x + "']"
                cat_list = helper.click_element(xpath, 12, 3)
                next_status = helper.find_element("//button[text()='Confirm']").get_attribute("disabled")
                if next_status == None:
                    print("next button status {0}={1}".format(i, next_status))
                    next_btn = helper.click_element("//button[text()='Confirm']")
                    break

            time.sleep(3)

            # fill section - specification
            f_brand = p['brand']
            product_brand = helper.click_element("//h2[text()='Specification']/..//span[text()='Brand']/../../../../..//input")
            product_brand.send_keys(f_brand)
            helper.click_element("//li[@title='" + f_brand + "']")
            product_brand = helper.find_element("//h2[text()='Specification']/..//span[text()='Brand']/../../../../..//span[contains(@class,'next-input-text-field')]")
            print("Brand={0}".format(product_brand.text))

            # fill section - variants
            f_price = p['price']
            product_price = helper.find_element("//input[@placeholder='Price']")
            product_price.send_keys(f_price)

            f_stock = p['stock']
            product_stock = helper.find_element("//input[@placeholder='quantity']")
            product_stock.send_keys(f_stock)

            helper.click_element("//h2[text()='Variants']/..//button[text()='Apply To All']")

            # fill section - delivery & warranty
            weight = p['weight']
            weight_input = helper.find_element("//input[@group='package' and @uitype='PackageWeight']")
            weight_input.send_keys(weight)

            parcel_size_w = p['parcel_size_w']
            parcel_size_l = p['parcel_size_l']
            parcel_size_h = p['parcel_size_h']
            dimension_edit = helper.find_element("//input[@group='package' and @placeholder='Width (cm)']")
            dimension_edit.send_keys(parcel_size_w)
            dimension_edit = helper.find_element("//input[@group='package' and @placeholder='Length (cm)']")
            dimension_edit.send_keys(parcel_size_l)
            dimension_edit = helper.find_element("//input[@group='package' and @placeholder='Height (cm)']")
            dimension_edit.send_keys(parcel_size_h)

            # Save draft
            save_product = helper.click_element("//button[text()='Save Draft']")
            print("Save draft {0}".format(p['name']))




        #### logout
        print("LOGOUT:")
        driver.get("https://sellercenter.lazada.com.my")

        try:
            helper.click_element("//body/div[contains(@class,'next-overlay-wrapper')]")
            print("closed modal overlay")
        except TimeoutException:
            pass

        profile_icon = helper.click_element("//div[@class='main-content']/div[@class='right-sidebar']//div[contains(@class,'profile-icon')]/img")
        logout_icon = helper.click_element("//div[@class='profile-menu-item log-out']")

        print("Logout ok")
        driver.quit()

    except Exception as e:
        print("Global exception #{0}/{1}:".format(attempt+1, MAX_ATTEMPT))
        driver.quit()
        print(traceback.format_exc())
        attempt += 1
        continue

    break

elapsed = time.time() - starttime
print("elapsed {0:.0f} secs".format(elapsed))
