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


class DeleteLinksByClass:
    """ Takes an SQL table and creates a copy of it and removes the non desired
    links base on the users preferences"""

    def __init__(self, links, cnxn, cls):
        self.links = links
        self.cnxn = cnxn
        self.cls = cls
        # Delete the links
        self.delete_links_by_class(cls)
        # Reset the FID column
        self.fid_reset()

    def delete_links_by_class(self, choice):
        """ This method removes the non-desired links
        @Param choice is the class of links that the user wants to remove"""

        # Delete the links whom class==choice
        self.cnxn.cursor().execute("DELETE FROM dbo."+self.links+" WHERE CLASS=?", (choice,))
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
            self.cnxn.cursor().execute("UPDATE dbo."+self.links+" SET FID=? WHERE FID=?", (counter+1, part,))
            self.cnxn.commit()
            counter += 1


def main():
    # Create a connection to the database and the desired tables
    connection = Connect("LINKS")
    # Create a new table and then delete the links
    DeleteLinksByClass(connection.links, connection.cnxn, "1")

if __name__ == '__main__':
    main()
