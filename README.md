# cloud-dqm-sample-payloads
Sample JSON payloads for Data Quality Management, microservices for location data

Quick start
-----------

By using sample files with Google Chrome's Postman app, you can quickly get started testing Data Quality Management microservices.
Download Postman App
--------------------

Download the Postman app for Chrome at https://www.getpostman.com

Download the Samples
--------------------
* Download the SamplePostmanRequests.zip file above.
* Extract the three sample .json files to your file system.

Import Collections
------------------
* Launch the Postman app from Chrome.
* Click the Import button in the upper left.

![sample1](/images/sample1.jpg)

* With Import File active, click Choose Files.

![sample2](/images/sample2.jpg)

* Browse for the three .json files that were downloaded and extracted in the previous step, and click Open.
    * samplesAddressCleanse.postman_collection.json
    * samplesEnvironment.postman_environment.json
    * samplesReverseGeo.postman_collection.json
Result: Two collections are added – samplesAddressCleanse and samplesReverseGeo. Click the collection name to expand it. The samplesAddressCleanse has multiple folders, therefore click a folder name to expand it. Click one of the sample names.

![sample3](/images/sample3.jpg)

An environment is also added. The environment combo box includes samplesEnvironment.

![sample4](/images/sample4.jpg)

Insert Values for Variables
---------------------------
The samples come with three variables, and you will have to substitute two of them to send requests:
* One variable applicationURL is in the post request URL for each sample.
* Two variables, oauthAccessToken and base64Credentials, are in the header section for each sample. You only need to substitute a value for one of these, depending on whether you are using OAuth or Basic authentication.

![sample5](/images/sample5.jpg)

Complete the following steps to substitute values for variables.
* Expand the environment combo box in the upper right and select Manage Environments.

![sample6](/images/sample6.jpg)

* Click samplesEnvironment.

![sample7](/images/sample7.jpg)

* Enter the application URL from your welcome email for the applicationURL variable.
* Enter the OAuth Access Token from your welcome email for the oauthAccessToken variable, if applicable.

Obtaining a Basic Authentication token
--------------------------------------
NOTE: Skip to the next section if you are using oAuth.

* Close the Manage Environments window. When you have the token, go back to the Manage Environments window and proceed with entering values for the variables.

* Expand one of the collections and select any of the samples. (Do not click Save while in the sample. You are here to obtain a token only.)

![sample9](/images/sample9.jpg)

* In the Authorization section, select Basic Auth in the Type combo box.

![sample10](/images/sample10.jpg)

* Enter your SAP username and password, and click Update Request.

![sample11](/images/sample11.jpg)

* Go to the Headers section, copy the token from the first Authorization variable, without the word “Basic”. This is the value to insert as the value for the base64Credentials variable.

![sample12](/images/sample12.jpg)

Update your environment variables
---------------------------------

* When you have finished entering the application URL and the token, click Update.

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

* Expand one of the collections and select any of the samples.

![sample16](/images/sample16.jpg)

* If you are using OAuth authentication, skip this step. If you are using Basic authentication, go to the Headers section, comment out the OAuth authentication and uncomment the Basic authentication by clicking the check to the left of the first Authorization to uncheck it and click the circle to the left of the second Authorization to check it.

![sample17](/images/sample17.jpg)

* Go to the Body section to see the request payload. Click Send.

![sample18](/images/sample18.jpg)

* You may make changes to the payload and send requests to test the service.