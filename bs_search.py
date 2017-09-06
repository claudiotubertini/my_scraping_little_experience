from bs4 import BeautifulSoup
import sys
data = {}
def download(url, user_agent='CLUEB', num_retries=2):
    """Download function that includes user agent support"""
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, user_agent, num_retries-1)
    return html
with open('res.txt', 'r') as myfile:
    d = csv.reader(myfile, delimiter=',')
# for
#         url = sys.argv[1]
#         html_doc = download(url)
#         soup = BeautifulSoup(html_doc, 'html.parser')
#         tag = soup.find('h2', string='Testi/Bibliografia')
#         books = tag.find_next('p').text
#         subject = soup.select_one('h1').string
#         subject = subject.strip()
#         topiclist = subject.split('-')
#         data[topiclist[0]: topiclist[1]]

from lxml import html
import requests

page = requests.get('http://www.ingegneriarchitettura.unibo.it/it/corsi/insegnamenti/insegnamento/2016/386157')
tree = html.fromstring(page.content)
exam = tree.xpath('//*[@id="u-content-intro"]/div/h1')
subjectCode = exam[0].text_content().strip().split('-')[0]
subjectTerm = exam[0].text_content().strip().split('-')[1]
aa = tree.xpath('//h2[@class="highlight"]')[0].text_content().strip().split('\n')[1].strip()
obiettivi = tree.xpath('//*[@id="u-content-main"]/div[1]/div/div/p[1]')[0].text_content()
contenuti = tree.xpath('//*[@id="u-content-main"]/div[1]/div/div/p[2]')[0].text_content()
testi = tree.xpath('//*[@id="u-content-main"]/div[1]/div/div/p[3]')[0].text_content()


tree = lxml.html.fromstring(html)
exam = tree.cssselect('#u-content-intro > div > h1')

aa = tree.cssselect('div.description-text > h2.highlight > span')







