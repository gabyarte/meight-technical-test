# Meight's Technical Test Solution

## Task Description: Forecasting Market Prices by Region

**Scenario**

Meight tracks market prices for road freight services (e.g., full-truck-load, less-than-truck-load, refrigerated, flatbeds, ...) in different european regions. The company wants to develop a system to compute prices analytics based on historical data.


**Objective**

Design and build a data pipeline that processes and transforms historical road freight market prices. Then, on user demand, outputs road freight price analytics on filtered by one or more of the following dimensions: pickup_region, delivery_region, season, service_type. We also want to know based in how many records our analysis are based.

**Challenge Steps**
1. Data Ingestion: Data Source: You will need to scrape market price data for various road freight services (+1 million records per day). Each record will have: service_type pickup_coordinate delivery_coordinate date price Ingest: Set up an ETL process that ingests this dataset from an API (mock the api call).
2. Data Transformation and Cleaning: Data Quality: Perform data cleaning steps such as: Handle missing data by inputing or removing records. Detect and remove outliers using methods like z-scores or IQR (Interquartile Range).
3. Data Storage: Storage Options: Store the cleaned and transformed data in a suitable place. Keep in mind performance when selecting the storage solution.
4. Data Pipeline Scheduling and Automation: Automation: Use a scheduling tool like Apache Airflow, AWS Lambda, or Google Cloud Functions to automate the ETL pipeline, ensuring the data is processed and updated regularly (e.g., daily or weekly).
5. Analytics Integration: Analytics output should return percentile 25, percentile 75 and average of the selected user input data
6. Data Visualization and Reporting (Bonus): Historical price trends by region and service. Forecasted prices and their comparison with actual prices. Moving averages, price fluctuations, and market trends.
7. Infrastructure (Bonus): Build your solution with infrastructure as code when aplicable
