# Datasphere Sample Data Quality Dashboard

## Description
This sample demonstrates an example of creating a Data Quality dashboard using the data produced by SAP Data Quality Management micorservices. The statistical data from the address validation and geocoding process are used to create objects in SAP Datasphere and build a story in SAP Analytics Cloud.

## SAP Datasphere

In this example, we will use the output data that was previously processed from SAP DQM microservices. You can find the [sample python scripts](https://github.com/SAP-samples/cloud-dqm-sample-payloads/blob/main/datasphere-dashboard/dqmm-dsp-dashboard.py) to call the service in [datasphere-python](https://github.com/SAP-samples/cloud-dqm-sample-payloads/tree/main/datasphere-python).

### Import the sample data

Go to Data Builder and import and deploy the datasets from above

| CSV File Name | Table Name | Sample JSON |
| --------- | ----------- | ----------- |
| DQMSampleData.csv | DQMSampleData | DQMSampleData.json |

![Alt text](resources/dsp-import-csv.png?raw=true "Import CSV File")

### Update the data types

Open the DQMSampleData table that was deployed and update the data types as following

| Technical Name | Data Type |
| --------- | ----------- |
| ID | Integer64 |
| STD_ADDR_COUNTRY_3CHAR | String(3) |
| STD_ADDR_COUNTRY_NAME | String(100) |
| ADDR_ASMT_INFO | String(1) |
| ADDR_ASMT_LEVEL | String(2) |
| ADDR_INFO_CODE | String(4) |
| ADDR_INFO_CODE_MSG | String(1024) |
| GEO_ASMT_LEVEL | String(4) |

![Alt text](resources/dsp-local-table.png?raw=true "Update Data Type")

### Create a View to prepare columns used for visualization

Create a SQL View on top of the DQMSampleData table

- In the New SQL View, add a SQL statement to query from the DQMSampleData table
- See the sample SQL statement in the DQMSampleData_SQL artifact below
- Optionally validate the SQL statement
- Save and Deploy

| Source Table | View Name | Sample JSON |
| --------- | ----------- | ----------- |
| DQMSampleData | DQMSampleData_SQL | DQMSampleData_SQL.json |

![Alt text](resources/dsp-sql-view.png?raw=true "Create a SQL View from Local Table data")

### Create a Dimension with the Address Assignment Level data

Create a Dimension View with the Address Assignment Level data and create a hierarchy

- In the New Graphical View, add the DQMSampleData_SQL table
- Change the Semantic Usage to Dimension
- Add a Projection (Rename/Exclude Columns) after the DQMSampleData_SQL table and exclude all columns except for ADDR_ASMT_LEVEL column and Address_Level column (based on our SQL example)
- Select the final View and add a Level Based Hierarchy with these columns
- Edit Attributes and select ADDR_ASMT_LEVEL column and set as Key
- Save and Deploy

| Source View | View Name | Sample JSON |
| --------- | ----------- | ----------- |
| DQMSampleData_SQL | DQMSampleData_Address_Level | DQMSampleData_Address_Level.json |

![Alt text](resources/dsp-dimension-address.png?raw=true "Create an Address Level Hierarchy")

### Create a Dimension with the Geocode Assignment Level data

Create a Dimension View with the Geocode Assignment Level data and create a hierarchy

- In the New Graphical View, add the DQMSampleData_SQL table
- Change the Semantic Usage to Dimension
- Add a Projection (Rename/Exclude Columns) after the DQMSampleData_SQL table and exclude all columns except for GEO_ASMT_LEVEL column and Geocode_Level column (based on our SQL example)
- Select the final View and add a Level Based Hierarchy with these columns
- Edit Attributes and select GEO_ASMT_LEVEL column and set as Key
- Save and Deploy

| Source View | View Name | Sample JSON |
| --------- | ----------- | ----------- |
| DQMSampleData_SQL | DQMSampleData_Geocode_Level | DQMSampleData_Geocode_Level.json |

![Alt text](resources/dsp-dimension-geocode.png?raw=true "Create a Geocode Level Hierarchy")

### Create a Fact View with Association to the Dimensions

Create a Fact View and with an Association to the Dimensions

- In the New Graphical View, add the DQMSampleData_SQL view
- Change the Semantic Usage to Fact
- In Attributes, change ID to Measure and change the aggregation type to COUNT
- Add an Association and select the DQMSampleData_Address_Level view
- Keep the Key map from ADDR_ASMT_LEVEL to ADDR_ASMT_LEVEL
- Add another Association and select the DQMSampleData_Geocode_Level view
- Keep the Key map from GEO_ASMT_LEVEL to GEO_ASMT_LEVEL
- Go to Edit Association
- Change the Semantic Type of STD_ADDR_COUNTRY_NAME to Text and set it to STD_ADDR_COUNTRY_3CHAR
- Change the Semantic Type of ADDR_INFO_CODE_MSG to Text and set it to ADDR_INFO_CODE
- Save and Deploy

| Source Table | View Name | Sample JSON |
| --------- | ----------- | ----------- |
| DQMSampleData_SQL | DQMSampleData_View | DQMSampleData_View.json |

![Alt text](resources/dsp-fact-attributes.png?raw=true "Set Text and Association")

### Create an Analytic Model

Create an Analytic Model on top of the Fact View

| Source View | Analytic Model | Sample JSON |
| --------- | ----------- | ----------- |
| DQMSampleData_View | DQMSampleData_Model | DQMSampleData_Model.json |

![Alt text](resources/dsp-analytic-model.png?raw=true "Create an Analytic Model")


## SAP Analytics Cloud

Navigate to SAP Analytics Cloud

### Create a Story

Go to Story and create a new Story

- Create a new Responsive Story (optionally open one of the pre-installed templates to get started)
- Select the Analytic Model from Datasphere (the Select Model icon at the top of Builder)
- Use a pie/donut/bar graph for preferred visualization (as our example below)
- Save the story

| Title | Widget | Dimention | Display Options |
| --------- | ----------- | ----------- | ----------- |
| Address Validation Summary | Pie Chart | Address_Validity | Sort by value |
| Address Validation Level | Pie Chart | ADDR_ASMT_LEVEL | Drill to Level 2, Sort by value |
| Geocode Validation Level | Pie Chart | GEO_ASMT_LEVEL | Drill to Level 2, Sort by value |
| Top 10 Reasons for Invalid Addresses | Bar Chart | ADDR_INFO_CODE | Rank Top 10, Sort by value |
| Top 10 Countries | Bar Chart | STD_ADDR_COUNTRY_3CHAR | Rank Top 10, Sort by value |

![Alt text](resources/sac-story-dashboard.png?raw=true "Create a Dashboard")

## Licensing

Copyright (c) 2024 SAP SE or an SAP affiliate company and dqmm-dsp-python-sample contributors. Please see our [LICENSE](LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available via the REUSE tool (link to https://api.reuse.software/info/github.com/SAP/dqmm-dsp-python-sample).

