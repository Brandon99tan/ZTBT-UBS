from flask import jsonify, request
import json
import logging
from routes import app

logger = logging.getLogger(__name__)


@app.route("/payload_crackme", methods=['GET'])
def payload_crackme():
    return json.dumps("334-12321321321")
