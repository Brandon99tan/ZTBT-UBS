from flask import jsonify, request, Response
import json
import logging
from routes import app

logger = logging.getLogger(__name__)

@app.route("/chinese-wall", methods=['GET'])
def chinese_wall():
    answer={
  "1": "Fluffy",
  "2": "Galactic",
  "3": "Mangoes",
  "4": "Subatomic",
  "5": "Monkey"
    }
    return Response(json.dumps(answer), mimetype='application/json')