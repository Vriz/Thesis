__author__ = 'vriz'
# !/usr/bin/env python
# -*-coding: utf-8-*-
import arcpy
import csv
import os
from prettytable import PrettyTable
import pyodbc
from random import randint
"""This module takes a polyline shapefile, calculates the geometry of each polyline, stores it in a list
for further use, prints it and finally saves it in a scv file"""


class Connect:
    """ Connects us to the database """
    def __init__(self):
        """ Connects us to the database and asks for the names of the node=table and link-table """

        self.cnxn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='localhost', database='PracticeCopy1')


class InsertCursor:

    def __init__(self, shapefile):
        # Inserts a cursor in the desired fields of our polyline.
        self.shapefile = shapefile
        # The path to our shape file
        self.path = r"C:\Users\vriz\Documents\ArcGIS\AddIns\Desktop10.1"
        self.fc = os.path.join(self.path, self.shapefile)
        # The desired fields
        self.fields = ["FID", "Shape@", "FromNodeID", "ToNodeID", "ID"]
        # The cursor
        self.cursor = arcpy.da.SearchCursor(self.fc, self.fields)


class FindGeometry:
    """ Finds the geometry of each polyline in a shape file, stores it to a list, saves it to a csv file
     and prints it in a pretty way """

    def __init__(self, cursor, cnxn,):
        self.cursor = cursor
        self.cnxn = cnxn
        self.create_tables()
        # Creates the list with the geometry of each polyline
        self.final_list = self.geometry(self.cursor)
        # Saves it to csv file
        self.start_and_ending_points = self.get_start_and_end(self.final_list[0])
        # self.save_to_csv(self.final_list, raw_input("Name of file:"))
        # Print it in a pretty way
        self.print_dictionary(self.start_and_ending_points)
        self.print_dictionary(self.final_list[0])

    def create_tables(self):
        cursor = self.cnxn.cursor()
        try:
            cursor.execute("CREATE TABLE NODES (FID int, ID int, VISIBILITY int, CLASS int, JUNCTION int, GEOMETRY geography)")
            cursor.commit()
        except:
            pass
        try:
            cursor.execute("CREATE TABLE LINKS (FID int, LinkID int, FromNodeID int, ToNodeID int, StartCost int, TravCost int, CLASS int, TwoWay int, StartCost2 int, GEOMETRY geography)")
            cursor.commit()
        except:
            pass

    def list_to_string(self, lst):
        i = 1
        string = ""
        for node in lst:
            if i == 1:
                string = string+str(node[0])+" "+str(node[1])
            else:
                string = string+", "+str(node[0])+" "+str(node[1])
            i += 1
        return string

    def geometry(self, cur):
        """ Extracts the geometry of each polyline and stores it to a list
        @Param cur is the cursor we insert to the desired fields of the shape file
        @Return is a list with the geometries """
        nodes_list = []
        for row in cur:
            if row[2] not in nodes_list:
                nodes_list.append(row[2])
            if row[3] not in nodes_list:
                nodes_list.append(row[3])
        cur.reset()
        length = len(nodes_list)+1
        # Create an empty list (this is the one that will be returned)
        list_final = []
        # For each row in our cursor
        for row in cur:
            # Create a temporary list that is going to be emptied every time we change row
            lst = []
            # For each part in the row[1]='shape' (It could be a multi part polyline)
            for part in row[1]:
                # For each vertex of the feature
                for pnt in part:
                    # reate list with X,Y coordinates of the vertex
                    lst_pnts = [pnt.X, pnt.Y]
                    # Append the temporary list which at the end contains every X,Y of the polyline
                    lst.append(lst_pnts)
            # Get starting coordinate
            start = lst[0]
            # Get ending coordinate
            end = lst[-1]
            coords = [start, end]
            cursor = self.cnxn.cursor()
            cursor.execute("INSERT INTO LINKS (FID, LinkID, FromNodeID, ToNodeID, StartCost, TravCost, CLASS, TwoWay, StartCost2) VALUES (?, ?, ?, ?, 0, 0, ?, ?, 0)", (row[0]+1, row[4], row[2], row[3], randint(1,5), randint(0,1)),)
            cursor.commit()
            coordinates = lst
            sql_string = self.list_to_string(coordinates)
            cursor.execute("UPDATE LINKS SET GEOMETRY=geography::STGeomFromText('LINESTRING("+sql_string+")', 4326) WHERE LinkID=?", (row[4]),)
            cursor.commit()
            if nodes_list != []:
                if row[2] in nodes_list:
                    cursor.execute("INSERT INTO NODES (FID, ID, VISIBILITY, CLASS, JUNCTION) VALUES (?, ?, 1, ?, 0)", (length-len(nodes_list), row[2], randint(1, 5)),)
                    cursor.commit()
                    coord_1 = str(coords[0][0])
                    coord_2 = str(coords[0][1])
                    cursor.execute("UPDATE NODES SET GEOMETRY = geography::Point("+coord_1+", "+coord_2+", 4326) WHERE ID=?", (row[2],))
                    cursor.commit()
                    nodes_list.remove(row[2])
                if row[3] in nodes_list:
                    cursor.execute("INSERT INTO NODES (FID, ID, VISIBILITY, CLASS, JUNCTION) VALUES (?, ?, 1, ?, 0)", (length-len(nodes_list), row[3], randint(1, 5)),)
                    cursor.commit()
                    coord_1 = str(coords[1][0])
                    coord_2 = str(coords[1][1])
                    cursor.execute("UPDATE NODES SET GEOMETRY = geography::Point("+coord_1+", "+coord_2+", 4326) WHERE ID=?", (row[3],))
                    cursor.commit()
                    nodes_list.remove(row[3])
            # Every time before we change row we append the final list with the temporary list
            list_final.append(lst)
        return [list_final, nodes_list]

    def get_start_and_end(self, geom):
        coords = []
        for lst in geom:
            point_1 = lst[0]
            point_2 = lst[-1]
            coords.append([point_1, point_2])
        return coords

    def print_dictionary(self, lst):
        """ This method takes a list and prints it in a pretty way
        @Param list is the list with the geometry of each polyline """
        count = 0
        for part in lst:
            k = PrettyTable(["FID "+str(count)])
            k.add_row(["----->"])
            print k
            t = PrettyTable(["Geometry"])
            for n in part:
                t.add_row([n])
            print t
            print ""
            count += 1

    def save_to_csv(self, lst, name_of_file):
        """ This method takes a list and saves it to a csv file
        @Param list is the list with the geometry of each polyline
        @Param Name_of_file is the name of the file in which the dictionary will be saved """
        w = csv.writer(open(name_of_file, "w"))
        count = 0
        for part in lst:
            w.writerow(["FID "+str(count)+"--->", part])
            count += 1


def main():
    """ main class here """
    # Create an instance of the insert_cursor class for the desired polyline
    connection = Connect()
    cur = InsertCursor("Diploma2.shp", )
    # Use the cursor of the instance to calculate the geometry
    check = FindGeometry(cur.cursor, connection.cnxn)
    i = 0
    for coords in check.start_and_ending_points:
        j = 0
        for coord2 in check.start_and_ending_points:
            if coords[0] == coord2[1]:
                print i, j
            j += 1
        i += 1
    lst = check.final_list[0]


if __name__ == '__main__':
    main()
