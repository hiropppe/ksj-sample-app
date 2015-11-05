from flask import Flask
from flask import request, render_template, jsonify

import pymongo

from view.json import render

app = Flask(__name__)

mongo = pymongo.MongoClient(host="192.168.1.10", port=27017)
geo_point = mongo.test.geo_point

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/spot/find")
def find_spot():
    ksj_class = request.args.get("ksj_class", "")
    ne = request.args.get("ne", "")
    sw = request.args.get("sw", "")

    q = {}
    if not ksj_class == "":
        q["ksj_class"] = ksj_class

    if not (ne == "" or sw == ""):
        ne_coord = [float(p) for p in ne.split(",")]
        sw_coord = [float(p) for p in sw.split(",")]

        q["point"] = {
            "$geoWithin": {
                "$geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [sw_coord[1], sw_coord[0]],
                            [sw_coord[1], ne_coord[0]],
                            [ne_coord[1], ne_coord[0]],
                            [ne_coord[1], sw_coord[0]],
                            [sw_coord[1], sw_coord[0]]
                        ]
                    ]
                }
            }
        }

    page = 1
    hit = 100
    docs = [render.populate(doc) for doc in geo_point.find(q).skip((page-1)*hit).limit(hit)]
    return jsonify(ResultSet=docs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

