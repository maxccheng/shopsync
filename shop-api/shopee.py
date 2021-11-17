from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException




#### browser session options
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--window-size=1920,1080")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument("disable-notifications")
timeout = 5

driver = Chrome(options=chromeOptions)
driver.implicitly_wait(timeout)
driver.get("https://seller.shopee.com.my")




#### sign in process
print("SIGN IN:")

str_user ="+60174799829"
str_password ="Popo1234"

input_user = driver.find_element(By.XPATH, "//label[@for='username']/..//input")
input_user.clear()
input_user.send_keys(str_user)
print("Login user={0}".format(input_user.get_attribute('value')))

input_password = driver.find_element(By.XPATH, "//label[@for='password']/..//input")
input_password.clear()
input_password.send_keys(str_password)
print("Login password={0}".format(input_password.get_attribute('value')))

btn_login = driver.find_element(By.XPATH, "//span[contains(text(),'Log In')]/..")
ActionChains(driver).move_to_element(btn_login).click().perform()

wait = WebDriverWait(driver, 5, ignored_exceptions=[StaleElementReferenceException])
accname = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='account-name']")))
accname_str = accname.text
print("Login success acc name={0}".format(accname_str))




##### list products
print("LIST PRODUCT:")
#driver.get("https://sellercenter.lazada.com.my/product/portal/index")
#
#
#product_name = driver.find_elements(By.XPATH, "//a[@class='product-desc-span-link']")
#for p in product_name:
#    print("Product name={0}".format(p.text))




#### logout
print("LOGOUT:")
acc_dropdown = driver.find_element(By.XPATH, "//span[@class='account-name']")
ActionChains(driver).move_to_element(acc_dropdown).click().perform()

span_logout = driver.find_element(By.XPATH, "//span[text()='Logout']")
ActionChains(driver).move_to_element(span_logout).click().perform()

input_user = driver.find_element(By.XPATH, "//label[@for='username']/..//input")
print("Logout ok.")

driver.close()

