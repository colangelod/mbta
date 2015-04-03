#port MySQLdb
import json
import MySQLdb as mdb
import time
from pprint import pprint

cnx = mdb.connect(host='localhost', user='root', passwd="bingobingo", db='databaseproject')
cursor = cnx.cursor()


t0 = time.time()


class MBTAMySQL:

    def __init__(self):
        self.file = open("mbta.json", "r")

        self.json_data = json.load(self.file)

    def main(self):
        for train in self.json_data:
            route_id = train['route_id']
            route_title = train['route_title']
            mode_name = train['mode_name']
            directions = train['directions']
            alerts = train['alerts']
            predictions = train['predictions']
            cursor.execute( "select RouteID from TrainRoutes where RouteID = (%s)", [route_id])
            res = cursor.fetchone()
            if res is None:
                cursor.execute( "insert into TrainRoutes (RouteID, RouteName, ModeName) VALUES (%s,%s,%s)", (route_id, route_title, mode_name))


            for direction in directions:
                direction_id = direction['direction_id']
                direction_name = direction['direction_name']
                trips = direction['trip']

            for prediction in predictions:

                already_trip = False
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
                        cursor.execute( "select TripID from TrainTrips where TripID = (%s)", [trip_id])
                        res = cursor.fetchone()
                        if res is None:
                            cursor.execute( "insert into TrainTrips (TripID, RouteId, VehicleId, TripHeadsign, InsertTime) VALUES (%s,%s,%s,%s,%s)", (trip_id, route_id, vehicle_id, trip_headsign, t0 ))  #  % vars()
                        already_trip = True
                    cursor.execute( "select VehicleID from TrainLocations where VehicleID = (%s) and TripID = (%s)", (vehicle_id, trip_id))
                    res = cursor.fetchone()
                    if res is None:
                        cursor.execute( "select TripID from TrainTrips where TripID = (%s) and VehicleID = (%s)", (trip_id, vehicle_id))
                        res = cursor.fetchone()
                        if res is not None:
                            cursor.execute( "insert into TrainLocations (TrainLAT, TrainLon,TripID,RouteId,VehicleID) VALUES (%s,%s,%s,%s,%s)", (vehicle_lat,vehicle_lon,trip_id,route_id,vehicle_id) )#  % vars()
                    else:
                        cursor.execute( "update TrainLocations set TrainLAT = (%s), TrainLON = (%s) where TripID = (%s) and VehicleID = (%s)", (vehicle_lat,vehicle_lon,trip_id,vehicle_id) )
                    stop_ids = []
                    for stop in prediction['stop']:
                        pre_away = stop['pre_away']
                        stop_sequence = stop['stop_sequence']
                        stop_name = stop['stop_name']
                        stop_id = stop['stop_id']
                        if stop_id not in stop_ids:
                            stop_ids.append(stop_id)
                            cursor.execute( "select TripID from TripStops where TripID = (%s) and StopID = (%s)", (trip_id, stop_id))
                            res = cursor.fetchone()
                            if res is None:
                                cursor.execute( "insert into TripStops (TripID, StopID, StopName, StopSequence, PredAway) VALUES (%s,%s,%s,%s,%s)",(trip_id,stop_id,stop_name,stop_sequence,pre_away))
                            else:
                                cursor.execute( "update TripStops set StopID = (%s), StopName = (%s), StopSequence = (%s), PredAway = (%s) where TripID = (%s) and StopID = (%s)", (stop_id,stop_name,stop_sequence,pre_away,trip_id,stop_id ))
            route_id = alerts['route_id']
            route_name = alerts['route_name']
            for alert in alerts['alerts']:
                alert_id = alert['alert_id']
                alert_text = alert['header_text']
                cursor.execute( "select AlertID from Alerts where RouteID = (%s) and AlertID = (%s)", (route_id, alert_id))
                res = cursor.fetchone()
                if res is None:
                    cursor.execute( "insert into Alerts (RouteID, AlertID, AlertText) values (%s,%s,%s)", (route_id, alert_id, alert_text))

        cnx.commit()
        print "MBTA transaction committed."
