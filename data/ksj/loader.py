from lxml import etree

import pymongo

from parser import schema 

def load_data(ksj_file, ksj_name, ksj_parser):
    mongo = pymongo.MongoClient(host="192.168.1.10", port=27017)
    db = mongo.test
    cl = db.geo_point
    
    point_context = etree.iterparse(
        ksj_file,
        events={"end",},
        tag="{http://www.opengis.net/gml/3.2}Point",
        recover=True
    )

    point_dict = {}
    for _, point in point_context:
        point_id = point.get("{http://www.opengis.net/gml/3.2}id")
        point_loc = point.find("gml:pos", namespaces=schema.namespaces).text
        point_dict[point_id] = [float(p) for p in point_loc.split()]

    ksj_context = etree.iterparse(
        ksj_file,
        events={"end",},
        tag="{http://nlftp.mlit.go.jp/ksj/schemas/ksj-app}%s" % ksj_name,
        recover=True
    )
    
    for _, ksj in ksj_context:
        cl.insert_one(ksj_parser.parse(ksj, point_dict))
