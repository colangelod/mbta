import MySQLdb as mdb
from tabulate import tabulate

cnx = mdb.connect(host="localhost", user="root", passwd="", db="databaseproject")
cursor = cnx.cursor()

def query16():
    query_and_print("Select delayedBuses.StopName as StopName, Max(Round(BusDelays.Slowness, 2)) as DelayedBY, (Select Count(Busses.BusTitle) from ((Busses Inner Join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) inner Join BusStops stops on stops.StopID = BusStopTimes.StopID) inner join BusDelays on BusStopTimes.VehicleNumber = BusDelays.VehicleNumber where BusDelays.isDelayed = '1' and stops.StopName = delayedBuses.StopName) as numberOfAffectedBuses from ((BusStops delayedBuses Inner Join BusStopTimes on delayedBuses.StopID= BusStopTimes.StopID) Inner Join BusDelays on BusStopTimes.StopID = BusDelays.StopID) where BusDelays.isDelayed = '1' and BusDelays.AffectedByLayover = '0'",
        ("Stop Name", "Slowness multiplyer", "Number of affected busses"))
def query15():
    query_and_print("Select Busses.BusTitle as bus_name, Round(AVG(Slowness), 2) as avg_slowness, Round(MAX(Slowness),2) as max_slowness, Round(SUM(Slowness),2) as total_slowness from (Select Busses.VehicleNumber as vehicleNumber from (Busses Inner Join BusDelays On BusDelays.VehicleNumber = Busses.VehicleNumber ) Inner Join Locations On Busses.VehicleNumber = Locations.VehicleNumber where BusDelays.isDelayed = '1' AND Locations.Predictable = '1') numbers Inner Join BusDelays On BusDelays.VehicleNumber = numbers.vehicleNumber Inner Join Busses on Busses.VehicleNumber = numbers.vehicleNumber where numbers.vehicleNumber = BusDelays.VehicleNumber Group by Busses.BusTitle Order by bus_name ASC, avg_slowness ASC, max_slowness ASC, total_slowness ASC",
        ("Route Number", "Average slowness multiplier", "Max slowness multiplier", "Sum slowness multiplyer"))

def query14():
    query_and_print("Select Count(TrainTrips.TripID) from (((TrainTrips inner join TrainRoutes on TrainTrips.RouteID = TrainRoutes.RouteID) inner join Alerts on Alerts.RouteID = TrainRoutes.RouteID ) inner join TrainLocations on TrainRoutes.RouteID = TrainLocations.RouteID) inner join TripStops on TripStops.TripID = TrainTrips.TripID where Alerts.AlertID IS NOT NULL AND TrainLocations.TrainLAT = '42.3476' and TrainLocations.TrainLON = '-71.0747' and TripStops.PredAway = (Select TripStops.PredAway as pred from TripStops where TripStops.PredAway <= 1)",
        ["Number of arriving trains with Alerts"])
def query13():
    query_and_print( "SELECT TrainTrips.RouteID, TrainRoutes.RouteName, Alerts.AlertID, TrainLocations.TrainLAT, TrainLocations.TrainLON from TrainTrips INNER JOIN TrainRoutes ON TrainTrips.RouteID = TrainRoutes.RouteID LEFT JOIN Alerts ON TrainRoutes.RouteID = Alerts.RouteID INNER JOIN TrainLocations ON TrainTrips.VehicleID = TrainLocations.VehicleID WHERE Alerts.AlertID != '0' AND Alerts.AlertID != '70641' ORDER BY Alerts.AlertID ASC, RouteID ASC",
        ("Route ID", "Route Name", "Alert ID", "Train LAT", "Train LON"))

