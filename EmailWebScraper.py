import argparse
import logging
import re
import urllib2
from pprint import pprint
from urlparse import urljoin, urlparse

import time
from bs4 import BeautifulSoup

from regex import email_regex

logging.basicConfig(filename='EmailWebScraper.log', level=logging.WARNING, format='%(asctime)s %(message)s')

def command_line_interface():

    parser = argparse.ArgumentParser(description='Scrapes email addresses from a website recursively')
    parser.add_argument('URL', metavar='URL', type=str, help='URL you want to scrape')
    parser.add_argument('-dm', '--domain', help='Only scrape initial domain', action='store_true')
    parser.add_argument('-hw', '--howmany', help='Scrape until collect N emails', type=int, default=10, metavar='N')
    parser.add_argument('-dp', '--depth', help='Scrape until N depth links', type=int, default=3, metavar='depth')
    args = parser.parse_args()

    return args

def email_locator(url):
    
    try:
        webContent = urllib2.urlopen(url).read()
        mails = re.findall(email_regex, webContent)
        totalmails.update(mails)

        return len(mails)

    except urllib2.HTTPError, e:

        logging.warning(e, exc_info=True)

    except urllib2.URLError, e:

        logging.warning(e, exc_info=True)


def link_locator(url, depth):
    
    try:
        webContent = urllib2.urlopen(url).read()
        sopa = BeautifulSoup(webContent, 'html.parser')
        links = sopa.find_all('a', href=True)
        
        for link in links:
            link = link['href']
            absolute = bool(link.startswith('http'))
            
            if absolute:

                if link in remaining_links:
                    pass
                else:
                    all_found_links.append(link)
                    remaining_links[link] = depth + 1

            elif not absolute:

                unitedurl = urljoin(url, link)

                if unitedurl in remaining_links:
                    pass
                else:
                    all_found_links.append(unitedurl)
                    remaining_links[unitedurl] = depth + 1

        return len(links)

    except urllib2.HTTPError, e:

        logging.warning(e, exc_info=True)

    except urllib2.URLError, e:

        logging.warning(e, exc_info=True)


def scrapper_control(args):
    url = "http://%s" % args.URL
    all_found_links.append(url)
    remaining_links[url] = 0
    initialdomain = urlparse(url)
    maxdepth = args.depth

    for link in all_found_links:

        depth = remaining_links[link]

        too_many_emails = len(totalmails) >= args.howmany

        url_not_in_domain = urlparse(link).netloc != initialdomain.netloc
        if depth > maxdepth:
            break
        elif url_not_in_domain and args.domain is True:
            pass
        elif too_many_emails:
            break
        else:
            correosenlink = email_locator(link)
            linksenlink = link_locator(link, depth)
            if (correosenlink is not None) and (linksenlink is not None):
                print "En %s hay %s correos y %s links " % (link, correosenlink, linksenlink)


def result_saver():

    with open ("archivo con los correos.txt", 'w') as output_file:

        output_file.write(str(totalmails))

start_time = time.time()

command_line_args = command_line_interface()

all_found_links = []
totalmails = set()
remaining_links = {}

scrapper_control(command_line_args)

pprint(totalmails)
print len(totalmails)

result_saver()

end_time = time.time() - start_time

print end_time
