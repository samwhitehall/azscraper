from Queue import Queue

from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException

import threading
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
items = []

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

    # put end token in when complete
    url_queue.put('END')

except NoSuchAttributeException:
    pass


# go through each URL in the list; load each page and scrape for further info 
# this is split up by worker threads.
class ScraperWorker(threading.Thread):
    def __init__(self, thread_id, queue):
        '''Initialise thread, including a browser instance.'''
        threading.Thread.__init__(self)
        self.queue = queue
        self.driver = webdriver.Firefox()
        self.thread_id = thread_id

        print 'Scraper worker initialised %d' % thread_id

    def run(self):
        while True:
            url = self.queue.get() # repeatedly sample queue
            print '>> thread %d doing %s' % (self.thread_id, url)

            if url == 'END': # end of queue token
                print '<< thread %d terminated' % self.thread_id
                self.queue.put('END') # put the token back, for other threads
                self.driver.close()
                break

            # convert to item (scrape URL page using this thread's browser)
            item = model.AmazonItem(url, self.driver)
            items.append(item)
            self.queue.task_done()

# create and start worker threads
workers = []
for i in range(settings.NUM_THREADS):
    worker = ScraperWorker(i, url_queue)
    worker.setDaemon(True)
    worker.start()
    workers.append(worker)

for worker in workers:
    worker.join() # block until all threads finished

driver.close()
