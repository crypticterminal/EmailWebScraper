import urllib2
import re
from pprint import pprint
import bs4
from bs4 import BeautifulSoup
from urlparse import urljoin, urlparse
import argparse
import logging

logging.basicConfig(filename='EmailWebScraper.log', level=logging.WARNING, format='%(asctime)s %(message)s')

parser = argparse.ArgumentParser(description='Scrapes email addresses from '
                                             'a website recursively')

parser.add_argument('URL', metavar='URL', type=str, help='URL you want'
                                                         ' to scrape')

parser.add_argument('-d','--domain', help='Only scrape initial domain', action='store_true')

parser.add_argument('-hw','--howmany', help='Scrape until collect N emails', type=int, default=10, metavar='N')

args = parser.parse_args()
print args
email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

totallinks = []
totalmails = set()
controllinks = set()

def ExtraeCorreos(url):
    print url
    try:
        webContent = urllib2.urlopen(url).read()

        mails = re.findall(email_regex, webContent)

        totalmails.update(mails)

        return len(mails)

    except urllib2.HTTPError, e:

        logging.warning(e, exc_info=True)

    except urllib2.URLError, e:

        logging.warning(e, exc_info=True)


def ExtraeLinks(url):

    try:
        webContent = urllib2.urlopen(url).read()

        sopa = BeautifulSoup(webContent, 'html.parser')

        links = sopa.find_all('a', href=True)

        for link in links:
            link = link['href']
            absolute = bool(link.startswith('http'))
            
            if absolute:

                if link in controllinks:
                    pass
                else:
                    totallinks.append(link)
                    controllinks.add(link)

            elif not absolute:

                unitedurl = urljoin(url, link)

                if unitedurl in controllinks:
                    pass
                else:
                    totallinks.append(unitedurl)
                    controllinks.add(unitedurl)

        return len(links)

    except urllib2.HTTPError, e:

        logging.warning(e, exc_info=True)

    except urllib2.URLError, e:

        logging.warning(e, exc_info=True)

url = "http://%s" % args.URL
totallinks.append(url)

initialdomain = urlparse(url)

for link in totallinks:
    if urlparse(link).netloc != initialdomain.netloc and args.domain == True:
        pass
    elif len(totalmails) > args.howmany: 
        break
    else:
        correosenlink = ExtraeCorreos(link)
        linksenlink = ExtraeLinks(link)
        print "En %s hay %s correos y %s links " % (link, correosenlink,
                                                    linksenlink)

pprint(totalmails)
print len(totalmails)
