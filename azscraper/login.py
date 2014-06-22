from selenium import webdriver

import login_details

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

driver.get('http://www.amazon.co.uk/gp/yourstore/recs/')
