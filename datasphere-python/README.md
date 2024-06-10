# dqmm-dsp-python-sample

## Description
This sample demonstrates how data in Datasphere can be enriched with geo-coordinates using Data Quality Management microservices and Python.

To use this sample Python script, a view needs to be created over the data to be enriched with geo-coordinates. The view will project the columns to names that are recognized by the Data Quality Management microservice in addition to an ID column that uniquely identifies each row. Optionally, the view could also filter only those rows that are desired for the geo analysis.

The resultant geo-coordinates are written to a table in a Datasphere database user OpenSQL schema. The value from the ID column in the view is included with the results so that the geo-coordinates can be joined to the original data.

The results are written to a table whose name is the technical name of the input view appended with “_GEO”. This table is created within the database user’s schema and contains the following columns:

| Column name | Description |
| ----------- | ----------- |
| ID | The ID provided in the view. This column is used to join the results back to the original data.<br>The data type will be the data type of the ID column in the view. |
| LATLONG | A geometry column used to store the latitude and longitude. This column is included to make it easy to use with a geo map in SAP Analytics Cloud.<br>The data type is ST_GEOMETRY and is populated with ST_POINT. |
| LATITUDE | The latitude. This column is included as a convenience to understand the results.<br>The data type is double. |
| LONGITUDE | The longitude. This column is included as a convenience to understand the results.<br>The data type is double. |
| GEO_ASMT_LEVEL | The level of assignment of the geo-coordinates. This can be used to filter the results to only include those with sufficient accuracy. The possible values can be found at https://help.sap.com/docs/data-quality-services/data-quality-services/geo-location-coordinates.<br>The data type is nvarchar(4). |
 
If a row does not assign to a geo-coordinate, the row will be added to the output table with the appropriate ID value and all remaining columns set to NULL.
 
## Requirements

A Datasphere tenant is required. While the script could be modified to work with any HANA database instance, the script assumes certain Datasphere naming conventions.

A subscription to Data Quality Management microservices is required to generate the geo-coordinates. To try the service for free, please see https://community.sap.com/t5/technology-blogs-by-sap/getting-started-with-sap-data-quality-management-microservices-for-location/ba-p/13527838.

A Python runtime is required to run the script.

The sample script uses the hdbcli library to access Datasphere. Use the following command to install the library…

>pip install hdbcli

Please see https://pypi.org/project/hdbcli/ for more information.

The requests library is used to make calls to Data Quality Management microservices. Use the following command to install the library...

>pip install requests

The script expects two configuration files in the folder from which the script is being run.

| File name | Description |
| --------- | ----------- |
| db-user.json | Contains the database user credentials used to connect to the Datasphere instance. A template for this file is included with the sample. |
| service-key.json | Contains the service key JSON from the service instance used to access Data Quality Management microservices. An empty file with this name is included in the sample. |

>**Note:** The script requires Datasphere database user and BTP service key credentials to be stored in the db-user.json and service-key.json files respectively. These files should be marked with the appropriate permissions to protect their contents.

**Architecture**

![Alt text](resources/dqmm-dsp-python.png?raw=true "Architecture")

<br>

## Configuration

<br>

### Create a Datasphere database user

A Datasphere database user needs to be created within the space containing the data to be enriched. Go to Datasphere Space Management, create a database user, and enable **<em>Read Access</em>** and **<em>Write Access</em>** so that the data to be enriched can be read and the results can be written into the database user’s schema.

![Alt text](resources/dqmm-dsp-python-sample-db-user.png?raw=true "Database User")

For more information, please see https://help.sap.com/docs/SAP_DATASPHERE/be5967d099974c69b77f4549425ca4c0/798e3fd6707940c3bd2219b2d1ebaac2.html.

<br>

### Update db-user.json with the database user credentials

The sample provides a db-user.json file with a JSON structure that needs to be populated with the database user information.

    {
        "hostName": "",
        "port": "443",
        "schema": "",
        "password": ""
    }
 
Open the Database User Details for the database user, and copy teh values for Host Name, Port, Open SQL Schema, and Password into the db-user.json file.

<br>

### Create a service key for your Data Quality Management microservices service instance

A service key is used to expose the credentials needed to send requests to the service.

This sample script works with service keys created for OAuth authentication which is the default for service keys associated with Data Quality Management microservices.

For more information, please see https://help.sap.com/docs/data-quality-services/data-quality-services/enabling-dqm-microservices-687506470c6f4becbd64334d1965b476.

<br>

### Update service-key.json with the service key JSON

The sample provides an empty file named service-key.json. The service key JSON needs to be copied into this file.

The service key can be viewed in the BTP cockpit. When viewing the service key, the JSON can be copied to the clipboard. Paste the JSON into the service-key.json file.

Alternatively, you can export the service key JSON into a file, rename it to service-key.json, and then copy it into the folder from which you are running the Python script.

