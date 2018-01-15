import time
from scrapy.http import HtmlResponse
from selenium import webdriver



from scrapy.http import HtmlResponse
from selenium import webdriver

class WikispiderSpiderMiddleware(object):
    def process_request(self, request, spider):
        driver = webdriver.Chrome(executable_path='../chromedriver')
        #driver = webdriver.PhantomJS(executable_path='../phantomjs-2.1.1-windows/bin/phantomjs')

        driver.get(request.url)
        time.sleep(10)

        body = driver.page_source
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)


'''    
class WikispiderSpiderMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='../chromedriver')  # your chosen driver

    def process_request(self, request, spider):
        # only process tagged request or delete this if you want all
        if not request.meta.get('selenium'):
            return
        self.driver.get(request.url)
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body)
        return response
'''


