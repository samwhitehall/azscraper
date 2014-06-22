class AmazonItem:
    def __init__(self, url, driver):
        self.url = url
        if driver.current_url != url:
            driver.get(url)

        self.name = self.get_name()

    def __repr__(self):
        return self.name
    
    def get_name(self):
        return self.driver.find_element_by_css_selector('h1').text
