__author__ = 'Neil'

import MySQLdb as mdb
import json
from pprint import pprint
import sys
import time

t0 = time.time()

file = open("nextbus.json", "r")

json_data = json.load(file)

con = mdb.connect(host="localhost", user="root", passwd="", db="databaseproject")
cursor = con.cursor()


for tag in json_data:
    routes = json_data[tag]['routes']
    title = json_data[tag]['title']


    i = 0
    for route in routes:
        for vehicle in json_data[tag]['routes'][i]['vehicles']:
            #print vehicle
            vehicle_id = vehicle['id']
            if "routeTag" in vehicle:
                route_tag = vehicle['routeTag']
            else:
                route_tag = "UNKWN"
            if "dirTag" in vehicle:
                dir_tag = vehicle['dirTag']
            lat = vehicle['lat']
            lon = vehicle['lon']
            secsSinceReport = vehicle['secsSinceReport']
            predictable = True if vehicle['predictable'] == "true" else False
            heading = vehicle['heading']

            cursor.execute("select VehicleNumber FROM Busses WHERE VehicleNumber = (%s) AND RTag = (%s)", (vehicle_id, route_tag))
            res = cursor.fetchone()
            if res is None:
                cursor.execute("insert into Busses (VehicleNumber, RTag, BusTitle) VALUES (%s, %s, %s)", (vehicle_id, route_tag, title))

            cursor.execute("insert into Locations (VehicleNumber, BusLAT, BusLON, Predictable) VALUES (%s,%s,%s,%s)", (vehicle_id, lat, lon, predictable))
        i = i + 1

for tag in json_data:
    routes = json_data[tag]['routes']
    title = json_data[tag]['title']

    i = 0
    for routes in json_data[tag]['routes']:
        route_tag = routes['tag']
        route_title = routes['title']
        if json_data[tag]['routes'][i]['stops'] is not None:
            stop = json_data[tag]['routes'][i]['stops']
            i = i + 1
            stop_title = stop['title']
            stop_lon = stop['lon']
            stop_lat = stop['lat']
            stop_id = stop['stopId']
            stop_tag = stop['tag']
            predictions = stop['predictions']

            cursor.execute("select StopID from BusStops WHERE StopID = (%s)", [stop_id])
            res = cursor.fetchone()

            if res is None:
                cursor.execute("insert into BusStops (StopID, StopName, StopLAT, StopLON) VALUES (%s,%s,%s,%s)", (stop_id, stop_title, stop_lat, stop_lon))

            for prediction in predictions:
                epochTime = prediction['epochTime']
                seconds = prediction['seconds']
                vehicle = prediction['vehicle']
                trip_tag = prediction['tripTag']
                isDeparture = prediction['isDeparture']
                dir_tag = prediction['dirTag']
                minutes = prediction['minutes']
                block = prediction['block']

                slowness, affectedByLayover, is_delayed = None, None, None
                if "slowness" in prediction:
                    slowness = prediction['slowness']
                if "affectedByLayover" in prediction:
                    affectedByLayover = prediction['affectedByLayover']
                if "isDelayed" in prediction:
                    is_delayed = True

                if slowness is not None and affectedByLayover is not None and is_delayed is not None:
                    cursor.execute("insert into BusDelays (VehicleNumber, StopID, AffectedByLayover, IsDelayed, Slowness) VALUES (%s,%s,%s,%s,%s)", (vehicle, stop_id, affectedByLayover, is_delayed, slowness))

                #print vehicle, stop_id, dir_tag, seconds
                cursor.execute("select VehicleNumber from Busses WHERE VehicleNumber = (%s)", [vehicle])
                res = cursor.fetchone()
                if res is not None:
                    cursor.execute("insert into BusStopTimes (VehicleNumber, StopID, DirTAG, Seconds) VALUES (%s,%s,%s,%s)", (vehicle, stop_id, dir_tag, seconds))
                else:
                    print "Failed to insert busstoptime for vehicleid %(vehicle)s -- stopid: %(stop_id)s dir_tag: %(dir_tag)s" % vars()

con.commit()

print time.time() - t0