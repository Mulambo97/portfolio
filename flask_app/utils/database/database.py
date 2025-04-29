from pprint import pprint
import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime
class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'


    def getDbInstance(self):
        return mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = self.getDbInstance()

        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info


    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        # Clear database on app start
        self.query("DROP TABLE IF EXISTS skills");
        self.query("DROP TABLE IF EXISTS experiences");
        self.query("DROP TABLE IF EXISTS positions");
        self.query("DROP TABLE IF EXISTS institutions");
        self.query("DROP TABLE IF EXISTS feedback");

        database_files = ["feedback","institutions", "positions", "experiences", "skills"]

        # Create new tables in database
        for file in database_files:

            filename = data_path+"create_tables/"+file+".sql"
            file_object = open(filename, "r")
            sql_file = file_object.read()
            sql_file.strip()
            self.query(sql_file)
            file_object.close()

        csv_files = database_files[1:]

        # Populate tables in database
        for file in csv_files:
            filename = data_path+"initial_data/"+file+".csv"
            file_object = open(filename, "r")
            reader = csv.reader(file_object)
            columns = None
            parameters = []
            for row in reader:
                if columns is None:
                    columns = row
                    continue
                parameters.append(row)

            self.insertRows(file, columns, parameters)


    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        cnx = self.getDbInstance()
        colSize = len(columns)
        colStr = ','.join(columns)
        paramStr = ','.join(['%s']*colSize)
        sql = f'INSERT INTO {table} ({colStr}) VALUES ({paramStr})'
        print(f"Generated SQL: {sql}")  # Debugging output

        cur = cnx.cursor()
        try:
            for row in parameters:
                if not row:  # Skip empty rows
                    print("Skipping empty row")
                    continue
                print(f"Inserting row: {row}")  # Debugging output
                if len(row) != colSize:
                    raise ValueError(f"Row length mismatch: Expected {colSize} values, got {len(row)}")
                cur.execute(sql, tuple(row))
            cnx.commit()
        except mysql.connector.Error as e:
            print(f"Error executing query: {sql}\nParameters: {parameters}\nError: {e}")
            cnx.rollback()
            raise
        finally:
            cur.close()
            cnx.close()


    def getResumeData(self):
        result_dict = dict()
        institutions = self.query("SELECT * FROM institutions")
        positions = self.query("SELECT * FROM positions")
        experiences = self.query("SELECT * FROM experiences")
        skills = self.query("SELECT * FROM skills")

        #builds the beginning of the master dictionary by entering in the institutions
        for i in institutions:
            inst_id = i['inst_id']
            type_ = i['type']
            name = i['name']
            dept = i['department']
            address = i['address']
            city = i['city']
            state = i['state']
            zip_ = i['zip']
            temp_dict = {'address': address, 'city': city, 'state': state, \
                'type': type_, 'zip': zip_, 'department': dept, 'name': name, 'positions': dict() }
            result_dict[inst_id] = temp_dict



        # adds the positions to the dictionary
        for p in positions:

            pos_id = p['position_id']
            inst_id = p['inst_id']
            title = p['title']
            respons = p['responsibilities']
            start_date = p['start_date']
            end_date = p['end_date']

            value_dict = {'end_date': end_date, 'responsibilities': respons, \
                'start_date': start_date, 'title': title, 'experiences': dict()}

            result_dict[inst_id]['positions'][pos_id] = value_dict

        # adds the experiences to the dictionary
        for e in experiences:
            exp_id = e['experience_id']
            pos_id = e['position_id']
            name = e['name']
            description = e['description']
            hyperlink = e['hyperlink']
            start_date = e['start_date']
            end_date = e['end_date']

            value_dict2 = {'name': name, 'description': description, \
                'hyperlink': hyperlink, 'start_date': start_date, 'end_date': end_date, 'skills': dict()}

            for ins, info in result_dict.items():
                for pos in info['positions'].keys():
                    if pos_id == pos:
                        result_dict[ins]['positions'][pos_id]['experiences'][exp_id] = value_dict2

        # adds the skills to the dictionary
        for s in skills:
            skill_id = s['skill_id']
            exp_id = s['experience_id']
            name = s['name']
            level = s['skill_level']

            value_dict4 = {'name': name, 'skill_level': level}

            for ins, info in result_dict.items():
                for pos, info2 in info['positions'].items():

                    for exp in info2['experiences'].keys():
                        # print(exp)
                        if exp == exp_id:
                            result_dict[ins]['positions'][pos]['experiences'][exp]['skills'][skill_id] = value_dict4

        return result_dict

    def insert_feedback(self, name, email, comment):
            query = """
            INSERT INTO feedback (name, email, comment)
            VALUES (%s, %s, %s)
            """
            self.query(query, (name, email, comment))

    def get_all_feedback(self):
        query = "SELECT * FROM feedback"
        return self.query(query)
