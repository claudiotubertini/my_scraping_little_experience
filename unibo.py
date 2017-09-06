
import urllib2
#url = "http://www.unibo.it/it/didattica/insegnamenti/view?pagenumber=1&pagesize=20&sort=descrizioneMateriaPrincipale&order=asc&search=True&DescInsegnamentoButton=cerca&descrizioneMateria=a&scuola-campus=&linguaInsegnamento=&codiceTipoCorso=&annoAccademico=2016"
import re
import robotparser

rp = robotparser.RobotFileParser()
rp.set_url(baseUrl + 'robots.txt')
rp.read()
user_agent = 'clueb'

# proxy = ...
# opener = urllib2.build_opener()
# proxy_params = {urlparse.urlparse(url).scheme: proxy}
# opener.add_handler(urllib2.ProxyHandler(proxy_params))
# response = opener.open(request)

def link_crawler(seed_url, link_regex, max_depth=2):
	max_depth = 2
	crawl_queue = [seed_url]
	seen = set(crawl_queue)
	while crawl_queue:
		url = crawl_queue.pop()
		if rp.can_fetch(user_agent, url):
			html = download(url)
			for link in get_links(html):
				if re.match(link_regex, link):
					link = urlparse.urljoin(seed_url, link)
					depth = seen[url]
					if depth != max_depth:
						for link in links:
							if link not in seen:
								seen.add(link)
								seen[link] = depth + 1
								crawl_queue.append(link)
		else:
			print 'Blocked by robots.txt: ', url

def get_links(html):
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(html)

max_errors = 5
num_errors = 0
for page in itertools.count(1):
	url = "http://www.unibo.it/it/didattica/insegnamenti/view?pagenumber=%s&pagesize=20&sort=descrizioneMateriaPrincipale&order=asc&search=True&DescInsegnamentoButton=cerca&descrizioneMateria=a&annoAccademico=2016" % page
	html = download(url)
	if html is None:
		num_errors += 1
		if num_errors == max_errors:
			break
	else:
		num_errors = 0
		pass



def download(url, user_agent='clueb', num_retries=2):
	headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    opener = urllib2.build_opener()
    if proxy:
    	proxy_params = {urlparse.urlparse(url).scheme: proxy}
    	opener.add_handler(urllib2.ProxyHandler(proxy_params))
	try:
        #html = urllib2.urlopen(request).read()
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                html = download(url, user_agent, proxy, num_retries-1)
    return html

class Throttle:
	def __init__(self, delay):
		self.delay = delay
		self.domains = {}

	def wait(self, url):
		domain = urlparse.urlaprse(url).netloc
		last_accessed = self.domains.get(domain)
		if self.delay > 0 and last_accessed is not None:
			sllep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time-spleep(sleep_secs)
		self.domains[domain] = datetime.datetime.now()





