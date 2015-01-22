# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 16:37:36 2015

@author: yifan
"""

from bs4 import BeautifulSoup,SoupStrainer
import httplib2
from urllib import urlopen
import shutil
import sys

def main(argv):
    if(len(argv) == 1):
        output_path = argv[0]
        print output_path
    else:
		output_path = 'TimeCat'
#output_path = 'helloWorld'
    URL = "http://www.timecat.info/wiki/index.php/TimeCat:Doc:Help?action=render"
     #URL = "http://128.2.116.101/mediawiki/index.php/HelpGenWiki4android?action=render"
    http = httplib2.Http()
    status,response = http.request(URL)
    for link in BeautifulSoup(response, parseOnlyThese = SoupStrainer('a')):
        if link.has_attr('href'):
            response = urlopen(link['href']+'?action=render')
            with open(output_path+'/'+link['title']+'.html','w') as out_file:
                shutil.copyfileobj(response,out_file)

if __name__== "__main__":
    main(sys.argv[1:])