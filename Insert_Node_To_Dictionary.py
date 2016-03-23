__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-
"""This module insert a node to the adjacency dictionary"""


from Adjacency_Dictionary_From_Database import Conversion, Connect
from Adjacency_Dictionary_To_Database import DictionaryToDatabase
import math


class InsertNode:

    def __init__(self, node_id, link_id, distance, dict):
        # The id of the new node
        self.node_id = node_id
        # The id of the link in which the new node will be inserted
        self.link_id = link_id
        # The distance from the start of the link in which new node will be inserted
        self.distance = distance
        # The adjacency dictionary
        self.dict = dict
        # Retrieve the data of the link that we will split in two and node key it belongs to
        self.data = self.retrieve_link_data_and_key(self.link_id, self.dict)
        # Create the new links
        self.new_links = self.create_the_new_links(self.data[0], self.distance)
        # Fix the dictionary
        self.fixed_dictionary = self.insert_to_dictionary(self.new_links[0], self.new_links[1], self.new_links[2], self.data[1], self.dict)

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

    def retrieve_link_data_and_key(self, id_of_link, dictionary):
        """This methods finds the link we want the new node to be inserted into and the key(node) of the adjacency
         dictionary in which the link belongs
         @Param id_of_link is the id the link
         @Param dictionary is the adjacency dictionary
         @Return link is the data of the link
         @Return key is the key(node) of the adjacency dictionary"""

        # For each key and its values in the dictionary
        for key, values in dictionary.items():
            # For every link exiting the node
            for link in values[1][0]:
                # If the id of the link matches the given id
                if link[0] == id_of_link:
                    # Return the link and the key
                    return [link, key]

    def create_the_new_links(self, link_data, distance):
        """This method forms the new links after splitting the link, that the new node will be inserted into, in two
        @Param link_data is the all the data for the link that is going to be split
        @Param distance is the desired distance in which we want the new node to be inserted
        @Reurn new_node is a list with the personal data of the new node
        @Return first_link is the first link that will enter the new node
        @Return second_link is the second link that will exit from the new node"""

        # Calculate the point of insertion and get the geometry for the new links
        point_and_link_geometry = self.calculate_point_of_insertion(link_data[8], distance)
        # Form the first link
        first_link = [999, link_data[1], self.node_id, 0, 0, link_data[5], link_data[6], 0, point_and_link_geometry[1]]
        # Form the second link
        second_link = [999, link_data[1], link_data[2], 0, 0, link_data[5], link_data[6], 0, point_and_link_geometry[2]]
        # The personal data for the new node
        new_node = [1, 3, point_and_link_geometry[0]]
        return [new_node, first_link, second_link]

    def insert_to_dictionary(self, new_node, first_link, second_link, key_node, dict):
        """This method inserts the new node to the adjacency dictionary
        @Param new_node is the id of the new node
        @Param first_link is the data of the first link that will enter the new node
        @Param second_link is the data for the second link that will exit from the new node
        @Param key_node is the node that the link, that was split, exits from
        @Return is the fixed adjacency dictionary"""

        # Remove the link that was split in two from the key_node
        dict[key_node][1][0].remove(self.data[0])
        # Add the first link to the key_node
        dict[key_node][1][0].append(first_link)

        # Go to the node that self.link_id enters into and remove the key_node from its FromNodeID list
        dict[second_link[2]][1][1].remove(key_node)
        # Add the new node to the same list
        dict[second_link[2]][1][1].append(self.node_id)
        # Create the new key in the adjacency dictionary with all the required data
        dict[self.node_id] = [new_node, [[second_link], [key_node]]]

        return dict


def main():
    connection = Connect("NODES", "LINKS")
    first = Conversion(connection.nodes, connection.links, connection.cnxn)
    sixth = InsertNode(200111, 1037509, 2, first.adjacency_dictionary)

    print sixth.data

    print sixth.fixed_dictionary[125088]


    seventh = DictionaryToDatabase(connection.cnxn, sixth.fixed_dictionary,'yeeeeeeeeeeah')

if __name__ == '__main__':
    main()
