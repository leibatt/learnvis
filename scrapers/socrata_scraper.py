import json
import re
import requests
import urllib2
import shutil
import os
import cStringIO as StringIO
from bs4 import BeautifulSoup
from time import gmtime, strftime
 
class Scraper:
 
customers = {}
 
def __init__(self):
self.base_url = "http://www.socrata.com/customer-spotlight/"
self.data_dir = "data"
self.extract_customers()
self.reset_data_dir()
print "initialized scraper"
 
def reset_data_dir(self):
shutil.rmtree(self.data_dir, ignore_errors=True)
os.mkdir(self.data_dir)
 
def extract_customers(self):
r = requests.get(self.base_url)
if r.status_code == 200:
cust_page = BeautifulSoup(r.text, "lxml")
else:
print "Featured customer URL is broken."
return
custs = cust_page.find_all("div", class_="one_fourth")
for cust in custs:
cust_name_tag = cust.strong.extract()
self.customers[cust_name_tag.text] = cust.text.rstrip().lstrip()
 
def get_vis_urls(self, cust):
page_num = 1
urls = []
while True and page_num < 10:
url = "http://%s/browse?limitTo=charts&page=%s" % (self.customers[cust], str(page_num),)
r = requests.get(url)
bs = BeautifulSoup(r.text, "lxml")
charts = bs.find_all("td", class_="typeChart")
if len(charts) > 0:
for chart in charts:
link = chart.a.extract()
urls.append(link.get('href'))
else:
break
page_num += 1
return urls
 
def pull_down_vis(self, cust, url):
# get unique ID
match = re.match(r'.*/(.*)$', url)
 
vis_meta = {}
 
base_url_match = re.match(r'http://([\w\.]+)/(.+)', url)
 
print url
 
base_url = ''
if base_url_match:
base_url = base_url_match.group(1)
else:
print "base url regex failed"
 
data_url = "https://%s/api/views/%s/rows.csv?accessType=DOWNLOAD"
 
if match:
id = match.group(1)
base = self.data_dir + '/' + self.customers[cust]
full = base + '/' + id
 
if os.path.exists(base) is False:
os.mkdir(base)
os.mkdir(full)
 
parmed_data_url = data_url % (base_url, id)
 
maxlength = 2 * 1024 * 1024
 
data_file = urllib2.urlopen(parmed_data_url)
buf = data_file.read(maxlength + 1)
 
if len(buf) == maxlength + 1:
os.rmdir(full)
return # don't bother with data files larger than 2MB
 
with open(full + '/data.csv', 'w') as f:
f.write(buf)
 
 
r = requests.get(url)
 
# pull out charttype
m = re.search(r'&quot;chartType&quot;:&quot;(\w+)&quot;', r.text)
 
if m:
vis_meta['charttype'] = m.group(1)
else:
print "Chart Type regex failed"
 
vis_meta['accesstime'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
vis_meta['id'] = id
vis_meta['cust'] = cust
vis_meta['baseurl'] = self.customers[cust]
vis_meta['url'] = url
 
with open(full + '/meta.json', 'w') as f:
f.write(json.dumps(vis_meta))
 
with open(full + '/COMPLETE', 'w') as f:
f.write('')
 
def scrape_customers(self):
for cust in self.customers:
try:
urls = self.get_vis_urls(cust)
except Exception as e:
print "get_vis_urls got borked"
print e
urls = []
curr_url = ''
for url in urls:
if 'http' not in url:
curr_url = 'http://' + self.customers[cust] + url
else:
curr_url = url
try:
self.pull_down_vis(cust, curr_url)
except Exception as e:
print "pull_down_vis got borked"
print e
 
 
def main():
scraper = Scraper()
scraper.scrape_customers()
 
 
if __name__ == "__main__":
main()
