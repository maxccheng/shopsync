from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoAlertPresentException

import helper




#### browser session options
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--window-size=1920,1080")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument("disable-notifications")

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




#### add one product
print("ADD PRODUCT:")
#driver.get("https://seller.shopee.com.my/portal/product/category")




#### logout
print("LOGOUT:")
acc_dropdown = helper.click_element("//span[@class='account-name']")
span_logout = helper.click_element("//span[text()='Logout']")

try:
    driver.switch_to.alert.accept()
except NoAlertPresentException:
    print("no unsaved changes alert")

input_user = helper.find_element("//label[@for='username']/..//input")

print("Logout ok.")

driver.quit()

