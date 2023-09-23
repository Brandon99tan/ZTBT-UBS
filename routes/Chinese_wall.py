from flask import jsonify, request
import json
import logging
from routes import app

logger = logging.getLogger(__name__)

@app.route("/chinese-wall", methods=['GET'])
def chinese_wall():
    answer={
  "1": "Fluffy",
  "2": "Galatic",
  "3": "Mangoes",
  "4": "Subatomic",
  "5": "Jellyfish"
}