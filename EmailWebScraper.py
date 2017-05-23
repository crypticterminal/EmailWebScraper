import urllib2
import re 
from pprint import pprint

url = "https://en.wikipedia.org/wiki/Email_address#Examples"

response = urllib2.urlopen(url)
webContent = response.read()

email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

pprint(re.findall(email_regex, webContent))
