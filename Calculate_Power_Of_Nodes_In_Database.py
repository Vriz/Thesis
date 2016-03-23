__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module calculates how many links exit a certain node and how many links enter the same node, and informs the
database"""

import pyodbc


class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database and asks for the names of the node=table and link-table """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class PowerOfNodes:

    def __init__(self, nodes, links, cnxn):
        self.nodes = nodes
        self.links = links
        self.cnxn = cnxn
        # Create two dictionaries that hold the connections between the nodes
        self.list_of_dictionaries = self.create_list_of_dictionaries(self.get_rows_of_table("SELECT * FROM dbo."+self.links))
        # Calculate the power of the nodes
        self.power_of_nodes_to_database(self.list_of_dictionaries)

    def get_rows_of_table(self, sql_string):
        """ This method gives us the desired rows of an Sql table
        @Param Sql_String is the Sql string
        @Return are the desired rows """
        cursor = self.cnxn.cursor()
        cursor.execute(sql_string)
        rows = cursor.fetchall()
        return rows

    def create_list_of_dictionaries(self, rows):
        """ This method creates 2 dictionaries
        The first dictionary contains the ID of the nodes where we can move to (from the Key node) and the required
        costs to do that.
        The key of the first dictionary will be a node from the FromNodeID column.
        The value of the key for the first dictionary will be a list of numerous 3 element sub-lists:
        FromNodeID--->[ToNodeID , ....repeat....]
        The second dictionary contains the ID of the nodes where we can travel from, towards the Key node.
        The key of the second dictionary will be a node from the ToNodeID column.
        The value of the key for the second dictionary will be a list of nodes:
        ToNodeID--->[FromNodeID , ....repeat....]
        @Param rows is the rows of the LINKS table
        @Return is a list with the dictionaries """

        # Create empty Dictionaries
        temp_dict_0 = {}
        temp_dict_1 = {}
        rows_0 = self.get_rows_of_table("SELECT * FROM dbo."+self.nodes)
        # For every node
        for row in rows_0:
            # Create a key for both of the dictionaries
            temp_dict_0[row[1]] = []
            temp_dict_1[row[1]] = []
        # For each row of the rows:
        for row in rows:
            # Building the Temp_Dict0:
            # Append the list with the values for the key: row[3] = FromNodeID
                temp_dict_0[row[3]].append(row[4])
            # Building the Temp_Dict_1:
            # Append the list with the values for the key: row[4] = ToNodeID
                temp_dict_1[row[4]].append(row[3])

        return [temp_dict_0, temp_dict_1]

    def power_of_nodes_to_database(self, dict_list):
        """This method takes the dictionaries that hold the connections between the nodes, calculates the power of
        each node and informs the database
        @Param dict_list is the list with the 2 dictionaries"""

        # For every key and value of the dictionary that holds the links that exit the key node
        for key, values in dict_list[0].items():
            # Inform the database (len(values) is the power of the node)
            cursor = self.cnxn.cursor()
            cursor.execute("UPDATE NODES SET LinksLeaving=? WHERE ID=?", (len(values), key,))
            cursor.commit()
            cursor.close()
        # For every key and value of the dictionary that holds the links that exit the key node
        for key, values in dict_list[1].items():
            # Inform the database (len(values) is the power of the node)
            cursor = self.cnxn.cursor()
            cursor.execute("UPDATE NODES SET LinksComing=? WHERE ID=?", (len(values), key,))
            cursor.commit()
            cursor.close()


def main():
    """ main class here."""
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")

    lis = PowerOfNodes(connection.nodes, connection.links, connection.cnxn)


if __name__ == '__main__':
    main()
