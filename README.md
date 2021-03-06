# blockchains_web_scraping

This is a summer scholar project by Dylan Kumar at Victoria University of New Zealand. 
Supervisors: Jean-Grégoire Bernard & Markus Luczak-Roesch

Description of Project:
The objective of this summer scholar project is to assemble a comprehensive dataset on the emergence and spread of blockchain technology since 2008.  Blockchain technology is the distributed ledger system that underlie Bitcoin, a decentralized virtual currency which has gone from concept in an 2008 anonymous white paper to a market circulation valued at $46 billion USD nowadays. Despite its dodgy origins on the dark web, blockchain technology has spawned an impressive ecosystem of investments from start-ups, well-regarded corporations and governments.  The dataset assembled from the digital footprints of blockchain technology communities, investment databases, media archives, the web and social media (Twitter, Wikipedia) will provide the empirics of a research programme on the social acceptance and diffusion of blockchain technology as an innovation.

Using this dataset, a programme of studies will be conducted to answer the broader research question that motivates this project: how do socially contested innovations gain legitimacy and spread over time in institutional fields?  We will target top-ranked journals in information systems, entrepreneurship, or organizational sciences depending on the studies’ objectives and theoretical relevance.  One study is planned to identify the frames employed to discuss blockchain technology over time by field actors, and track the critical junctures related to changes in the frames’ content and prominence.  In another study, we will identify the legitimation tactics employed by blockchain entrepreneurs and examine the success of these tactics in attracting visibility and securing resources. 
(5) Classroom applications. Subparts of the dataset could eventually be used in the classroom in big data-related INFO, MIM, & MBusAn courses to demonstrate computational analysis techniques. 


## Technical Guide

Note: 
Github Scraper using Scrapy and Selenium is depreciated, use Github_API scraper instead (in github folder). 
The Factivia Scraper doesn't really work fully. "fact2" is the name of the main script.

The forum scraper for bitcointalk.org is in bitcoin_talk_forum_scraper, whilst all other forum scrapers in forum_scraper.

You can see the scripts in the <b>spiders folder</b>. e.g. blockchains_web_scraping/forum_scraper/forum_scraper/spiders/ for all the scripts for the different forums. 

Please note that the minimum value that data goes to on the time series graphs (found in time series) is 1, not 0. Not sure why this is, If anyone knows feel free to message me. 

Scripts are meant to be used together, e.g. the time_series_twitter graph goes over csv files of the same format of the csv files you get after running the twitterAPI scraper.


### HOW TO RUN

To run a python script type <b><python nameofscript.py></b>
If you want a process to run in linux in the background without the terminal left open, use nohup.
e.g. nohup python nameofscript.py & disown
https://unix.stackexchange.com/questions/3886/difference-between-nohup-disown-and

You can make scrapy scrape the page/Forum you want by calling the name specified in the script. e.g. run the command (without angle brackets): <b><scrapy crawl "eth"></b> to crawl https://forum.ethereum.org/. This is because the name variable in the file is set to "eth".

Note in the script we have: <b><name = "eth"></b>

Make sure you move (cd) into the directory with the scrapy.cfg file, or else it won't be able to find the scrapy script.
In Scrapy the 'name' variable holds what we call when running 

I recommend using anaconda to set up a virtual environment, and calling the command from there (useful as provides a bash terminal for windows users as well).
To install a package using this virtual environment, search for your package on the site and run the shown command, 

e.g. for requests:
https://anaconda.org/anaconda/requests

run the command: <b><conda install -c anaconda requests></b> in your terminal to install it.

Use <i>GitHub_API_Scraper_Original.py</i> if you want to scrape information regarding one repo (and it's forks).
<i>GitHub_API_Scraper_Build 1.1.py</i> is an extention upon the original with added methods that either scrape every repo from a user, or ever repo from a specific topic. Read comments in files on how to edit. 


