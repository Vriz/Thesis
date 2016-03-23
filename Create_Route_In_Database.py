
import pyodbc
import math
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module takes list of links, creates a route made of those links and an SQL table with the starting node,
ending node, length and geometry of the route"""

class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database and asks for the names of the node=table and link-table """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class CreateRoute:
    """Create the route bases on the links given in a list"""

    def __init__(self, nodes, links, cnxn, route_links):

        self.cnxn = cnxn
        self.nodes = nodes
        self.links = links
        self.route_links = route_links
        # Create the route
        self.route = self.make_route(self.route_links)
        # Calculate the distance
        self.route_distance = self.calculate_length(self.route)
        # Find the starting point and ending node of the route
        self.start_and_end = self.start_and_end_node(self.route_links)
        # Insert the route to an SQL table
        self.insert_route_to_database(self.route_distance, self.start_and_end)

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

    def calculate_min(self, distance_list):
        """This method takes a list and returns the element with tha lowest value
        @Param distance_list is a list of distances
        @Return is the minimum of those distances"""

        # Set the first element as minimum
        min = distance_list[0]
        # For each remaining element of the list
        for i in range(1, len(distance_list)):
            # If the distance is smaller than the minimum one
            if distance_list[i] < min:
                # Set that distance as minimum
                min = distance_list[i]
                
        return min

    def calculate_length(self, coordinates_list):
        """This method calculates the length of a polyline
        @Param coordinates_list is the list that holds the coordinates of the polyline
        @Return is the length of the polyline"""

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

    def list_to_string(self, lst):
        """This method takes a list of float coordinates and forms the string to use as input to the database
        @Param lst if the list of coordinates
        @Return is the desired string"""
        
        # Set i to 1 in order to be able to dictate the first coordinate
        i = 1
        # Create an empty string
        string = ""
        # For every node in the list
        for node in lst:
            # If it is the first node
            if i == 1:
                string = string+str(node[0])+" "+str(node[1])
            # For every other node
            else:
                string = string+", "+str(node[0])+" "+str(node[1])
            i += 1
            
        return string

    def make_route(self, id_list):
        """This method takes a list of links and creates a route
        @Param id_list is a list containing the id of the links that will form the route
        @Return is a list that contains the coordinates of the route"""
        
        # Create a cursor
        cursor = self.cnxn.cursor()
        # Get the coordinates of the first link in the list
        cursor.execute("SELECT GEOMETRY.STAsText() FROM dbo.LINKS WHERE LinkID=?", (id_list[0],))
        row = cursor.fetchone()
        string_geometry = row[0]
        # Get the coordinates of the first link convert them to float coordinates and set the list of those coordinates
        # as the route
        route = self.string_to_list(string_geometry)
        # For the rest links in the id_list
        for i in range(1, len(id_list)):
            #Create a cursor
            cursor_1 = self.cnxn.cursor()
            # Get the coordinates of the link
            cursor_1.execute("SELECT GEOMETRY.STAsText() FROM dbo.LINKS WHERE LinkID=?", (id_list[i],))
            row = cursor_1.fetchone()
            string_geometry = row[0]
            # Get the coordinates of the link convert them to float coordinates and set the list of those coordinates
            # as the list_geometry (the link that we want to add to our route)
            list_geometry = self.string_to_list(string_geometry)
            # If the first coordinate of the route is the same as the last coordinate of the link we want to add
            if route[0] == list_geometry[-1]:
                # Remove the last coordinate from the link
                list_geometry = list_geometry[:-1]
                # Add the link to the route
                route = list_geometry + route
            # If the first coordinate of the route is the same as the first coordinate of the link we want to add
            elif route[0] == list_geometry[0]:
                # Remove the first element of the link
                list_geometry = list_geometry[1:]
                # Reverse the link
                list_geometry.reverse()
                # Add the link to the route
                route = list_geometry + route
            # If the last coordinate of the route is the same as the first coordinate of the link we want to add
            elif route[-1] == list_geometry[0]:
                # Remove the first coordinate from the link
                list_geometry = list_geometry[1:]
                # Add the link to the route
                route = route + list_geometry
            # If the last coordinate of the route is the same as the last coordinate of the link we want to add
            elif route[-1] == list_geometry[-1]:
                # Remove the last coordinate from the link
                list_geometry = list_geometry[:-1]
                # Reverse the link
                list_geometry.reverse()
                # Add the link to the route
                route = route + list_geometry
            # If nothing of the above is happening it means that at least two of the links given in the id_list
            #  do not connect with each other. In that case:
            else:
                # First coordinate the route
                route_start = route[0]
                # Last coordinate of the route
                route_end = route[-1]
                # First coordinate of the link we want to add to the route
                link_to_add_start = list_geometry[0]
                # Last coordinate of the link we want to add to the route
                link_to_add_end = list_geometry[-1]
                # Calculate the distance of each possible combination between the start and and of the route and start
                # and end of the link we want to add to the route
                distance_1 = self.calculate_ds(route_start, link_to_add_start)
                distance_2 = self.calculate_ds(route_start, link_to_add_end)
                distance_3 = self.calculate_ds(route_end, link_to_add_start)
                distance_4 = self.calculate_ds(route_end, link_to_add_end)
                # Find the minimum of the those 4 distances
                min = self.calculate_min([distance_1, distance_2, distance_3, distance_4])
                # If the minimum distance is the one between the start of the route and the start of the link
                #  we want to add 
                if min == distance_1:
                    # Reverse the link we want to add
                    list_geometry.reverse()
                    # Add the link to the route
                    route = list_geometry + route
                # If the minimum distance is the one between the start of the route and the end of the link
                #  we want to add    
                elif min == distance_2:
                    # Add the link to the route
                    route = list_geometry + route
                # If the minimum distance is the one between the end of the route and the start of the link
                #  we want to add
                elif min == distance_3:
                    # Add the link to the route
                    route = route + list_geometry
                # If the minimum distance is the one between the end of the route and the end of the link we want to add
                else:
                    # Reverse the link we want to add
                    list_geometry.reverse()
                    # Add the link to the route
                    route = route + list_geometry

        return route

    def start_and_end_node(self, id_list):
        """This method finds the id of the starting and ending node of our route
        @Param id_list is a list containing the id of the links that will form the route
        @Return is a list with the starting and ending node"""
        
        # Create an empty list that we are going to put all the possible nodes that could be the ones we are looking for
        possible_nodes = []
        # Create a cursor
        cursor = self.cnxn.cursor()
        # The nodes we are looking are located in the first link of the id_list of the last link of the id_list
        
        # Append the possible nodes list with the FromNodeID and the ToNodeID of the first link
        cursor.execute("SELECT LinkID, FromNodeID, ToNodeID FROM LINKS WHERE LinkID = ?", (id_list[0]))
        row = cursor.fetchone()
        possible_nodes.append(row[1])
        possible_nodes.append(row[2])
        # Append the possible nodes list with the FromNodeID and the ToNodeID of the last link
        cursor.execute("SELECT LinkID, FromNodeID, ToNodeID FROM LINKS WHERE LinkID = ?", (id_list[-1]))
        row = cursor.fetchone()
        possible_nodes.append(row[1])
        possible_nodes.append(row[2])
        start = None
        end = None
        # For every node in the possible nodes list
        for node in possible_nodes:
            # Create a cursor
            cursor = self.cnxn.cursor()
            # Get the coordinates of the node
            cursor.execute("SELECT GEOMETRY.Long, GEOMETRY.Lat FROM NODES WHERE ID=?", (node,))
            row = cursor.fetchone()
            node_coord = [row[1], row[0]]
            # if the coordinates match the first coordinates of the route
            if node_coord == self.route[0]:
                # Set the node as the starting node
                start = node
            # if the coordinates match the last coordinates of the route
            elif node_coord == self.route[-1]:
                # Set the node as the ending node
                end = node
            else:
                pass
        return [start, end]

    def insert_route_to_database(self, distance, nodes):
        """This method creates an SQL table and puts the route in it
        @Param distance is the length of the route
        @Param nodes is the list with starting and ending nodes"""
        
        # Create the table
        cursor = self.cnxn.cursor()
        cursor.execute("CREATE TABLE Route (FID int, FromNodeID int, ToNodeID int, Length float, GEOMETRY geography)")
        cursor.commit()
        # Insert the data in the table
        cursor.execute("INSERT INTO Route (FID, FromNodeID, ToNodeID, Length) VALUES(1, ?, ?, ?)", (nodes[0], nodes[1], distance,))
        cursor.commit()
        # Form the string to use as input for the geometry of the route
        sql_string = self.list_to_string(self.route)
        cursor = self.cnxn.cursor()
        # Insert the geometry to the table
        cursor.execute("UPDATE Route SET GEOMETRY=geography::STGeomFromText('LINESTRING("+sql_string+")', 4326 )")
        cursor.commit()


def main():
    """ main class here."""
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")
    # Create the adjacency Dictionary
    lis = CreateRoute(connection.nodes, connection.links, connection.cnxn, [1005612, 1005609, 1005618, 1005615, 1005611, 1037506])
    print lis.route_links
    print lis.route
    print lis.route_distance
    print lis.start_and_end

if __name__ == '__main__':
    main()
