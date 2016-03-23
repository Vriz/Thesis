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


class ChangeVisibilityByClass:
    """ Takes an SQL table creates an exact copy and then changes the visibility of certain nodes based on on on the
     users preferences """

    def __init__(self, nodes, cnxn, cls):
        self.nodes = nodes
        self.cnxn = cnxn
        self.cls = cls
        self.change_visibility_by_class(self.cls)

    def change_visibility_by_class(self, cls):
        """ This method changes the visibility of certain nodes based on their class """

        self.cnxn.cursor().execute("UPDATE dbo."+self.nodes+" SET VISIBILITY=? WHERE CLASS=?", (0, cls,))
        self.cnxn.commit()


def main():
    # Create a connection to the database and the desired tables
    connection = Connect("NODES")
    # Changes the visibility of certain nodes
    ChangeVisibilityByClass(connection.nodes, connection.cnxn, "1")

if __name__ == '__main__':
    main()
