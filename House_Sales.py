#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      densm
#
# Created:     19/11/2017
# Copyright:   (c) densm 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib
from bs4 import BeautifulSoup
import json
import time
import csv
from datetime import datetime

myfinalcsv="C:/Users/densm/Desktop/house_new.csv"
header=['id', 'bed', 'bath', 'parking', 'price', 'address', 'lat', 'long', 'FloorplanURL', 'pageURL', 'sale date','landsize','daysago']
myurlbase1='https://www.realestate.com.au/sold/property-house-between-0-1000000-in-granville%2c+nsw+2142%3b+lidcombe%2c+nsw+2141%3b+merrylands%2c+nsw+2160%3b+guildford%2c+nsw+2161%3b+auburn%2c+nsw+2144%3b+parramatta%2c+nsw+2150%3b+holroyd%2c+nsw+2142%3b+old+guildford%2c+nsw+2161%3b+rosehill%2c+nsw+2142%3b+harris+park%2c+nsw+2150%3b+south+granville%2c+nsw+2142%3b+clyde%2c+nsw+2142%3b+newington%2c+nsw+2127%3b+silverwater%2c+nsw+2128/list-'
myurlbase2='?activeSort=solddate'
Pages=50

with open(myfinalcsv,'wb') as g:
    w = csv.writer(g)
    w.writerow(header)

    for page in range(1,51):
        print str(page)+" of 50"
        myurl=myurlbase1+str(page)+myurlbase2

        r = urllib.urlopen(myurl).read()
        soup = BeautifulSoup(r, "html.parser")

        scripts = soup.find_all('script')

        count=1
        for script in scripts:
            ss = script.prettify()
            if 'REA.initialState = ' in ss:
                J = str(script)
                J1 = J.split('REA.initialState = ')
                J2 = J1[1].rsplit('</script')
                J3 = J2[0].rsplit(';', 1)
                JsonText = J3[0].decode('utf-8')
                print "script# "+str(count)
            count+=1

        housedata = json.loads(JsonText)

        for record in range(0,20):

            id_=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['listingId']
            bed=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['features']['general']['bedrooms']
            bath=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['features']['general']['bathrooms']
            parking=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['features']['general']['parkingSpaces']
            price=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['price']['display']
            address=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['address']['streetAddress']+" "+housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][0]['address']['locality']
            try:
                lat=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['address']['location']['latitude']
                longi=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['address']['location']['longitude']
            except:
                lat=''
                longi=''
            try:
                floorplan=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['images'][-1]['server']+'/2522x1950-resize,r=33,g=40,b=46'+housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][0]['images'][-1]['uri']
            except:
                floorplan=''
            page=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['_links']['prettyUrl']['href']
            saledate=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['dateSold']['value']
            try:
                landsize=housedata['pageData']['data']['searchResults']['tieredResults'][0]['results'][record]['landSize']['value']
            except:
                landsize=''

            b=saledate.split('-')
            saledate2 = datetime(int(b[0]), int(b[1]),int(b[2]))
            diff = datetime.now() - saledate2
            daysago=diff.days
            item=[id_,bed,bath,parking,price,address,lat,longi,floorplan,page,saledate,landsize,daysago]
            w.writerow(item)


        time.sleep(10)
