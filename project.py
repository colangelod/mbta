import MySQLdb as mdb
from tabulate import tabulate

cnx = mdb.connect(host="localhost", user="root", passwd="bingobingo", db="databaseproject")
cursor = cnx.cursor()

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

def query6():   #see all busses for a particular route (eg 23) and if they are delayed and by how much
    busTitle = mdb.escape_string(raw_input("Enter a bus title: "))
    get_and_print("Select Busses.BusTitle as Route, Busses.VehicleNumber,  BusStops.StopName as StopName, BusDelays.isDelayed as isDelayed, BusDelays.Slowness from ((Busses Inner join BusStopTimes on Busses.VehicleNumber = BusStopTimes.VehicleNumber ) inner join BusStops on BusStops.StopID = BusStopTimes.StopID) left join BusDelays on BusDelays.VehicleNumber = Busses.VehicleNumber where Busses.BusTitle = (%s)",
    [busTitle],
    ("Route ID", "Vehicle Number", "Stop Name", "Delayed?", "Slowness"))

def query7():   #see train alerts
    routeID = mdb.escape_string(raw_input("Enter a train route ID: "))
    get_and_print("Select Alerts.RouteID as Route,Alerts.AlertText as TextMessage from Alerts where RouteID = (%s)",
    [routeID],
    ("Route", "Alert"))

def query8():
    vehiclenum = mdb.escape_string(raw_input("Enter a bus vehicle number: "))
    get_and_print("Select Locations.VehicleNumber as BusVehicleNumber, Busses.BusTitle as BusName,  Locations.BusLAT as BusLAT, Locations.BusLON as BusLON from Locations left Join Busses on Busses.VehicleNumber = Locations.VehicleNumber where Busses.VehicleNumber = (%s)",
    [vehiclenum],
    ("Vehicle Number", "Bus Number", "Bus Latitude", "Bus Longitude"))

def query9():
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
    print "8 - See the location of a given bus vehicle number (number obtained from 6)."
    print "9 - See the location of a given train vehicle number (number obtained from 2)."
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
    9: query9
}

if __name__ == '__main__':
    main()
