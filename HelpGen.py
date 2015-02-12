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

def linkDownLoad(url,filename):
    print url,filename
    urlretrieve(url,"TimeCat/"+filename+'.html')

def parseImages(soup):
    #Take care of the images inside each page:
    imgs = soup.find_all('a',{'class':'image'})
    for im in imgs:
        filename = im.img['src'].split("/")[-1]
	imageDownload("http://www.timecat.info"+im.img['src'],filename)
 	#modify the reference to the image
        new_tag =soup.new_tag( 'img', src="images/"+filename)
	soup.find('a',{'href':im['href']}).replaceWith(new_tag) 
    return soup
def main(argv):
    if(len(argv) == 1):
        output_path = argv[0]
    else:
	output_path = 'TimeCat'
#	output_path = 'helloWorld'
    URL = "http://www.timecat.info/wiki/index.php/TimeCat:Doc:Help?action=render"
#    URL = "http://128.2.116.101/mediawiki/index.php/HelpGenWiki4android?action=render"
    http = httplib2.Http()
    status,response = http.request(URL)

    filelist=[]
    for link in BeautifulSoup(response, parseOnlyThese = SoupStrainer('a')):
        if link.has_attr('href') and link.has_attr('title'):
	    print link
            status2,response2 = http.request(link['href']+'?action=render')
    	    soup=BeautifulSoup(response2)
 	    
	    soup=parseImages(soup); 
            
     	    #Take care of the links inside each page  
            ilinks = soup.find_all('a');
            for ilink in ilinks:
                filename = ilink['href'].split("/")[-1]
                
                if filename != '' and ilink['href'].startswith("https://www.timecat.info"):
		    filename = filename.replace(':','_')
		    if filename not in filelist: 
		    	linkDownLoad(ilink['href']+"?action=render",filename)
                        filelist.append(filename)
		    ilink['href']=filename+".html"
		    del(ilink['title'])
            with open(output_path+'/'+link['title'].replace(':','_')+'.html','w') as out_file:
            	out_file.write(soup.prettify(encoding="utf8"));

if __name__== "__main__":
    main(sys.argv[1:])
