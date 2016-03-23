__author__ = 'vriz'
# !/usr/bin/env python
# -*-coding: utf-8-*-
"""This module takes node-SQL table and changes the visibility of certain nodes
based on on the users preferences"""

import pyodbc


class Connect:
    """ Connects us to the database """

    def __init__(self, nodes, ):
        """ Connects us to the database and and assigns the node table to the appropriate variable """
        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver = '{SQL Server}', server = 'localhost', database = 'PracticeCopy1')
        self.nodes = nodes


class ChangeVisibilityByID:
    """ Takes an SQL table creates an exact copy and then changes the visibility of certain nodes based on on on the
    users preferences """

    def __init__(self, nodes, cnxn, lst):
        self.nodes = nodes
        self.cnxn = cnxn
        self.lst = lst
        # Change the visibility of the nodes
        self.change_visibility_by_id(self.lst)

    

    def change_visibility_by_id(self, list_0):
        """This method takes a list of ids and sets the visibility of those nodes to zero
        @Param list_0 is the list with the ids"""

        # For each id in the list
        for node in list_0:
            self.cnxn.cursor().execute("UPDATE dbo."+self.nodes+" SET VISIBILITY=? WHERE ID=?", (0, node,))
            self.cnxn.commit()


def main():
    # Create a connection to the database and the desired tables
    connection = Connect("NODES")
    temp_list = []
    condition = True
    # As long as condition == True
    while condition:
        # Promt the user to give us the id of the nodes he wants their visibility to be changed or to end the process
        temp_id = raw_input("Please type the id of the node or type End to continue! :")
        # If the users does not want the process to end
        if temp_id != 'End':
            # Get the integer of the users input
            ids = int(temp_id)
            # Append the list with tha id
            temp_list.append(ids)
        # If the user types 'End'
        else:
            condition = False
    # Changes the visibility of certain nodes
    ChangeVisibilityByID(connection.nodes, connection.cnxn, temp_list)

if __name__ == '__main__':
    main()
