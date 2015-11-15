#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import pymongo, gridfs, json
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

url_template = u'https://www.chiikinogennki.soumu.go.jp/k-cloud-api/v001/kanko/view/{refbase}/{fid}'

def crawl(host='192.168.1.10', port=27017,
        data_db='test', data_collection='geo',
        image_db='test'):
    client = pymongo.MongoClient(host=host, port=port)
    geo = client[data_db][data_collection]
    gfs = gridfs.GridFS(client[image_db])
    
    data_count = 0
    image_count = 0
    put_count = 0

    q = {
        'views': {'$exists': 1}
    }
    
    for data in geo.find(q, no_cursor_timeout=True):
        data_count += 1
        
        refbase = data['mng']['refbase']
        for i, view in enumerate(data['views']):
            image_count += 1

            fid = view['fid']
            caption = None
            if 'name' in view:
                caption = view['name']['written']

            url = url_template.format(refbase=refbase, fid=fid)
    
            s = requests.Session()
            s.mount('https://', TLSv1Adapter())
    
            print 'Fetch:', url
            r = requests.get(url)

            if r.status_code == 200:
                gfs.put(r.content,
                        filename=fid,
                        data_id=data['_id'],
                        caption=caption,
                        content_type='image/jpeg') 
            else:
                print r.status_code
        
            put_count += 1

    print 'Total', data_count, 'data', image_count, 'image', put_count, 'put'
