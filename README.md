# Daily-Flight-Data-Analysis-Automated-Pipeline

Steps in the Pipeline

Step 1: Fetching and Storing Raw Flight Data

Source: Flight data is fetched daily from aviationstack.com API.

Process:
->A Lambda function triggers the API to fetch the latest flight data.
->The raw flight data is stored in an S3 bucket, partitioned by the current date.

Output: Raw data is available in S3 for further processing.


Step 2: Data Transformation and Processing
Source: The raw flight data stored in S3.

Process:
->Another Lambda function retrieves the raw data from the S3 bucket.
->Data is transformed to align with the requirements of the target dashboard insights.
->The processed data is stored in a separate S3 bucket named "processed bucket," partitioned by the current date.

Output: Transformed data is ready for metadata creation and querying.


Step 3: Metadata Management
Tool: AWS Glue Crawler

Process:
->A Glue Crawler scans the processed flight data in the S3 "processed bucket."
->Metadata is created and maintained in the AWS Glue Data Catalog.

Output: A structured schema of the processed flight data for querying.


Step 4: Querying and Visualization
Tools: AWS Athena and Amazon QuickSight

Process:
->Glue Catalog is connected to AWS Athena to enable SQL-like querying of the data.
->Athena is further connected to Amazon QuickSight to create interactive dashboards.
->Dashboards are scheduled to refresh daily to provide up-to-date flight insights.

Output: Visualizations and insights into daily flight data.
