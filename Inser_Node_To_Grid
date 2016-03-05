__author__ = 'vriz'
# !/usr/bin/env python
# -*-coding: utf-8-*-
"""This module takes data for a new node that is about to be inserted to our grid. Creates a copy of our database and
inserts the new node in the appropriate nodes-table. After that, it splits the link in which we want the new node
to be inserted, in two parts"""

import pyodbc
import math


class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database and asks for the names of the node=table and link-table """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class InsertNode:

    def __init__(self, nodes, links, cnxn, list_1, list_2, distance):
        self.nodes = nodes
        self.links = links
        self.cnxn = cnxn
        self.cursor = self.cnxn.cursor()
        self.distance = distance

        # The id of the node
        self.node_id = list_1[0]

        # The list that holds the information for the insert method
        self.nodes_info_list = list_1

        # Get the correct FID number for the row that is about to be inserted
        self.fid = self.get_fid(self.nodes)

        # The list that holds the information for the split_link method
        self.links_info_list = list_2

        # Get the length and the geometry of the target link
        self.link_length_and_geometry = self.calculate_link_length(self.links_info_list[0])

        # Find the point (X, Y) that the node will be inserted as well as the geometries of the two new links
        # that will be created
        self.point_of_insertion = self.calculate_point_of_insertion(self.link_length_and_geometry[1], self.distance)

        # Insert the row
        self.insert(self.nodes_info_list)

        # Split the link
        self.split_link(self.links_info_list)

        # Reset the FID column
        self.fid_reset(self.links)

    def calculate_point_of_insertion(self, coordinates_list, distance):
        """This method takes a list of coordinates, a given distance and returns a list with 3 elements.
        First element is the point that the coordinates_list will be split
        Second and third element hold the coordinates of after we split the coordinates_list at the
        desired point
        @Param ooordinates_list is a list with the geometry of a link
        @Param distance is a given distance based on which the coordinates_list we be split in two
        @Return is the 3 element list"""

        xy = coordinates_list
        link_length = 0
        # For every coordinate of the polyline except the last one
        for i in range(0, len(coordinates_list)-1):
            # Calculate the ds between a point and its next one
            ds = self.calculate_ds(xy[i], xy[i+1])
            # Add it to the length
            link_length += ds
            # If the length at that point is equal or larger than the distance given:
            if link_length > distance:
                # Split the link at that point
                point_to_split = coordinates_list[i]
                point_index = coordinates_list.index(point_to_split)
                link_1 = coordinates_list[0:point_index+1]
                link_2 = coordinates_list[point_index:len(coordinates_list)]
                break
            else:
                pass

        return [point_to_split, link_1, link_2]

    def string_to_list(self, input_string):
        """This method takes a string of coordinates and puts them in a list
        as floats
        @Param input_string is the string(x y, x y, x y) with the coordinates
        @Return is a list[[x, y], [x, y] ,[x ,y]] with the same coordinates"""

        # Put all the letters in a list
        lst = []
        for letter in input_string:
            lst.append(letter)
        # Remove the unnecessary characters
        for i in range(0, 12):
            lst.pop(0)
        lst = lst[:-1]
        # Reform the String
        string_1 = "".join(lst)
        # Split the string on the spaces and put the parts on a list
        lst_2 = string_1.split()
        # Putting the coordinates in pairs and then in a list (For uniting links)
        # Create the list that we are going to use as a base
        final_list = []
        # Create a temporary list
        temp_list = []
        i = 0
        # For every coordinate in the list
        for coord in lst_2:
            # Append the temporary list with the coordinate
            temp_list.append(coord)
            # If the coordinate is in position 1,3,5,7...
            if i % 2 != 0:
                # Append the final list with the temporary one
                final_list.append(temp_list)
                # And empty the temporary one
                temp_list = []
            i += 1
        # Create an empty list that we are going to store the pairs of coordinates as floats
        final_list_2 = []
        # For every pair o coordinates in final list we want to make a pair of float coordinates
        for part in final_list:
            # Create a temporary list
            temp_list_2 = []
            # For every 'string' coordinate
            for cord in part:
                # If the 'string' coordinate does not end in comma
                if cord[-1] != ",":
                    # Append the list with the float of the 'string' coordinate
                    temp_list_2.append(float(cord))
                # If the 'string' coordinate ends in comma
                if cord[-1] == ",":
                    # Remove the comma
                    word = cord[:-1]
                    # Append the list with the the float of the 'string' coordinate
                    temp_list_2.append(float(word))
                # Append the final list with the temporary list
            final_list_2.append(temp_list_2)
        return final_list_2

    def list_to_string(self, geometry):
        """This method takes a list of coordinates and builds a string that we be used to store the geometry
        in our database
        @Param geometry is a list of coordinates (floats)
        @Return is the string to use as input to the database"""

        # Set a counter to 1
        i = 1
        # Create an empty string
        string = ""
        # For every node the geometry
        for node in geometry:
            # If it's the first node of the geometry
            if i == 1:
                string = string+str(node[0])+" "+str(node[1])
            # For every other node
            else:
                string = string+", "+str(node[0])+" "+str(node[1])
            i += 1
        return string

    def calculate_ds(self, point_1, point_2):
        """This method calculates the distance between two points
        @Param point_1 is the first point
        @Param point_2 is the second point
        @Return is the distance in Km"""

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
    
    def calculate_length(self, coordinates_list):
        """This method calculates the length of a link
        @Param coordinates_list is the list that holds the coordinates of the link
        @Return is the length of the link"""

        xy = coordinates_list
        # Set length to zero
        link_length = 0
        # For every coordinate of the polyline except the last one
        for i in range(0, len(coordinates_list)-1):
            # Calculate the ds between a point and its next one
            ds = self.calculate_ds(xy[i], xy[i+1])
            # Add it to the length
            link_length += ds
        return link_length

    def get_fid(self, table):
        """ This method finds the correct FID number for our row
        we want to insert in the nodes-table
        @ Param new_table is the copy of the nodes-table
        @ Return is the FID number"""

        # Select everything from our table
        self.cursor.execute("SELECT * FROM dbo."+table+" ORDER BY FID ASC")
        # Assign the rows
        rows = self.cursor.fetchall()
        # Set a counter to zero
        counter = 0
        # For every row of the table
        for row in rows:
            # Add one to our counter
            counter += 1
        return counter+1

    def insert(self, data_list):
        """This method inserts the row to our nodes-table
        @ Param new_table is the copy of the nodes table
        @ Param data_list is the list that holds all the
        information for the new node:
        data_list[1] is the Id of the new node
        data_list[2] is the visibility of the new node
        data_list[3] is the class of the new node
        data_list[4] is the junction variable for the new node"""

        self.cursor.execute("INSERT INTO dbo.NODES (FID, ID, VISIBILITY, CLASS, JUNCTION) VALUES(?, ?, ?, ?, ?)", (self.fid, self.node_id, data_list[1], data_list[2], data_list[3],))
        self.cnxn.commit()
        self.cursor.execute("UPDATE dbo.NODES SET GEOMETRY = geography::Point("+str(self.point_of_insertion[0][0])+", "+str(self.point_of_insertion[0][1])+", 4326) WHERE ID=?", (self.node_id,))
        self.cnxn.commit()

    def calculate_link_length(self, link_id):

        self.cursor.execute("SELECT GEOMETRY.STAsText() FROM dbo.LINKS WHERE LinkID=?", (link_id,))
        row = self.cursor.fetchone()
        geometry = self.string_to_list(row[0])
        length = self.calculate_length(geometry)
        return [length, geometry]

    def split_link(self, data_list):
        """This method takes a links-table and data for a node that is going to be
        inserted in link and splits the link in 2 parts
        @ Param new_table is the copy of the links-table
        @ Param data_list is a list that holds all the required information :
        data_list[0] is the Id of the link we are about to split in two
        data_list[1] is the Id of the first new link we will create
        data_list[2] is the Id of the second new link we will create
        data_list[3] is the start cost_2 for the first new link
        data_list[4] is the start cost for the second new link
        data_list[5] is the traverse cost for the first new link
        data_list[6] is the traverse cost for the second new link
        """
        # Get the row where the LinID is the one we want to split in two
        self.cursor.execute("SELECT * FROM dbo.LINKS WHERE LinkID=?", (data_list[0],))
        row = self.cursor.fetchone()
        # FromNodeID for the first link
        from_node_1 = row[2]
        # ToNodeID for the first link
        to_node_1 = self.node_id
        # The class for both of the new links
        link_class = row[6]
        # The TWOWAY attribute of the new links
        link_TWOWAY = row[7]
        # StartCost for the first new link
        start_cost = row[4]
        # FromNodeID for the second link
        from_node_2 = self.node_id
        # ToNodeID for the second link
        to_node_2 = row[3]
        # StarCost2 for the second new link
        start_cost_2 = row[8]
        # Find the appropriate FID for the new links we are about to insert in our database
        self.cursor.execute("SELECT * FROM dbo.LINKS")
        rows = self.cursor.fetchall()
        counter = 0
        for part in rows:
            counter += 1
        # Insert first link
        self.cursor.execute("INSERT INTO dbo.LINKS (FID, LinkID, FromNodeID, ToNodeID, StartCost, TravCost, CLASS, TWOWAY, StartCost2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (counter+1, data_list[1], from_node_1, to_node_1, start_cost, data_list[5], link_class, link_TWOWAY, data_list[3], ))
        # Inform the database
        self.cnxn.commit()
        # Form the string that will be used as input for the geometry column of our first new link
        string_to_database = self.list_to_string(self.point_of_insertion[1])
        self.cnxn.cursor().execute("UPDATE LINKS SET GEOMETRY=geography::STGeomFromText('LINESTRING("+string_to_database+")', 4326) WHERE LinkID=?", (data_list[1],))
        self.cnxn.commit()
        # Insert second link
        self.cursor.execute("INSERT INTO dbo.LINKS (FID, LinkID, FromNodeID, ToNodeID, StartCost, TravCost, CLASS, TWOWAY, StartCost2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (counter+2, data_list[2], from_node_2, to_node_2, data_list[4], data_list[6], link_class, link_TWOWAY, start_cost_2, ))
        # Inform the database
        self.cnxn.commit()
        # Form the string that will be used as input for the geometry column of our second new link
        string_to_database_2 = self.list_to_string(self.point_of_insertion[2])
        self.cnxn.cursor().execute("UPDATE LINKS SET GEOMETRY=geography::STGeomFromText('LINESTRING("+string_to_database_2+")', 4326) WHERE LinkID=?", (data_list[2],))
        self.cnxn.commit()
        # Delete the link we have already split in two
        self.cursor.execute("DELETE FROM dbo.LINKS WHERE LinkID=?", (data_list[0],))
        self.cnxn.commit()

    def fid_reset(self, table):
        """This method resets the Fid column of a SQL table after we have
        deleted some rows
        @ Param new_table is the copy of the links-table"""

        # Select all the columns and sort them by their FID with ascending order
        self.cursor.execute("SELECT * FROM dbo.LINKS ORDER BY FID ASC")
        # Get all the rows of the table
        rows = self.cursor.fetchall()
        # Create an empty list in which we are going to store the FIDs of the remaining links
        fid_list = []
        # Fill the list with the FIDs
        for part in rows:
            fid_list.append(part.FID)
        # Set a counter to 0
        counter = 1
        # For every element in the fid_list:
        for part in fid_list:
            # Reset the FIDs of every link
            self.cursor.execute("UPDATE dbo."+table+" SET FID=? WHERE FID=?", (counter, part,))
            self.cnxn.commit()
            counter += 1


def main():
    connection = Connect("NODES", "LINKS")
    # The numbers are for test purposes
    lis = InsertNode(connection.nodes, connection.links, connection.cnxn, [5555, 1, 11, 0], [1005572, 11, 22, 101, 102, 1011, 1022], 2)
    print lis.link_length_and_geometry[0]
    print lis.link_length_and_geometry[1]
    print lis.point_of_insertion[0]
    print lis.point_of_insertion[1]
    print lis.point_of_insertion[2]

if __name__ == '__main__':
    main()