def query12():
    query_and_print("Select * from ((Select TrainRoutes.RouteName as maxRouteTime from (TrainRoutes inner join TrainTrips on TrainTrips.RouteID = TrainRoutes.RouteID) inner join TripStops on TripStops.TripID = TrainTrips.TripID where TripStops.PredAway = (Select Max(TripStops.PredAway) as maxPredAway from TripStops inner join TrainTrips on TripStops.TripID = TrainTrips.TripID inner join TrainRoutes on TrainRoutes.RouteID = TrainTrips.RouteID ))  as MaxRouteName, (Select TrainRoutes.RouteName  as minRouteTime from (TrainRoutes inner join TrainTrips on TrainTrips.RouteId = TrainRoutes.RouteID) inner join TripStops on TripStops.TripID = TrainTrips.TripID where TripStops.PredAway = (Select Min(TripStops.PredAway) as maxPredAway from TripStops inner join TrainTrips on TripStops.TripID = TrainTrips.TripID inner join TrainRoutes on TrainRoutes.RouteID = TrainTrips.RouteID)) as MinRouteName) limit 1",
                    ("Max Route Time", "Min Route Time"))
def query1():
    query_and_print("select TripID, RouteID, VehicleID, TripHeadsign from TrainTrips",
        ("Trip ID", "Line", "Vehicle Number", "Destination"))

def query2():
    routeID = mdb.escape_string(raw_input("Enter a train route ID (Red, Blue, Orange): "))
    get_and_print("Select TrainRoutes.RouteName as RouteName, TrainTrips.VehicleID,  TrainRoutes.ModeName, TrainTrips.TripID, TrainTrips.TripHeadsign from TrainRoutes inner join TrainTrips on TrainRoutes.RouteId= TrainTrips.RouteID where TrainRoutes.RouteID = %s",
                  [routeID],
                  ("Line", "Vehicle Number", "Mode", "Trip ID", "Destination"))


def query3(): #see all active stops (being serviced by busses on the road)
    query_and_print("Select distinct BusStops.StopID, BusStops.StopName from (Busses Inner join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) Inner join BusStops on BusStopTimes.StopId = BusStops.StopID",
                    ["StopID", "StopName"])

def query4():
    stopFragment = mdb.escape_string(raw_input("Enter the full or partial title of the desired stop: "))
    stopFragment = "%%%s%%" % stopFragment

    get_and_print("select * from BusStops where StopName like (%s)",
    [stopFragment],
    ("Stop ID", "Stop Name", "Stop Latitude", "Stop Longitude"))

def query5():
    stopID = mdb.escape_string(raw_input("Enter a stop ID: "))
    get_and_print("Select distinct BusStopTimes.VehicleNumber as BusVehicleNumber, Busses.BusTitle as BusName, BusStops.StopID as Bus_Stop_ID, BusStops.StopName as StopName, BusStopTimes.Seconds as Seconds_Away, BusDelays.Slowness, ((BusStopTimes.Seconds*BusDelays.Slowness)+BusStopTimes.Seconds) as SecWdelay from (((Busses Inner join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) Inner join BusStops on BusStopTimes.StopID = BusStops.StopID) left join BusDelays on Busses.VehicleNumber = BusDelays.VehicleNumber) where BusStops.StopID = (%s)",
    [stopID],
    ("Vehicle Number", "Route Number", "Stop ID", "Stop Name", "Scheduled Arrival (sec)", "Slowness Multiplier", "Estimated Arrival (sec)"))

def query6():
    busTitle = mdb.escape_string(raw_input("Enter a bus title: "))
    get_and_print("Select Busses.BusTitle as Route, Busses.VehicleNumber,  BusStops.StopName as StopName, BusDelays.isDelayed as isDelayed, BusDelays.Slowness from ((Busses Inner join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) inner join BusStops on BusStops.StopID = BusStopTimes.StopID) left join BusDelays on BusDelays.VehicleNumber = Busses.VehicleNumber where Busses.BusTitle = (%s)",
    [busTitle],
    ("Route ID", "Vehicle Number", "Stop Name", "Delayed?", "Slowness"))

def query7():
    routeID = mdb.escape_string(raw_input("Enter a train route ID: "))
    get_and_print("Select Alerts.RouteID as Route,Alerts.AlertText as TextMessage from Alerts where RouteID = (%s)",
    [routeID],
    ("Route", "Alert"))

