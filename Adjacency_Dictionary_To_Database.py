__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module inserts the data of the adjacent dictionary to a new LINKS TABLE"""
from Adjacency_Dictionary_From_Database import Conversion
from Finds_Nodes_To_Remove_From_Database import NodesToRemove
from Removing_Nodes_From_Dictionary import RemoveNodes


class DictionaryToDatabase:

    def __init__(self, cnxn, dict, name_of_table):
        self.cnxn = cnxn
        self.dict = dict
        # The name of the new table
        self.name_of_table = name_of_table
        # Create the new Links table
        self.create_table(self.name_of_table)
        # Insert the data
        self.insert_data(self.name_of_table, self.dict)

    def list_to_string(self, lst):
            """This method takes a list of float coordinates and forms the string to use as input to the database
            @Param lst if the list of coordinates
            @Return is the desired string"""

            # Set i to 1 in order to be able to dictate the first coordinate
            i = 1
            # Create an empty string
            string = ""
            # For every node in the list
            for node in lst:
                # If it is the first node
                if i == 1:
                    string = string+str(node[0])+" "+str(node[1])
                # For every other node
                else:
                    string = string+", "+str(node[0])+" "+str(node[1])
                i += 1

            return string

    def create_table(self, name):
        """This method creates a new links table in our database
        @Param name is the name of the new table"""
        cursor = self.cnxn.cursor()
        cursor.execute("CREATE TABLE "+name+" (FID int, LinkID int, Visibility int, FromNodeID int, ToNodeID int, StartCost int, TravCost int, CLASS int, TwoWay int, StartCost2 int, GEOMETRY geography)")
        cursor.commit()

    def insert_data(self, name, dict):
        """This method inserts tha data of the adjacent dictionary to the new table
        @Param name is the name of the table
        @Param dict is the adjacent dictionary"""

        cursor = self.cnxn.cursor()
        counter = 0
        # For every key and value of the dictionary
        for key, values in dict.items():
            # For every link that exit a certain node
            for link in values[1][0]:
                # Convert the geometry to string
                string = self.list_to_string(link[8])
                # Insert the data
                cursor.execute("INSERT INTO "+name+" (FID, LinkID, Visibility, FromNodeID, ToNodeID, StartCost, TravCost, CLASS, TwoWay, StartCost2) VALUES(?,?,?,?,?,?,?,?,?,?)", (counter, link[0], link[1], key, link[2], link[3], link[4], link[5], link[6], link[7]), )
                cursor.commit()
                cursor.execute("UPDATE "+name+" SET GEOMETRY=geography::STGeomFromText('LINESTRING("+string+")', 4326 ) WHERE FID=?", (counter), )
                cursor.commit()
                counter += 1


def main():
    """ main class here."""
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")
    # Create the adjacency Dictionary
    first = Conversion(connection.nodes, connection.links, connection.cnxn)
    adjacency_dictionary = first.adjacency_dictionary
    # Find the nodes we need to remove
    second = NodesToRemove(connection.nodes, connection.links, connection.cnxn)
    nodes_to_remove = second.final_nodes_to_remove
    # Remove the nodes and adjust the dictionary
    third = RemoveNodes(adjacency_dictionary, nodes_to_remove)
    # Insert the fixed links to a new table in our database
    fourth = DictionaryToDatabase(connection.cnxn, third.fixed_dictionary, "Fixed_links")

if __name__ == '__main__':
    main()
