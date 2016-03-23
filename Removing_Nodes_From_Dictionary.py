__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-

"""This module takes a list of nodes and removes the from the adjacency dictionary"""

import pyodbc
from Adjacency_Dictionary_From_Database import Conversion
from Finds_Nodes_To_Remove_From_Database import NodesToRemove
from prettytable import PrettyTable


class Connect:
    """ Connects us to the database """
    def __init__(self, nodes, links):
        """ Connects us to the database and asks for the names of the node=table and link-table """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')
        self.nodes = nodes
        self.links = links


class RemoveNodes:

    def __init__(self, dictionary, lst):
        # The adjacency dictionary
        self.dictionary = dictionary
        # The list with the nodes we have to remove
        self.lst = lst
        # Remove the nodes and store the fixed dictionary
        self.fixed_dictionary = self.remove_unnecessary_nodes(self.dictionary, self.lst)
        # Print it in a pretty way
        self.print_dictionary(self.fixed_dictionary)

    def adjust_dict_0(self, node, dict):
        """This method takes a node that has exactly one link exiting the node and exactly one link entering the node
        removes it from the dictionary and adjust the connections
        @Param nodes is the id of the node we want to delete
        @Param if the adjacency dictionary"""

        # The id of the node that one of its exiting links is the one that enters our node
        key_from = dict[node][1][1][0]
        # The link we are going to use as the second one in line to form the new link
        second_link = dict[node][1][0][0]
        # The id of the node that one of its entering links is the one that exits our node
        key_to = second_link[2]
        # Go to the dictionary of the node that the new link will end, remove our node and add the node that the
        # new link will start
        dict[key_to][1][1].remove(node)
        dict[key_to][1][1].append(key_from)
        # For every link that exits the node that the new link will start from
        for link in dict[key_from][1][0]:
            # If that link heads towards our node
            if link[2] == node:
                # This is the link that we are going to use as first in line to form the new link
                first_link = link
        # For every link that exits the node that the new link will start from
        for link in dict[key_from][1][0]:
            # If that link heads towards our node
            if link[2] == node:
                # Remove it
                dict[key_from][1][0].remove(link)
        dict[key_from][1][0].append([999, first_link[1], second_link[2], first_link[3], first_link[4] + second_link[4], first_link[5], first_link[6], second_link[7], first_link[8] + second_link[8][1:]])

    def adjust_dict_1(self, node, dict, lst, temp_list):
        """This method takes a node that has exactly two links exiting the node and exactly zero links entering the
        node, remove it from the dictionary and adjust the connections
        @Param node is the id of the node we want to delete
        @Param dict is the adjacency dictionary
        @Param lst is the list with all the nodes we want to delete
        @Param temp_list is a list that we are going to store the nodes we cannot delete at this point"""

        # Store the first and second link that exit our node
        first_link = dict[node][1][0][0]
        second_link = dict[node][1][0][1]
        # If both of our links head towards a node that we have to delete
        if first_link[2] in lst[2] and second_link[2] in lst[2]:
                # Store it in a list to delete it later
                temp_list.append(node)
        # If the first link heads towards a node we have to delete then we have to direct the new link towards that node
        elif first_link[2] in lst[2]:
            # Switch the first and second link
            tranfer = second_link
            first_link = tranfer
            second_link = first_link
            # The id of the node that the new link will start from
            key_from = first_link[2]
            # The id of the node that the new link will end to
            key_to = second_link[2]
            # Remove our node from the FromNode list of the key_from and key_to node
            dict[key_from][1][1].remove(node)
            dict[key_to][1][1].remove(node)
            # Go to the dictionary of the key_to node and append is with key_from node
            dict[key_to][1][1].append(key_from)
            # Remove the first coordinate of the geometry of the first link
            start = first_link[8][1:]
            # and reverse it
            start.reverse()
            # Form the new link
            dict[key_from][1][0].append([999, 1, key_to, first_link[7], first_link[4] + second_link[4], first_link[5], first_link[6], second_link[7], start + second_link[8]])

        elif second_link[2] in lst[2]:
            # The id of the node that the new link will start from
            key_from = first_link[2]
            # The id of the node that the new link will end to
            key_to = second_link[2]
            # Remove our node from the FromNode list of the key_from and key_to node
            dict[key_from][1][1].remove(node)
            dict[key_to][1][1].remove(node)
            # Go to the dictionary of the key_to node and append is with key_from node
            dict[key_to][1][1].append(key_from)
            # Remove the first coordinate of the geometry of the first link
            start = first_link[8][1:]
            # and reverse it
            start.reverse()
            # Form the new link
            dict[key_from][1][0].append([999, 1, key_to, first_link[7], first_link[4] + second_link[4], first_link[5], first_link[6], second_link[7], start + second_link[8]])
        else:
            # The id of the node that the new link will start from
            key_from = first_link[2]
            # The id of the node that the new link will end to
            key_to = second_link[2]
            # Remove our node from the FromNode list of the key_from and key_to node
            dict[key_from][1][1].remove(node)
            dict[key_to][1][1].remove(node)
            # Go to the dictionary of the key_to node and append is with key_from node
            dict[key_to][1][1].append(key_from)
            # Remove the first coordinate of the geometry of the first link
            start = first_link[8][1:]
            # and reverse it
            start.reverse()
            # Form the new link
            dict[key_from][1][0].append([999, 1, key_to, first_link[7], first_link[4] + second_link[4], first_link[5], first_link[6], second_link[7], start + second_link[8]])

    def adjust_dict_2(self, node, dict):
        """This method takes a node that has exactly zero links exiting the node and exactly two links entering the
        node, remove it from the dictionary and adjust the connections
        @Param node is the id of the node we want to delete
        @Param if the adjacency dictionary"""

        # The key of the first node that one of its link head towards our node
        first_key = dict[node][1][1][0]
        # The key of the second node that one of its link head towards our node
        second_key = dict[node][1][1][1]
        # For every link that exit the first key node
        for link in dict[first_key][1][0]:
            # if that link heads towards our node
            if link[2] == node:
                # Store it as the first link
                first_link = link
                # and remove it
                dict[first_key][1][0].remove(first_link)
        # For every link that exit the second key node
        for link in dict[second_key][1][0]:
            # if that link heads towards our node
            if link[2] == node:
                # Store it as the second link
                second_link = link
                # and remove it
                dict[second_key][1][0].remove(second_link)

        from_key = first_key
        to_key = second_key
        # Remove the last coordinate of the geometry of the second link
        end = second_link[8][:-1]
        # Reverse it
        end.reverse()
        # Form the link
        dict[from_key][1][0].append([999, first_link[1], to_key, first_link[3], first_link[4] + second_link[4], first_link[5], first_link[6], second_link[3], first_link[8] + end])
        # Add the from_key node in the FromNodes list of the to_key node
        dict[to_key][1][1].append(from_key)

    def adjust_dict_3(self, node, dict):
        """This method takes a node that has exactly two links exiting the node and exactly zero links entering the
        node, remove it from the dictionary and adjust the connections
        @Param node is the id of the node we want to delete
        @Param dict is the adjacency dictionary"""

        first_link = dict[node][1][0][0]
        second_link = dict[node][1][0][1]

        # The id of the node that the new link will start from
        key_from = first_link[2]
        # The id of the node that the new link will end to
        key_to = second_link[2]
        # Remove our node from the FromNode list of the key_from and key_to node
        dict[key_from][1][1].remove(node)
        dict[key_to][1][1].remove(node)
        # Go to the dictionary of the key_to node and append is with key_from node
        dict[key_to][1][1].append(key_from)
        # Remove the first coordinate of the geometry of the first link
        start = first_link[8][1:]
        # and reverse it
        start.reverse()
        # Form the new link
        dict[key_from][1][0].append([999, 1, key_to, first_link[7], first_link[4] + second_link[4], first_link[5], first_link[6], second_link[7], start + second_link[8]])

    def remove_unnecessary_nodes(self, dict, lst):
        """This method removes nodes from the adjacency dictionary
        @Param dict is the adjacency dictionary
        @Param lst is the list with the nodes we want to remove"""

        # Create a temporary list that we are going to store the nodes we will delete later
        temp_list = []
        # For every node in the first list of nodes we want to remove
        for node in lst[0]:
            # Remove the nodes and adjust the dictionary
            self.adjust_dict_0(node, dict)
        # For every node in the second list of nodes we want to remove
        for node in lst[1]:
            # Remove the nodes and adjust the dictionary
            self.adjust_dict_1(node, dict, lst, temp_list)
        # For every node in the third list of nodes we want to remove
        for node in lst[2]:
            # Remove the nodes and adjust the dictionary
            self.adjust_dict_2(node, dict)
        # For every node in the list of nodes we wanted to delete later
        for node in temp_list:
            # If only one link exits the node and only one link enters the node
            if len(dict[node][1][0]) == 1 and len(dict[node][1][0]) == 1:
                self.adjust_dict_0(node, dict)
            # If only two links exit the node and zero links enter the node
            elif len(dict[node][1][0]) == 2 and len(dict[node][1][0]) == 0:
                self.adjust_dict_3(node, dict)
            # If only zero links exit the node and two links enter the node
            elif len(dict[node][1][0]) == 0 and len(dict[node][1][0]) == 2:
                self.adjust_dict_2(node, dict)
            else:
                pass
        # For every node we want to delete
        for part in lst:
            for node in part:
                    # Remove it as keys from the dictionary
                    del dict[node]
        return dict

    def print_dictionary(self, dict2):
        """This method takes a dictionary and prints it in a pretty way
        @Param dict is the dictionary """
        i = 1
        for keys, values in dict2.items():
                print i
                k = PrettyTable([keys])
                k.add_row(["----->"])
                print k
                t = PrettyTable(['Visiblity', 'Class', 'Geometry'])
                t.add_row(values[0])
                f = PrettyTable(['LinkID', 'Visibility', 'ToNodeID', 'StartCost', 'TravCost', 'Class', 'TwoWay', 'StartCost2', 'Geometry'])
                for part in values[1][0]:
                    f.add_row(part)
                c = PrettyTable(['FromNodeID'])
                for part in values[1][1]:
                    c.add_row([part])
                print t
                print f
                print c
                print ""
                print ""
                i += 1


def main():
    """ main class here."""
    # Create a connection to the database and the desired tables
    connection = Connect("NODES", "LINKS")
    # Create the adjacency Dictionary
    first = Conversion(connection.nodes, connection.links, connection.cnxn)
    second = NodesToRemove(connection.nodes, connection.links, connection.cnxn)
    adjacency_dictionary = first.adjacency_dictionary
    nodes_to_remove = second.final_nodes_to_remove
    third = RemoveNodes(adjacency_dictionary, nodes_to_remove)


if __name__ == '__main__':
    main()
