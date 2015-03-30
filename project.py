__author__ = 'Neil'

import MySQLdb as mdb
from tabulate import tabulate

con = mdb.connect(host="localhost", user="root", passwd="", db="databaseproject")
cursor = con.cursor()

def query1():
    vehicleNum = mdb.escape_string(raw_input("Enter a vehicle number: "))
    route_tag = mdb.escape_string(raw_input("Enter a route tag: "))
    get_and_print("select vehicleNumber, rtag, bustitle FROM busses WHERE vehiclenumber = (%s) AND rtag = (%s)",
                  [vehicleNum, route_tag],
                  ("vehicle number", "route tag", "bus title"))


def query2():
    print "world"

def query3():
    print "fuckyou"

def main():
    print "Do some shit? Do some shit. 0 for exit"
    answer = int(raw_input("Enter the number corresponding to your requested action: "))

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

ALLOWED_ACTIONS = {
    0: exit,
    1: query1,
    2: query2,
    3: query3
}

if __name__ == '__main__':
    main()