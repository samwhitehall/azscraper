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
        return u'''
        Name:   %s
        Rating: %s
        Price: %.2f GBP
        Top Review:
        %s ...
        URL: %s
        ''' % (
            self.name,
            '*' * int(round(self.rating)),
            self.price,
            self.top_review[:100].encode('ascii', 'ignore'),
            self.url
        )
    
    def get_name(self):
        return self.driver.find_element_by_css_selector('h1').text

    def get_rating(self):
        selector = 'span.crAvgStars > span > a > span'
        rating = self.driver.find_element_by_css_selector(selector).\
            get_attribute('title')
        rating = rating[:3]
        return float(rating)

    def get_price(self):
        selector = 'td#actualPriceContent b'
        price = self.driver.find_element_by_css_selector(selector).text[1:]
        return float(price)

    def get_top_review(self):
        top = self.driver.find_elements_by_class_name('reviews')
        text = top[0].find_element_by_class_name('reviewText').text
        return text
