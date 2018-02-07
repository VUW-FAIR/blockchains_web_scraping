# blockchains_web_scraping
Scrapers that scrape information regarding various blockchain technologies such as bitcoin from various websites.

Note: Github Scraper using Scrapy and Selenium is depreciated, use Github_API scraper instead (in github folder). 

Forum scraper for bitcointalk.org in bitcoin_talk_forum_scraper, whilst all other forum scrapers in forum_scraper.
You can see the scripts in the spiders folder. e.g. blockchains_web_scraping/forum_scraper/forum_scraper/spiders/ for all the scripts for the different forums. 

You can make scrapy scrape the page/forum you want by calling the name specified in the script. e.g. run the command (without angle brackets): <scrapy crawl "eth"> to crawl https://forum.ethereum.org/. Make sure you move (cd) into the directory with the scrapy.cfg file, or else it won't be able to find the scrapy script.
I recommend using anaconda to set up a virtual environment, and calling the command from there (useful as provides a bash terminal for windows users as well).

Please note that the minimum value that data goes to on the time series graphs (found in time series) is 1, not 0. Not sure why this is, If anyone knows feel free to message me. 





