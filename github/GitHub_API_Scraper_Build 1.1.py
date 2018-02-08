import os
import requests
from requests.auth import HTTPBasicAuth
import json
import time


'''
Please provide github username and password for higher rate requests
'''
username = 'username'
password = 'password'
forks_list = []

'''
This script utilizes the github API to scrape information into json files.
'''

def main():
    print("main function")

    #provide name of user or topic here:
    name = "cryptocurrency"
    
    make_dir("GitHubScraping", name)

    '''NOTE: call parse_user_page() if you want all repos of user, otherwise parse_topics_page() for all repos of a topic'''
    repos_of_user = parse_topics_page(name) 
    #repos_of_user = parse_user_page(name) 

    for repo in repos_of_user:
        parse_all_info(repo, "GitHubScraping/" + repo)


'''
USE THIS method if you're trying to get all repos of a 'topic', otherwise
use parse_users_page() if you want to get all all repos of a certain 'user'
'''
def parse_topics_page(name):
    url = 'https://api.github.com/search/repositories?q=' + name + '&per_page=100&page='
    topic_page = requests.get(url + '1', auth=(username, password))
    page = 1
    topic_repos = []
    if(topic_page.ok):
        repos = json.loads(topic_page.text or topic_page.content)
        while len(repos) > 0:
            try:
                itm = repos['items']
                for items in itm:
                    print(items['full_name'])
                    topic_repos.append(items['full_name'])

                page += 1
                topic_page = requests.get(url + str(page), auth=(username, password))
                repos = json.loads(topic_page.text or topic_page.content)
            except:
                repos = []
    return topic_repos


'''
Parses users page for all repos
'''
def parse_user_page(users_name):
    url = 'https://api.github.com/users/' + users_name + '/repos?per_page=100&page='
    users_page = requests.get(url + '1', auth=(username, password))
    page = 1
    users_repos = []
    if(users_page.ok):

        repos = json.loads(users_page.text or users_page.content)
        for items in repos:
            print(items['full_name'])
            users_repos.append(items['full_name'])
        while len(repos) > 0:
            page += 1
            users_page = requests.get(url + str(page), auth=(username, password))
            repos = json.loads(users_page.text or users_page.content)
    return users_repos



'''
Parses all forks of a repo, ensuring the duplicate forks aren't also parsed.
'''
def parse_forks(full_name, directory):
    forks = requests.get('https://api.github.com/repos/' + full_name + '/forks?per_page=100&page=1', auth=(username, password))
    if (forks.ok):
        page = 1
        forksItem = json.loads(forks.text or forks.content)
        while len(forksItem) > 0:
            print("next page")
            for fork in forksItem:
                print("forking")
                new_name = fork['full_name']
                if(new_name not in forks_list):
                    forks_list.append(new_name)
                    make_dir("GitHubScraping", new_name)
                    parse_all_info(full_name, "GitHubScraping/" + new_name)

            with open('./' + directory + '/forks_' + str(page) + '.json', 'w') as outfile:
                json.dump(forksItem, outfile)

            print("getting next page")
            page += 1
            forks = requests.get('https://api.github.com/repos/' + full_name +'/forks?per_page=100&page=' + str(page), auth=(username, password))
            forksItem = json.loads(forks.text or forks.content)

'''
Makes new directory at subpath of specified directory 
'''
def make_dir(directory, name):
    newpath = r'./' + directory + '/' + name
    if not os.path.exists(newpath):
        print("making dir")
        os.makedirs(newpath)


'''
Checks the request limit of the Github API, and sleeps the program for an hour if the request amount is exceeded. 
'''
def check_request_limit(request_amount):
    rateLimit = requests.get('https://api.github.com/rate_limit', auth=(username, password))
    if (rateLimit.ok):
        rateLimitItem = json.loads(rateLimit.text or rateLimit.content)
        print(rateLimitItem['resources']['core']['remaining'])
        if(rateLimitItem['resources']['core']['remaining'] < request_amount):
            time.sleep(3600)
    else:
        print("Rate limit request wasn't successful")

'''
Parses different API requests
'''
def parse_all_info(full_name, directory):
    check_request_limit(10)
    parse_single_page_info(requests.get('https://api.github.com/repos/' + full_name + '/releases?per_page=100&page=1', auth=(username, password)), "releases", "https://api.github.com/repos/" + full_name + "releases?per_page=100&page=", directory)
    check_request_limit(10)
    parse_single_page_info(requests.get('https://api.github.com/repos/' + full_name + '?per_page=100&page=1', auth=(username, password)), "repo_info_", "https://api.github.com/repos/" + full_name + "?per_page=100&page=", directory)
    check_request_limit(50)
    parse_all_pages_info(requests.get('https://api.github.com/repos/' + full_name + '/comments?per_page=100&page=1', auth=(username, password)), "comments_", "https://api.github.com/repos/" + full_name + "/comments?per_page=100&page=", directory)
    check_request_limit(50)
    parse_all_pages_info(requests.get('https://api.github.com/repos/' + full_name + '/issues?per_page=100&page=1', auth=(username, password)), "issues", "https://api.github.com/repos/" + full_name + "/issues?per_page=100&page=", directory)
    check_request_limit(50)
    parse_all_pages_info(requests.get('https://api.github.com/repos/' + full_name + '/pulls?per_page=100&page=1', auth=(username, password)), "pull_requests", "https://api.github.com/repos/" + full_name + "/pulls?per_page=100&page=", directory)
    check_request_limit(800)
    parse_branches(full_name, directory)
    check_request_limit(1000)
    parse_contributors(full_name, directory)
    check_request_limit(100)

    '''UNCOMMENT THIS LINE IF YOU WANT TO ALSO PARSE ALL FORKS''' 
    #parse_forks(full_name, directory)

