# Datasphere Sample Objects

## Description
This sample demonstrates how to create the objects in Datasphere using the geo location data that was populated by SAP DQM micorservices and to create a GeoMap story in SAP Analytics Cloud.

## SAP Datasphere

In this example, we will use the sample data provided in
- https://github.com/SAP-samples/datasphere-content/tree/main/Sample_Bikes_Sales_content

For simplicity, we will use only the following datasets
- https://github.com/SAP-samples/datasphere-content/blob/main/Sample_Bikes_Sales_content/CSV/Addresses.csv
- https://github.com/SAP-samples/datasphere-content/blob/main/Sample_Bikes_Sales_content/CSV/BusinessPartners.csv
- https://github.com/SAP-samples/datasphere-content/blob/main/Sample_Bikes_Sales_content/CSV/SalesOrders.csv

### Import the sample data

Go to Data Builder and import and deploy the datasets from above.

| CSV File Name | Table Name | Sample JSON |
| --------- | ----------- | ----------- |
| Addresses.csv | Addresses | Addresses.json |
| BusinessPartners.csv | BusinessPartners | BusinessPartners.json |
| SalesOrders.csv | SalesOrders | SalesOrders.json |

![Alt text](resources/dsp-import-csv.png?raw=true "Import CSV File")

### Create a View to be consumed by SAP DQM microservices

Create a View on top of the Addresses table

- In the New Graphical View, add the Addresses table from Sources
- Add a Projection (Rename/Exclude Columns) after the source table
- Map the address columns to the DQM service fields and exclude all non-mapped columns
- Expose for consumption
- Save and Deploy

| Source Fields | View Fields |
| --------- | ----------- |
| ADDRESSID | ID |
| CITY | LOCALITY |
| POSTALCODE | POSTCODE |
| STREET | MIXED |
| COUNTRY | COUNTRY |

| Source Table | View Name | Sample JSON |
| --------- | ----------- | ----------- |
| Addresses | Addresses_View | Addresses_View.json |

![Alt text](resources/dsp-input-view.png?raw=true "Create a View from Local Table data in Data Builder")

### Run the Python script to get the Geo Location data from SAP DQM microservices

Run the Python script as described in the main README
- https://github.wdf.sap.corp/dqmm/dqmm-dsp-python-sample/blob/main/README.md
- python3 dqmm-dsp.py Addresses_View

| Input Table | Output Table | Sample JSON |
| --------- | ----------- | ----------- |
| Addresses_View | Addresses_View_GEO | Addresses_View_GEO.json |

The output table is created in your Open SQL Schema

![Alt text](resources/dsp-output-table.png?raw=true "Output table created by the Python script in Database Explore")

### Create a Dimension with the Location data

Create a Dimension View with the Location data and select which column to be the Key field to be used in GeoMap.

You have two options
1. Use the Geo Location column from SAP DQM microservices directly
2. Use the Latitude and Longitude columns from SAP DQM microservices to create a Geo-Coordinates Column in Datasphere

Either will work but the Geo Location column must be based on the Mercator projection (3857) to work with SAP Analytics Cloud GeoMap.

For this sample reference, both options are added in the View.

- In the New Graphical View, add the Addresses_View_GEO table
- Change the Semantic Usage to Dimension
- Add a Filter after Addresses_View_GEO table to exclude the NULL value using the Expression: *LATLONG IS NOT NULL*
- Add the BusinessPartners table
- Add a Projection (Rename/Exclude Columns) after the BusinessPartners table and exclude the columns except for COMPANYNAME column
- Join the two tables with the key mapping from ID to ADDRESSID columns
- Optionally add a Calculated Column and create a Geo-Coordinates Column using Latitude and Longitude columns. Keep the Spatial Reference Identifier to 4326.
- Select COMPANYNAME column in the final View and set as Key
- Save and Deploy

| Source Table | Join Table | Sample JSON |
| --------- | ----------- | ----------- |
| Addresses_View_GEO | BusinessPartners | Addresses_Location.json |

![Alt text](resources/dsp-dimension-join.png?raw=true "Join two tables")

![Alt text](resources/dsp-dimension-geo-column.png?raw=true "Create a Geo-Coordinates Column")

![Alt text](resources/dsp-dimension-key.png?raw=true "Set a Column as Key")

### Create a Fact with the Location Dimension

Create a Fact View and with an Association to the Location Dimension

- In the New Graphical View, add the SalesOrders table and BusinessPartners table to join them
- Map PARTNERID column to PARTNERID column to join the tables 
- Change the Semantic Usage to Fact
- In Attributes, change GROSSAMOUNT and NETAMOUNT to Measure
- Add an Association and select the Addresses_Location view
- Keep the Key map from COMPANYNAME to COMPANYNAME
- Save and Deploy

| Source Table | View Name | Sample JSON |
| --------- | ----------- | ----------- |
| SalesOrders, BusinessPartners | SalesOrders_View | SalesOrders_View.json |

![Alt text](resources/dsp-fact-join.png?raw=true "Join two tables")

![Alt text](resources/dsp-fact-measure.png?raw=true "Set Attribute as Measure")

![Alt text](resources/dsp-fact-association.png?raw=true "Add an Association to Location Dimension")

### Create an Analytic Model

Create an Analytic Model on top of the Fact View

| Source View | Analytic Model | Sample JSON |
| --------- | ----------- | ----------- |
| SalesOrders_View | SalesOrders_Model | SalesOrders_Model.json |


![Alt text](resources/dsp-analytic-model.png?raw=true "Create an Analytic Model")


## SAP Analytics Cloud

Navigate to SAP Analytics Cloud

### Create a Story

Go to Story and create a new Story with GeoMap.

- Create a new Responsive Story
- Add a GeoMap widget to a new Story
- Add a Layer
- Select the Analytic Model from Datasphere (the Select Model icon at the top of Builder)
- Select Location Dimension to the location column in the Analytic Model
- Optionally style the GeoMap with your preference such as Base Layer Style
- Save the story

![Alt text](resources/sac-story-geomap.png?raw=true "Create a Story with GeoMap")

![Alt text](resources/sac-story-style.png?raw=true "Streets Layer Style in GeoMap")

## Licensing

Copyright (c) 2024 SAP SE or an SAP affiliate company and dqmm-dsp-python-sample contributors. Please see our [LICENSE](/LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available via the REUSE tool (link to https://api.reuse.software/info/github.com/SAP-samples/cloud-dqm-sample-payloads).

