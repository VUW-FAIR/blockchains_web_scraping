# -*- coding: utf-8 -*-
import csv

import os
import scrapy
import time

from bs4 import BeautifulSoup

from wikiSpider.items import Release, Commit, Contributor

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CommitsSpider(scrapy.Spider):

    name = "commits"
    start_urls = ['https://github.com/bitcoin/bitcoin/']
    download_delay = 5

    def parse(self, response):

        MainLinks = response.selector.xpath('//*[contains(@class,"numbers-summary")]//@href').extract()

        for url in MainLinks:
            print(url)
            url = response.urljoin(url)
            if "commits" in url:
                print("")
                yield scrapy.Request(url=url, callback=self.parse_commit_page)
            elif "branches" in url:
                 yield scrapy.Request(url=url, callback=self.parse_branches_page)
            elif "releases" in url:
                 yield scrapy.Request(url=url, callback=self.parse_releases_page, meta={'page': 1})
            elif "contributors" in url:
                yield scrapy.Request(url=url, callback=self.parse_contributors_page)
            elif "blob" in url:
                yield scrapy.Request(url=url, callback=self.parse_blob_page)
            else:
                print("some other link, this shouldn't happen ideally")


    def parse_branches_page(self, response):

        allBranches = response.selector.xpath('//a[@class="subnav-item js-subnav-item js-branches-all selected"]//@href').extract()

        if(len(allBranches) > 1):
            print("shouldn't have more than one all branches button")
            #throw exception

        for url in allBranches:
            print(url)
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_all_branches_page)

    def parse_all_branches_page(self, response):
        branchURLs = response.selector.xpath('//a[@class="branch-name css-truncate-target"]//@href').extract()
        for url in branchURLs:
            print(url)
            url = response.urljoin(url)
            '''parseIndividualBranches'''
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_contributors_page(self, response):

        contributorName = response.selector.xpath('//a[@class="text-normal"]/text()').extract()
        #contributorInfo = response.selector.xpath('//span[@class="cmeta"]/text()').extract()

        bsObj = BeautifulSoup(response.body)
        contributorInfo = bsObj.findAll("span", {"class": "cmeta"})

        if(len(contributorInfo) != len(contributorName)):
            print("Different number of contributors to contirbutor information sections")
            #throw exception

        newpath = r'./contributors'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        index = 0
        print(len(contributorName)) #comes out to 100...
        for name in contributorName:
            print(name)
            print(contributorInfo[index].getText())

            with open("./contributors/contributor_" + name + ".csv", "w") as f:
                cr = csv.writer(f, delimiter=";", lineterminator="\n")
                cr.writerow({'name' : name})
                cr.writerow({'info' : str(contributorInfo[index].getText())})

            index += 1


        item = Contributor(name = contributorName, info = contributorInfo)
        yield item

    def parse_releases_page(self, response):
        page = response.meta['page']

        bsObj = BeautifulSoup(response.body)
        releaseTitle= bsObj.findAll("h1", {"class": "release-title"})
        releaseOwnerShip = bsObj.findAll("p", {"class": "release-authorship"})

        desc = bsObj.findAll("div", {"class": "markdown-body"})

        times = response.selector.xpath('//p[@class="release-authorship"]//relative-time/@datetime').extract()

        release_title = []
        release_ownership = []
        description = []

        for p in releaseTitle:
            print(p.getText())
            release_title.append(p.getText())

        for p in releaseOwnerShip:
            print(p.getText())
            release_ownership.append(p.getText())

        for p in desc:
            print(p.getText())
            description.append(p.getText())

        item = Release(title=release_title, ownership=release_ownership, desc=description, time=times)


        print("RELEASETITLE:")
        for i in release_title:
            print(i)

        with open("releases_page_" + str(page) + ".csv", "w") as f:
            cr = csv.writer(f, delimiter=";", lineterminator="\n")
            cr.writerow(release_title)
            cr.writerow(times)
            cr.writerow(release_ownership)
            cr.writerow(description)

        yield item

        nextPages = response.selector.xpath('//*[contains(@class,"pagination")]//@href').extract()
        print(len(nextPages))
        for url in nextPages:
            print(url)
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_releases_page, meta={'page': page+1})


    def parse_commit_page(self, response):
        urls = response.selector.xpath('//*[contains(@class,"message")]//@href').extract()

        for url in urls:
            print(url)
            url = response.urljoin(url)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_commit_details)

        # nextPages = response.selector.xpath('//*[contains(@class,"pagination")]//@href').extract()
        # print(len(nextPages))
        # for url in nextPages:
        #     print(url)
        #     url = response.urljoin(url)
        #     yield scrapy.Request(url=url, callback=self.parse_commit_page)


    def parse_commit_details(self, response):

        #TODO fix duplicate times being listed

        bsObj = BeautifulSoup(response.body)
        commitTitle = bsObj.find("p", {"class": "commit-title"})
        desc = bsObj.findAll("div", {"class": "commit-desc"})
        time = response.selector.xpath('//relative-time/@datetime').extract()

        commitTitle = commitTitle.getText()
        time = time[0]

        print(commitTitle)
        print(time)

        description = []

        for p in desc:
            print(p.getText())
            description.append(p.getText())

        #TODO fix bad formatting for title and time
        with open("commit_at_" + str(time)[:10] + ".csv", "w") as f:
            cr = csv.writer(f, delimiter=";", lineterminator="\n")
            cr.writerow(commitTitle)
            cr.writerow(str(time))
            cr.writerow(description)

        item = Commit(title=commitTitle, desc=description, time=time)
        yield item



    def parse_pull_requests(self, response):
        urls = response.selector.xpath('//a[contains(@class,"link-gray-dark no-underline h4 js-navigation-open")]//@href').extract()


    def parse_pull_request(self, response):

        bsObj = BeautifulSoup(response.body)
        title = bsObj.find("span", {"class": "js-issue-title"})
        request = bsObj.find("div", {"class": "TableObject-item TableObject-item--primary"})

        usernames = bsObj.find("span", {"class": "author text-inherit"})
        times = response.selector.xpath('//a[@class="timestamp"]//relative-time/@datetime').extract()
        comment = bsObj.find("div", {"class": "edit-comment-hide"})

        commits = bsObj.find("a", {"class": "message"})

        with open("test"+ ".csv", "w") as f:
            cr = csv.writer(f, delimiter=";", lineterminator="\n")
            cr.writerow(title)
            cr.writerow(request)


        if(len(usernames) != len(times) != len(comment)):
            print("bad! Amount of usernames, times and comments should be the same")
            #throw exception

        index = 0
        for username in usernames:
            print(username)
            print(times[index])
            print(comment[index])

            with open("test" + ".csv", "a") as f:
                cr = csv.writer(f, delimiter=";", lineterminator="\n")
                cr.writerow(username)
                cr.writerow(times[index])
                cr.writerow(comment[index])

        #TODO may have to refactor/change
        for commit in commits:
            print(commit)
            with open("test" + ".csv", "a") as f:
                cr = csv.writer(f, delimiter=";", lineterminator="\n")
                cr.writerow("Commit:")
                cr.writerow(commit)
