#!/usr/bin/env python
# -*- coding:utf-8 -*-

import schema

def parse(data, point_dict):
    ksj_id = data.get("{http://www.opengis.net/gml/3.2}id")
    point_id = data.find("ksj:loc", namespaces=schema.namespaces).get("{http://www.w3.org/1999/xlink}href")[1:]
    point = point_dict[point_id]
    
    adm = data.find("ksj:adm", namespaces=schema.namespaces).text
    lgn = data.find("ksj:lgn", namespaces=schema.namespaces).text
    nop = data.find("ksj:nop", namespaces=schema.namespaces).text
    kdp = data.find("ksj:kdp", namespaces=schema.namespaces).text
    pop = data.find("ksj:pop", namespaces=schema.namespaces).text
    cop = data.find("ksj:cop", namespaces=schema.namespaces).text
    opd = data.find("ksj:opd/gml:TimeInstant/gml:timePosition", namespaces=schema.namespaces).text
    opa = data.find("ksj:opa", namespaces=schema.namespaces).text
    cpd = data.find("ksj:cpd", namespaces=schema.namespaces).text
    rmk = data.find("ksj:rmk", namespaces=schema.namespaces).text

    json = {
        "ksj_id": ksj_id,
        "point_id": point_id,
        "point": {
            "type": "Point",
            "coordinates": [point[1], point[0]]
        },
        "adm": adm,
        "lgn": lgn,
        "nop": nop,
        "kdp": kdp,
        "pop": pop,
        "cop": cop,
        "opd": opd,
        "opa": opa,
        "cpd": cpd,
        "rmk": rmk
    }

    return json
