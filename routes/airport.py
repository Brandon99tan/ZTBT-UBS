from flask import jsonify, request, Response
import json
import logging
from routes import app

logger = logging.getLogger(__name__)
class Passenger:
    def __init__(self, departureTime):
        self.departureTime = departureTime
        self.numberOfRequests = 0
    def askTimeToDeparture(self):
        self.numberOfRequests += 1
        return self.departureTime
    def getNumberOfRequests(self):
        return self.numberOfRequests

    def execute(prioritisation_function, passenger_data, cut_off_time):
        totalNumberOfRequests = 0
        passengers = []
        # Initialise list of passenger instances
        for i in range(len(passenger_data)):
            passengers.append(Passenger(passenger_data[i]))
        print(f"passengers: {passengers}")
        # Apply solution and re-shuffle with departure cut-off time
        prioritised_and_filtered_passengers = prioritisation_function(passengers, cut_off_time)

        # Sum totalNumberOfRequests across all passengers
        for i in range(len(passengers)):
            totalNumberOfRequests += passengers[i].getNumberOfRequests()
        print("totalNumberOfRequests: " + str(totalNumberOfRequests))

        # Print sequence of sorted departure times
        print("Sequence of prioritised departure times:")
        prioritised_filtered_list = []
        for i in range(len(prioritised_and_filtered_passengers)):
            # print(prioritised_and_filtered_passengers[i].departureTime, end=" ")
            prioritised_filtered_list.append(prioritised_and_filtered_passengers[i].departureTime)

        print("\n")
        return {
            "sortedDepartureTimes": prioritised_filtered_list,
            "numberOfRequests": totalNumberOfRequests,
        }
    def prioritisation_function(passengers, cut_off_time):
        dict_P = {}
        for i in range(len(passengers)):
            dict_P[passengers[i]] = passengers[i].askTimeToDeparture()
            logging.info("dict_P {}".format(dict_P))

        #sort the dictionary based on the value keep the key
        sorted_dict_P = dict(sorted(dict_P.items(), key=lambda item: item[1]))
        logging.info("dict_P SORTED VERS {}".format(sorted_dict_P))

        #if value < cut_off_time then remove the key from the dictionary
        filtered_dict = {key: value for key, value in sorted_dict_P.items() if value >= cut_off_time}

        return filtered_dict


@app.route("/airport", methods=['POST'])
def airport_check_in():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for record in data:
        res = Passenger.execute(Passenger.prioritisation_function, record["departureTimes"], record["cutOffTime"])
        result.append({"id": record["id"], **res})
    return Response(json.dumps(result), mimetype="application/json")
