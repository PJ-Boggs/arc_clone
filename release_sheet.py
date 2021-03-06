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
                           "drop_length DOUBLE 'Drop Length' # # #;"
                           "x DOUBLE # # # #;"
                           "y DOUBLE # # # #;"
                           "latitude DOUBLE # # # #;"
                           "longitude DOUBLE # # # #;"
                           "starting_structure TEXT 'OR Object ID' 255 # #;"
                           "structure_owner TEXT 'Structure Owner' 255 # #;"
                           "pianoi TEXT PIANOI 255 # #;"
                           "build_status TEXT 'Build Status' 255 # #;"
                           "loc_desc TEXT 'Loc Description' 255 # #;"
                           "loc_type TEXT 'Loc Type' 255 # #;"
                           "route_id TEXT 'Route ID' 255 # #;"
                           "builddate DATE 'Build Date' 255 # #;"
                           "releasedate DATE 'Release to Sales Date' # # #;"
                           "zone TEXT Zone 255 # #;"
                           "test_results TEXT 'Test Results' 255 # #")

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
                                                               ' + " " + !street! + ", " + !town! + ", " + !postcode!',
                                "PYTHON3", '',
                                "TEXT", "NO_ENFORCE_DOMAINS")
# Cleanse Address Information
arcpy.management.CalculateField("Release_Sheet", "summary_ad", "Replace($feature.summary_ad, '0 ', '')",
                                "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField("Release_Sheet", "summary_ad", "Replace($feature.summary_ad, '       ,  ,  ',"
                                                               " 'New Address')", "ARCADE", '', "TEXT",
                                "NO_ENFORCE_DOMAINS")
arcpy.management.CalculateField("Release_Sheet", "summary_ad", "Replace($feature.summary_ad, '  ',"
                                                               "'')", "ARCADE", '', "TEXT", "NO_ENFORCE_DOMAINS")

# Calculate Country - Default as NI, change when required
arcpy.management.CalculateField("Release_Sheet", "country", "'NI'", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Calculate Build_Status - Default as Planned (1), change when required
arcpy.management.CalculateField("Release_Sheet", "build_status", "'1'", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
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

# Calc PIANOI
# Spatial Join (SJ) PIANOI Boundary with ReleaseSheet
target_features3 = "Release_Sheet"
join_features3 = "Noi_Boundaries"
out_feature_class3 = "Noi_SJ"

arcpy.SpatialJoin_analysis(target_features3, join_features3, out_feature_class3)
# Calc Pianoi from piano
arcpy.management.CalculateField("Noi_SJ", "pianoi", "!piano!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Remove Unnecessary Fields
arcpy.management.DeleteField("Noi_SJ", "Join_Count;TARGET_FID;id;noi;noi_no;piano;GlobalID_1;Shape__Are;Shape__Len",
                             "DELETE_FIELDS")
# Overwrite Release_Sheet with Noi_SJ
arcpy.FeatureClassToFeatureClass_conversion("Noi_SJ",
                                            "C:/Users/pjbog/arc_clone/DATA/project.gdb",
                                            "Release_Sheet")
# Delete working Noi_SJ Feature Class
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Noi_SJ")

# Calc LOC
# Spatial Join (SJ) Loc Boundary with ReleaseSheet
target_features4 = "Release_Sheet"
join_features4 = "Loc_Boundaries"
out_feature_class4 = "Loc_SJ"

arcpy.SpatialJoin_analysis(target_features4, join_features4, out_feature_class4)
# Calc Loc_desc from Loc_desc
arcpy.management.CalculateField("Loc_SJ", "loc_desc", "!loc_desc_1!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Calc Loc_type from Loc_type
arcpy.management.CalculateField("Loc_SJ", "loc_type", "!loc_type_1!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Remove Unnecessary Fields
arcpy.management.DeleteField("Loc_SJ", "Join_Count;TARGET_FID;id;level_;name;w_homes;g_homes;t_homes;loc_type_1;"
                                       "loc_desc_1;GlobalID_1;Shape__Are;Shape__Len", "DELETE_FIELDS")
# Overwrite Release_Sheet with Loc_SJ
arcpy.FeatureClassToFeatureClass_conversion("Loc_SJ",
                                            "C:/Users/pjbog/arc_clone/DATA/project.gdb",
                                            "Release_Sheet")
# Delete working Loc_SJ Feature Class
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Loc_SJ")

# Calc Drop wires and Structure info
# Merge Chambers and Poles
arcpy.management.Merge("Chambers;Poles", r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Structures",
                       'Structure "Structure" true true false 254 Text 0 0,First,#,Chambers,Structure,0,254,'
                       'Poles,structure_,0,20;owner "owner" true true false 254 Text 0 0,First,#,Chambers,owner,0,254,'
                       'Poles,owner,0,254', "NO_SOURCE_INFO")
# Spatial Join (SJ) Structures to Drop Wires
target_features5 = "Drop_Wires"
join_features5 = "Structures"
out_feature_class5 = "Dw_Str_SJ"

arcpy.SpatialJoin_analysis(target_features5, join_features5, out_feature_class5)

# Add Shape_Length Field to Dw_Str_SJ
arcpy.AddField_management("Dw_Str_SJ", "Drop_Length", "DOUBLE")
# Calc Shape Length
arcpy.management.CalculateGeometryAttributes("Dw_Str_SJ", "Drop_Length LENGTH", "METERS", '',
                                             'PROJCS["TM75_Irish_Grid",GEOGCS["GCS_TM75",'
                                             'DATUM["D_TM75",SPHEROID["Airy_Modified",6377340.189,299.3249646]],'
                                             'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],'
                                             'PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",200000.0],'
                                             'PARAMETER["False_Northing",250000.0],PARAMETER["Central_Meridian",-8.0],'
                                             'PARAMETER["Scale_Factor",1.000035],PARAMETER["Latitude_Of_Origin",53.5],'
                                             'UNIT["Meter",1.0]]', "SAME_AS_INPUT")
# Spatial Join (SJ) Dw_Str_SJ to Release Sheet
target_features6 = "Release_Sheet"
join_features6 = "Dw_Str_SJ"
out_feature_class6 = "Dw_Str_SJ2"

arcpy.SpatialJoin_analysis(target_features6, join_features6, out_feature_class6)
# Calc Feed Type from placement
arcpy.management.CalculateField("Dw_Str_SJ2", "feed_type", "!placement!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Calc Drop Length from Shape Length
arcpy.management.CalculateField("Dw_Str_SJ2", "drop_length", "!Drop_Length_1!", "PYTHON3", '', "TEXT",
                                "NO_ENFORCE_DOMAINS")
# Calc OR Object ID from Structure
arcpy.management.CalculateField("Dw_Str_SJ2", "starting_structure", "!Structure!", "PYTHON3", '', "TEXT",
                                "NO_ENFORCE_DOMAINS")
# Calc Structure Owner from owner
arcpy.management.CalculateField("Dw_Str_SJ2", "structure_owner", "!owner!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

arcpy.management.DeleteField("Dw_Str_SJ2", "Join_Count;TARGET_FID;Join_Count_1;TARGET_FID_1;status;owner;"
                                           "cab_size;cab_type;placement;ref;prem_id;loc;GlobalID_1;Milestone;use_;"
                                           "Structure;owner_1;Drop_Length_1", "DELETE_FIELDS")
# Overwrite Release_Sheet with Noi_SJ
arcpy.FeatureClassToFeatureClass_conversion("Dw_Str_SJ2",
                                            "C:/Users/pjbog/arc_clone/DATA/project.gdb",
                                            "Release_Sheet")
# Delete working Feature Classes
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Structures")
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Dw_Str_SJ")
arcpy.Delete_management(r"C:/Users/pjbog/arc_clone/DATA/project.gdb/Dw_Str_SJ2")

# Assign Domains to Fields
arcpy.AssignDomainToField_management("Release_Sheet",
                                     "premise_ty", "premise_typ")
arcpy.AssignDomainToField_management("Release_Sheet",
                                     "feed_type", "feed_typ")
arcpy.AssignDomainToField_management("Release_Sheet",
                                     "build_status", "build_status")
arcpy.AssignDomainToField_management("Release_Sheet",
                                     "structure_owner", "owner")

# QC for Nulls - Function
""" QC Function checks for null values, approving features without.

Input parameters are the fields of the Release Sheet which are to be evaluated.
The function outputs 'approved' values within the test_results field of the Release Sheet.

"""
arcpy.management.CalculateField("Release_Sheet", "test_results", "QC (!PN!,!SN!,!feed_type!,!pianoi!)", "PYTHON3",
                                """def QC (PN,SN,feed_type,pianoi):
    BlockList = [PN, SN, feed_type, pianoi]
    mylist = []
    for i in BlockList:
        if i == None:
            myList.append(i)
    return 'APPROVED'
    """, "TEXT", "NO_ENFORCE_DOMAINS")

# Export Feature Class Attribute Table to Excel (Stored in arc_clone Folder)
arcpy.conversion.TableToExcel("Release_Sheet", r"C:\Users\pjbog\arc_clone\DATA\ReleaseSheet.xls",
                              "ALIAS", "DESCRIPTION")
