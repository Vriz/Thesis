__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
""" Takes an SQL table and changes the visibility of links based on the users preferences """


from Adjacency_Dictionary_From_Database import Connect


class ChangeVisOfLink:

    def __init__(self, links, cnxn, cls):
        self.links = links
        self.cnxn = cnxn
        self.cls = int(cls)
        # Change the visibility of the links
        self.change_links_by_class(cls)

    def change_links_by_class(self, choice):
        """ This method changes the visibility of links based on their class

        @Param choice is the class of links we want their visibility to be changed"""
        cursor = self.cnxn.cursor()
        # Change the visibility of the links
        cursor.execute("UPDATE dbo."+self.links+" SET Visibility=0 WHERE CLASS=?", (choice,))
        self.cnxn.commit()


def main():
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")
    # Change the visibility of the links
    ChangeVisOfLink(connection.links, connection.cnxn, "1")

if __name__ == '__main__':
    main()
