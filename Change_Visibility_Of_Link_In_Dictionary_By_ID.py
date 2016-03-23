__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module changes the visibility of links in the adjacency dictionary based on their ID"""

from Adjacency_Dictionary_From_Database import Conversion, Connect


class ChangeVisInDictByID:

    def __init__(self, dict, lst):
        self.dict = dict
        self.lst = lst
        # Change the visibility of the links
        self.change_visibility(self.dict, self.lst)

    def change_visibility(self, dictionary, lst):
        """This method changes the visibility of links based on their ID
        @Param dictionary is the adjacency dictionary
        @Param lst is the list of links we want their visibility changed"""

        # For every key and value in the adjacency dictionary
        for key, values in dictionary.items():
            # For every link
            for link in values[1][0]:
                # If tha link's ID is in the lst
                if link[0] in lst:
                    # Set the visibility to zero
                    link[1] = 0


def main():
    connection = Connect("NODES", "LINKS")
    first = Conversion(connection.nodes, connection.links, connection.cnxn)
    temp_list = []
    condition = True
    # As long as condition == True
    while condition:
        # Promt the user to give us the id of a link he wants to change or to end the process
        temp_id = raw_input("Please type the id of the link or type End to continue! :")
        # If the users does not want the process to end
        if temp_id != 'End':
            # Get the integer of the users input
            ids = int(temp_id)
            # Append the list with tha id
            temp_list.append(ids)
        # If the user types 'End'
        else:
            condition = False
    ChangeVisInDictByID(first.adjacency_dictionary, temp_list)

if __name__ == '__main__':
    main()
