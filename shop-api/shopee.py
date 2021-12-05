from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoAlertPresentException

import os
import json
import urllib.request # python3 std lib
import urllib.error
import traceback

# custom library
import helper




#### browser session options
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--window-size=1920,1080")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument("--disable-notifications")

MAX_ATTEMPT = 2
attempt = 0
while attempt < MAX_ATTEMPT:
    try:

        driver = Chrome(options=chromeOptions)
        helper.set_driver(driver)
        driver.get("https://seller.shopee.com.my")




        #### sign in process
        print("SIGN IN:")

        str_user ="+60174799829"
        str_password ="Popo1234"

        input_user = helper.find_element("//label[@for='username']/..//input")
        input_user.clear()
        input_user.send_keys(str_user)
        print("Login user={0}".format(input_user.get_attribute('value')))

        input_password = driver.find_element(By.XPATH, "//label[@for='password']/..//input")
        input_password.clear()
        input_password.send_keys(str_password)
        print("Login password={0}".format(input_password.get_attribute('value')))

        btn_login = helper.click_element("//span[normalize-space()='Log In']/..")

        accname = helper.find_element("//span[@class='account-name']", ignored_exceptions=[StaleElementReferenceException])
        accname_str = accname.text
        print("Login success acc name={0}".format(accname_str))




        #### list products
        print("LIST PRODUCT:")
        driver.get("https://seller.shopee.com.my/portal/product/list/all")

        product_name = driver.find_elements(By.XPATH, "//a[@class='product-name-wrap']/span")
        for p in product_name:
            print("Product name={0}".format(p.text))




        #### download one product
        print("DL ONE PRODUCT:")
        driver.get("https://seller.shopee.com.my/portal/product/list/all")
        href_product = helper.find_element("//a[@class='product-name-wrap']")
        driver.get(href_product.get_attribute("href"))

        details_title = helper.find_element("//a[text()='Product Details']")


        # download file functions
        def get_field_val(field_type, element):
            if field_type == 'image':
                return get_image(element)
            elif field_type == 'video':
                return get_video(element)
            elif field_type == 'textarea':
                return get_textarea(element)
            elif field_type == 'select':
                return get_selected(element)
            else:
                return None

        def get_image(element):
            try:
                url = element.get_attribute('src')
                return urllib.request.urlretrieve(url)[0]
            except urllib.error.URLerror as e:
                print(e.__dict__)
            except urllib.error.HTTPerror as e:
                print(e.__dict__)

        def get_video(element):
            try:
                url = element.get_attribute('src')
                return urllib.request.urlretrieve(url)[0]
            except urllib.error.URLerror as e:
                print(e.__dict__)
            except urllib.error.HTTPerror as e:
                print(e.__dict__)


        # product_image
        product_thumbnails = helper.find_elements("//span[text()='Product Images']/../..//div[@class='shopee-image-manager__image']/..")
        crop_tools = helper.find_elements_presence("//span[contains(@class,'shopee-image-manager__icon--crop')]")
        for idx, t in enumerate(product_thumbnails):
            ActionChains(driver).move_to_element(t).perform()
            ActionChains(driver).move_to_element(crop_tools[idx]).pause(0.5).click().perform()
            product_img = helper.find_element_presence("//div[@class='image-container']/img")
            local_img = get_field_val('image', product_img)
            modal_close = helper.click_element("//i[@class='shopee-icon shopee-modal__close']")
            print("local_img_{0}={1}".format(idx, local_img))


        # product video
        product_video = helper.find_element("//div[contains(@class,'video-container')]")
        ActionChains(driver).move_to_element(product_video).perform()
        view_video = helper.click_element("(//div[contains(@class,'video-container')]/div[@class='action-tools']/span[@class='action-tools-icon'])[1]")
        video_src = helper.find_element_presence("//video/source")
        local_video = get_field_val('video', video_src)
        video_close = helper.click_element("//div[@class='video-close']")
        print("local_video={0}".format(local_video))


        # text fields
        text_label = helper.find_elements("//div[@class='grid edit-row']//div[@class='edit-label edit-title']")
        text_select = helper.find_elements("//div[@class='grid edit-row']//div[@class='edit-input edit-text']")
        text_input = helper.find_elements_presence("//div[contains(@class,'edit-row')]//div[contains(@class,'edit-input')]//input[@type='text']")
        text_area = helper.find_element("//div[@class='product-basic-info']//div[contains(@class,'description-wrap')]//textarea")
        text_category = helper.find_element("//div[contains(@class,'category-name')]")
        text_radio = helper.find_elements_presence("//input[@class='shopee-radio__input']")
        text_logistics = helper.find_element_presence("//div[contains(@class,'optional-item')]//div[contains(@class,'logistics-item-name')]")
        text_switch = helper.find_element_presence("//div[contains(@class,'shopee-switch')]")

        print("text_label count={0}".format(len(text_label)))
        print("text_select count={0}".format(len(text_select)))
        print("text_input count={0}".format(len(text_input)))

        for i, x in enumerate(text_label):
            print("label {0}={1}".format(i, x.text.replace("\n"," ")))

        for i, x in enumerate(text_select):
            print("select text {0}={1}".format(i, x.text.replace("\n"," ")))

        for i, x in enumerate(text_input):
            print("input text {0}={1}".format(i, x.get_property('value').replace("\n"," ")))

        print("text area {0}".format(text_area.get_property('value').replace("\n"," ")))
        print("text category {0}".format(text_category.text.replace("\n"," ")))

        for i, x in enumerate(text_radio):
            print("text radio {0}={1}".format(i, x.get_attribute("checked")))
            radio_label = x.find_element(By.XPATH, "../span[@class='shopee-radio__label']")
            print("text radio label {0}={1}".format(i, radio_label.text.replace("\n"," ")))

        switch_class = text_switch.get_attribute('class')
        if 'shopee-switch--open' in switch_class:
            print("text logistics {0} on".format(text_logistics.text))
        elif 'shopee-switch--closed' in switch_class:
            print("text logistics {0} off".format(text_logistics.text))
        else:
            print("text logistics {0} class={1}".format(text_logistics.text, switch_class))



        #### add one product
        print("ADD PRODUCT:")

        file_product = open("test_products.json", "r")
        json_product = file_product.read()
        products = json.loads(json_product)

        for p in products:
            print("p.name={0} p.category={1}".format(p['name'], p['category']))

            driver.get("https://seller.shopee.com.my/portal/product/category")

            try:
                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                print("no unsaved changes alert")

            product_name = helper.find_element("//div[@class='product-name-edit']//input")
            product_name.clear()
            product_name.send_keys(p['name'])

            # category
            cat_full = p['category']
            cat_split = cat_full.split(" > ")

            for i,x in enumerate(cat_split):
                xpath = "//div[@class='category-list']/ul[" + str(i+1) + "]//p[normalize-space()='" + x + "']/.."
                cat_list = helper.click_element(xpath)
                next_status = helper.find_element("//span[normalize-space()='Next']/..").get_attribute("disabled")
                if next_status == None:
                    print("next button status {0}={1}".format(i, next_status))
                    next_btn = helper.click_element("//span[normalize-space()='Next']/..")
                    break

            # upload image
            if 'image' in p:
                print("product image found")
                image_all = p['image']
                for i,x in enumerate(image_all):
                    image_input = helper.find_element_presence("//div[contains(@class,'shopee-image-manager')]/div/div[" + str(i+1) + "]//input[@type='file']")
                    image_input.send_keys(os.path.abspath(x))
                    verify_upload = helper.find_element("//div[contains(@class,'shopee-image-manager')]/div/div[" + str(i+1) + "]//div[@class='shopee-image-manager__image']")
                    print("verify upload thumbnail={0}".format(verify_upload.get_attribute('style')))

            # description
            descrip = p['description']
            #desc_text = helper.find_element_presence("//textarea[contains(@class,'shopee-input__inner--normal')]")
            #desc_text.send_keys(descrip)

            # dangerous goods
            danger = p['dangerous_good']
            xpath = "//div[contains(@class,'dangerous-goods-row')]//span[normalize-space()='" + danger + "']//ancestor::label[@class='shopee-radio']"
            print("xpath {0}".format(xpath))
            danger_radio = helper.click_element("//div[contains(@class,'dangerous-goods-row')]//span[normalize-space()='" + danger + "']//ancestor::label[@class='shopee-radio']")
            danger_radio = helper.find_element_presence("//div[contains(@class,'dangerous-goods-row')]//span[normalize-space()='" + danger + "']//ancestor::label[@class='shopee-radio']/input")
            print("danger_radio json={0} checked={1}".format(danger, danger_radio.get_attribute('checked')))



        #### logout
        print("LOGOUT:")
        acc_dropdown = helper.click_element("//span[@class='account-name']")
        span_logout = helper.click_element("//span[text()='Logout']")

        wait = WebDriverWait(driver, 5).until(EC.alert_is_present())

        try:
            driver.switch_to.alert.accept()
        except NoAlertPresentException:
            print("no unsaved changes alert")

        input_user = helper.find_element("//label[@for='username']/..//input")

        print("Logout ok.")
        driver.quit()

    except Exception as e:
        print("Global exception #{0}/{1}:".format(attempt+1, MAX_ATTEMPT))
        print(traceback.format_exc())
        driver.quit()
        attempt += 1
        continue

    break

