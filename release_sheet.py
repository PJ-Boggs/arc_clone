import arcpy
import os

# Where you want the File Geo-database (fgdb) to go
working_path = r"C:/Users/pjbog/arc_clone/DATA"

# Create a new fgdb to both work from and store data
arcpy.CreateFileGDB_management(f"{working_path}", f"ReleaseSheet.gdb")

# Set new fgdb as workspace
arcpy.env.workspace = "C:/Users/pjbog/project/DATA/ReleaseSheet.gdb"

fgdb = os.path.join(f"{working_path}", f"ReleaseSheet.gdb")

# Export Demand_Points file as a copy to work from
