class AmazonItem:
    def __init__(self, url, driver):
        self.url = url
        if driver.current_url != url:
            driver.get(url)
        self.driver = driver

        self.name = self.get_name()
        self.rating = self.get_rating()
        self.price = self.get_price()
        self.top_review = self.get_top_review()

    def __repr__(self):
        return self.name
    
    def get_name(self):
        return self.driver.find_element_by_css_selector('h1').text

    def get_rating(self):
        selector = 'span.crAvgStars > span > a > span'
        rating = self.driver.find_element_by_css_selector(selector).\
            get_attribute('title')
        rating = rating[:3]
        return rating

    def get_price(self):
        selector = 'td#actualPriceContent b'
        price = self.driver.find_element_by_css_selector(selector).text[1:]
        return price

    def get_top_review(self):
        top = driver.find_elements_by_class_name('reviews')[0]
        text = top[0].find_element_by_class_name('MHRHead').text
        return text
