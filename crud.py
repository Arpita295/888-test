import argparse
from datetime import datetime
from getpass import getpass
import logging

from database import SQL


def parser1():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument('action', help="Action to choose", choices=['create', 'read', 'update'], type=str.lower)
    parser.add_argument('table_name', help="Table name", type=str.lower)
    args = parser.parse_args()
    return args


def insert(mysql, table_name):
    args = {}
    if table_name == 'sports':
        sport = input("Enter name of sport: ")
        is_active = input("Enter active status (0/1):")
        args = {
            'name': sport,
            'is_active': is_active if is_active is not None else 1,
        }
    elif table_name == 'events':
        sports = mysql.read_query("SELECT name from sports")
        all_sport = []
        for sport in sports:
            all_sport.append(str(sport[0]))
        name = input("Enter name for event: ")
        is_active = input("Enter active status (0/1):")
        type = input("Enter type of event (preplay/inplay): ")
        while True:
            sport_name_string = "Enter sports name ({}):".format("/".join(all_sport))
            sport1 = input(sport_name_string)
            if sport1 in all_sport:
                break
            print("Wrong sports entered")
        status = input("Enter status of event (pending/started/ended/cancelled): ")
        scheduled_start = input("Enter start time: ")
        actual_start = input("Enter actual start time: ")
        args = {
            'name': name,
            'type': type if type else 'preplay',
            'is_active': is_active if is_active is not None else 0,
            'sport': sport1,
            'status': status if status else 'pending',
            'scheduled_start': scheduled_start if scheduled_start else datetime.utcnow(),
            'actual_start': actual_start if scheduled_start else datetime.utcnow()
        }

    elif table_name == 'selections':
        name = input("Enter name for selection: ")
        is_active = input("Enter active status (0/1):")
        all_event = []
        events = mysql.read_query("SELECT name from events")
        for event in events:
            all_event.append(str(event[0]))
        while True:
            event_name_string = "Enter event name ({}):".format("/".join(all_event))
            event1 = input(event_name_string)
            if event1 in all_event:
                break
            print("Wrong event entered")
        price = input("Enter price for selection: ")
        outcome = input("Enter outcome of selection (unsettled/void/lose/win): ")
        args = {
            'name': name,
            'is_active': is_active if is_active is not None else 0,
            'event': event1,
            'price': price if price else 0.00,
            'outcome': outcome if outcome else 'void'
        }
    logging.info("Parameters for insertion into {} is -->".format(table_name, args))
    mysql.insert(table_name, args=args)


def read(mysql, table_name):
    things = []
    if table_name == 'sports':
        things = ['name', 'slug', 'is_active']
    elif table_name == 'events':
        things = ['name', 'slug', 'is_active', 'type', 'sport', 'status', 'scheduled_start_time', 'actual_start_time']
    elif table_name == 'selections':
        things = ['name', 'event', 'price', 'active', 'outcome']

    to_display = input("Enter things to read comma-seperated(Hit Enter/type all for *) {}: ".format(things))
    print("Enter conditions for  displaying data")
    i = 1
    conditions = ""
    while True:
        cond = input("Enter condition {} (press enter to exit) : ".format(i))
        if not cond:
            break
        if i == 1:
            conditions = cond
        # handling multiple conditions with AND
        conditions = conditions + " AND " + cond
    res = mysql.read_table(table_name, to_display, conditions)
    logging.info("Got data from table {}".format(table_name))
    logging.info(res)


def update(mysql, table_name):
    things = []
    if table_name == 'sports':
        things = ['slug', 'is_active']
    elif table_name == 'events':
        things = ['slug', 'is_active', 'type', 'sport', 'status', 'scheduled_start_time', 'actual_start_time']
    elif table_name == 'selections':
        things = ['event', 'price', 'is_active', 'outcome']
    args = {}
    print ("Enter parameters to be updated from")
    while things:
        for i in range(0, len(things)):
            print("{}.{}".format(i+1, things[i]))
        update = input("Enter number to be updated (or press Enter to exit): ")
        if not update:
            break
        elif things[int(update)-1] in things:
            thing = things[int(update)-1]
            val = input("Enter new value for {}: ".format(thing))
            args[thing] = val
            things.remove(thing)
        else:
            print("Select only from the given list --> {}".format(things))
            continue
    if args:
        n = 1
        cond = input("Enter the condition for updation (like name='<name>'): ")
        while n <= 3:
            if n == 3 or cond:
                break
            if not cond:
                cond = input("Enter the condition for updation (like name='<name>'): ")
        if not cond:
            logging.error("Condition not provided for update, exiting updation")
            return

        mysql.update_table(table_name, cond, args=args)

        # if all the events of particular sport is inactive, set sprot as inactive
        if table_name == 'events' and 'is_active' in args:
            query = ""
            res = mysql.read_query("SELECT sport, is_active from events")
            result = {}
            for res1 in res:
                if res1[0] not in result:
                    result[res1[0]] = [res1[1]]
                else:
                    result[res1[0]].append(res1[1])

            for key, value in result.items():
                if 1 not in value:
                    query = "UPDATE sports set is_active=0 where name='{}'".format(key)
                    mysql.execute_query(query)

        # if all the selections of particular event is inactive, set event as inactive
        elif table_name == 'selections' and 'is_active' in args:
            res = mysql.read_query("SELECT event,is_active from selections")
            result = {}
            for res1 in res:
                if res1[0] not in result:
                    result[res1[0]] = [res1[1]]
                else:
                    result[res1[0]].append(res1[1])

            for k, v in result.items():
                if 1 not in v:
                    query = "UPDATE events set is_active=0 where name='{}'".format(k)
                    mysql.execute_query(query)

    else:
        logging.error("Cannot update table {} as no attribute provided for updation".format(table_name))


def main(args):
    args = parser1()
    username = input("Enter username for SQL: ")
    password = getpass("Enter password for SQL: ")
    hostname = input("Enter hostname for SQL(press Enter for localhost): ")
    database = input("Enter database to connect to (creates db if not there): ")
    if not hostname:
        hostname = 'localhost'

    mysql = SQL(username, password, hostname)
    mysql.create_database(database)
    table_name = args.table_name
    list_tables = ['sports', 'events', 'selections']
    if table_name not in list_tables:
        logging.error("Table name should be from list --> {}. Provided table_name as {}".format(list_tables,table_name))
        return
    if args.action == 'create':
        insert(mysql, table_name)

    elif args.action == 'read':
        read(mysql, table_name)

    elif args.action == 'update':
        update(mysql, table_name)


if __name__ == '__main__':
    logging.basicConfig(filename='crud_app.log', filemode='w',
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    arguments = parser1()
    main(arguments)
