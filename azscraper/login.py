from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException

import login_details

# login to Amazon
driver = webdriver.Firefox()
driver.get('http://www.amazon.co.uk')

login_button = driver.find_element_by_partial_link_text('Sign in')
login_button.click()

email_box = driver.find_element_by_id('ap_email')
email_box.send_keys(login_details.EMAIL)

pass_box = driver.find_element_by_id('ap_password')
pass_box.send_keys(login_details.PASSWORD)

signin_button = driver.find_element_by_id('signInSubmit-input')
signin_button.click()

# navigate pagination for recommendations page
driver.get('http://www.amazon.co.uk/gp/yourstore/recs/')

try:
    while True:
        next_page = driver.find_element_by_id('ysMoreResults')
        next_page.click()

        # do something interesting
except NoSuchAttributeException:
    pass
