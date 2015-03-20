__author__ = 'Neil'

import MySQLdb
import json

file = open("mbta.json", "r")

json_data = json.load(file)

for train in json_data:
    route_id = train['route_id']
    route_title = train['route_title']
    directions = train['directions']
    alerts = train['alerts']
    predictions = train['predictions']

    print route_id, route_title

    for direction in directions:
        direction_id = direction['direction_id']
        direction_name = direction['direction_name']
        trips = direction['trip']

        #print direction_id, direction_name

        for trip in trips:
            trip_id = trip['trip_id']
            trip_name = trip['trip_name']
            stops = trip['stop']
            print trip

            #print trip_id, trip_name

            for stop in stops:
                stop_sequence = stop['stop_sequence']
                sch_dep_dt = stop['sch_dep_dt']
                sch_arr_dt = stop['sch_arr_dt']
                stop_name = stop['stop_name']
                stop_id = stop['stop_id']

                #print stop_sequence, stop_id, stop_name

    for prediction in predictions:
        direction_name = prediction['direction_name']
        route_id = prediction['route_id']
        route_type = prediction['route_type']
        trip_id = prediction['trip_id']
        mode_name = prediction['mode_name']
        trip_name = prediction['trip_name']
        vehicle_id = prediction['vehicle']['vehicle_id']
        vehicle_lat = prediction['vehicle']['vehicle_lat']
        vehicle_lon = prediction['vehicle']['vehicle_lon']
        vehicle_bearing = prediction['vehicle']['vehicle_bearing']
        vehicle_timestamp = prediction['vehicle']['vehicle_timestamp']

        #insert into TrainLocations (TrainLAT, TrainLon,TrainTrips_TripID,TrainTrips_RouteId,TrainTrips,VehicleID)

        for stop in prediction['stop']:
            pre_away = stop['pre_away']
            stop_sequence = stop['stop_sequence']
            stop_name = stop['stop_name']
            stop_id = stop['stop_id']
            #insert into TrainStops (TripID, StopID, StopName, StopSequence, PredAway)
    print "\n\n"