'''
Parses a singular page
'''
def parse_single_page_info(req, fileName, url, directory):
    print("parseSinglePage")
    if (req.ok):
        reqItem = json.loads(req.text or req.content)
        make_dir(directory, fileName)
        with open("./" + directory + "/" + fileName + "/" + fileName + '.json', 'w') as outfile:
            json.dump(reqItem, outfile)


'''
Parses the information from multiple pages until no more results are found
'''
def parse_all_pages_info(req, fileName, url, directory):

    if (req.ok):
        print("parse multiple pages")
        page = 1
        reqItem = json.loads(req.text or req.content)
        make_dir(directory, fileName)
        while len(reqItem) > 0:
            with open("./" + directory + "/" + fileName + "/" + fileName + str(page) + '.json', 'w') as outfile:
                json.dump(reqItem, outfile)
            page += 1
            req = requests.get(url + str(page), auth=(username, password))
            reqItem = json.loads(req.text or req.content)


'''
Parse branches, and in turn each commit for the branches
'''
def parse_branches(full_name, directory):
    branches = requests.get('https://api.github.com/repos/' + full_name + '/branches', auth=(username, password))
    if(branches.ok):
        branchesItem = json.loads(branches.text or branches.content)
        make_dir(directory, "branches")
        with open('./' + directory + "/branches/" + 'all_branches.json', 'w') as outfile:
            json.dump(branchesItem, outfile)
        for branch in branchesItem:
            print('nextbranch')
            i = 0
            commitSHA = (branch['commit'])['sha']
            while commitSHA != '' or i == 0:
                i = 1
                currentCommitPage = requests.get('https://api.github.com/repos/' + full_name + '/commits?per_page=100&sha=' + commitSHA, auth=(username, password))
                if currentCommitPage.ok:
                    currentCommitPageItem = json.loads(currentCommitPage.text or currentCommitPage.content)
                    make_dir(directory, "commits")
                    with open('./' + directory + '/commits/' + 'commits_at_branch_' + branch['name'].replace("/", "").replace("\\", "") + '_commits_sha_' +  commitSHA +  '.json', 'w') as outfile:
                        json.dump(currentCommitPageItem, outfile)

                    #get the next page, if you get an exception you know you're on the last one (kinda a hack)
                    try:
                        commitSHA = ((currentCommitPageItem[len(currentCommitPageItem)-1])['parents'][0]['sha'])
                        print(commitSHA)
                    except IndexError:
                        commitSHA = ''
                    except:
                        print("some error")

'''
Parse all contributors for a repo, including their own singular user page. 
'''
def parse_contributors(full_name, directory):

    try:
        contributors = requests.get('https://api.github.com/repos/' + full_name + '/contributors?per_page=100&page=1&anon=1', auth=(username, password))
        if(contributors.ok):
            page = 1
            contributorsItem = json.loads(contributors.text or contributors.content)
            while len(contributorsItem) > 0:
                print(len(contributorsItem))
                make_dir(directory, "contributors")
                make_dir(directory, "all_contributors")
                with open('./' + directory + '/all_contributors/' + 'contributors_page_' + str(page) + '.json', 'w') as outfile:
                    json.dump(contributorsItem, outfile)

                for contributor in contributorsItem:
                    try:
                        _contributor = contributor['login']
                        print(_contributor)
                        contributorInfo = requests.get('https://api.github.com/users/' + _contributor + '/repos', auth=(username, password))
                        if (contributorInfo.ok):
                            contributorsInfoItem = json.loads(contributorInfo.text or contributorInfo.content)
                            with open('./' + directory + '/contributors/' + 'contributor_repos_' + _contributor + '.json', 'w') as outfile:
                                json.dump(contributorsInfoItem, outfile)
                        contributorInfo2 = requests.get('https://api.github.com/users/' + _contributor, auth=(username, password))
                        if (contributorInfo2.ok):
                            contributorInfo2Item = json.loads(contributorInfo2.text or contributorInfo2.content)
                            with open('./' + directory + '/contributors/' + 'contributor_page_' + _contributor + '.json', 'w') as outfile:
                                json.dump(contributorInfo2Item, outfile)

                    except KeyError:
                        print("anon user")
                    except:
                        print("some other error")

                page += 1
                contributors = requests.get('https://api.github.com/repos/' + full_name + '/contributors?per_page=100&page=' + str(page) + '&anon=1', auth=(username, password))
                contributorsItem = json.loads(contributors.text or contributors.content)
    except Exception as e:
        print("Oops something went wrong in contributors")
        print(e)
main()
