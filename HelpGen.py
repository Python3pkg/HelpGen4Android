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
import ConfigParser
import os
#download the image with specified url
def imageDownload(outputDir,page_url,filename):
    urlretrieve(page_url,outputDir+"/images/"+filename)

def linkDownLoad(outputDir,url,filename):
    print url,filename
    urlretrieve(url,outputDir+"/"+filename+'.html')

def parseImages(outputDir, server,soup):
    #Take care of the images inside each page:
    imgs = soup.find_all('a',{'class':'image'})
    for im in imgs:
        filename = im.img['src'].split("/")[-1]
	imageDownload(outputDir,server+im.img['src'],filename)
 	#modify the reference to the image
        new_tag =soup.new_tag( 'img', src="images/"+filename)
	soup.find('a',{'href':im['href']}).replaceWith(new_tag) 
    return soup

def downloadLinkRecursively(url):
    status,response = http.request(url+'?action=render')
    soup=BeautifulSoup(response)
 	    
    soup=parseImages(outputDir, server, soup); 
            
    #Take care of the links inside each page  
    ilinks = soup.find_all('a');
    for ilink in ilinks:
        #find out the static file name
        filename = ilink['href'].split("/")[-1]
        #if this page belongs to the same site and it hasnt been downloaded yet 
        if filename != '' and ilink['href'].startswith(server):
        #modify name to fix a mediawiki bug
            filename = filename.replace(':','_')
            if filename not in filelist: 
	        linkDownLoad(outputDir,ilink['href']+"?action=render",filename)
                filelist.append(filename)
		ilink['href']=filename+".html"
		del(ilink['title'])
        with open(outputDir+'/'+link['title'].replace(':','_')+'.html','w') as out_file:
            	out_file.write(soup.prettify(encoding="utf8"));

      
def main(argv):

    # get configuration
    config = ConfigParser.SafeConfigParser()
    config.read('config.cfg')
    
    outputDir = config.get('s1','outputDir')  
    URL = config.get('s1','wikitemplateurl')+"?action=render"
    print URL
    server = URL.split("/")[0]+"//"+URL.split("/")[2]
    print server
    #preparing output directory
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    if not os.path.exists(outputDir+'/images/'):
        os.makedirs(outputDir+'/images/') 
     
#    URL = "http://128.2.116.101/mediawiki/index.php/HelpGenWiki4android?action=render"
    http = httplib2.Http()
    status,response = http.request(URL)

    filelist=[]
    for link in BeautifulSoup(response, parseOnlyThese = SoupStrainer('a')):
        if link.has_attr('href') and link.has_attr('title'):
	    print link
            status2,response2 = http.request(link['href']+'?action=render')
    	    soup=BeautifulSoup(response2)
 	    
	    soup=parseImages(outputDir, server, soup); 
            
     	    #Take care of the links inside each page  
            ilinks = soup.find_all('a');
            for ilink in ilinks:
                #find out the static file name
		filename = ilink['href'].split("/")[-1]
                #if this page belongs to the same site and it hasnt been downloaded yet 
                if filename != '' and ilink['href'].startswith(server):
		    #modify name to fix a mediawiki bug
		    filename = filename.replace(':','_')
		    if filename not in filelist: 
		    	linkDownLoad(outputDir,ilink['href']+"?action=render",filename)
                        filelist.append(filename)
		    ilink['href']=filename+".html"
		    del(ilink['title'])
            with open(outputDir+'/'+link['title'].replace(':','_')+'.html','w') as out_file:
            	out_file.write(soup.prettify(encoding="utf8"));

if __name__== "__main__":
    main(sys.argv[1:])
