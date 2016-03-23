__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module checks if the links given connect to each other"""

from Adjacency_Dictionary_From_Database import Conversion, Connect


class CheckForContinuation:

    def __init__(self, diction, lst):
        # The adjacency dictionary
        self.dict = diction
        # The list with the links
        self.lst = lst
        # Find the links in the dictionary
        self.list_of_links = self.find_links(self.dict, self.lst)
        # Check them
        self.check = self.check_for_connectivity(self.list_of_links)
        
    def find_links(self, diction, lst):
        """This method finds the links in the adjacency dictionary based on the list of ids given
        @Param diction if the adjacency dictionary
        @Param lst is the list with the ids of the links
        @Return is a list with all the data of each link"""

        # Create an empty list
        list_to_return = []
        # For every key and value in the adjacency dictionary
        for key, values in diction.items():
            # For every link in the links exiting the node
            for link in values[1][0]:
                # If the id of the link is in the list of the list
                if link[0] in lst:
                    # Put the data of the link in the list
                    list_to_return.append(link)

        return list_to_return

    def check_for_connectivity(self, lst):
        """This method checks if the links given connect to each other
        @Param lst is the list with the all the data for each link
        @Return is True or False"""

        # Create an empty list
        star_and_end_list = []
        # For every link in the list
        for part in lst:
            # Put the starting and ending point of each link in the list
            star_and_end_list.append(part[8][0])
            star_and_end_list.append(part[8][-1])
        # Set a counter to zero
        count = 0
        # For every item in the list
        for i in range(0, len(star_and_end_list)):
            # Store the coordinate
            coord = star_and_end_list[i]
            # If the coordinate appears only one time in the list
            if star_and_end_list.count(coord) == 1:
                # Add one to the counter
                count += 1
        # If there only two coordinates that appear one time in the list
        if count == 2:
            # Retrun True
            return True
        else:
            # Return False
            return False


def main():
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")
    # Create the adjacency Dictionary
    first = Conversion(connection.nodes, connection.links, connection.cnxn)
    fifth = CheckForContinuation(first.adjacency_dictionary, [1005612, 1005609, 1005618, 1005615, 1005611, 1037506])

    print fifth.check


if __name__ == '__main__':
    main()
