# Let's import the libraries we need

from pyspark.sql import *
import pyspark.sql.functions as F
from pyspark import SparkContext
import pickle
import os
import json
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.databricks:spark-xml_2.11:0.7.0 pyspark-shell'

spark = SparkSession \
    .builder \
    .master("yarn") \
    .getOrCreate()


# create the context
sc = spark.sparkContext


r = spark.read.format("xml") \
    .option("rowTag","release") \
    .load("/datasets/discogs/discogs_20190101_releases.xml")


df_style = r.select("_id","styles", \
               F.explode(r.genres.genre).alias("genre")) \
               .filter(F.col('genre') == 'Electronic') \
               .select("_id",F.explode(r.styles.style).alias('style')) \
               .filter(F.col('style') == 'House')
             

df_style.write.csv('style_house.csv')