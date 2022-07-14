import arcpy
import os

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
