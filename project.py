import MySQLdb as mdb
from tabulate import tabulate

cnx = mdb.connect(host="localhost", user="root", passwd="bingobingo", db="databaseproject")
cursor = cnx.cursor()

def query1():   #info for a train routeid
    routeID = mdb.escape_string(raw_input("Enter a train route ID (Red, Blue, Orange): "))
    get_and_print("Select TrainRoutes.RouteID, TrainRoutes.RouteName as RouteName , TrainRoutes.ModeName, TrainTrips.TripID, TrainTrips.TripHeadsign from TrainRoutes inner join TrainTrips on TrainRoutes.RouteId= TrainTrips.RouteID where TrainRoutes.RouteID = %s",
                  [routeID],
                  ("RouteID", "RouteName", "ModeName", "TripID", "TripHeadsign"))


def query2(): #see all active stops (being serviced by busses on the road)
    query_and_print("Select distinct BusStops.StopID, BusStops.StopName from (Busses Inner join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) Inner join BusStops on BusStopTimes.StopId = BusStops.StopID",
                    ["StopID", "StopName"])

def query3():   #see busses servicing a stop
    stopID = mdb.escape_string(raw_input("Enter a stop ID: "))
    get_and_print("Select distinct BusStopTimes.VehicleNumber as BusVehicleNumber, Busses.BusTitle as BusName, BusStops.StopID as Bus_Stop_ID, BusStops.StopName as StopName, BusStopTimes.Seconds as Seconds_Away, BusDelays.Slowness, ((BusStopTimes.Seconds*BusDelays.Slowness)+BusStopTimes.Seconds) as SecWdelay from (((Busses Inner join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) Inner join BusStops on BusStopTimes.StopID = BusStops.StopID) left join BusDelays on Busses.VehicleNumber = BusDelays.VehicleNumber) where BusStops.StopID = (%s)",
    [stopID],
    ("vehiclenum", "Bus Number", "Stop ID", "Stop Name", "Scheduled Arrival", "Slowness Multiplier", "Estimated Arrival (sec)"))

def query4():   #see trip info relating to train routeid
    routeID = mdb.escape_string(raw_input("Enter a train route ID (Red, Blue, Orange): "))
    get_and_print("Select TrainRoutes.RouteID, TrainRoutes.RouteName as RouteName, TrainRoutes.ModeName, TrainTrips.TripID, TrainTrips.TripHeadsign from TrainRoutes inner join Traintrips on TrainRoutes.RouteId= TrainTrips.RouteID where TrainRoutes.RouteID = (%s)",
    [routeID],
    ("Route ID", "Route Name", "Mode Name", "Trip ID", "Headsign"))

def query5():   #see all busses for a particular route (eg 23) and if they are delayed and by how much
    busTitle = mdb.escape_string(raw_input("Enter a bus title: "))
    get_and_print("Select Busses.BusTitle as Route, BusStops.StopName as StopName, BusDelays.isDelayed as isDelayed, BusDelays.Slowness from ((Busses Inner join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) inner join BusStops on BusStops.StopID = BusStopTimes.StopID) left join BusDelays on BusDelays.VehicleNumber = Busses.VehicleNumber where Busses.BusTitle = (%s)",
    [busTitle],
    ("Route ID", "Stop Name", "Delayed?", "Slowness"))

def query6():   #see train alerts
    routeID = mdb.escape_string(raw_input("Enter a train route ID: "))
    get_and_print("Select Alerts.RouteID as Route,Alerts.AlertText as TextMessage from Alerts where RouteID = (%s)",
    [routeID],
    ("Route", "Alert"))

def main():
    print "Do some stuff? Do some stuff. 0 for exit"
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
    6: query6
}

if __name__ == '__main__':
    main()