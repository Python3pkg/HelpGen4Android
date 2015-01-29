# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 16:37:36 2015

@author: yifan
"""

from bs4 import BeautifulSoup,SoupStrainer,Tag
import httplib2
from urllib import urlopen
from urllib import urlretrieve
import shutil
import sys

#download the image with specified url
def imageDownload(page_url,filename):
    urlretrieve(page_url,"TimeCat/images/"+filename)

def main(argv):
    if(len(argv) == 1):
        output_path = argv[0]
        print output_path
    else:
	output_path = 'TimeCat'
#	output_path = 'helloWorld'
    URL = "http://www.timecat.info/wiki/index.php/TimeCat:Doc:Help?action=render"
#    URL = "http://128.2.116.101/mediawiki/index.php/HelpGenWiki4android?action=render"
    http = httplib2.Http()
    status,response = http.request(URL)
    for link in BeautifulSoup(response, parseOnlyThese = SoupStrainer('a')):
        if link.has_attr('href') and link.has_attr('title'):
            response1 = urlopen(link['href']+'?action=render')
            with open(output_path+'/'+link['title']+'.html','w') as out_file:
                shutil.copyfileobj(response1,out_file)
	    status2,response2 = http.request(link['href']+'?action=render')
    	    soup=BeautifulSoup(response2)

 	    #Take care of the images inside each page:
	    imgs = soup.find_all('a',{'class':'image'})
	    for im in imgs:
		filename = im.img['src'].split("/")[-1]
		print filename
		imageDownload("http://www.timecat.info"+im.img['src'],filename)

if __name__== "__main__":
    main(sys.argv[1:])
