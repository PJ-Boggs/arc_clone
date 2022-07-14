import arcpy
import os

# Set project fgdb as workspace
arcpy.env.workspace = "C:/Users/pjbog/arc_clone/DATA/project.gdb"

# Where you want the new File Geo-database (fgdb) to go
working_path = r"C:/Users/pjbog/arc_clone/DATA"

# Create a new fgdb to store outputs
arcpy.CreateFileGDB_management(f"{working_path}", f"ReleaseSheet.gdb")

storage_fgdb = os.path.join(f"{working_path}", f"ReleaseSheet.gdb")

# Export Demand_Points file as a foundation to work from
arcpy.FeatureClassToFeatureClass_conversion("Demand_Points", storage_fgdb, "Release_Sheet")
