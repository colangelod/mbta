__author__ = 'Neil'

#port MySQLdb
import json
from pprint import pprint

file = open("mbta.json", "r")

json_data = json.load(file)

for train in json_data:
    route_id = train['route_id']
    route_title = train['route_title']
    mode_name = train['mode_name']
    directions = train['directions']
    alerts = train['alerts']
    predictions = train['predictions']

    print "INSERT INTO TrainRoutes " \
          "(RouteID, RouteName, ModeName) " \
          "VALUES ('%(route_id)s', '%(route_title)s', '%(mode_name)s');" % vars()

    for direction in directions:
        direction_id = direction['direction_id']
        direction_name = direction['direction_name']
        trips = direction['trip']

        #print direction_id, direction_name


    for prediction in predictions:
        already_trip = False
        #pprint(prediction)
        direction_name = prediction['direction_name']
        route_id = prediction['route_id']
        route_type = prediction['route_type']
        trip_id = prediction['trip_id']
        mode_name = prediction['mode_name']
        trip_name = prediction['trip_name']
        trip_headsign = prediction['trip_headsign']

        if "vehicle" in prediction:
            vehicle_id = prediction['vehicle']['vehicle_id']
            vehicle_lat = prediction['vehicle']['vehicle_lat']
            vehicle_lon = prediction['vehicle']['vehicle_lon']
            vehicle_bearing = prediction['vehicle']['vehicle_bearing']
            vehicle_timestamp = prediction['vehicle']['vehicle_timestamp']

            if not already_trip:
                print "INSERT INTO TrainTrips " \
                    "(TripID, RouteID, VehicleID, TripHeadsign) " \
                    "VALUES ('%(trip_id)s', '%(route_id)s', '%(vehicle_id)s', '%(trip_headsign)s');" % vars()
                already_trip = True

            print "INSERT INTO TrainLocations " \
                  "(TrainLAT, TrainLon,TrainTrips_TripID,TrainTrips_RouteID,TrainTrips,VehicleID) " \
                  "VALUES ('%(vehicle_lat)s', '%(vehicle_lon)s', '%(trip_id)s', '%(route_id)s', '%(vehicle_id)s');" % vars()

        for stop in prediction['stop']:
            pre_away = stop['pre_away']
            stop_sequence = stop['stop_sequence']
            stop_name = stop['stop_name']
            stop_id = stop['stop_id']
            print "INSERT INTO  TrainStops (TripID, StopID, StopName, StopSequence, PredAway) " \
                  "VALUES ('%(trip_id)s', '%(stop_id)s', '%(stop_name)s', '%(stop_sequence)s', '%(pre_away)s');" % vars()


    route_id = alerts['route_id']
    route_name = alerts['route_name']
    for alert in alerts['alerts']:
        alert_id = alert['alert_id']
        alert_text = alert['description_text']
        print "INSERT INTO Alerts " \
              "(RouteID, AlertID, AlertText) " \
              "VALUES ('%(route_id)s', '%(alert_id)s', '%(alert_text)s');" % vars()

    #print "\n\n"