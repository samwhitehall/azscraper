class AmazonItem:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

        self.name = self.get_name()

    def __repr__(self):
        return self.name
    
    def get_name(self):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)

        title = self.driver.find_element_by_css_selector('h1').text
        return title
