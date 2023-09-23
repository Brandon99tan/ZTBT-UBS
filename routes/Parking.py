import json
import logging
from flask import jsonify, request, Response

from routes import app

logger = logging.getLogger(__name__)

@app.route('/parking-lot', endpoint='parking-lot', methods=['POST'])
def evaluate():
    data = request.get_json()
    logger.info("data sent for evaluation {}".format(data))
    BusParkingSlots = data.get("BusParkingSlots",0)
    CarParkingSlots = data.get("CarParkingSlots",0)
    ParkingCharges = data.get("ParkingCharges",0)
    expected_buses = data.get("Buses")
    expected_cars = data.get("Cars")
    expected_bikes = data.get("Bikes")
    bus_charges = ParkingCharges.get("Bus")
    car_charges = ParkingCharges.get("Car")
    bike_charges = ParkingCharges.get("Bike")

    # Initialize rejected counts
    rejected_buses = 0
    rejected_cars = 0
    rejected_bikes = 0
    result={}

    inbus = {}
    inbus["bike"] = bike_charges*12
    inbus["car"] = car_charges*2
    inbus["car2_and_2bike"] = car_charges*2 + bike_charges*2
    inbus["_car1_and7bike"] = car_charges*1 + bike_charges*7
    inbus["bus"] = bus_charges*1

    incar ={}
    incar["bike"] = bike_charges*5
    incar["car"] = car_charges*1

    inbus_sorted = sorted(inbus.items(), key=lambda x: x[1], reverse=True)
    incar_sorted = sorted(incar.items(), key=lambda x: x[1], reverse=True)
    profit = 0
    # Check if there are enough parking slots
    while CarParkingSlots>0 and (expected_buses>0 or expected_cars>0 or expected_bikes>0) :
        for key,value in incar_sorted:
            if key == "bike":
                if expected_bikes>=5:
                    expected_bikes -= 5
                    CarParkingSlots -= 1
                    profit += value
                    break
                else:
                    if expected_bikes * bike_charges >  car_charges:
                        expected_bikes = 0
                        CarParkingSlots -= 1
                        profit += expected_bikes * bike_charges
                        break
            else:
                if expected_cars>=1:
                    expected_cars -= 1
                    CarParkingSlots -= 1
                    profit += value
                    break
    while BusParkingSlots>0 and (expected_buses>0 or expected_cars>0 or expected_bikes>0):
        logger.info("BUS")
        for key,value in inbus_sorted:
            if key == "bike":
                if expected_bikes>=12:
                    expected_bikes -= 12
                    BusParkingSlots -= 1
                    profit += value
                    break
            elif key == "car":
                if expected_cars>=2:
                    expected_cars -= 2
                    BusParkingSlots -= 1
                    profit += value
                    break
            elif key == "car2_and_2bike":
                if expected_cars>=2 and expected_bikes>=2:
                    expected_cars -= 2
                    expected_bikes -= 2
                    BusParkingSlots -= 1
                    profit += value
                    break
            elif key == "_car1_and7bike":
                if expected_cars>=1 and expected_bikes>=7:
                    expected_cars -= 1
                    expected_bikes -= 7
                    BusParkingSlots -= 1
                    profit += value
                    break
            else:
                if expected_buses>=1:
                    expected_buses -= 1
                    BusParkingSlots -= 1
                    profit += value
                    break
        if expected_cars >0 or expected_bikes >0:
            carNbike = 0
            if expected_cars ==1 and expected_bikes<7:
                carNbike = car_charges + expected_bikes * bike_charges
            value = max(carNbike, bike_charges*expected_bikes)
            if expected_bikes>0:
                expected_bikes -= 7 if value == carNbike else expected_bikes
            expected_cars -= 1 if value == carNbike else 0
            profit += value

    result["profit"] = profit
    result["rejected_buses"] = expected_buses
    result["rejected_cars"] = expected_cars
    result["rejected_bikes"] = expected_bikes
    logger.info("My result :{}".format(inbus_sorted))
    logger.info("My result :{}".format(incar_sorted))
    answer={}
    answer["answer"] = result
    return json.dumps(answer)
