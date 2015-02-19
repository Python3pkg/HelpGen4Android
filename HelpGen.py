# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 16:37:36 2015

@author: yifan
"""
from collections import Counter
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

def parsePage(server,soup):
     #Take care of the links inside each page  
    ilinks = soup.find_all('a');
    for ilink in ilinks:
        #find out the static file name
        filename = ilink['href'].split("/")[-1] 
        if filename != '' and ilink['href'].startswith(server):
        #modify name to fix a mediawiki bug
            filename = filename.replace(':','_')
	    ilink['href']=filename+".html"
	    del(ilink['title'])
    return soup
  
def downloadPage(outputDir, url, soup):
    name = url.split("/")[-1].split("?")[0]	 
    print name             
    with open(outputDir+'/'+name.replace(':','_')+'.html','w') as out_file:
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
    
    traversal_queue = []
    download_queue = []
 
#    URL = "http://128.2.116.101/mediawiki/index.php/HelpGenWiki4android?action=render"
    http = httplib2.Http()
    status,response = http.request(URL)

    #enque the link in the template page
    for link in BeautifulSoup(response, parseOnlyThese = SoupStrainer('a')):
        if link.has_attr('href') and link.has_attr('title'):
	    print link
            traversal_queue.append(link['href']+'?action=render')
    
    #traverse the link graph
    while  traversal_queue:
	link = traversal_queue.pop(0)
	#find internel links
	status, response = http.request(link)
        soup = BeautifulSoup(response)
	ilinks=soup.find_all('a')
	for ilink in ilinks:
            if ilink.has_attr('href'):
                render_ilink =ilink['href']+'?action=render'    
	        if ilink['href'].startswith(server) \
			and render_ilink not in traversal_queue\
			and render_ilink not in download_queue\
			and not (ilink.has_attr('class') and ilink['class']!='image' ):
	            traversal_queue.append(render_ilink)
        #enque link into download_queue
        download_queue.append(link)
        #print Counter(traversal_queue)
    print download_queue

    #download the link
    while download_queue:
	link = download_queue.pop(0)
        print link
        status, response = http.request(link)
	soup = BeautifulSoup(response)
        #parse and download images
        soup = parseImages(outputDir, server, soup)
        #parse page
        soup = parsePage(server,soup)
        #download page
        downloadPage(outputDir, link, soup)   
        
'''
    soup=parseImages(outputDir, server, soup)
            
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
'''
if __name__== "__main__":
    main(sys.argv[1:])
