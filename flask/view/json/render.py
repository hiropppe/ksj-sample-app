#!/usr/bin/env python
# -*- coding:utf-8 -*-

def populate(doc):
    doc["_id"] = str(doc["_id"])
    return doc
