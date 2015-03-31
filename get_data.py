import time
from mbta import MBTA as MBTA
from nextbus import NextBus as NextBus
from mbta_mysql import MBTAMySQL as MBTA_Mysql
from multiprocessing.pool import ThreadPool as Pool
from nextbus_mysql import NextBusMySQL as NextBus_Mysql

pool_size = 15
pool = Pool(pool_size)

def main():
    pool.apply_async(mbta)
    pool.apply_async(nextbus)

    pool.close()
    pool.join()

    MBTA_Mysql().main()
    NextBus_Mysql().main()

def mbta():
    try:
        MBTA().main()
    except Exception as e:
        print(e)

def nextbus():
    try:
        NextBus().main()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)