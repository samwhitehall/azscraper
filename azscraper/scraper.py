from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException

import model
import settings

# login to Amazon
driver = webdriver.Firefox()
driver.get('http://www.amazon.co.uk')

login_button = driver.find_element_by_partial_link_text('Sign in')
login_button.click()

email_box = driver.find_element_by_id('ap_email')
email_box.send_keys(settings.EMAIL)

pass_box = driver.find_element_by_id('ap_password')
pass_box.send_keys(settings.PASSWORD)

signin_button = driver.find_element_by_id('signInSubmit-input')
signin_button.click()

# navigate pagination for recommendations page
driver.get('http://www.amazon.co.uk/gp/yourstore/recs/')

url_queue = []
items = []

try:
    for _ in range(settings.NUM_PAGES):
        # find links; filter to those that link to items for sale
        is_item_link = lambda a: a.get_attribute('id').startswith('ysProdLink')
        links = filter(is_item_link, driver.find_elements_by_css_selector('.ys a'))

        # add recommened item URLs to a queue
        for link in links:
            url = link.get_attribute('href')
            url_queue.append(url)

        # navigate to next page
        next_page = driver.find_element_by_id('ysMoreResults')
        next_page.click()

    for url in url_queue:
        item = model.AmazonItem(url, driver)
        items.append(item)

except NoSuchAttributeException:
    pass
