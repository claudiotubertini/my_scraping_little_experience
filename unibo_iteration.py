import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import Queue
import itertools
import json
import csv
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.adozioni
collection = db.bologna

def iteration(link_regex=None, delay=5, headers=None, user_agent='clueb', proxy=None, num_retries=1):
    max_errors = 5 # maximum number of consecutive download errors allowed
    num_errors = 0 # current number of consecutive download errors

    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent
    #for page in itertools.count(1):
    for page in range(1,59):
        links = []
        out = []
        url = 'http://www.unibo.it/it/didattica/insegnamenti/view?pagenumber=%d&pagesize=10&sort=descrizioneMateriaPrincipale&order=asc&search=True&DescInsegnamentoButton=cerca&descrizioneMateria=a&scuola-campus=&linguaInsegnamento=&codiceTipoCorso=&annoAccademico=2016' % page
        #url = 'http://example.webscraping.com/view/-{}'.format(page)
        throttle.wait(url)
        myhtml = download(url, headers, proxy=proxy, num_retries=num_retries)
        if myhtml is None:
            # received an error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                # reached maximum amount of errors in a row so exit
                break
        else:
            if link_regex:
                    links.extend(link for link in get_links(myhtml) if (re.match(link_regex, link) and not re.match('.*/orariolezioni', link)))

        for link in links:
            page = requests.get(link)
            tree = html.fromstring(page.content)
            exam = tree.xpath('//*[@id="u-content-intro"]/div/h1')
            subjectCode = exam[0].text_content().strip().split('-')[0]
            subjectTerm = exam[0].text_content().strip().split('-')[1]
            aa = tree.xpath('//h2[@class="highlight"]')[0].text_content().strip().split('\n')[1].strip()
            obiettivi = tree.xpath('//*[@id="u-content-main"]/div[1]/div/div/p[1]')[0].text_content()
            contenuti = tree.xpath('//*[@id="u-content-main"]/div[1]/div/div/p[2]')[0].text_content()
            testi = tree.xpath('//*[@id="u-content-main"]/div[1]/div/div/p[3]')[0].text_content()
            corso = {"course_id": subjectCode,
                    "corso": subjectTerm,
                    "anno": aa,
                    "obiettivi": obiettivi,
                    "contenuti": contenuti,
                    "testi": testi}
            out.append(corso)
        result = collection.insert_many(out)


    # output = ','.join(links)
    # with open("res.txt", "a", newline="") as myfile:
    #     csv.writer(myfile, delimiter=',')

def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='clueb', proxy=None, num_retries=1):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = Queue.deque([seed_url])
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = 0
    rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=1)
            links = []

            depth = seen[url]
            if depth != max_depth:
                # can still crawl further
                if link_regex:
                    # filter for links matching our regular expression
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)
                        # check link is within same domain
                        # if same_domain(seed_url, link):
                        #     # success! add this new link to queue
                        #     crawl_queue.append(link)

            # check whether have reached downloaded maximum
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url



class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


def download(url, headers, proxy, num_retries, data=None):
    print 'Downloading:', url
    request = urllib2.Request(url, data, headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries-1, data)
        else:
            code = None
    return html

# def download(url, user_agent='CLUEB', num_retries=2):
#     """Download function that includes user agent support"""
#     print 'Downloading:', url
#     headers = {'User-agent': user_agent}
#     request = urllib2.Request(url, headers=headers)
#     try:
#         html = urllib2.urlopen(request).read()
#     except urllib2.URLError as e:
#         print 'Download error:', e.reason
#         html = None
#         if num_retries > 0:
#             if hasattr(e, 'code') and 500 <= e.code < 600:
#                 # retry 5XX HTTP errors
#                 html = download(url, user_agent, num_retries-1)
#     return html

def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


if __name__ == '__main__':
    iteration(link_regex='(.*?/corsi/insegnamenti/.*)', delay=5, headers=None, user_agent='clueb', proxy=None, num_retries=1)
