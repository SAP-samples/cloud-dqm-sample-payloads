# cloud-dqm-sample-payloads
This repository contains sample Postman (www.getpostman.com) Collections as examples for testing the Data Quality Management, microservices for location data service on SAP Cloud Platform. 

You can find more information about how to get a free trial account here:
https://blogs.sap.com/2017/03/19/sap-data-quality-management-microservices-generally-available-to-customers/

Formal documenation for the serivce can be found here: https://help.sap.com/viewer/d95546360fea44988eb614718ff7e959/Cloud/en-US


Quick start
-----------

By using these sample collections for the Postman app, you can quickly get started testing Data Quality Management, microservices.

Download Postman App
--------------------

Download the Postman app for Chrome at https://www.getpostman.com

Download the Samples
--------------------
* Download the SamplePostmanRequests.zip file 

![sample1](/images/postman.jpg)

![sample1](/images/postmanTwo.jpg)

* Extract the four sample .json files to your file system.

Import Collections
------------------
1. Launch the Postman app.
2. Click the Import button in the upper left.

![sample1](/images/postman1.jpg)

3. Click Choose Files.

* Browse for the four .json files that were downloaded and extracted in the previous step, and click Open.
    * samplesAddressCleanse.postman_collection.json
    * samplesAdminTasks.postman_collection.json
    * samplesEnvironment.postman_environment.json
    * samplesReverseGeo.postman_collection.json
   Result: Three collections are added – samplesAddressCleanse, samplesAdminTasks, and samplesReverseGeo. 
    Click the collection name to expand it. The samplesAddressCleanse has multiple folders, therefore click a folder name to expand it. 
    Click one of the sample names.

![sample3](/images/postman3.jpg)

* Result: In the environment box in the upper right corner, samplesEnvironment is now included.

![sample4](/images/postman4.jpg)


Requesting an OAuth Token
--------------------------------------
In the samplesAdminTasks collection, the “Request oAuth token” request has two special variables that you must substitute with values from your account. One is in the URL, and the other is the value for the Authorization header.

![oauth1](/images/postman6.jpg)

 Follow these steps to obtain the value for the {ReplaceWithOAuthTokenEndpoint} and {ReplaceWithBasicAuthToken} variables.
   1. Log into the SAP Cloud Platform cockpit and select the appropriate account.
   2. In the Navigation, navigate to Security > OAuth.
   3. Copy the URL for Token Endpoint, and use this as the value for the {ReplaceWithOAuthTokenEndpoint} variable.
   4. On the OAuth page in the cockpit, open the Clients tab and click Register New Client.
   5. Fill out the name field and select the dqmmicro app from the Subscription dropdown.
   6. Select Client Credentials for the Authorization Grant type, and provide a Secret password.
   7. Adjust the token lifetime if desired.
     * NOTE: requesting refresh tokens is not covered in this guide.
   8. Save the Client and copy the Client ID for use in Postman.
     * Note: You may change the ID to something else. For instance, the name you selected in step 5. 
   9. Expand the samplesAdminTasks collection and select the “Request oAuth token” sample.

    ![sample8](/images/postman8.jpg)

   10. In the Authorization tab, select “Basic Auth” in the Type combo box, add the Client ID to the username field and the Secret you chose above to the password field.
   * Click the Preview Request button.

    ![sample9](/images/postman9.jpg)

   * Result: Go to the Headers tab, and you will see an expandable Temporary Headers section. Copy the variable from the Temporary Headers Authorization Value (excluding the word "Basic") and paste it into the "{ReplaceWithBasicAuthToken}" value above. 
   
    ![sample12](/images/postman12.jpg)
   
   11. After replacing both variables with values from your account, you may send the “Request oAuth token” request.
   
   * Result: The request will return with your access token. 
   
   
   *  NOTE:  More details on obtaining an OAuth token can be found here:  https://help.sap.com/viewer/d95546360fea44988eb614718ff7e959/Cloud/en-US/f891afcaae9b40d3aa23d7be8ae08371.html



Update your Environment Variables
---------------------------
The samples come with two variables that you will need to substitute in order to send requests:
* One variable is the applicationURL that is in the post request URL for each sample.
* The other variable, oauthAccessToken, is in the header section for each sample. 
```
NOTE: Basic Auth is only available on SAP Cloud Platform Trial Edition
```

Complete the following steps to substitute values for these variables.

1. In the upper right corner, select the gear icon to Manage Environments.

![sample6](/images/postman10.jpg)

2. Click samplesEnvironment.

![sample7](/images/postman11.jpg)

3. To obtain the application URL, navigate to Applications > Subscriptions in the left-hand menu in the SAP Cloud Platform Cockpit and click the "dqmmicro" Application link under the "Subscribed Java Applications" section of the page. Copy and paste the application URL into the "applicationURL" variable. 

Note: You will need to have enabled our service, Data Quality Management in the SAP Cloud Platform Services Cockpit.
     
4. Enter the OAuth Access Token that you recieved from step 11 into the variable "oauthAccessToken" (by default all examples are setup to use OAuth in the headers)

5. Click Update and close the Manage Environments window.

6. In the environment combo box, select samplesEnvironment.

![sample15](/images/postman4.jpg)

Send Sample Requests
--------------------

1. Click one of the collections to expand it. If you select the samplesAddressCleanse collection, then click one of the folders to expand it. Select one of the POST requests in the list.

2. Go to the Body section to see the request payload. Click Send.

![sample18](/images/sample18.jpg)

 You may make changes to the payload and send requests to test the service.
