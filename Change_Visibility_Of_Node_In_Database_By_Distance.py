__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module takes node-centric table, a link-centric table, a certain node id and a distance. Then changes the
visibility of the nodes that are in greater distance (given distance) from the node (node id) and removes all the
links that are associated with those nodes"""


import pyodbc
import math


class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database where the node-table and link-table are located"""

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class ChangeVisibilityBasedOnDistance:

    def __init__(self, nodes, links, cnxn, node_id, distance):
        self.nodes = nodes
        self.links = links
        self.cnxn = cnxn
        self.node_id = node_id
        self.distance = distance
        # Get the list of the distant nodes
        self.distant_nodes = self.get_the_list_of_distant_nodes(self.node_id, self.distance)

        # Change their visibility
        self.change_visibility(self.distant_nodes)

        # Get the nodes that are neighboring the main node
        self.nodes_not_to_delete = self.get_list_of_nodes_we_must_not_delete()

        # Remove the links
        self.remove_links(self.distant_nodes, self.nodes_not_to_delete)

    def calculate_ds(self, point_1, point_2):
        """Calculate the great circle distance between two points
        on the earth (specified in decimal degrees
        @Param point_1 is the first point (x, y)
        @Param point_2 is the second point (x, y))
        @Return is the distance between the two nodes in Kilometers"""

        latitude_1 = point_1[0]
        longitude_1 = point_1[1]
        latitude_2 = point_2[0]
        longitude_2 = point_2[1]

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [longitude_1, latitude_1, longitude_2, latitude_2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        km = 6367 * c
        return km

    def get_the_list_of_distant_nodes(self, node_id, distance):
        """This method finds the nodes of the distant nodes
        @Param node_id is our main node
        @Param distance is the distance in which we want our nodes to be located
        @Return is a list with the distant nodes"""

        # Insert a cursor
        cursor_1 = self.cnxn.cursor()
        # Select the row that holds the information of our node
        cursor_1.execute("SELECT GEOMETRY.Long, GEOMETRY.Lat FROM "+self.nodes+" WHERE ID=?", (node_id,))
        row = cursor_1.fetchone()
        primary_node_coord = [row[1], row[0]]
        # Close the cursor
        cursor_1.close()
        # Insert a second cursor
        cursor_2 = self.cnxn.cursor()
        # Select all the rows of the nodes table
        cursor_2.execute("SELECT ID FROM dbo."+self.nodes)
        rows = cursor_2.fetchall()
        # Create an empty list
        nodes_list = []
        # For every row in rows
        for row in rows:
            # If the node id of the row is not the same as the node_id (node id giver by the user)
            if row[0]!= node_id:
                # Set the coordinates of the node as the secondary coordinates
                cursor_3 = self.cnxn.cursor()
                cursor_3.execute("SELECT GEOMETRY.Long, GEOMETRY.Lat FROM "+self.nodes+" WHERE ID=?", (row[0],))
                rows = cursor_3.fetchone()
                secondary_node_coord = [rows[1], rows[0]]
                # If the distance between the two nodes is greater than the distance given by the user
                if self.calculate_ds(primary_node_coord, secondary_node_coord) >= distance:
                    # Append the nodes list
                    nodes_list.append(row.ID)
                cursor_3.close()
        # Close the cursor
        cursor_2.close()
        return nodes_list

    def get_list_of_nodes_we_must_not_delete(self):
        """This method finds the node that are neighbours to our main node
         @Return is the list with those nodes"""

        cursor_5 = self.cnxn.cursor()
        # Get the all the rows tha begin or end with our main node
        cursor_5.execute("SELECT * FROM dbo."+self.links+" WHERE (FromNodeID=?) OR (ToNodeID=?)", (self.node_id, self.node_id), )
        rows = cursor_5.fetchall()
        # Create an empty list
        nodes_list = []
        # For every row
        for row in rows:
            # if the FromNodeID is our main node
            if row[2] != self.node_id:
                # Then append the list with the ToNodeID
                nodes_list.append(row[2])
            # if the ToNodeID is our main node
            if row[3] != self.node_id:
                # Then append the list with the FromNodeID
                nodes_list.append(row[3])
        # Return the list
        return nodes_list

    def change_visibility(self, nodes):
        """This method changes the visibility of the distant nodes
        @Param nodes is the list with the distant nodes"""

        # Insert a cursor
        cursor_3 = self.cnxn.cursor()
        # For every node is the distant nodes list
        for node in nodes:
            # Set the visibility to 2
            cursor_3.execute("UPDATE dbo."+self.nodes+" SET VISIBILITY=2 WHERE ID=?", (node,))
            cursor_3.commit()
            # Close the cursor
        cursor_3.close()

    def remove_links(self, nodes, nodes_2):
        """This method removes all the links associated with the distant nodes
        except the ones that connect to our main node
        @Param nodes is the distant nodes list"""

        # Insert a cursor
        nodes_3 = [item for item in nodes if item not in nodes_2]
        cursor_4 = self.cnxn.cursor()
        # For every node is the distant nodes list
        for node in nodes_3:
            # Remove the links that have the node as starting point or ending point
            cursor_4.execute("DELETE FROM dbo."+self.links+" WHERE (FromNodeID=?) OR (ToNodeID=?)", (node, node))
            cursor_4.commit()
        for node in nodes_2:
            cursor_4.execute("SELECT * FROM dbo."+self.links+" WHERE (FromNodeID=?) OR (ToNodeID=?)", (node, node))
            rows = cursor_4.fetchall()
            for row in rows:
                if row[2] != self.node_id and row[3] != self.node_id:
                    cursor_4.execute("DELETE FROM dbo."+self.links+" WHERE LinkID=?", (row[1],))
                    cursor_4.commit()
        # Close the cursor
        cursor_4.close()


def main():
    """ main class here."""
    # Create a connection to the database and the desired tables
    connection = Connect("NODES","LINKS" )
    lis = ChangeVisibilityBasedOnDistance(connection.nodes, connection.links, connection.cnxn, 104377, 50)
    print lis.distant_nodes
    print lis.nodes_not_to_delete

if __name__ == '__main__':
    main()
