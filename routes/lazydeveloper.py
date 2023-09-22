import json
import logging

from flask import request
from routes import app

logger = logging.getLogger(__name__)

@app.route('/lazy-developer', endpoint='lazy-developer', methods=['POST'])
def evaluate():
    data = request.get_json()
    classes = data.get("classes")
    statements = data.get("statements")
    logging.info("classes{} , statements{}".format(classes, statements))

    # Fill in your solution here and return the correct output based on the given input
    results = {}
    dict_class = {}
    val = [
      k for c in classes for k in c.keys()
    ]  # Order, OrderType, MarketOrderType, LimitOrderType, OrderSide, Status, Allocation, LongAllocation, EmptyAllocation
    for item in classes:
      dict_class.update(item)
    print(dict_class)
    for statement in statements:
      words = [""]
      query = statement.split('.')
      results[statement] = words
      if query[0] in dict_class.keys():
        if isinstance(dict_class[query[0]], list):
          words = sorted(dict_class[query[0]])
        if isinstance(dict_class[query[0]], dict):
          words = sorted([k for k in dict_class[query[0]].keys()])
        if isinstance(dict_class[query[0]], str):
          continue

        if len(query) > 1:
          print(type(dict_class.get(query[1], None)))
          if query[1] == '':
            print("empty")
            words = sorted([k for k in dict_class[query[0]].keys()])
          elif isinstance(dict_class.get(query[1], None), list):
            words = sorted(dict_class[query[1]])
          else:  # start with query[1]
            # print(type(dict_class.get(query[0],None)[query[1]]))
            x = [k for k in words if k.startswith(query[1])]
            words = x

      if len(words) > 5:
        words = words[:5]
      results[statement] = words


      return json.dumps(results)