from pyspark.sql import SparkSession

def write_to_parquet():
    spark = SparkSession.builder.appName("JSON_to_Parquet").getOrCreate()
    df = spark.read.json("sample_data_json.json")
    df.write.parquet("sample_data.parquet", mode="overwrite")

def read_from_parq():
    spark = SparkSession.builder.appName("Read_Parquet").getOrCreate()
    df = spark.read.parquet("sample_data.parquet")
    rows = df.collect()  # Returns a list of Row objects
    for row in rows:
        breakpoint()
        print(row)  # Access data like a dictionary