__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
""" Takes an SQL table and changes the visibility of links based on the users preferences """

from Adjacency_Dictionary_From_Database import Connect


class ChangeVisOfLinkByID:

    def __init__(self, links, cnxn, lst):
        self.links = links
        self.cnxn = cnxn
        self.list_to_change = lst
        # Change the visibility of the links
        self.change_links_by_id(self.list_to_change)

    def change_links_by_id(self, list_0):
        """This method takes a list of ids and changes the visibility of those links
        @Param list_0 is the list with the ids"""

        # For each id in the list
        for link in list_0:
            self.cnxn.cursor().execute("UPDATE dbo."+self.links+" SET Visibility=0 WHERE LinkID=?", (link,))
            self.cnxn.commit()


def main():
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")
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
    ChangeVisOfLinkByID(connection.links, connection.cnxn, temp_list)

if __name__ == '__main__':
    main()