<br>

## Process Data

Perform the following steps to process your data.

An example of this process can be found at [dsp](dsp).


### Create a view in your space to project the data to service-related input fields

The view accomplishes two things. The first is to make the data accessible outside of the space. When creating a view, enable **<em>Expose for Consumption</em>** so that the view can be accessed using the database user.

The second is to map column names to service-related input field names. The allowable input field names can be found at https://help.sap.com/docs/data-quality-services/data-quality-services/input-fields.

In addition to the columns required by the service, an additional column named **<em>ID</em>** needs to be included in the view. This column is used to join the output back to the original input.

![Alt text](resources/dqmm-dsp-python-sample-view.png?raw=true "View")

The view can also be used to filter record so that only records meeting the specified criteria are processed. For example, only records from a specific country or region.

The script assumes that the view is created in the space associated with the database user. The name of the database user has the following format:

&nbsp;&nbsp;&nbsp;&nbsp;**<em>space-name</em>**#**<em>database-user-name-suffix</em>**

The script will access the view in the **<em>space-name</em>** schema.

When creating the view, note the technical name of the view since that is the name that will need to be provided to the script.

<br>

### Run the script

The script is run using the Python runtime. The script accepts one argument which is the name of the view to be processed.

The script can be run using the following command…

&nbsp;&nbsp;&nbsp;&nbsp;python3 dqmm-dsp.py **<em>technical-view-name</em>**

where **<em>technical-view-name</em>** is the technical name of the view to be processed.

The script reads records from the view in groups of 100. Every 100 records a message is displayed.

The script creates a table in the database user schema whose name is the same as the technical name of the view with “_GEO” appended to it. The format of the result table is:

| Column name | Description |
| ----------- | ----------- |
| ID | The ID provided in the view. This column is used to join the results back to the original data.<br>The data type will be the data type of the ID column in the view. |
| LATLONG | A geometry column used to store the latitude and longitude. This column is included to make it easy to use with a geo map in SAP Analytics Cloud.<br>The data type is ST_GEOMETRY and is populated with ST_POINT. |
| LATITUDE | The latitude. This column is included as a convenience to understand the results.<br>The data type is double. |
| LONGITUDE | The longitude. This column is included as a convenience to understand the results.<br>The data type is double. |
| GEO_ASMT_LEVEL | The level of assignment of the geo-coordinates. This can be used to filter the results to only include those with sufficient accuracy. The possible values can be found at https://help.sap.com/docs/data-quality-services/data-quality-services/geo-location-coordinates.<br>The data type is nvarchar(4). |

The results of the processing are inserted into this table.

<br>

### Join the results to the original data

Once the processing is complete, the original data can be joined to the results.

The table created within the database user's schema is not immediately consumable within Datasphere. The table needs to be imported and deployed to be used within a view. Also, to join it with the original data, an association needs to be created between it and the original data.

***Import and deploy the table***

- Navigate to **Data Builder**.
- Click **New Graphical View**.
- Click on **Sources** and expand the database user used to enrich the data.
- Drag the result table onto the canvas.
- A pop-up will be displayed. Click **Import and Deploy**.

***Create an association to the original data***

- Click on **Repository Explorer**. A pop-up will be displayed stating that there are unsaved changes. Click **Discard**.
- Enter in the name of the output table (name of the view with **_GEO** appended) and click the search icon.
- Click on the table name in the results.
- Click on the **Associations** tab.
- Click the **Create Association** icon (plus sign) and select **Association**.
- Click on the row (not the name) of the original table in the **Select Association Target** screen.
- Click **Select**.
- In the **Mappings** section, drag the **ID** column from the result table to the column of the original object used to provide the ID value.
- Click the Save icon and select **Save**.

***Join the result table to the original data***

- Navigate to **Data Builder**.
- Click **New Graphical View**.
- Click on **Repository**.
- From the **Repository** list, drag the output table onto the canvas.
- Click the **Join Suggestion** icon in the pop-up menu associated with the result table on the canvas, and select the original object.
- Name the view appropriately.
- Click the Save icon and then the Deploy icon.
	
<br>

## How to obtain support

This project is provided "as-is" with no expectation for major changes or support.

For additional support, [ask a question](https://answers.sap.com/questions/ask.html) in SAP Community. 

## Contributing

This project is provided "as-is" and does not support community contributions.

## Code of Conduct

Members, contributors, and leaders pledge to make participation in our community a harassment-free experience. By participating in this project, you agree to always abide by its [Code of Conduct](https://github.com/SAP/.github/blob/main/CODE_OF_CONDUCT.md).

## Licensing

Copyright (c) 2024 SAP SE or an SAP affiliate company and dqmm-dsp-python-sample contributors. Please see our [LICENSE](/LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available via the REUSE tool (link to https://api.reuse.software/info/github.com/SAP/dqmm-dsp-python-sample).

