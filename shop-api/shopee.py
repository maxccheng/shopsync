from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoAlertPresentException

import json
import urllib.request # python3 std lib
import urllib.error

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

btn_login = helper.click_element("//span[contains(text(),'Log In')]/..")

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
text_input = [helper.find_element("//div[@class='product-basic-info']//div[contains(@class,'edit-row')]//div[contains(@class,'edit-input')]//input")]
text_area = helper.find_element("//div[@class='product-basic-info']//div[contains(@class,'description-wrap')]//textarea")
text_category = helper.find_element("//div[contains(@class,'category-name')]")

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




#### add one product
print("ADD PRODUCT:")

json_product = \
    '[' \
    '{"name": "Google Home for Smart House", "category": "Home Appliances > Small Household Appliances > Others"},' \
    '{"name": "CR2032 small coin cell battery", "category": "Home Appliances > Battery"}' \
    ']'

products = json.loads(json_product)

for p in products:
    driver.get("https://seller.shopee.com.my/portal/product/category")

    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        print("no unsaved changes alert")

    product_name = helper.find_element("//div[@class='product-name-edit']//input")
    product_name.clear()
    print("p.name={0} p.category={1}".format(p['name'], p['category']))
    product_name.send_keys(p['name'])




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

