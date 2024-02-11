from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Step 1: Create a Spark session
spark = SparkSession.builder.appName("BMIAnalysis").getOrCreate()

# Step 2: Create a test dataset (replace this with your actual data)
data = [("John", "Doe", 72, 180),
        ("Jane", "Smith", 65, 140),
        ("Bob", "Johnson", 68, 200),
        # Add more data as needed
       ]

# Define the schema for the dataset
schema = ["FirstName", "LastName", "Height", "Weight"]

# Create a DataFrame from the test data
df = spark.createDataFrame(data, schema=schema)

# Step 3: Calculate BMI and filter out over-weighted students
df = df.withColumn("BMI", (col("Weight") * 703) / (col("Height") ** 2))
over_weighted_students = df.filter(col("BMI") > 24.9)

# Select only required columns for the output
result_df = over_weighted_students.select("FirstName", "LastName", "BMI")

# Step 4: Save the results to an output file (replace 'output_path' with your desired path)
result_df.write.mode("overwrite").option("header", "true").csv("Adv Database 531/Practise/output")

# Stop the Spark session
spark.stop()
