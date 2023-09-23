from flask import jsonify, request
import json
import logging
from routes import app

logger = logging.getLogger(__name__)

@app.route("/railway-builder", methods=['POST'])
def railway_builder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    res = get_railway_combinations(data)
    logging.info("My result :{}".format(res))
    return json.dumps(res)


def build_railway_combinations(railway_length, types_of_track_pieces, length_track_piece):
    dp = [0] * (railway_length + 1)
    dp[0] = 1
    for i in range(0, types_of_track_pieces):
        for j in range(length_track_piece[i], railway_length+1):
            dp[j] += dp[j - length_track_piece[i]]
    return dp[railway_length]

def get_railway_combinations(data):
    result = []
    for d in data:
        values = list(map(int, d.split(",")))
        railway_length = values[0]
        types_of_track_pieces = values[1]
        length_track_piece = values[2:]
        result.append(build_railway_combinations(railway_length, types_of_track_pieces, length_track_piece))
    return result