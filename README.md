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
* Download the SamplePostmanRequests.zip file above.
* Extract the four sample .json files to your file system.

Import Collections
------------------
1. Launch the Postman app.
2. Click the Import button in the upper left.



3. Click Choose Files.

![sample2](/images/sample2.jpg)

* Browse for the four .json files that were downloaded and extracted in the previous step, and click Open.
    * samplesAddressCleanse.postman_collection.json
    * samplesAdminTasks.postman_collection.json
    * samplesEnvironment.postman_environment.json
    * samplesReverseGeo.postman_collection.json
    * Result: Three collections are added – samplesAddressCleanse, samplesAdminTasks, and samplesReverseGeo. 
    Click the collection name to expand it. The samplesAddressCleanse has multiple folders, therefore click a folder name to expand it. 
    Click one of the sample names.

![sample3](/images/sample3.jpg)

An environment is also added in the top right corner. In the dropdown of the environment combo box, samplesEnvironment is now included.

![sample4](/images/sample4.jpg)

Insert Values for Variables
---------------------------
The samples come with three variables, and you will have to substitute two of them to send requests:
* One variable is the applicationURL that is in the post request URL for each sample.
* The other two variables, oauthAccessToken and base64Credentials, are in the header section for each sample. You only need to substitute a value for one of these, depending on whether you are using OAuth or Basic authentication with our service.
```
NOTE: Basic Auth is only available on SAP Cloud Platform Trial Edition
```

![sample5](/images/sample5.jpg)

Complete the following steps to substitute values for variables.

1. Expand the environment combo box in the upper right and select Manage Environments.

![sample6](/images/sample6.jpg)

* Click samplesEnvironment.

![sample7](/images/sample7.jpg)

* Enter the application URL for your SAP Cloud Platform account. You find this URL for our service for your SAP Cloud Platform account by:
   *  Pre-requisite: You have already enabled our service (Data Quality Microservices) in the SAP Cloud Platform Services Cockpit.
   *  Select "Subscriptions" in the left hand menu in the SAP Cloud Platform Cockpit.
   *  Select the "dqmmicro" Application link under the "Subscribed Java Applications" section of the page. 
   *  You will find the application URL for your account on this page.  Copy and past that into this variable. 
* Enter the OAuth Access Token into the variable "oauthAccessToken" (by default all examples are setup to use OAuth in the headers)

Requesting an OAuth Token
--------------------------------------
* In the samplesAdminTasks collection, the “Request oAuth token” request has two special variables that you must substitute values from your account. One is in the URL, and the other is the value for the Authorization header.

![oauth1](/images/oauth1.jpg)

* Follow these steps to obtain the value for the {ReplaceWithOAuthTokenEndpoint} and {ReplaceWithBasicAuthToken} variables.
   1. Log into the SAP Cloud Platform cockpit and select the appropriate account.
   2. In the Navigation, navigate to Security > OAuth.
   3. Copy the URL for Token Endpoint, and use this as the value for the {ReplaceWithOAuthTokenEndpoint} variable.

    ![oauth2](/images/oauth2.jpg)

   4. Open the Clients tab and click Register New Client.
   5. Fill out the name field and select the dqmmicro app from the Subscription dropdown.
   6. Select Client Credentials for the Authorization Grant type, and provide a Secret password.
   7. Adjust the token lifetime if desired.
     * NOTE: requesting refresh tokens is not covered in this guide.
   8. Save the Client and copy the Client ID for use in Postman.
     * Note: You may change the ID to something else. For instance, the name you selected in step 5. 
   9. Expand the samplesAdminTasks collection and select the “Request oAuth token” sample.

    ![oauth3](/images/oauth3.jpg)

   * In the Authorization tab, select “Basic Auth” in the Type combo box, add the Client ID to the username field and the Secret you chose above to the password field.
   * Click the Update Request button.

    ![oauth4](/images/oauth4.jpg)

   * Result: Go the Headers tab, and you will see the value for the Authorization variable was automatically completed with “Basic” followed by a token.
   * After replacing both variables with values from your account, you may send the “Request oAuth token” request.

   *  NOTE:  More details on obtaining an OAuth token can be found here:  https://help.sap.com/viewer/d95546360fea44988eb614718ff7e959/Cloud/en-US/f891afcaae9b40d3aa23d7be8ae08371.html

Obtaining a Basic Authentication Variable Value (If you want to use Basic Authentication instead of OAuth)
--------------------------------------
```
NOTE: Basic Auth is only available on SAP Cloud Platform Trial Edition. 
      Skip to the next section if you are using OAuth.
```

NOTE:  The SAP Cloud Platform, and thus our service, by default uses the SAP ID Service as it's identity provider. For basic authentication with our service you would use your:
   *  Customer/Partner:  S-user or P-user ID and password.   If you don't have one or don't know, you can create an account here: http://scn.sap.com/welcome -> click on the “Join Us” link
   *  SAP Employee:  user your internal network ID (E.g. I or D number and password)

NOTE: Basic Authentication requires that a base-64 encoded string, based on your username and password, are supplied in the header.  So to keep things relatively simple the instructions here tell you how to use Postman to generate the base-64 encoded variable value you'll use in your variable. 

* Expand one of the collections and select any of the samples. (Do not click Save while in the sample. You are here to obtain a token only.)

![sample9](/images/sample9.jpg)

* In the Authorization section, select Basic Auth in the Type combo box.

![sample10](/images/sample10.jpg)

* Enter your SAP ID Service username and password (remember your S/P-user or SAP I/D number), and click Update Request.

![sample11](/images/sample11.jpg)

* Go to the Headers section, copy the value from the first Authorization variable, without the word “Basic”. This is the value to insert as the value for the base64Credentials variable.

![sample12](/images/sample12.jpg)

Update your environment variables
---------------------------------

* When you have finished entering the application URL and the variable value, click Update.

![sample8](/images/sample8.jpg)

After completing this step, the Manage Environments window will look like the following, but with values issued for your account.
If you are using OAuth authentication, it looks like this:

![sample13](/images/sample13.jpg)

If you are using Basic authentication, it looks like this:

![sample14](/images/sample14.jpg)

Send Sample Requests
--------------------

* In the environment combo box, select samplesEnvironment.

![sample15](/images/sample15.jpg)

* Click one of the collections to expand it. If you select the samplesAddressCleanse collection, then click one of the folders to expand it. Select one of the POST requests in the list.

![sample16](/images/sample16.jpg)

* If you are using OAuth authentication, skip this step. If you are using Basic authentication, go to the Headers section, comment out the OAuth authentication and uncomment the Basic authentication by clicking the check to the left of the first Authorization to uncheck it and click the circle to the left of the second Authorization to check it.

![sample17](/images/sample17.jpg)

* Go to the Body section to see the request payload. Click Send.

![sample18](/images/sample18.jpg)

* You may make changes to the payload and send requests to test the service.
