from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC




#### browser session options
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--disable-blink-features")
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
chromeOptions.add_argument("--window-size=1920,1080")
timeout = 2

driver = Chrome(options=chromeOptions)
driver.implicitly_wait(timeout)
driver.get("https://sellercenter.lazada.com.my")




#### sign in process
print("SIGN IN:")

str_user ="+60174799829"
str_password ="popo1234"

input_user = driver.find_element(By.XPATH, "//input[@id='account']")
input_user.clear()
input_user.send_keys(str_user)
print("Login user={0}".format(input_user.get_attribute('value')))

input_password = driver.find_element(By.XPATH, "//input[@id='password']")
input_password.clear()
input_password.send_keys(str_password)
print("Login password={0}".format(input_password.get_attribute('value')))

btn_login = driver.find_element(By.XPATH, "//span[text()='Login']/..")
ActionChains(driver).move_to_element(btn_login).click().perform()

wait = WebDriverWait(driver, 6, ignored_exceptions=[])
profile = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'asc-profile-info')]/a")))
shopname = profile.text # not sure why this is needed
print("Login success shop name={0}".format(profile.get_attribute('innerHTML')))




#### list products
print("LIST PRODUCT:")
driver.get("https://sellercenter.lazada.com.my/product/portal/index")


product_name = driver.find_elements(By.XPATH, "//a[@class='product-desc-span-link']")
for p in product_name:
    print("Product name={0}".format(p.text))




#### logout
print("LOGOUT:")
profile_icon = driver.find_element(By.XPATH, "//div[contains(@class,'profile-icon')]/img")
ActionChains(driver).move_to_element(profile_icon).click().perform()

logout_icon = driver.find_element(By.XPATH, "//div[contains(@class,'log-out')]")
ActionChains(driver).move_to_element(logout_icon).click().perform()

wait = WebDriverWait(driver, 6, ignored_exceptions=[])
input_user = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='account']")))
print("Logout ok.")

driver.close()

