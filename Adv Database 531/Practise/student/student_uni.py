from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Step 1: Create a Spark session
spark = SparkSession.builder.appName("MergeDatasets").getOrCreate()

# Step 2: Create test datasets (replace these with your actual data)
# First dataset: Student enrollment information
enrollment_data = [("John", "Doe", "University1", "PhD"),
                   ("Jane", "Smith", "University2", "MS"),
                   ("Bob", "Johnson", "University1", "BS"),
                   # Add more data as needed
                  ]

# Second dataset: Number of units needed to graduate
units_data = [("University1", "PhD", 60),
              ("University2", "MS", 30),
              ("University1", "BS", 120),
              # Add more data as needed
             ]

# Define schemas for the datasets
enrollment_schema = ["FirstName", "LastName", "University", "Program"]
units_schema = ["University", "Program", "NumberOfUnits"]

# Create DataFrames from the test data
enrollment_df = spark.createDataFrame(enrollment_data, schema=enrollment_schema)
units_df = spark.createDataFrame(units_data, schema=units_schema)

# Step 3: Merge the datasets using the join transformation
merged_df = enrollment_df.join(units_df, on=["University", "Program"], how="inner")

# Step 4: Select only the required columns for the output
result_df = merged_df.select("FirstName", "LastName", "University", "Program", "NumberOfUnits")

# Step 5: Save the results to an output file (replace 'output_path' with your desired path)
result_df.write.mode("overwrite").option("header", "true").csv("Adv Database 531/Practise/student/output")

# Step 6: Stop the Spark session
spark.stop()
