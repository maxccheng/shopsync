from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




#### variables

# shop platform name
SHOPEE = 1
LAZADA = 2
MUDAH = 3

driver = None




#### shared functions

def set_driver(d):
    global driver
    driver = d


def find_element(xpath, explicit_timeout=6, poll_frequency=1.0, ignored_exceptions=[]):
    wait = WebDriverWait(driver, explicit_timeout, poll_frequency=poll_frequency, ignored_exceptions=ignored_exceptions)
    elem = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return elem


def find_elements(xpath, explicit_timeout=6, poll_frequency=1.0, ignored_exceptions=[]):
    wait = WebDriverWait(driver, explicit_timeout, poll_frequency=poll_frequency, ignored_exceptions=ignored_exceptions)
    elem = wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
    return elem


def click_element(xpath, explicit_timeout=6, poll_frequency=1.0, ignored_exceptions=[]):
    wait = WebDriverWait(driver, explicit_timeout, poll_frequency=poll_frequency, ignored_exceptions=ignored_exceptions)
    elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    ActionChains(driver).move_to_element(elem).click().perform()
    return elem

