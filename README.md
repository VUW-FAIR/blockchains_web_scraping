# blockchains_web_scraping

This is a summer scholar project by Dylan Kumar at Victoria University of New Zealand. 
Supervisors: Jean-Grégoire Bernard & Markus Luczak-Roesch

Description of Project:
The objective of this summer scholar project is to assemble a comprehensive dataset on the emergence and spread of blockchain technology since 2008.  Blockchain technology is the distributed ledger system that underlie Bitcoin, a decentralized virtual currency which has gone from concept in an 2008 anonymous white paper to a market circulation valued at $46 billion USD nowadays. Despite its dodgy origins on the dark web, blockchain technology has spawned an impressive ecosystem of investments from start-ups, well-regarded corporations and governments.  The dataset assembled from the digital footprints of blockchain technology communities, investment databases, media archives, the web and social media (Twitter, Wikipedia) will provide the empirics of a research programme on the social acceptance and diffusion of blockchain technology as an innovation.

Using this dataset, a programme of studies will be conducted to answer the broader research question that motivates this project: how do socially contested innovations gain legitimacy and spread over time in institutional fields?  We will target top-ranked journals in information systems, entrepreneurship, or organizational sciences depending on the studies’ objectives and theoretical relevance.  One study is planned to identify the frames employed to discuss blockchain technology over time by field actors, and track the critical junctures related to changes in the frames’ content and prominence.  In another study, we will identify the legitimation tactics employed by blockchain entrepreneurs and examine the success of these tactics in attracting visibility and securing resources. 
(5) Classroom applications. Subparts of the dataset could eventually be used in the classroom in big data-related INFO, MIM, & MBusAn courses to demonstrate computational analysis techniques. 


### Before you use Notes

Scrapers that scrape information regarding various blockchain technologies such as bitcoin from various websites.

Note: Github Scraper using Scrapy and Selenium is depreciated, use Github_API scraper instead (in github folder). 

Forum scraper for bitcointalk.org in bitcoin_talk_forum_scraper, whilst all other forum scrapers in forum_scraper.
You can see the scripts in the spiders folder. e.g. blockchains_web_scraping/forum_scraper/forum_scraper/spiders/ for all the scripts for the different forums. 

You can make scrapy scrape the page/forum you want by calling the name specified in the script. e.g. run the command (without angle brackets): <scrapy crawl "eth"> to crawl https://forum.ethereum.org/. Make sure you move (cd) into the directory with the scrapy.cfg file, or else it won't be able to find the scrapy script.
I recommend using anaconda to set up a virtual environment, and calling the command from there (useful as provides a bash terminal for windows users as well).

Please note that the minimum value that data goes to on the time series graphs (found in time series) is 1, not 0. Not sure why this is, If anyone knows feel free to message me. 

Scripts are meant to be used together, e.g. the time_series_twitter graph goes over csv files of the same format of the csv files you get after running the twitterAPI scraper.




