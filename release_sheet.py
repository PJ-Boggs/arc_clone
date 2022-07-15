import arcpy

# Allow outputs to be overwritten
arcpy.env.overwriteOutput = True

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

# Calc Geometry Fields
arcpy.management.CalculateGeometryAttributes("Release_Sheet", "x POINT_X;y POINT_Y", '', '',
                                             'PROJCS["TM75_Irish_Grid",GEOGCS["GCS_TM75",DATUM'
                                             '["D_TM75",SPHEROID["Airy_Modified",6377340.189,299.3249646]],'
                                             'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],'
                                             'PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",200000.0],'
                                             'PARAMETER["False_Northing",250000.0],PARAMETER["Central_Meridian",-8.0],P'
                                             'ARAMETER["Scale_Factor",1.000035],PARAMETER["Latitude_Of_Origin",53.5],'
                                             'UNIT["Meter",1.0]]', "SAME_AS_INPUT")

arcpy.management.CalculateGeometryAttributes("Release_Sheet", "latitude POINT_Y;longitude POINT_X", '', '', None, "DD")

# Calc Summary Address Field
arcpy.management.CalculateField("Release_Sheet", "summary_ad", '!sub_buildi! + " " + !building_n! + " " + !building_1!'
                                ' + " " + !street! + ", " + !town! + ", " + !postcode!', "PYTHON3", '',
                                "TEXT", "NO_ENFORCE_DOMAINS")
# Cleanse Address Information
arcpy.management.CalculateField("Release_Sheet", "summary_ad", "Replace($feature.summary_ad, '0 ', '')",
                                "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField("Release_Sheet", "summary_ad", "Replace($feature.summary_ad, '       ,  ,  ',"
                                " 'New Address')", "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField("Release_Sheet", "summary_ad", "Replace($feature.summary_ad, '  ',"
                                "'')", "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")

# Calculate Country - Default as NI, change when required
arcpy.management.CalculateField("Release_Sheet", "country", "'NI'", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Remove Unnecessary Fields
arcpy.management.DeleteField("Release_Sheet", "sub_buildi;building_n;building_1;street;town;postcode;"
                                              "CreationDa;Creator;EditDate;Editor", "DELETE_FIELDS")

# Calc Pop ID
# Spatial Join (SJ) Pop Boundary with ReleaseSheet
target_features = "Release_Sheet"
join_features = "Pop_Boundary"
out_feature_class = "Pop_SJ"

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class)
# Calc Pop_ID from Name
arcpy.management.CalculateField("Pop_SJ", "pop_id", "!name!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Remove Unnecessary Fields
arcpy.management.DeleteField("Pop_SJ", "Join_Count;TARGET_FID;id;level_;name;w_homes;g_homes;t_homes;loc_type_1;"
                                       "loc_desc_1;GlobalID_1;Shape__Are;Shape__Len", "DELETE_FIELDS")
# Overwrite Release_Sheet with Pop_SJ
arcpy.FeatureClassToFeatureClass_conversion("Pop_SJ", 
                                            "C:/Users/pjbog/arc_clone/DATA/project.gdb", 
                                            "Release_Sheet")
# Delete working Pop_SJ Feature Class
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Pop_SJ")

# Calc Primary Node
# Spatial Join (SJ) JN Boundary with ReleaseSheet
target_features1 = "Release_Sheet"
join_features1 = "Jn_Boundaries"
out_feature_class1 = "Jn_SJ"

arcpy.SpatialJoin_analysis(target_features1, join_features1, out_feature_class1)
# Calc PN_ID from Name
arcpy.management.CalculateField("Jn_SJ", "PN", "!name!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Remove Unnecessary Fields
arcpy.management.DeleteField("Jn_SJ", "Join_Count;TARGET_FID;id;level_;name;w_homes;g_homes;t_homes;loc_type_1;"
                                       "loc_desc_1;GlobalID_1;Shape__Are;Shape__Len", "DELETE_FIELDS")
# Overwrite Release_Sheet with Jn_SJ
arcpy.FeatureClassToFeatureClass_conversion("Jn_SJ",
                                            "C:/Users/pjbog/arc_clone/DATA/project.gdb",
                                            "Release_Sheet")
# Delete working Jn_SJ Feature Class
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Jn_SJ")

# Calc Secondary Node
# Spatial Join (SJ) MPT Boundary with ReleaseSheet
target_features2 = "Release_Sheet"
join_features2 = "Mpt_Boundaries"
out_feature_class2 = "Mpt_SJ"

arcpy.SpatialJoin_analysis(target_features2, join_features2, out_feature_class2)
# Calc SN_ID from Name
arcpy.management.CalculateField("Mpt_SJ", "SN", "!name!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Remove Unnecessary Fields
arcpy.management.DeleteField("Mpt_SJ", "Join_Count;TARGET_FID;id;level_;name;w_homes;g_homes;t_homes;loc_type_1;"
                                       "loc_desc_1;GlobalID_1;Shape__Are;Shape__Len", "DELETE_FIELDS")
# Overwrite Release_Sheet with Mpt_SJ
arcpy.FeatureClassToFeatureClass_conversion("Mpt_SJ",
                                            "C:/Users/pjbog/arc_clone/DATA/project.gdb",
                                            "Release_Sheet")
# Delete working Mpt_SJ Feature Class
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Mpt_SJ")

# NOTE TO SELF - Add codded value domains at end

# NOTE TO SELF - Create Function for removing Unnecessary fields
