#!/usr/bin/python3
#-*- coding: Utf-8 -*-
import re
import os
import sys
import csv
import sqlite3
from jinja2 import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from wsgiref.simple_server import make_server
from datetime import *

####################################################################################################
### Valknut - Micro Server, GSS & SQLite3 manager
### developped by Meyer Daniel for Python 3, July 2020
### last update : November 2020
### this is version 0.1.0
####################################################################################################

####################################################################################################
### New database creation class
####################################################################################################
class Valknut_sqlite_New():
    ################################################################################################
    ### initialization function for a new database
    ################################################################################################
    def __init__(self, database):
        ### presentation ###
        print("### Valknut - SQLite3 manager ###")
        ### file to create ###
        self.database = database
        ### creation of the new databse ###
        if os.path.exists(self.database) == False and os.path.isfile(self.database) == False:
            connexion = sqlite3.connect(self.database)
            connexion.close()
            ### try to access ###
            if os.path.exists(self.database) == True and os.path.isfile(self.database) == True:
                print("...verification if access path to file is ok...",
                      os.path.exists(self.database))
                print("...verification if path is a valid file...",
                      os.path.isfile(self.database))
                print("...ACCESS DATA OK - NEW DATABASE READY TO OPERATE...")
            else:
                print("!!! ERROR WHILE CREATION OF THE NEW DATABASE !!!")
        else:
            print("!!! THIS DATABASE ALREADY EXIST !!!")
            
