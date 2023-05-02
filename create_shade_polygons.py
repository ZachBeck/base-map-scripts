import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension('spatial')


#   create_shade_polygons(work space, input raster, reclass dictionary, resolution for out name (30Meter), minimum poly size to delete (1000)
def create_shade_polygons(work_space, in_raster, remap_intervals, raster_resolution, min_poly_area):

    with arcpy.EnvManager(workspace=work_space):
        arcpy.env.overwriteOutput = True

        out_fc_list = [] 

        for interval in remap_intervals:

            out_raster = f'class{interval}_{raster_resolution}'
            out_polygons = f'ShadePolygons_{raster_resolution}_class{interval}'

            new_range = RemapRange(remap_intervals[interval])

            outRaster = Reclassify(in_raster, 'Value', new_range)
            outRaster.save(out_raster)
            print(out_raster + ' Created')

            arcpy.RasterToPolygon_conversion(out_raster, out_polygons, 'SIMPLIFY')
            out_fc_list.append(out_polygons)
            print(f'{out_polygons} Created')
            
            sql_254 = f'"gridcode" = 254'
            out_polys_254FL = arcpy.MakeFeatureLayer_management(out_polygons, 'out_polys_254FL', sql_254)

            arcpy.DeleteFeatures_management(out_polys_254FL)
            arcpy.Delete_management(out_polys_254FL)
            print('Deleted gridcode 254')

            sql_min_poly = f'"Shape_Area" < {min_poly_area}'
            polygons_to_remove_FL = arcpy.MakeFeatureLayer_management(out_polygons, 'polygons_to_remove_FL', sql_min_poly)

            arcpy.DeleteFeatures_management(polygons_to_remove_FL)
            arcpy.Delete_management(polygons_to_remove_FL)
            print(f'Deleted polygons less than {min_poly_area} sq meters')

            #Delete reclassified rasters
            if not arcpy.TestSchemaLock(out_raster):
                print(f'{out_raster} is LOCKED')
                continue
            else:
                arcpy.Delete_management(out_raster)
                print(f'Deleted {out_raster} raster')

        #Append shade polygons, eliminate small donut holes, and clean up your mess
        out_fc_list.sort()
        arcpy.Append_management(out_fc_list[1:], out_fc_list[0])
        arcpy.EliminatePolygonPart_management(out_fc_list[0], f'ShadePolygons_{raster_resolution}', 'AREA', min_poly_area)
        for fc in out_fc_list:
            if arcpy.Exists(fc):
                arcpy.Delete_management(fc)


reclassify_90 = {80:[[0, 80, 80], [80.1, 254, 254]],
                 130:[[0, 130, 130], [130.1, 254, 254]],
                 165:[[0, 165, 165], [165.1, 254, 254]],
                 175:[[0, 175, 175], [175.1, 254, 254]]}

reclassify_30 = {45:[[0, 45, 45], [45.1, 254, 254]],
                 100:[[0, 100, 100], [100.1, 254, 254]],
                 160:[[0, 160, 160], [160.1, 254, 254]],
                 175:[[0, 175, 175], [175.1, 254, 254]]}

reclassify_10 = {40:[[0, 40, 40], [40.1, 254, 254]],
                 100:[[0, 100, 100], [100.1, 254, 254]],
                 140:[[0, 140, 140], [140.1, 254, 254]],
                 170:[[0, 170, 170], [170.1, 254, 254]]}

fgdb = r'C:\Basemaps\testing\BasemapTesting.gdb'
in_hillshade90 = r'C:\ZBECK\NED\DEM90\hillshd90'
in_hillshade30 = r'C:\ZBECK\Elevation\UT_Statewide_30m_gdalHill_z3.tif'
in_hillshade10 = r'C:\ZBECK\Elevation\Hillshade_10Meter_Utah_focal3z3.tif'


create_shade_polygons(fgdb, in_hillshade30, reclassify_30, '30Meter', 500)


