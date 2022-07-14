import arcpy

# Set project fgdb as workspace
workspace = "C:/Users/pjbog/arc_clone/DATA/project.gdb"
arcpy.env.workspace = workspace

# Export Demand_Points file as a foundation to work from
arcpy.FeatureClassToFeatureClass_conversion("Demand_Points", workspace, "Release_Sheet")

# Add Required ReleaseSheet Fields
arcpy.management.AddFields("Release_Sheet",
                           "country TEXT Country 255 # #;"
                           "summary_ad TEXT 'Summary Address' 255 # #;"
                           "pop_id TEXT POP_ID 255 # #;"
                           "PN TEXT 'Primary Node' 255 # #;"
                           "SN TEXT 'Secondary Node' 255 # #;"
                           "feed_type TEXT 'Feed Type' 255 # #;"
                           "drop_length LONG 'Drop Length' # # #;"
                           "x DOUBLE # # # #;"
                           "y DOUBLE # # # #;"
                           "latitude DOUBLE # # # #;"
                           "longitude DOUBLE # # # #;"
                           "starting_structure TEXT 'OR Object ID' 255 # #;"
                           "route_id TEXT 'Route ID' 255 # #;"
                           "structure_owner TEXT 'Structure Owner' 255 # #;"
                           "builddate DATE 'Build Date' 255 # #;"
                           "releasedate DATE 'Release to Sales Date' # # #;"
                           "test_results TEXT 'Test Results' 255 # #;"
                           "zone TEXT Zone 255 # #;"
                           "pianoi TEXT PIANOI 255 # #;"
                           "build_status TEXT 'Build Status' 255 # #;"
                           "loc_desc TEXT 'Loc Description' 255 # #;"
                           "loc_type TEXT 'Loc Type' 255 # #")

arcpy.management.CalculateGeometryAttributes("Release_Sheet", "x POINT_X;y POINT_Y", '', '',
                                             'PROJCS["TM75_Irish_Grid",GEOGCS["GCS_TM75",DATUM'
                                             '["D_TM75",SPHEROID["Airy_Modified",6377340.189,299.3249646]],'
                                             'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],'
                                             'PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",200000.0],'
                                             'PARAMETER["False_Northing",250000.0],PARAMETER["Central_Meridian",-8.0],P'
                                             'ARAMETER["Scale_Factor",1.000035],PARAMETER["Latitude_Of_Origin",53.5],'
                                             'UNIT["Meter",1.0]]', "SAME_AS_INPUT")

arcpy.management.CalculateGeometryAttributes("Release_Sheet", "latitude POINT_Y;longitude POINT_X", '', '', None, "DD")