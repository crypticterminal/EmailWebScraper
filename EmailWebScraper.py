import urllib2
import re
from pprint import pprint
import bs4
from bs4 import BeautifulSoup
from urlparse import urljoin
import argparse


parser = argparse.ArgumentParser(description='Scrapes email addresses from '
                                             'a website recursively')

parser.add_argument('URL', metavar='URL', type=str, help='URL you want'
                                                         ' to scrape')

args = parser.parse_args()
print args
email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

totallinks = []
totalmails = set()


def ExtraeCorreos(url):
    try:
        webContent = urllib2.urlopen(url).read()

        mails = re.findall(email_regex, webContent)

        totalmails.update(mails)

        return len(mails)
    except urllib2.HTTPError, e:
        print e


def ExtraeLinks(url):
    try:
        webContent = urllib2.urlopen(url).read()

        sopa = BeautifulSoup(webContent, 'html.parser')

        links = sopa.find_all('a', href=True)

        for link in links:
            if link['href'].startswith('http'):
                totallinks.append(link['href'])
            elif not link['href'].startswith('http'):
                totallinks.append(urljoin(url, link['href']))

        return len(links)

    except urllib2.HTTPError, e:
        print e

url = "http://%s" % args.URL
totallinks.append(url)

for link in totallinks:

    if len(totalmails) > 10:
        break
    correosenlink = ExtraeCorreos(link)
    linksenlink = ExtraeLinks(link)
    print "En %s hay %s correos y %s links " % (link, correosenlink,
                                                linksenlink)

pprint(totalmails)
print len(totalmails)
