from Queue import Queue

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

# scrape together list of URLs from listing page, to scrape later
url_queue = Queue()
items = Queue()

driver.get('http://www.amazon.co.uk/gp/yourstore/recs/')

try:
    for _ in range(settings.NUM_PAGES):
        # find links; filter to those that link to items for sale
        is_item_link = lambda a: a.get_attribute('id').startswith('ysProdLink')
        links = filter(is_item_link, driver.find_elements_by_css_selector('.ys a'))

        # add recommened item URLs to a queue
        for link in links:
            url = link.get_attribute('href')
            url_queue.put(url)

        # navigate to next page
        next_page = driver.find_element_by_id('ysMoreResults')
        next_page.click()
except NoSuchAttributeException:
    pass

# go through each URL in the list; load each page and scrape for further info 
while not url_queue.empty():
    url = url_queue.get()
    item = model.AmazonItem(url, driver)
    items.put(item)
