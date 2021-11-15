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
chromeOptions.add_argument("--window-size=1920,1080")
timeout = 2

driver = Chrome(options=chromeOptions)
driver.implicitly_wait(timeout)
driver.get("http://www.mudah.my")




#### sign in process
print("SIGN IN:")

str_email ="maxccheng@gmail.com"
str_password ="popo1234"

# main button
link_signin = driver.find_element(By.XPATH, "//a[contains(@href,'signin=1')]")
link_signin.click()

# choose login account type
h_privateseller = driver.find_element(By.XPATH, "//h1[contains(text(),'Private Account')]")
test_str = h_privateseller.text
print("Login account type={0}".format(test_str))

link_privatelogin = h_privateseller.find_element(By.XPATH, "./../../../button")
link_privatelogin.click()


input_email = driver.find_element(By.XPATH, "//input[@name='email']")
input_email.clear()
input_email.send_keys(str_email)
print("Login email={0}".format(input_email.get_attribute('value')))

input_password = driver.find_element(By.XPATH, "//input[@name='password']")
input_password.clear()
input_password.send_keys(str_password)
print("Login password={0}".format(input_password.get_attribute('value')))

btn_login = driver.find_element(By.XPATH, "//form[@action='#']//button[@type='submit']")
btn_login.click()

span_greet = driver.find_element(By.XPATH, "//span[@class='greetings']")
print("Login success greeting={0}".format(span_greet.text))




#### show active ads
print("SHOW ACTIVE ADS:")
div_livead = driver.find_element(By.XPATH, "//div[@class='live_ad_box']")
print("Live ads count={0}".format(div_livead.text))




#### list one item
print("LIST ONE ITEM:")
btn_newpost = driver.find_element(By.XPATH, "//a[contains(@href,'mudah.my/ai')]")
btn_newpost.click()

clear_unfinished_ad = driver.find_elements(By.XPATH, "//button[contains(text(),'START NEW AD')]")

# clear previous unfinished ad
if len(clear_unfinished_ad) > 0:
    print("clear unfinished ad")
    clear_unfinished_ad.click()
else:
    print("skip clear ad")

btn_clear = driver.find_element(By.XPATH, "//button[contains(text(),'CLEAR ALL')]")
ActionChains(driver).move_to_element(btn_clear).click().perform()

div_category = driver.find_element(By.XPATH, "//div[@id='category-form-field']")
ActionChains(driver).move_to_element(div_category).click().perform()

option_car = driver.find_element(By.XPATH, "//div[@role='option']/span[contains(text(),'Land')]/../..")
ActionChains(driver).move_to_element(option_car).click().perform()

btn_confirm = driver.find_elements(By.XPATH, "//button[contains(text(),'YES, LET ME CHANGE IT')]")

if len(btn_confirm) > 0:
    print("confirm change select option")
    btn_confirm.click()

input_category = driver.find_element(By.XPATH, "//input[@id='category']")
print("Input category={0}".format(input_category.get_attribute('value')))




#### logout
print("LOGOUT:")
driver.get("https://www2.mudah.my/useraccount.html")
btn_dropdown = driver.find_element(By.XPATH, "//li[contains(@class,'dropdown')]")
btn_logout = driver.find_element(By.XPATH, "//a[contains(@href,'logout=1')]")

hover_click = ActionChains(driver) \
                .move_to_element(btn_dropdown) \
                .click(btn_logout)
hover_click.perform()

print("Logout ok.url={0}".format(driver.current_url))

driver.close()

