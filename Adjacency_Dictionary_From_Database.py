__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module takes node-centric table and a link-centric table and creates
 an adjacency dictionary"""

# dbo.NODES ---> Columns ( FID ID VISIBILITY CLASS JUNCTION)
# dbo.LINKS ---> Columns ( FID LinkID FromNodeID ToNodeID StartCost TravCost TWOWAY StartCost2 )

import pyodbc
import csv
from prettytable import PrettyTable


class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database and asks for the names of the node=table and link-table """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class Conversion:

    def __init__(self, nodes, links, cnxn):
        self.nodes = nodes
        self.links = links
        self.cnxn = cnxn
        # Create two dictionaries that hold the connections between the nodes
        self.list_of_dictionaries = self.create_list_of_dictionaries(self.get_rows_of_table("SELECT * FROM dbo."+self.links))
        # Create a dictionary with the personal data of each node
        self.dictionary_of_personal_data = self.create_dictionary_of_personal_data(self.get_rows_of_table("SELECT * FROM dbo."+self.nodes))
        # Build the adjacency dictionary
        self.adjacency_dictionary = self.build_dictionary(self.dictionary_of_personal_data, self.list_of_dictionaries)
        # Print it in a pretty way
        self.print_dictionary(self.adjacency_dictionary)

    def get_rows_of_table(self, sql_string):
        """ This method gives us the desired rows of an Sql table
        @Param Sql_String is the Sql string
        @Return are the desired rows """
        cursor = self.cnxn.cursor()
        cursor.execute(sql_string)
        rows = cursor.fetchall()
        return rows

    def string_to_list(self, input_string):
        """This method takes a string of coordinates and puts them in a list
        as floats
        @Param input_string is the string(x y, x y, x y) with the coordinates
        @Return is a list[[x, y], [x, y] ,[x ,y]] with the same coordinates"""

        # Put all the letters in a list
        lst = []
        for letter in input_string:
            lst.append(letter)
        # Remove the unnecessary characters
        for i in range(0, 12):
            lst.pop(0)
        lst = lst[:-1]
        # Reform the String
        string_1 = "".join(lst)
        # Split the string on the spaces and put the parts on a list
        lst_2 = string_1.split()
        # Putting the coordinates in pairs and then in a list (For uniting links)
        # Create the list that we are going to use as a base
        final_list = []
        # Create a temporary list
        temp_list = []
        i = 0
        # For every coordinate in the list
        for coord in lst_2:
            # Append the temporary list with the coordinate
            temp_list.append(coord)
            # If the coordinate is in position 1,3,5,7...
            if i % 2 != 0:
                # Append the final list with the temporary one
                final_list.append(temp_list)
                # And empty the temporary one
                temp_list = []
            i += 1
        # Create an empty list that we are going to store the pairs of coordinates as floats
        final_list_2 = []
        # For every pair o coordinates in final list we want to make a pair of float coordinates
        for part in final_list:
            # Create a temporary list
            temp_list_2 = []
            # For every 'string' coordinate
            for cord in part:
                # If the 'string' coordinate does not end in comma
                if cord[-1] != ",":
                    # Append the list with the float of the 'string' coordinate
                    temp_list_2.append(float(cord))
                # If the 'string' coordinate ends in comma
                if cord[-1] == ",":
                    # Remove the comma
                    word = cord[:-1]
                    # Append the list with the the float of the 'string' coordinate
                    temp_list_2.append(float(word))
                # Append the final list with the temporary list
            final_list_2.append(temp_list_2)
        return final_list_2

    def create_list_of_dictionaries(self, rows):
        """ This method creates 2 dictionaries
        The first dictionary contains the ID of the nodes where we can move to (from the Key node) and the required
        costs to do that.
        The key of the first dictionary will be a node from the FromNodeID column.
        The value of the key for the first dictionary will be a list of numerous 3 element sub-lists:
        FromNodeID--->[[LinkID, Visibility, ToNodeID, StartCost, TravCost, Class, TwoWay, StartCost2, Geometry] , ....repeat....]
        The second dictionary contains the ID of the nodes where we can travel from, towards the Key node.
        The key of the second dictionary will be a node from the ToNodeID column.
        The value of the key for the second dictionary will be a list of nodes:
        ToNodeID--->[FromNodeID , ....repeat....]
        @Param rows is the rows of the LINKS table
        @Return is a list with the dictionaries """

        # Create empty Dictionaries
        temp_dict_0 = {}
        temp_dict_1 = {}

        rows_0 = self.get_rows_of_table("SELECT ID FROM dbo."+self.nodes)
        # For every node
        for row in rows_0:
            # Create a key for both of the dictionaries
            temp_dict_0[row[0]] = []
            temp_dict_1[row[0]] = []
        # For each row of the of the LINKS table:
        for row in rows:
            # Building the Temp_Dict0:
            cursor = self.cnxn.cursor()
            # Get the coordinates of the link
            cursor.execute("SELECT GEOMETRY.STAsText() FROM dbo.LINKS WHERE LinkID=?", (row[1],))
            row_0 = cursor.fetchone()
            string_geometry = row_0[0]
            # Put the coordinates in a list
            geometry_list = self.string_to_list(string_geometry)
            cursor.close()
            # Building the temp_dict_0
            temp_dict_0[row[3]].append([row[1], row[2], row[4], row[5], row[6], row[7], row[8], row[9], geometry_list])
            # Building the Temp_Dict_1:
            temp_dict_1[row[4]].append(row[3])

        return [temp_dict_0, temp_dict_1]

    def create_dictionary_of_personal_data(self, rows):
        """ This method creates a dictionary for the Nodes of the NODES table.
        The keys will be the ID of each node and the value will be a 3 element list
        ID--->[VISIBILITY, CLASS, Geometry]
        @Param rows is the rows of the NODES table
        @Return is the dictionary """

        # Create an empty dictionary
        temp_dict = {}
        # For every row in the nodes table
        for row in rows:
            # Get the coordinate of the node
            cursor = self.cnxn.cursor()
            cursor.execute("SELECT GEOMETRY.Long, GEOMETRY.Lat FROM "+self.nodes+" WHERE ID=?", (row[1],))
            row_0 = cursor.fetchone()
            cursor.close()
            # Put it in a list
            geometry = [row_0[1], row_0[0]]
            # Build the temp_dict
            temp_dict[row[1]] = [row[2], row[3], geometry]

        return temp_dict

    def build_dictionary(self, node_data, connections_dict):
        """This method builds the adjacency dictionary
        @Param node_data is the dictionary withe personal information of each node
        @Param connections_dict is the list with the two dictionaries that hold the connections between the nodes"""

        # Create an empty dictionary
        final_dictionary = {}
        rows = self.get_rows_of_table("SELECT ID FROM dbo."+self.nodes)
        # For every row of the nodes table
        for row in rows:
            # Build the dictionary
            final_dictionary[row[0]] = [node_data[row[0]], [connections_dict[0][row[0]], connections_dict[1][row[0]]]]

        return final_dictionary

    def print_dictionary(self, dict2):
        """This method takes a dictionary and prints it in a pretty way
        @Param dict is the dictionary """
        i = 1
        for keys, values in dict2.items():
                print i
                k = PrettyTable([keys])
                k.add_row(["----->"])
                print k
                t = PrettyTable(['Visiblity', 'Class', 'Geometry'])
                t.add_row(values[0])
                f = PrettyTable(['LinkID', 'Visibility', 'ToNodeID', 'StartCost', 'TravCost', 'Class', 'TwoWay', 'StartCost2', 'Geometry'])
                for part in values[1][0]:
                    f.add_row(part)
                c = PrettyTable(['FromNodeID'])
                for part in values[1][1]:
                    c.add_row([part])
                print t
                print f
                print c
                print ""
                print ""
                i += 1


def main():
    """ main class here."""
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")
    # Create the adjacency Dictionary
    lis = Conversion(connection.nodes, connection.links, connection.cnxn)


if __name__ == '__main__':
    main()
