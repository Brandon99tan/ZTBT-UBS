from flask import jsonify, request, send_file
import json
import logging
from routes import app


logger = logging.getLogger(__name__)


@app.route("/payload_crackme", methods=['GET'])
def payload_crackme():
    return send_file('payload_crackme', as_attachment=True)