####################################################################################################
### Database manager class
####################################################################################################
class Valknut_sqlite():
    ################################################################################################
    ### initialization function
    ################################################################################################
    def __init__(self, database):
        ### framework variables ###
        self.debug_sqlite_instruction = False  ### True for showing sqlite instructions will running
        self.displaying_line = True            ### True for printing at screen
        ### presentation ###
        print("### Valknut - SQLite3 manager ###")
        ### file to analyse ###
        self.database = database
        ### verification if file exist and if access path is ok ###
        if os.path.exists(self.database) == True and os.path.isfile(self.database) == True:
            print("...verification if access path to file is ok...",
                  os.path.exists(self.database))
            print("...verification if path is a valid file...",
                  os.path.isfile(self.database))
            print("...ACCESS DATAS OK !...")
        else: 
            print("!!! ERROR : FILE DOES NOT EXIST !!!")
            self.database = None

    ################################################################################################
    ### entry modification in a table
    ################################################################################################
    def modification_values(self, table, column_to_modify, new_value, reference_column, reference_value):
        """permit to change an entry in table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"UPDATE {table} SET {column_to_modify} = '{new_value}' WHERE {reference_column} = '{reference_value}'")
            self.debug_sqlite(instruction)
            ### try to execute the instruction ###
            try:
                c.execute(instruction)
                mark = True
            except:
                print("Impossible to modifie the value, something does not match !")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### add an entry to specific table
    ################################################################################################
    def add_values(self, table, *elements):
        """permit to add an entry to a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"""INSERT INTO {table} VALUES {str(elements)}""")
            self.debug_sqlite(instruction)
            ### try to execute the instruction ###
            try:
                c.execute(instruction)
                mark = True
            except:
                print("Impossible to add the values, something does not match !")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### add an entry to specific increased table
    ################################################################################################
    def add_increased_values(self, table, *elements):
        """permit to add an entry to a specific increased table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction, searching the maximal value of id column ###
            instruction = f"""SELECT MAX (id) FROM {table}"""
            self.debug_sqlite(instruction)
            nb_id = 0
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                nb_id = out[0] + 1
            except:
                print("no maximal values yet, will start with 1")
                nb_id = 1
                mark = False
            ### values concatenation in 'elements' adding the id number ###
            elements = (nb_id, ) + elements
            ### concatenation of the SQL instruction ###
            instruction_2 = (f"""INSERT INTO {table} VALUES {str(elements)}""")
            self.debug_sqlite(instruction_2)
            ### try to execute the instruction ###
            try:
                c.execute(instruction_2)
                mark = True
            except:
                print("Impossible to add the values, something does not match !")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### creating a new table with specific columns
    ################################################################################################
    def new_table(self, table, *columns):
        """permit to create a new table with specific columns"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"CREATE TABLE {table} {str(columns)}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("New table create")
            except:
                print("Impossible to add a new table to database")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### creating a new increased table with specific columns
    ################################################################################################
    def new_increased_table(self, table, *columns):
        """permit to create a new increased table with specific columns"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            cols = ('id',) + columns
            instruction = (f"CREATE TABLE {table} {str(cols)}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("New table create")
            except:
                print("Impossible to add a new table to database")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### copy a table to a new one
    ################################################################################################
    def copy_table(self, source_table, destination_table):
        """permit to copy a table to a new table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"CREATE TABLE {destination_table} AS SELECT * FROM {source_table}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("Table has been copied")
            except:
                print("Impossible to copy this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### copy specific columns from a table to a new one
    ################################################################################################
    def copy_control_table(self, source_table, destination_table, *columns):
        """permit to copy a table to a new table only with specified columns"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = f"CREATE TABLE {destination_table} AS SELECT "
            for x in range(0, len(columns)):
                instruction += columns[x]
                if x != len(columns) - 1:
                    instruction += ", "
                else:
                    instruction += " "
            instruction += f"FROM {source_table}"
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("Table has been copied")
            except:
                print("Impossible to copy this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### redo a specific table with only specific columns
    ################################################################################################
    def redo_table(self, source_table, *columns):
        """permit to redo a table only with specified column"""
        mark = None
        destination_table = source_table
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = f"CREATE TABLE survival_temporary_table AS SELECT "
            for x in range(0, len(columns)):
                instruction += columns[x]
                if x != len(columns) - 1:
                    instruction += ", "
                else:
                    instruction += " "
            instruction += f"FROM {source_table}"
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print("Table has been copied to valknut_temporary_table.")
                ### then delete the source table
                try :
                    print("Deleting old version of the table")
                    self.delete_table(source_table)
                    print("Restitution of the new version of the table")
                    self.copy_table('valknut_temporary_table', destination_table)
                    print("Deleting temporary exchange table")
                    self.delete_table('valknut_temporary_table')
                    mark = True
                except:
                    print("Something gone wrong while trying to redo the specified table")
                    mark = False
            except:
                print("Impossible to copy this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### add a new column in specific table
    ################################################################################################
    def add_column(self, table, column):
        """permit to add a new column in specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"ALTER TABLE {table} ADD {column}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("New column created")
            except:
                print("Impossible to add a new column to this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### delete a table with its entry from database
    ################################################################################################
    def delete_table(self, table):
        """permit to delete a table from database"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"""DROP TABLE {table}""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print(f"The table {table} has been deleted !")
                mark = True
            except:
                print("Impossible to delete the table, she does not exist")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### purge a table 
    ################################################################################################
    def purge_table(self, table):
        """permit to purge a table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"""DELETE FROM '{table}'""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print(f"The table {table} has been purged !")
                mark = True
            except:
                print("Impossible to purge the table, she does not exist")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### delete an entry
    ################################################################################################
    def delete_entry(self, table, column, value):
        """permit to delete an entry from a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"DELETE FROM {table} WHERE {column} = {value}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print(f"The value {value} from the column {column} has been deleted !")
                mark = True
            except:
                print("Impossible to delete the entry, she does not exist")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry in a specific table
    ################################################################################################
    def search_value(self, table, column, value):
        """permit to search an entry in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            if type(value) == str:
                instruction = (f"SELECT * FROM {table} WHERE {column} = '{value}'")
            elif type(value) == int or type(valeur) == float:
                instruction = (f"SELECT * FROM {table} WHERE {column} = {value}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry in a specific table between 2 values in 2 columns
    ################################################################################################
    def search_between_2cols(self, table, column1, column2, value):
        """permit to search an entry in a specific table"""
        mark = None
                
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            if type(value) == str:
                value = "'" + value + "'"
            instruction = (f"SELECT * FROM {table} WHERE {column1} <= {value} AND {column2} >= {value}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry in a specific table between 2 values in 2 columns with condition
    ################################################################################################
    def search_between_2cols_condition(self, table, column1, column2, value, condition_column, condition_value):
        """permit to search an entry in a specific table"""
        mark = None
                
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            if type(value) == str:
                value = "'" + value + "'"
            if type(condition_value) == str:
                condition_value = "'" + condition_value + "'"
            instruction = (f"SELECT * FROM {table} WHERE ({column1} <= {value} AND {column2} >= {value}) AND ({condition_column} = {condition_value})")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x) 
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark
        
    ################################################################################################
    ### searching an entry who starts with what's specified 
    ################################################################################################
    def search_start_like_value(self, table, column, value):
        """permit to search an entry who starts with the specified value"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"SELECT * FROM {table} WHERE {column} LIKE '{value}%'")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry who ends with what's specified 
    ################################################################################################
    def search_end_like_value(self, table, column, value):
        """permit to search an entry who ends with the specified value"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"SELECT * FROM {table} WHERE {column} LIKE '%{value}'")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry who contain what's specified 
    ################################################################################################
    def search_seems_like_value(self, table, column, value):
        """permit to search an entry who contain the specified value"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"SELECT * FROM {table} WHERE {column} LIKE '%{value}%'")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching entries between an interval in a specific table
    ################################################################################################
    def between_value(self, table, column, interval_1, interval_2):
        """permit to search entries between an interval in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"""SELECT * FROM {table} WHERE {column} BETWEEN '{interval_1}' AND '{interval_2}'""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching entries not between an interval in a specific table
    ################################################################################################
    def not_between_value(self, table, column, interval_1, interval_2):
        """permit to search entries between an interval in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"""SELECT * FROM {table} WHERE {column} NOT BETWEEN '{interval_1}' AND '{interval_2}'""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### sorting the entries in a specific table
    ################################################################################################
    def sort_value(self, table, sens, *column):
        """permit to sort the entries in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction by analyse of *arg column ###
            if sens == 0: ### in ascendence ###
                instruction = (f"SELECT * FROM {table} ORDER BY ")
                for x in range (0, len(column)):
                    instruction += column[x]
                    if x != len(column) - 1:
                        instruction += " ,"
                    else:
                        instruction += " "
                instruction += "ASC"
            elif sens == 1: ### in descendence ###
                instruction = (f"SELECT * FROM {table} ORDER BY ")
                for x in range (0, len(column)):
                    instruction += column[x]
                    if x != len(column) - 1:
                        instruction += " ,"
                    else:
                        instruction += " "
                instruction += "DESC"
            ### incase of too much trouble ###
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### return each table's name and column's name
    ################################################################################################
    def return_structure(self):
        """return database's structure via dictionnary"""
        mark = {}
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            ### c : analyse the tables, d : analyse column's name ###
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### another cursor to analyse the table's entry ###
            connexion2 = sqlite3.connect(self.database)
            e = connexion2.cursor()
            ### concatenation of the first instruction ###
            instruction_1 = """SELECT name FROM sqlite_master WHERE type = 'table' """
            self.debug_sqlite(instruction_1)
            ### analyse table's name of the database with c ###
            c.execute(instruction_1)
            for x in iter(c.fetchall()):
                ### concatenation of the second instruction ###
                instruction_2 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_2)
                ### analyse column's name of each tables with d ###
                d.execute(instruction_2)
                mark[x[0]] = d.fetchone().keys()
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return None

    ################################################################################################
    ### display the integrality of the database
    ################################################################################################
    def show_all(self):
        """display the integrality of the database"""
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            ### c : analyse the tables, d : analyse column's name ###
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### another cursor to analyse the table's entry ###
            connexion2 = sqlite3.connect(self.database)
            e = connexion2.cursor()
            ### display the contains ###
            print("\n...OK... The database contains :")
            print(self.database)
            print("  |")
            ### concatenation of the first instruction ###
            instruction_1 = """SELECT name FROM sqlite_master WHERE type = 'table' """
            self.debug_sqlite(instruction_1)
            ### analyse table's name of the database with c ###
            c.execute(instruction_1)
            for x in iter(c.fetchall()):
                ### concatenation of the second instruction ###
                instruction_2 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_2)
                ### analyse column's name of each tables with d ###
                d.execute(instruction_2)
                ### display the tree ###
                print("  + -",x[0])
                try:
                    print("  |       \ _ _ _ _ _", d.fetchone().keys())
                except:
                    print("  | ")
                ### concatenation of the third instruction ###
                instruction_3 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_3)
                ### analyse of the table contains with e ###
                for y in e.execute(instruction_3):
                    ligne = ""
                    ### concatenation of datas in one line ###
                    for z in range(0, len(y)):
                        ligne = ligne + str(y[z]) + " - "
                    ### display the data ###
                    print("  |\t\t\t", ligne)
            ### closing ###
            connexion.close()
            ### and final line of the tree display ###
            print("  | \n  |_ END OF DATAS !\n")
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return None
            
    ################################################################################################
    ### display the structure of the database
    ################################################################################################
    def show_structure(self):
        """display database's structure"""
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            ### c : analyse the tables, d : analyse column's name
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### display the contains ###
            print("\n...OK... This is database's tree :")
            print(self.database)
            print("  |")
            ### analyse the name of the table with c ###
            c.execute("""SELECT name FROM sqlite_master WHERE type = 'table' """)
            for x in iter(c.fetchall()):
                ### analyse column's name with d ###
                d.execute(f"SELECT * FROM {x[0]}")
                ### display the tree ###
                print("  + -",x[0])
                try:
                    print("  |       \ _ _ _ _ _", d.fetchone().keys())
                except:
                    print("  | ")
            ### closing ###                 
            connexion.close()
            ### and final line of the tree display ###
            print("  | \n  |_ END OF DATAS !\n")
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return None

    ################################################################################################
    ### do the sum of a column
    ################################################################################################
    def column_sum(self, table, column):
        """return the sum of a specific column and return it as integer or float"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT SUM({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to do the sum of this column.")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark
            
    ################################################################################################
    ### do the total of a column
    ################################################################################################
    def column_total(self, table, column):
        """return the total of a specific column and return an float"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT TOTAL({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to do the total of this column")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### find the minimal value of a table
    ################################################################################################
    def data_minimal(self, table, column):
        """find and return the minimal value in a specific column of a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT MIN({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to find the minimal value, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### find the maximal value of a table
    ################################################################################################
    def data_maximal(self, table, column):
        """find and return the maximal value in a specific column of a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT MAX({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to find the maximal value, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### do the average of a group of values
    ################################################################################################
    def data_average(self, table, column):
        """do the average of a group of non-null values"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT AVG({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to do the average, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### do an innerjoin between two tables, will return only those who are present in both tables
    ################################################################################################
    def data_crosscheck(self, table_1, table_2, column_t1, column_t2):
        """do an innerjoin between two tables, return only those who are present in both tables"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT * FROM {table_1} INNER JOIN {table_2} WHERE {table_1}.{column_t1} = {table_2}.{column_t2}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                c.execute(instruction)
                for x in iter(c.fetchall()):
                    self.displaying_return(x)
                    mark += [x]
            except:
                print("Impossible to do the crosscheck, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### do an union between two tables, will return the integrity of both tables without doubles
    ################################################################################################
    def data_union(self, table_1, table_2):
        """do an union between two tables, will return the intergrity of both tables without doubles"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT * FROM {table_1} UNION SELECT * FROM {table_2}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                c.execute(instruction)
                for x in iter(c.fetchall()):
                    self.displaying_return(x)
                    mark += [x]
            except:
                print("Impossible to do the crosscheck, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################       
    ### output database's structure to a txt file
    ################################################################################################
    def edit_structure_txt(self, nom_fichier_sortie = "analyse_valknut.txt"):
        """output database's structure to a txt file"""
        ### if database is a valid file ###
        if self.database != None:
            ### create and open a new text file ###
            fichier_texte = open(nom_fichier_sortie, "w")
            ### connection to database ###
            ### c : analyse the tables, d : analyse the column's name ###
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### concatenation of the lines for file header ###
            ligne_entete_01 = "\n...OK... This is the tree :"
            ligne_entete_02 = self.database
            ligne_entete_03 = "  |"
            ### write the header to file ###
            fichier_texte.write(ligne_entete_01 + "\n")
            fichier_texte.write(ligne_entete_02 + "\n")
            fichier_texte.write(ligne_entete_03 + "\n")
            ### concatenation of the first instruction ###
            instruction_1 = """SELECT name FROM sqlite_master WHERE type = 'table' """
            self.debug_sqlite(instruction_1)
            ### analyse the tables in the database with c ###
            c.execute(instruction_1)
            for x in iter(c.fetchall()):
                ### concatenation of the second instruction ###
                instruction_2 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_2)
                ### analyse the column's name with d ###
                d.execute(instruction_2)
                ### concatenation for output ###
                ligne_A = "  + -" + str(x[0])
                try:
                    ligne_B = "  |       \ _ _ _ _ _" + str(d.fetchone().keys())
                except:
                    ligne_B = "  | "
                ### write the lines into the file ###
                fichier_texte.write(ligne_A + "\n")
                fichier_texte.write(ligne_B + "\n")
            ### definition of the final line ###
            ligne_fin = "  | \n  |_ END OF DATAS !\n"
            fichier_texte.write(ligne_fin + "\n")
            ### closing database and text file ###
            connexion.close()
            fichier_texte.close()
            ### if job is done return True ###
            return True
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            ### if job is not done return False ###
            return False

    ################################################################################################
    ### output a specific table to CSV
    ################################################################################################
    def edit_contains_csv(self, table, nom_fichier_sortie = "analyse_valknut.csv"):
        """output the contain of a specific table to a csv spreadsheet"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### create and open a new csv file ###
            fichier_csv = open(nom_fichier_sortie, "w", newline = "")
            ecriture = csv.writer(fichier_csv)
            ### first connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### second connection to database to put out column's name ###
            connexion2 = sqlite3.connect(self.database)
            connexion2.row_factory = sqlite3.Row
            d = connexion2.cursor()
            try:
                ### concatenation of the first instruction ###
                instruction_1 = (f"SELECT * FROM {table}")
                self.debug_sqlite(instruction_1)
                ### analuse column's name ###
                d.execute(instruction_1)
                colonnes = d.fetchone()
                ### write the column's name into the file ###
                ecriture.writerow(colonnes.keys())
                ### concatenation of the second instruction ###
                instruction_2 = (f"SELECT * FROM {table}")
                self.debug_sqlite(instruction_2)
                ### analyse the contain of the table and output to file ###
                for x in c.execute(instruction_2):
                    ecriture.writerow(x)
                ### closing database and csv file ###
                fichier_csv.close()
                connexion.close()
                connexion2.close()
                mark = True
            except:
                ### in case of impossibility to check the table ###
                print("This table does not exist")
                mark = False
            ### return if job done or not ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### function using system to clear screen
    ################################################################################################
    def clear_screen(self):
        local_comp = sys.platform
        if local_comp == "linux":
            os.system("clear")
        elif local_comp == "win32":
            os.system("cls")
        else:
            print("\n" * 100)

    ################################################################################################
    ### function using system to make a break until user use Enter
    ################################################################################################
    def waiter(self):
        local_comp = sys.platform
        if local_comp == "linux":
            print("Press Enter to continue...")
            os.system("read")
        elif local_comp == "win32":
            os.system("pause")
        else:
            print("Press Enter to continue...")
            input("")

    ################################################################################################
    ### function returning the date in french format
    ################################################################################################
    def return_date_fr(self):
        instant = datetime.now()
        instant = instant.strftime("%d/%m/%Y")
        return instant

    ################################################################################################
    ### function returning the time in french format
    ################################################################################################
    def return_time_fr(self):
        instant = datetime.now()
        instant = instant.strftime("%H:%M:%S")
        return instant

    ################################################################################################
    ### function returning the date in english / american format
    ################################################################################################
    def return_date_en(self):
        instant = datetime.now()
        instant = instant.strftime("%m-%d-%Y")
        return instant

    ################################################################################################
    ### function returning the time in english / american format
    ################################################################################################
    def return_time_en(self):
        instant = datetime.now()
        instant = instant.strftime("%I:%M:%S -%p")
        return instant
            
    ################################################################################################
    ### debugging function : will display the SQL instructions while running
    ################################################################################################
    def debug_sqlite(self, instruction):
        if self.debug_sqlite_instruction == True:
            print(instruction)

    ################################################################################################
    ### general displaying function : will print at screen if displaying_line = True
    ################################################################################################
    def displaying_return(self, display_this):
        if self.displaying_line == True:
            print(display_this)
