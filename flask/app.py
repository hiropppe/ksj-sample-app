import io

from flask import Flask
from flask import request, render_template, jsonify
from flask import send_file
from bson import ObjectId

import pymongo, gridfs

from view.json import render

app = Flask(__name__)

mongo = pymongo.MongoClient(host="192.168.1.10", port=27017)
geo = mongo.test.geo
imagefs = gridfs.GridFS(mongo.test)

@app.route("/geo")
def index():
    return render_template("index.html")

@app.route("/geo/find")
def find_geo():
    data_class = request.args.get("data_class", "")
    ne = request.args.get("ne", "")
    sw = request.args.get("sw", "")

    q = {}
    if not data_class == "":
        q["data_class"] = data_class

    if not (ne == "" or sw == ""):
        ne_coord = [float(p) for p in ne.split(",")]
        sw_coord = [float(p) for p in sw.split(",")]

        q["geo"] = {
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
        print q 
    page = 1
    hit = 1000
    docs = [render.populate(doc) for doc in geo.find(q).skip((page-1)*hit).limit(hit)]
    return jsonify(ResultSet=docs)

@app.route("/image")
def find_image():
    id = request.args.get("data_id")
    seq = request.args.get("seq")

    q = { "data_id": ObjectId(id) }
    
    image = imagefs.find_one(q)
    if image: 
        return send_file(io.BytesIO(image.read()),
                    attachment_filename=image.filename,
                    mimetype='image/jpeg')
    else:
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

