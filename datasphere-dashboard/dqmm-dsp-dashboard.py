
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from hdbcli import dbapi

# get the view exposing the data to be enriched with geo-coordinates
viewName = sys.argv[1];

# the associated geo-coordinates will be written to a table
# with the same name as the view with "_GEO" appended
outputTable = viewName + "_GEO";

# read the database user configuration
f  = open('db-user.json')
dbUser = json.load(f)
f.close();
space = dbUser["schema"].split("#")[0];

# read the service key for Data Quality Management microservices
f  = open('service-key.json')
serviceKey = json.load(f)
f.close();
uaa = serviceKey['uaa'];
uri = serviceKey['uri'];

# connect to the database
db = dbapi.connect(
    address=dbUser["hostName"],
    port=dbUser["port"],
    user=dbUser["schema"],
    password=dbUser["password"],
    schema=dbUser["schema"],
    encrypt='true',
    sslValidateCertificate='false',
    disableCloudRedirect='true',
    communicationTimeout='0',
    autocommit='true',
    sslUseDefaultTrustStore='true'
);
print("Connected to Datasphere at {} as {}".format(dbUser["hostName"], dbUser["schema"]));

# get the data type for the ID column of the view
query = "select concat(data_type_name, case when LOCATE('VARCHAR,NVARCHAR,ALPHANUM,SHORTTEXT,VARBINARY,', data_type_name||',') > 0 then '('||LENGTH||')' else '' end) FROM VIEW_COLUMNS WHERE SCHEMA_NAME='{}' and VIEW_NAME = '{}' and upper(COLUMN_NAME) = 'ID'".format(space, viewName)
selectCursor = db.cursor();
selectCursor.execute(query);
res = selectCursor.fetchone();
idType = res[0];
selectCursor.close();

# generate a token for accessing Data Quality Management microservices
response = requests.get(uaa['url'] + "/oauth/token?grant_type=client_credentials", auth=HTTPBasicAuth(uaa['clientid'], uaa['clientsecret']));
token = response.json()['access_token'];
print("Generated token for Data Quality Management microservices");

# query the view for records to be enriched
query="SELECT * FROM \"{}\".\"{}\"".format(space, viewName);
selectCursor = db.cursor();
selectCursor.execute(query);
print("Queried view {} for records to be enriched".format(viewName));

# create the table to hold the geo-coordinates
createTable = "CREATE COLUMN TABLE \"{}\" (id {}, latlong ST_GEOMETRY(3857), latitude DOUBLE, longitude DOUBLE, addr_asmt_info NVARCHAR(1), addr_asmt_level NVARCHAR(2), addr_info_code NVARCHAR(4), addr_info_code_msg NVARCHAR(1024), std_addr_country_3char NVARCHAR(3), std_addr_country_name NVARCHAR(100), geo_asmt_level NVARCHAR(4))".format(outputTable, idType);
cursor = db.cursor();
cursor.execute(createTable);
cursor.close();
db.commit();
print("Created table {} to hold geo-coordinates".format(outputTable));

# prepare to insert the geo-coordinates into the output table
insertCursor = db.cursor();

# prepare for calls to Data Quality Management microservices
url = "https://" + uri + "/dq/addressCleanse/batch";
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Accept": "application/json"
};
request = {
    "addressInput": [{}],
    "outputFields": [ "addr_asmt_info",
                      "addr_asmt_level",
                      "addr_info_code",
                      "addr_info_code_msg",
                      "std_addr_country_3char",
                      "std_addr_country_name",
                      "geo_asmt_level",
                      "addr_latitude",
                      "addr_longitude"
                    ],
    "addressSettings": {
        "processingMode": "both"
    }
};


# process the records in batches of 100
res = selectCursor.fetchmany(100);
columnHeaders = [i[0] for i in selectCursor.description]

while res:
    for row in res:

        # construct the input address
        # save the ID value to include in the output table
        address = {};
        for i in range(len(columnHeaders)):
            if columnHeaders[i].upper() == 'ID':
                idVal = row[i];
            else:
                address[columnHeaders[i].lower()] = row[i];

        # create the payload for the request to Data Quality Management microservices
        request["addressInput"][0] = address;

        # call Data Quality Management microservices
        response = requests.post(url=url, headers=headers, data=json.dumps(request));

        # if there was an error then just stop processing
        if response.status_code != 200:
            print("Error calling Data Quality Management microservices");
            print(response.content.decode('utf-8'));
            break;

        # retrieve the geo-coordinates from the result
        result = response.json()['addressOutput'][0];

        # insert the results into the output table
        insert = "INSERT INTO \"{}\" VALUES ('{}', ST_GeomFromText('POINT({} {})', 4326).ST_TRANSFORM(3857), {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(outputTable, idVal,
                    result['addr_longitude'],
                    result['addr_latitude'],
                    result['addr_latitude'],
                    result['addr_longitude'],
                    result['addr_asmt_info'],
                    result['addr_asmt_level'],
                    result['addr_info_code'],
                    result['addr_info_code_msg'],
                    result['std_addr_country_3char'],
                    result['std_addr_country_name'],
                    result['geo_asmt_level']);
        if result['addr_latitude'] == None:
            insert = "INSERT INTO \"{}\" VALUES ('{}', null, null, null, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(outputTable, idVal,
                    result['addr_asmt_info'],
                    result['addr_asmt_level'],
                    result['addr_info_code'],
                    result['addr_info_code_msg'],
                    result['std_addr_country_3char'],
                    result['std_addr_country_name'],
                    result['geo_asmt_level']);
        else:
            insert = "INSERT INTO \"{}\" VALUES ('{}', ST_GeomFromText('POINT({} {})', 4326).ST_TRANSFORM(3857), {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(outputTable, idVal,
                    result['addr_longitude'],
                    result['addr_latitude'],
                    result['addr_latitude'],
                    result['addr_longitude'],
                    result['addr_asmt_info'],
                    result['addr_asmt_level'],
                    result['addr_info_code'],
                    result['addr_info_code_msg'],
                    result['std_addr_country_3char'],
                    result['std_addr_country_name'],
                    result['geo_asmt_level']);
        insertCursor.execute(insert);

    # get the next set of records
    print("Processed {} records".format(len(res)));
    db.commit();
    res = selectCursor.fetchmany(100);

insertCursor.close();
selectCursor.close();

