``` <python>
__author__ = 'vriz'
# !/usr/bin/env python
# -*-coding: utf-8-*-
"""This module takes the name of an SQL table and creates an exact copy of it"""

import pyodbc


class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class CopyTable:
    """Creates a copy of the desired table"""

    def __init__(self, nodes, cnxn, new_nodes):

        self.nodes = nodes
        self.cnxn = cnxn
        self.new_nodes = new_nodes
        self.cursor = self.cnxn.cursor()
        # Get the column names
        self.titles = self.get_column_names()
        # Create a copy of our table
        self.create_sql_table(self.nodes, self.new_nodes, self.titles)

    def get_column_names(self):
        """This method returns a list that holds the names of the columns of our table"""
        self.cursor.execute("SELECT * FROM "+self.nodes)
        return [i[0] for i in self.cursor.description]

    def create_sql_table(self, table, new_table, titles):
            """ This method creates an exact copy of a SQL nodes-table
            @Param table is the table that is going to be copied
            @Param new_table is the new table"""

            # Create an empty string
            sql_string = " "
            # Create an empty list
            type_list = []
            # For every column in our table
            for row in self.cursor.columns(table='NODES'):
                # Append the list with the variable type of each column
                type_list.append(row.type_name)
            # Set a counter to zero
            count = 0
            for title in titles:
                # Set the correct SQL string for execution
                sql_string = sql_string+" "+title+" "+type_list[count]+","
                count += 1
            # Remove the last comma
            sql_string = sql_string[:-1]
            # Create the new table
            self.cursor.execute("CREATE TABLE dbo."+new_table+" ("+sql_string+" )")
            # Inform the database so that we can see the changes in the management studio
            self.cnxn.commit()
            # Select all the columns
            self.cursor.execute("SELECT * FROM dbo."+table+" ORDER BY FID ASC")
            # Get all the rows of the table
            rows = self.cursor.fetchall()
            # For every row:
            # Create an empty string
            sql_string_2 = " "
            # For every row:
            for part in rows:
                # For every column of the table
                for i in range(0, len(self.titles)):
                    # Set the correct SQL string for the values
                    sql_string_2 = sql_string_2 + " "+str(part[i])+" ,"
                # Remove the last comma
                sql_string_2 = sql_string_2[:-1]
                print sql_string_2
                # Pass the values to the new table
                self.cursor.execute("INSERT INTO dbo."+new_table+" VALUES("+sql_string_2+")")
                sql_string_2 = " "
                # Inform the database
                self.cnxn.commit()


def main():
    connection = Connect("NODES", "LINKS")
    CopyTable(connection.nodes, connection.cnxn, "New_Nodes")

if __name__ == '__main__':
    main()
```
