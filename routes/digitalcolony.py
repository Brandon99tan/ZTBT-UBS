import json
import logging

from flask import request
from routes import app

logger = logging.getLogger(__name__)

@app.route('/digital-colony', endpoint='digital-colony', methods=['POST'])
def evaluate():
    data = request.get_json()
    colony = data[0].get("colony")
    counter = 0
    answer=[]
    while counter < 50:
        counter += 1
        colony = next_generation(colony)
        if counter == 20:
            answer.append(colony)
        if counter == 50:
            answer.append(colony)
    return json.dumps(answer)

def next_generation(colony):
    answer = ""
    answer+= colony[0]
    weight = 0
    for x in colony:
        weight += int(x)
    for x in range(len(colony)-1):
        first = colony[x]
        second = colony[x+1]
        if first == second:
            answer += 0
        else:
            signature = first - second
            if signature < 0:
                signature = 10-signature
            temp = signature+weight
            temp = temp%10
            answer += temp
    return answer
