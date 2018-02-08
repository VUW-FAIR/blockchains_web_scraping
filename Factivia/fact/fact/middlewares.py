import time
from scrapy.http import HtmlResponse
from selenium import webdriver



from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class factSpiderMiddleware(object):
    driver = webdriver.Chrome(executable_path='../chromedriver')

    def process_request(self, request, spider):
        #driver = webdriver.PhantomJS(executable_path='../phantomjs-2.1.1-windows/bin/phantomjs')

        self.driver.get(request.url)
        time.sleep(2)

        try:
            inputElement = self.driver.find_element_by_id("ftx")
            if(inputElement != None):
                inputElement.send_keys('bitcoin')
                self.driver.find_element_by_xpath("//select[@name='dr']/option[text()='All Dates']").click()

                print("yeet")
                inputElement.send_keys(Keys.ENTER)
        except:
            print("no searchbox found")




        time.sleep(1)
        try:
            self.driver.find_element_by_xpath('//*[@class="nextItem"]').click()
            print("next page")
        except Exception as exc:
            print("no next button")
            print(exc)
            print (type(exc))

        try:
            # rtfButton = self.driver.find_element_by_class_name("ppsBtn")
            # if(rtfButton != None):
            #     rtfButton.click()
            # rtf =


            self.driver.find_element_by_xpath('//*[@title="Download Articles in RTF Format"]').click()
            time.sleep(5)
                # self.driver.find_element_by_link_text('Download Articles in RTF Format')
            self.driver.find_element_by_xpath('//*[@id="listMenu-id-3"]/li[3]/a').click()
            time.sleep(2)
            print("downloaded")
        except Exception as inst:
            print("no download buttons found")
            print(inst)
            print (type(inst))



        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)


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


