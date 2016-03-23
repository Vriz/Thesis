__author__ = 'vriz'
# !/usr/bin/env python
#  -*-coding: utf-8-*-

from Adjacency_Dictionary_From_Database import Conversion, Connect
import arcpy
import os

"""This module takes an adjacency dictionary and creates a node shapefile and a links shapefile"""


class DictToShapefile:

    def __init__(self, nodes, links, dict):
        self.nodes = nodes
        self.links = links
        self.dict = dict
        # Create the two shapefiles
        self.create_shapefiles(self.nodes, self.links)
        # Add the required fields
        self.add_fields(self.nodes, self.links)
        # Add the data
        self.add_data(self.nodes, self.links, self.dict)

    def create_shapefiles(self, nds, lks):
        """This method creates two shapefiles. A shapefile for points and a shapefile for polylines
        @Param nds is the name of the points shapefile
        @Param lks is the name of the polylines shapefile"""

        # Create the links shapefile

        arcpy.CreateFeatureclass_management(r"C:\Users\vriz\Desktop\ARGIS",  lks, "POLYLINE", spatial_reference=arcpy.Describe(r"C:\Users\vriz\Desktop\ARGIS\Diploma2.shp").spatialReference)
        # Create the nodes shapefile
        arcpy.CreateFeatureclass_management(r"C:\Users\vriz\Desktop\ARGIS", nds, "POINT", spatial_reference=arcpy.Describe(r"C:\Users\vriz\Desktop\ARGIS\RailNode.shp").spatialReference)

    def add_fields(self, nds, lks):
        """This method add the required fields to our shapefiles that we created before
        @Param nds is the name of the points shapefile
        @Param lks is the name of the polylines shapefile"""

        # Set our arcpy environment
        arcpy.env.workspace = r"C:\Users\vriz\Desktop\ARGIS"
        # Add the fields in the nodes shapefile
        arcpy.AddField_management(nds, 'NodeID', 'DOUBLE')
        arcpy.AddField_management(nds, 'Visibility', 'DOUBLE')
        arcpy.AddField_management(nds, 'Class', 'DOUBLE')
        arcpy.DeleteField_management(nds, "Id")
        # Add the fields in the links shapefile
        arcpy.AddField_management(lks, 'LinkID', 'DOUBLE')
        arcpy.AddField_management(lks, 'Visibility', 'DOUBLE')
        arcpy.AddField_management(lks, 'FromNodeID', 'DOUBLE')
        arcpy.AddField_management(lks, 'ToNodeID', 'DOUBLE')
        arcpy.AddField_management(lks, 'StartCost', 'DOUBLE')
        arcpy.AddField_management(lks, 'TravCost', 'DOUBLE')
        arcpy.AddField_management(lks, 'Class', 'DOUBLE')
        arcpy.AddField_management(lks, 'TwoWay', 'DOUBLE')
        arcpy.AddField_management(lks, 'StartCst_2', 'DOUBLE')
        arcpy.DeleteField_management(lks, "Id")

    def add_data(self, nds, lks, dict):
        """This method adds the data to our shapefiles
        @Param nds is the name of the points shapefile
        @Param lks is the name of the polylines shapefile
        @Param dict is the adjacency dictionary"""

        # Links feature Class
        fc = os.path.join(r"C:\Users\vriz\Desktop\ARGIS", lks)
        # The fields
        fields = ['FID', "Shape@", 'LinkID', 'Visibility', 'FromNodeID', 'ToNodeID', 'StartCost', 'TravCost', 'Class', 'TwoWay', 'StartCst_2']
        # Nodes feature Class
        fc_2 = os.path.join(r"C:\Users\vriz\Desktop\ARGIS", nds)
        # The fields
        fields_2 = ["Shape@", 'ID', 'Visibility', 'Class']

        # Cursor for the links shapefile
        rows = arcpy.InsertCursor(fc, fields)
        # Create an arcpy array that we are going to use to input geometry data to our polylines
        array = arcpy.Array()
        # Cursor for the links shapefile
        rows_2 = arcpy.InsertCursor(fc_2, fields_2)
        
        # For every key and its values in our dictionary
        for key, values in dict.items():
            # Create a new row
            row_2 = rows_2.newRow()
            # Set the values
            row_2.setValue("NodeID", key)
            row_2.setValue('Visibility', values[0][0])
            row_2.setValue('Class', values[0][1])
            point = arcpy.Point(values[0][2][1], values[0][2][0])
            row_2.setValue('Shape', point)
            # Insert the row
            rows_2.insertRow(row_2)
            # For every link in the dictionary
            for links in values[1][0]:
                # Create a new row
                row = rows.newRow()
                # Set the values
                row.setValue("LinkID", links[0])
                row.setValue('Visibility', links[1])
                row.setValue('FromNodeID', key)
                row.setValue('ToNodeID', links[2])
                row.setValue('StartCost', links[3])
                row.setValue('TravCost', links[4])
                row.setValue('Class', links[5])
                row.setValue('TwoWay', links[6])
                row.setValue('StartCst_2', links[7])
                # Set the Shape value for the polyline
                for cord in links[8]:
                    array.add(arcpy.Point(cord[0], cord[1]))
                polyline = arcpy.Polyline(array)
                row.setValue('Shape', polyline)
                # Clear the array so that its empty for the next polyline
                array.removeAll()
                # Insert the row
                rows.insertRow(row)


def main():


    connection = Connect("NODES", "LINKS")
    first = Conversion(connection.nodes, connection.links, connection.cnxn)

    arcgis = DictToShapefile("nodes.shp", "links.shp", first.adjacency_dictionary)


if __name__ == '__main__':
    main()
