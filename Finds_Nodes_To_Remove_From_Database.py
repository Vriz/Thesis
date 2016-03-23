__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module detects the node that we need to remove from our network"""

import pyodbc

class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database and asks for the names of the node=table and link-table """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class NodesToRemove:

    def __init__(self, nodes, links, cnxn):

        self.nodes = nodes
        self.links = links
        self.cnxn = cnxn
        # Find the possible nodes to remove based on how many links entering and exiting a certain node
        self.possible_nodes_to_remove = self.create_list_of_possible_nodes_to_remove(self.get_rows_of_table("SELECT ID, LinksLeaving, LinksComing FROM dbo."+self.nodes+" WHERE VISIBILITY=1"))
        # If the links entering or exiting the nodes have the same two-way attribute put them in the final list
        self.final_nodes_to_remove = self.create_final_list(self.possible_nodes_to_remove)

    def get_rows_of_table(self, sql_string):
        """ This method gives us the desired rows of an Sql table
        @Param Sql_String is the Sql string
        @Return are the desired rows """
        cursor = self.cnxn.cursor()
        cursor.execute(sql_string)
        rows = cursor.fetchall()
        return rows

    def create_list_of_possible_nodes_to_remove(self, rows):
        """This method finds the possible nodes we have to remove from our network
        based on how many links entering and exiting a certain node
        @Param rows is the rows of the NODES table
        @Return is the list with the possible nodes"""

        # Create an empty list
        list_to_return = [[], [], []]
        # For every row in the NODES table
        for row in rows:
            # If there is exactly one link exiting the node and exactly one link entering the node
            if row[1] == 1 and row[2] == 1:
                # Put it the first sub list
                list_to_return[0].append(row[0])
            # If there are exactly two links exiting the node and exactly zero links entering the node
            elif row[1] == 2 and row[2] == 0:
                # Put it the second sub list
                list_to_return[1].append(row[0])
            # If there are exactly zero links exiting the node and exactly two links entering the node
            elif row[1] == 0 and row[2] == 2:
                # Put it the third sub list
                list_to_return[2].append(row[0])
            else:
                pass
        return  list_to_return

    def create_final_list(self, nodes_list):
        """This method finds the final nodes that we have to remove from our network based on two-way attribute
        @Param nodes_list is the list with the possible nodes to remvoe
        @Return is the final list with the nodes we have to remove"""

        # Create an empty list
        final_list = [[], [], []]
        # For every node in the first sub list
        for node in nodes_list[0]:
            # Get the link that enter the node
            cursor_1 = self.cnxn.cursor()
            cursor_1.execute("SELECT TwoWay FROM LINKS WHERE ToNodeID=?", (node,))
            row = cursor_1.fetchone()
            first = row[0]
            cursor_1.close()
            # Get the link that exits the node
            cursor_2 = self.cnxn.cursor()
            cursor_2.execute("SELECT TwoWay FROM LINKS WHERE FromNodeID=?", (node,))
            row = cursor_2.fetchone()
            second = row[0]
            cursor_2.close()
            # If both links have the same value in the two-way attribute
            if first == second :
                # Put it in the final list
                final_list[0].append(node)
        # For every node in the second sub list
        for node in nodes_list[1]:
            # Get both links that exit the node
            cursor_2 = self.cnxn.cursor()
            cursor_2.execute("SELECT TwoWay FROM LINKS WHERE FromNodeID=?", (node,))
            rows = cursor_2.fetchall()
            cursor_2.close()
            i =1
            for row in rows:
                if i == 1:
                    first = row[0]
                else:
                    second = row[0]
                i +=1
            # If both links are bidirectional
            if first == 1 and second ==1:
                # Put the node in the final list
                final_list[1].append(node)
        # For every node in the third sub list
        for node in nodes_list[2]:
            # Get both links that enter the node
            cursor_3 = self.cnxn.cursor()
            cursor_3.execute("SELECT TwoWay FROM LINKS WHERE ToNodeID=?", (node,))
            rows = cursor_3.fetchall()
            cursor_3.close()
            i =1
            for row in rows:
                if i == 1:
                    first = row[0]
                else:
                    second = row[0]
                i +=1
            # If both links are bidirectional
            if first == 1 and second ==1:
                # Put the node in the final list
                final_list[2].append(node)

        return final_list



def main():
    """ main class here."""
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")

    lis = NodesToRemove(connection.nodes, connection.links, connection.cnxn)

    print lis.possible_nodes_to_remove

    print lis.final_nodes_to_remove



if __name__ == '__main__':
    main()
