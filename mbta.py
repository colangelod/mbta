from pprint import pprint
import json
import urllib2
import time

from multiprocessing.pool import ThreadPool as Pool


pool_size = 15
pool = Pool(pool_size)


URL="http://realtime.mbta.com/developer/api/v2/{0}?api_key=3yCIHX5F2ketSKY0T6s0LA&format=json"

ROUTE_TYPES = ['0', '1']

CMD_ROUTES = "routes"
CMD_SCHEDULE_BY_ROOT = "schedulebyroute"
CMD_PREDICTIONS = "predictionsbytrip"
CMD_ALERTS = "alertsbyroute"

res = urllib2.urlopen(URL.format(CMD_ROUTES))

js_res = json.load(res)

routes = []
trip_res = []

class MBTA:

    def __init__(self):
        self.counter = 1

    def main(self):
        for mode in js_res['mode']:
            if mode['route_type'] in ROUTE_TYPES:
                for route in mode['route']:
                    route_id = route['route_id']
                    print route_id
                    res = urllib2.urlopen(URL.format(CMD_SCHEDULE_BY_ROOT)+"&route={0}&datetime={1}".format(route['route_id'], int(time.time())))
                    schd = json.load(res)
                    alert_res = False
                    try:
                        res = urllib2.urlopen(URL.format(CMD_ALERTS)+"&route={0}".format(route['route_id']))
                        alert_res = json.load(res)
                    except urllib2.HTTPError:
                        pass
                    except AttributeError:
                        pass
                    temp = {}
                    temp.update({
                        "route_id": route['route_id'],
                        "route_title": route['route_name'],
                        "mode_name": mode['mode_name'],
                        "directions": schd['direction'],
                        "alerts": alert_res,
                        "predictions": []
                    })
                    for direction in schd['direction']:
                        for trip in direction['trip']:
                            #pool.apply_async(get_directions, (trip, route_id,))
                            try:
                                res = urllib2.urlopen(URL.format(CMD_PREDICTIONS)+"&trip={0}".format(trip['trip_id']))
                                temp['predictions'].append(json.load(res))
                            except urllib2.HTTPError:
                                pass
                            except AttributeError:
                                pass
                            except Exception as e:
                                print(e)

                    routes.append(temp)


        pool.close()
        pool.join()
        with open("mbta.json", "w") as out:
            #pprint(routes, stream=out)
            json.dump(routes, out, indent=4, sort_keys=True)


    def get_directions(self, trip, route_id):
        pass

if __name__ == "__main__":
    t0 = time.time()
    inst = MBTA()
    #print time.time() - t0