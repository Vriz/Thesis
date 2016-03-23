__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module changes the visibility of links in the adjacency dictionary based on their class"""

from Adjacency_Dictionary_From_Database import Conversion, Connect


class ChangeVisInDictByClass:

    def __init__(self, dict, cls):
        self.dict = dict
        self.cls = int(cls)
        # Change the visibility of the links
        self.change_visibility(self.dict, self.cls)

    def change_visibility(self, dictionary, cls):
        """This method changes the visibility of links based on their class
        @Param dictionary is the adjacency dictionary
        @Param cls is the class of links we want theirs visibility changed"""

        # For every key and value in the adjacency dictionary
        for key, values in dictionary.items():
            # For every link
            for link in values[1][0]:
                # If tha links class == cls
                if link[5] == cls:
                    # Set the visibility to zero
                    link[1] = 0


def main():
    connection = Connect("NODES", "LINKS")
    first = Conversion(connection.nodes, connection.links, connection.cnxn)
    ChangeVisInDictByClass(first.adjacency_dictionary, "2")


if __name__ == '__main__':
    main()
