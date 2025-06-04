# ✈️ Daily Flight Data Ingestion & Automation Pipeline

This project automates the ingestion and processing of daily flight data using AWS native services. It includes orchestration, metadata cataloging, and alerting.

## 🚀 Tech Stack
- Python
- AWS Lambda
- AWS Step Functions
- Amazon S3
- AWS Glue Crawler
- AWS Glue Catalog
- Amazon EventBridge
- Amazon SNS
- Amazon QuickSight

## 📌 Features
- Daily scheduled ingestion pipeline triggered via Step Functions
- Flight data stored in S3 and cataloged using Glue Crawler
- EventBridge rules trigger alerting workflows via SNS
- Data made available for visualization in Amazon QuickSight

## 🏗️ Architecture
1. Step Function triggers a Lambda to fetch and write flight data to S3
2. Glue Crawler updates metadata in Glue Catalog
3. EventBridge monitors pipeline status and triggers notifications
4. Quicksight uses the cataloged data for dashboarding

![Architecture](https://github.com/user-attachments/assets/32c8843a-bb64-46d3-a83b-15f88165a47e)
