import logging
from mysql.connector import connect, Error


class SQL:
    def __init__(self, username, password, hostname):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.database = None
        self.connection = None

    def create_connection(self):
        """
        Connects to the given database
        :return: Returns the connection object
        """
        try:
            connection = connect(host=self.hostname, user=self.username, password=self.password, database=self.database)
            return connection
        except ConnectionError as e:
            logging.error("Unable to connect to database {}".format(self.database))
            raise e

    def create_database(self, name):
        """
        Creates database if not exist and connect to it
        :param name: name of database
        :return: None
        """
        query = "CREATE DATABASE IF NOT EXISTS {}".format(name)
        try:
            connection = connect(host=self.hostname, user=self.username, password=self.password)
            create_db_query = "CREATE DATABASE IF NOT EXISTS {}".format(name)
            cursor = connection.cursor()
            cursor.execute(create_db_query)
            self.database = name
            self.connection = self.create_connection()

        except Error as e:
            logging.error("Error occurred while creating/connecting to database {}".format(name))
            raise e

    def read_query(self, query):
        """
        Fetches the output of query (queries like SELECT has output)
        :param query: Query whose output needs to be seen
        :return: result of the query execution
        """
        cursor = self.connection.cursor()
        try:
            logging.info("Executing query --> {}".format(query))
            cursor.execute(query)
            result = cursor.fetchall()
            logging.info("Query execution successful")
            return result
        except Error as err:
            logging.error("Error {} occurred while reading from table".format(err))
            raise err

    def execute_query(self, query, val=None):
        """

        :param query: Query to be executed
        :param val: tuple needed only while inserting into table
        :return: None
        """
        cursor = self.connection.cursor()
        try:
            logging.info("Executing query --> {}".format(query))
            if val:
                logging.info("values --> {}".format(val))
            cursor.execute(query, val)
            self.connection.commit()
            logging.info("Query execution successful")
            logging.info("{} records affected".format(cursor.rowcount))
        except Error as err:
            logging.error("Error {} occurred while executing query {}".format(err, query))
            raise err

    def create_table(self, table_name):
        """
        Creates a table if not exists with table_name
        :param table_name: table to be created
        :return: None
        """
        query = ""
        if table_name == 'sports':
            query = """
            CREATE TABLE if not exists sports(
              name VARCHAR(40) NOT NULL PRIMARY KEY,
              slug VARCHAR(200),
              is_active BOOLEAN DEFAULT FALSE
            );"""
        elif table_name == 'events':
            query = """
            CREATE TABLE if not exists events(
              name VARCHAR(40) NOT NULL PRIMARY KEY,
              slug VARCHAR(200) NOT NULL,
              is_active BOOLEAN default FALSE,
              type ENUM('preplay','inplay') DEFAULT 'preplay',
              sport VARCHAR(40),
              status ENUM('pending','started','ended','cancelled') DEFAULT 'pending',
              scheduled_start_time DATETIME,
              actual_start_time DATETIME
            );"""
        elif table_name == 'selections':
            query = """
             CREATE TABLE if not exists selections(
               name VARCHAR(40) NOT NULL,
               event VARCHAR(40) not NULL,
               price FLOAT(20,2) DEFAULT 0.00,
               is_active BOOLEAN DEFAULT FALSE,
               outcome ENUM('unsettled','void','lose','win') DEFAULT 'void'
             );"""
        self.execute_query(query)

    def insert(self, table_name, **args):
        """
        Insert values into table
        :param table_name: name of the table
        :param args: values to be inserted(dict)
        :return: None
        """
        query = ""
        val = ()
        args = args['args']
        self.create_table(table_name)
        if table_name == 'sports':
            query = "INSERT INTO sports (name,slug) values (%s,%s)"
            val = (args['name'], args['name'])
        elif table_name == 'events':
            query = "INSERT INTO events (name,slug,type,sport,status,scheduled_start_time,actual_start_time) " \
                    "values (%s,%s,%s,%s,%s,%s,%s)"
            val = (args['name'], args['name'], args['type'], args['sport'], args['status'],
                   args['scheduled_start'], args['actual_start'])
        elif table_name == 'selections':
            query = "INSERT INTO selections (name,event,price,outcome) values (%s,%s,%s,%s)"
            val = (args['name'], args['event'], args['price'], args['outcome'])
        self.execute_query(query, val)

    def update_table(self, table_name, cond, **args):
        """
        Update table
        :param table_name: name of the table
        :param cond: condition on which updation will be performed
        :param args: dict format key,val pair to be updated
        :return: None
        """
        if not cond:
            logging.info("No conditions given for updation")
            return
        args = args['args']
        if args:
            query = "update {} set ".format(table_name)
            i = True
            for k, v in args.items():
                if i:
                    query += '{}="{}"'.format(k, v)
                    i = False
                else:
                    query += ',{}="{}" '.format(k, v)
            query += "where {}".format(str(cond))
            self.execute_query(query)

    def read_table(self, table_name, columns_to_display=None, condition=None):
        """
        Read contents of a table
        :param table_name: name of the table
        :param columns_to_display: columns to display in the output
        :param condition: Condition on which read is performed
        :return: Contents from table
        """
        if not columns_to_display:
            query = "SELECT * from {}".format(table_name)
        elif (not columns_to_display or columns_to_display == "all") and not condition:
            query = "SELECT * from {}".format(table_name)
        elif columns_to_display and not condition:
            query = "SELECT {} from {}".format(columns_to_display, table_name)
        elif not columns_to_display or columns_to_display == "all":
            query = "SELECT * from {} where {}".format(table_name, condition)
        else:
            query = "SELECT {} from {} where {}".format(columns_to_display, table_name, condition)
        return self.read_query(query)
