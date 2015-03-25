__author__ = 'Neil'


from pprint import pprint
import xml.etree.ElementTree as ET
import json
import urllib2
import time
import sys

from multiprocessing.pool import ThreadPool as Pool

pool_size = 35
pool = Pool(pool_size)

t0 = time.time()


CMD_ROUTELIST = "routeList"
CMD_ROUTECONFIG = "routeConfig"
CMD_PREDICTIONS = "predictions"
CMD_LOCATIONS = "vehicleLocations"

URL = "http://webservices.nextbus.com/service/publicXMLFeed?command={0}&a=mbta"

#route_dict = {}

routes = {}

def main():
    file = urllib2.urlopen(URL.format(CMD_ROUTELIST))


    tree = ET.parse(file)
    root = tree.getroot()

    i = 0
    for route in root.iter('route'):
        route_dict = {}
        tag = route.attrib['tag']
        title = route.attrib['title']
        #route_dict.update(title=title, tag=tag)

        res = urllib2.urlopen(URL.format(CMD_ROUTECONFIG)+"&r={0}".format(tag))
        t = ET.parse(res)
        r = t.getroot()
        routes.update({tag: {"tag": tag, "title": title, "routes": []}})
        for stop in r.iterfind('route/stop'):
            pool.apply_async(worker, (stop, tag, title))
            #worker(stop,tag,title)
            i = i + 1

            print i

    t1 = time.time()

    print t1 - t0

    print i


    pool.close()
    pool.join()
    time.sleep(5)
    with open("nextbus.json", "w") as file:
        #pprint(routes, stream=file)
        json.dump(routes, file, indent=4, sort_keys=True)

def worker(stop, tag, title):
    try:
        route_dict = {}
        route_dict.update(title=title, tag=tag)
        stop_dict = {}
        vehicles = []
        if "title" in stop.attrib and "stopId" in stop.attrib:
            stop_dict.update(stop.attrib,
                        predictions=[]
            )
            res = urllib2.urlopen(URL.format(CMD_PREDICTIONS)+"&r={0}&stopId={1}".format(tag, stop.attrib['stopId']))
            _t = ET.parse(res)
            _r = _t.getroot()
            for directions in _r.iterfind('predictions/direction/prediction'):
                stop_dict['predictions'].append(directions.attrib)
                res = urllib2.urlopen(URL.format(CMD_LOCATIONS)+"&r={0}&t=0".format(tag))
                __t = ET.parse(res)
                __r = __t.getroot()
                for vehicle in __r.iter('vehicle'):
                    vehicles.append(vehicle.attrib)
#print stop_dict
            route_dict.update({"stops": stop_dict, "vehicles": vehicles})
            routes[tag]['routes'].append(route_dict)
    except Exception as e:
        print('Error.?%(e)s' % vars())

if __name__ == "__main__":
    main()