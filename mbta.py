__author__ = 'Neil'

from pprint import pprint
import json
import urllib2
import time

from multiprocessing.pool import ThreadPool as Pool

pool_size = 35
pool = Pool(pool_size)


URL="http://realtime.mbta.com/developer/api/v2/{0}?api_key=wX9NwuHnZU2ToO7GmGR9uw&format=json"

ROUTE_TYPES = ['0', '1']

CMD_ROUTES = "routes"
CMD_SCHEDULE_BY_ROOT = "schedulebyroute"
CMD_PREDICTIONS = "predictionsbytrip"
CMD_ALERTS = "alertsbyroute"

res = urllib2.urlopen(URL.format(CMD_ROUTES))

js_res = json.load(res)

routes = []
trip_res = []

def main():
    for mode in js_res['mode']:
        if mode['route_type'] in ROUTE_TYPES:
            for route in mode['route']:
                print route['route_id']
                res = urllib2.urlopen(URL.format(CMD_SCHEDULE_BY_ROOT)+"&route={0}&datetime={1}".format(route['route_id'], int(time.time())))
                schd = json.load(res)
                for direction in schd['direction']:
                        for trip in direction['trip']:
                            pool.apply_async(get_directions, (trip,))
                alert_res = False
                try:
                    res = urllib2.urlopen(URL.format(CMD_ALERTS)+"&route={0}".format(route['route_id']))
                    alert_res = json.load(res)
                except urllib2.HTTPError:
                    pass
                except AttributeError:
                    pass

                routes.append({
                    route['route_id']: route['route_name'],
                    "directions": schd['direction'],
                    "trips": trip_res,
                    "alerts": alert_res
                })


    pool.close()
    pool.join()
    time.sleep(5)
    with open("mbta.json", "w") as out:
        pprint(routes, stream=out)


def get_directions(trip):
    try:
        res = urllib2.urlopen(URL.format(CMD_PREDICTIONS)+"&trip={0}".format(trip['trip_id']))
        trip_res.append(json.load(res))
    except urllib2.HTTPError:
        pass
    except AttributeError:
        pass
    except Exception:
        pass

if __name__ == "__main__":
    main()