#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import pymongo, json
import requests, urllib
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class TLSv1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

url_template = u'https://www.chiikinogennki.soumu.go.jp/k-cloud-api/v001/kanko/{genre}/json?skip={skip}&limit={limit}'

def crawl(genre, host='192.168.1.10', port=27017, db='test', collection='geo'):
    client = pymongo.MongoClient(host=host, port=port)
    geo = client[db][collection]
    
    encoded_genre = urllib.quote(genre.encode('utf-8'))

    data_count = 0
    insert_count = 0

    skip = 0
    limit = 50
    
    print genre 
    while True:
        url = url_template.format(genre=genre, skip=skip, limit=limit)
    
        s = requests.Session()
        s.mount('https://', TLSv1Adapter())
    
        print 'Fetch:', url
        r = requests.get(url)

        if r.status_code == 200:
            json_data = json.loads(r.text)
            tourspots = json_data[u'tourspots']
            
            if len(tourspots) == 0:
                break
            
            data_count += len(tourspots)
            
            for spot in tourspots:
                spot['data_class'] = 'kcloud_tour'
                spot['name'] = spot['name']['name1']['written']
                if 'coordinates' in spot['place']:
                    coordinates = spot['place']['coordinates']
                    if 'longitude' in coordinates and 'latitude' in coordinates:
                        lng = float(coordinates['longitude'])
                        lat = float(coordinates['latitude'])
                
                        spot['geo'] = {'type': 'Point', 'coordinates': [lng, lat]}

                try:
                    geo.insert(spot)
                except Exception, e:
                    print e.message
                insert_count += 1
        else:
            print r.status_code
        
        skip += limit

    print 'Total', data_count, 'data', insert_count, 'inserted'
