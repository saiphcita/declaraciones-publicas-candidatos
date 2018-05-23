# impor spark, set spark context
from pyspark import SparkContext, SparkConf
from pyspark.sql.context import SQLContext
import sys
import os

if len(sys.argv) == 1:
    sys.stderr.write("Must enter input file to convert")
    sys.exit()
input_file = sys.argv[1]
if len(sys.argv) >= 3:
    output_path = os.path.join(
        sys.argv[2], os.path.basename(input_file).split(".", 1)[0])
else:
    output_path = os.path.join("to_json_" + input_file.split(".", 1)[0])

conf = SparkConf().setAppName(
    "parquet_to_json_%{f}".format(f=input_file.split(".", 1)[0]))
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

# set sql context
parquetFile = sqlContext.read.parquet(input_file)
parquetFile.write.json(output_path)