def query8():
        query_and_print("select RTag as Route, VehicleNumber as Vechicle from Busses",
        ("Route", "Vehicle Number"))

def query9():
    query_and_print("select RouteID as Route, TripHeadsign as Headsign, VehicleID as Vehicle from TrainTrips",
        ("Line", "Destination", "Vehicle ID"))

def query10():
    vehiclenum = mdb.escape_string(raw_input("Enter a bus vehicle number: "))
    get_and_print("Select Locations.VehicleNumber as BusVehicleNumber, Busses.BusTitle as BusName,  Locations.BusLAT as BusLAT, Locations.BusLON as BusLON from Locations left Join Busses on Busses.VehicleNumber = Locations.VehicleNumber where Busses.VehicleNumber = (%s)",
    [vehiclenum],
    ("Vehicle Number", "Bus Number", "Bus Latitude", "Bus Longitude"))

def query11():
    vehiclenum = mdb.escape_string(raw_input("Enter a train vehicle number: "))
    get_and_print("Select distinct TrainLocations.VehicleID as TrainVehicleID, TrainTrips.TripHeadsign as TripName, TrainLocations.TrainLAT as TrainLAT, TrainLocations.TrainLON as TrainLON from (TrainLocations inner join TrainTrips on TrainLocations.VehicleID = TrainTrips.VehicleID) where TrainLocations.VehicleID = (%s)",
    [vehiclenum],
    ("Vehicle Number", "Train Destination", "Train Latitude", "Train Longitude"))

def main():
    print "Choose from the following options - "
    print "1 - View all trains on the tracks."
    print "2 - View information for all trains on a specified line (Red, Blue, Orange)."
    print "3 - See all active stops currently being serviced by busses."
    print "4 - See the stop ID of a potential match given a partial stop name."
    print "5 - See busses serving a particular stop, including scheduled and predicted arrival time(s)."
    print "6 - See all stops for a particular route number and associated delays."
    print "7 - See all alerts for a train line (Red, Blue, Orange)."
    print "8 - See all active bus routes and their vehicle numbers."
    print "9 - See all active trains, destinations, and their vehicle numbers."
    print "10 - See the location of a given bus vehicle number (number obtained from 6 or 8)."
    print "11 - See the location of a given train vehicle number (number obtained from 2 or 9)."
    print "12 - Complex query 1 - See the train line with the longest and shortest arrival times."
    print "13 - Complex Query 2 - See trains with an active alert and their locations, omitting a single known, long-standing alert."
    print "14 - Complex Query 3 - View the number of trains arriving in less than on eminute at a specific location with an active alert."
    print "15 - Complex Query 4 - View a list of busses with delays and information regarding how long they are delayed by."
    print "16 - Complex Query 5 - View the bus stop with the highest delay and see how many busses are affected."
    try:
        answer = int(raw_input("Enter the number corresponding to your requested action: "))
    except Exception:
        print "Invalid action."
        main()

    if answer not in ALLOWED_ACTIONS:
        print "Invalid action."
        main()
    else:
        ALLOWED_ACTIONS[int(answer)]()
        main()

def get_and_print(query, filter_variables, headers):
    cursor.execute(query, filter_variables)
    rows = cursor.fetchall()
    if len(rows) < 1:
        print "No rows returned."
    print tabulate(rows, headers, tablefmt="grid")

def query_and_print(query, headers):
    cursor.execute(query)
    rows = cursor.fetchall()
    if len(rows) < 1:
        print "No rows returned."
    print tabulate(rows, headers, tablefmt="grid")


ALLOWED_ACTIONS = {
    0: exit,
    1: query1,
    2: query2,
    3: query3,
    4: query4,
    5: query5,
    6: query6,
    7: query7,
    8: query8,
    9: query9,
    10: query10,
    11: query11,
    12: query12,
    13: query13,
    14: query14,
    15: query15,
    16: query16
}

if __name__ == '__main__':
    main()

