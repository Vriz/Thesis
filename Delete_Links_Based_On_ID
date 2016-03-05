__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
""" Takes an SQL table and creates a copy of it and removes the non desired links based on the users preferences """

import pyodbc


class Connect:
    """Connects us to the database"""
    def __init__(self, links):
        """ Connects us to the database and and assigns and link table to the appropriate variable """
        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.links = links


class DeleteLinksByID:
    """ Takes an SQL table and creates a copy of it and removes the non desired
    links base on the users preferences"""

    def __init__(self, links, cnxn):
        self.links = links
        self.cnxn = cnxn
        self.cond = True
        # Create a list with the ids of the nodes that the used wants to be removed
        self.list_to_delete = self.links_to_remove(self.cond)
        # Delete the links
        self.delete_links_by_id(self.list_to_delete)
        # Reset the FID column
        self.fid_reset()

    def links_to_remove(self, condition):
        """This metgod creates a list with all the Ids of the links that
        the user wants to be removed
        @Param condition is boolean variable set to True
        @Return is a list that contains the Ids of the links the user wants
        to be removed"""

        # Create an empty list
        temp_list = []
        # As long as condition == True
        while condition:
            # Promt the user to give us the id of a link he wants to remove or to end the process
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
        return temp_list

    def delete_links_by_id(self, list_0):
        """This method takes a list of ids and deletes the links
        with those ids
        @Param list_0 is the list with the ids"""

        # For each id in the list
        for link in list_0:
            self.cnxn.cursor().execute("DELETE FROM dbo."+self.links+" WHERE LinkID=?", (link,))
            self.cnxn.commit()

    def fid_reset(self):
        """This method resets the Fid column of a SQL table after we have
        deleted some rows"""

        cursor = self.cnxn.cursor()
        # Select all the columns and sort them by their FID with ascending order
        cursor.execute("SELECT * FROM dbo."+self.links+" ORDER BY FID ASC")
        # Get all the rows of the table
        rows = cursor.fetchall()
        # Create an empty list in which we are going to store the FIDs of the remaining links
        fid_list = []
        # Fill the list with the FIDs
        for part in rows:
            fid_list.append(part.FID)
        # Set a counter to 0
        counter = 0
        # For every element in the fid_list:
        for part in fid_list:
            # Reset the FIDs of every link
            cursor.execute("UPDATE dbo."+self.links+" SET FID=? WHERE FID=?", (counter+11005563, part,))
            self.cnxn.commit()
            counter += 1


def main():
    # Create a connection to the database and the desired tables
    connection = Connect("LINKS")
    # Create a new table and then delete the links
    DeleteLinksByID(connection.links, connection.cnxn)

if __name__ == '__main__':
    main()
