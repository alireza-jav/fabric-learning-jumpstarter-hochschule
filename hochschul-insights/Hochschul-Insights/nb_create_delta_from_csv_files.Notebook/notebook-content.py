# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e375b3fb-afcd-4fad-979f-16e4fd3e7423",
# META       "default_lakehouse_name": "hochschul_insights_lh",
# META       "default_lakehouse_workspace_id": "08740f54-d8a9-4eaf-9b29-982474a26002",
# META       "known_lakehouses": [
# META         {
# META           "id": "e375b3fb-afcd-4fad-979f-16e4fd3e7423"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
import os
SNAP_DIR = "/lakehouse/default/Files/snapshot"
print(os.listdir(SNAP_DIR))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pandas as pd
pdf = pd.read_csv(f"{SNAP_DIR}/Studierende.csv", parse_dates=["Jahr"])
print(pdf.shape)       # (rows, columns)
print(pdf.dtypes)      # the type pandas gave each column
display(pdf.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sdf = spark.createDataFrame(pdf)   # no schema: Spark guesses the types
sdf.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.table("Genesis.studierende")   # the finished table
df.printSchema()                          # compare with the guessed types above
print(df.count())
display(df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    raise FileNotFoundError("/lakehouse/default/Files/snapshot/Studierende.csv")
except Exception as e:
    print(f"FAIL Studierende: {e}")
print("Snapshot load done.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import os
import pandas as pd

SNAP_DIR = "/lakehouse/default/Files/snapshot"
tables = [f[:-4] for f in sorted(os.listdir(SNAP_DIR)) if f.endswith(".csv")]

rows = []
for t in tables:
    tbl = f"Genesis.{t.lower()}"
    csv_rows   = len(pd.read_csv(f"{SNAP_DIR}/{t}.csv"))                 # rows in the source file
    table_rows = spark.table(tbl).count()                                 # rows in the table
    last_write = spark.sql(f"DESCRIBE HISTORY {tbl} LIMIT 1").collect()[0]["timestamp"]  # when it was last written
    rows.append({"table": t, "csv_rows": csv_rows, "table_rows": table_rows,
                 "match": csv_rows == table_rows, "last_written": last_write})

display(pd.DataFrame(rows))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
