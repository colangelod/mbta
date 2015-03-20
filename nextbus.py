__author__ = 'Neil'


from pprint import pprint
import xml.etree.ElementTree as ET
import json
import urllib2
import time

from multiprocessing.pool import ThreadPool as Pool

pool_size = 35
pool = Pool(pool_size)

t0 = time.time()


CMD_ROUTELIST = "routeList"
CMD_ROUTECONFIG = "routeConfig"
CMD_PREDICTIONS = "predictions"

URL = "http://webservices.nextbus.com/service/publicXMLFeed?command={0}&a=mbta"

route_dict = {}


def main():
    file = urllib2.urlopen(URL.format(CMD_ROUTELIST))

    routes = {}

    tree = ET.parse(file)
    root = tree.getroot()

    i = 0
    for route in root.iter('route'):
        tag = route.attrib['tag']
        title = route.attrib['title']
        route_dict.update(title=title)
        res = urllib2.urlopen(URL.format(CMD_ROUTECONFIG)+"&r={0}".format(tag))
        t = ET.parse(res)
        r = t.getroot()
        for stop in r.iterfind('route/stop'):
            pool.apply_async(worker, (stop, tag,))
            i = i + 1
            print i
        routes.update({tag: route_dict})

    t1 = time.time()

    print t1 - t0

    print i

    pool.close()
    pool.join()
    time.sleep(5)
    with open("nextbus.json", "w") as file:
        #pprint(routes, stream=file)
        json.dump(routes, file, indent=4, sort_keys=True)

def worker(stop,tag):
    try:
        stop_dict = {}
        if "title" in stop.attrib and "stopId" in stop.attrib:
            stop_dict.update(stop.attrib,
                        predictions=[]
            )
            res = urllib2.urlopen(URL.format(CMD_PREDICTIONS)+"&r={0}&stopId={1}".format(tag, stop.attrib['stopId']))
            _t = ET.parse(res)
            _r = _t.getroot()
            for directions in _r.iterfind('predictions/direction/prediction'):
                stop_dict['predictions'].append(directions.attrib)
                #print stop_dict
            route_dict.update({tag: stop_dict})
    except Exception as e:
        print('Error.?%(e)s' % vars())

if __name__ == "__main__":
    main()