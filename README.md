# Snowflake Data Test - Starter Project(Solution By Ayan Chakraborty)

## Primary Diagonostic of the solution file provided and setup

### Local environment setup

The environment was set up as per the guidence provided at the primay solutioon file. There was an error with BWS category which was fixed and for the primary data test the file was changed to 1 months of data instead of multiple months.

### Setup AWS and S3

1. AWS account has been created by using personal email. Details of the account can be provided on request as it is a brand new account and has no data/ setup except Convex Insurance.
2. We have set up S3 bucket in ***APAC Singapore region. This is important as our Snowflake account is in the same region.*** This is not true that Snowflake will not be able to read data from another region but that need a bit more complex setup in the AWS security end. To make the project simple and straight forward we have setup both(Snowflake and S3) on the same region
3. Inside S3 we have created 3 different folder for three different types of data :
- convex-customers - Contains Customer data (File tipe: .csv)
- convex-products - Contains Product data (File Type: .csv)
- convex-transactions - Contains Transactional data (File Type: Json)

## Load data into S3 

####Automation - 1 
The script main_data_generator.py has been updated with a function to upload the data automatically from generated folder to respective S3 buckets. To do this the code need to have the credentials to authenticate the folder. For that, another file is created as per the standard called - config.ini which stores the credential data. This is a good practice but not the ideal or best solution. best case will be to work with environment variables to pass thise parameters to the code.
This is again mentioned in the future betterment scope section.

## Design and setup the Snoflake schema structure (Data Modelling)

First of all an external stage area has been created for different file types.(Example : Json, .CSV). Once this is done the authentication has been made as snowflake can read the data from S3 bucket. <br />
The Snowflake database has been designed to have four schemas for four different purposes :
1. Convex_Stage : Staging area and flattern the JSON files
2. Convex_vault : To design the data vault 2.0 to accept any future changes in the data model in an agile way
3. Convex_warehouse : To design the facts and dimensions(Can be called as information vault as well) 
4. Convex_datamart : to have the aggregated output to be consumed by data science team.

Below is the architechture of the whole snoflake schema :

### DATA VAULT 2.0

![convex_insurance (1)](https://user-images.githubusercontent.com/38339739/186567262-fe34f8b8-cc1d-4b84-acea-cf293bc82404.png)

### INFORMATION VAULT (DIMENSIONAL MODELLING)

![Copy of convex_insurance (1)](https://user-images.githubusercontent.com/38339739/186568500-38b41257-53d2-4777-b8a5-31ee85c3fc29.png)

## DATA LOAD AUTOMATION AND ARCHITECHTURE

####Automation - 2
The data has been loaded using stream and task as a batch processing. ***The automation have been done by scheduling the stream jobs with tasks.*** <br />

####Automation - 3

Tasks are designed in a way that, one task is depend on another. So sucess on one task will automatically trigger another task. So, there is no manual intervension between the tasks. 

There is another option to create automate load in Snoflake Using Snowpipe. But, this option should be choose only when we have stream data(effectively for a microservice based architecgture.) <br />

We are using **Multi Table Insert(MTI)** to load the data in parallel from a stream to the respective destination tables. <br />
***Below is the implementation diagram which shows the whole process in short***
<img width="832" alt="convex_data_landscape" src="https://user-images.githubusercontent.com/38339739/186574745-0444245f-450e-4e49-bb52-7c33b2bad0d6.png">


***Also Different role and credentials have been created for Data science user to have only access to data mart layer***

## Future betterment scope
1. The code should read the keys from environment. This can be done in multiple ways. For example: AWS Key Gen, Environment Variables, kubernetes, Terraform(*Infra as code*). But, I would require devops support for that. 
2. Automation and auto deduplication of data can be done using Snowpipe.
3. Use of DBT can bring a huge change in the final data modelling structure which is in below for proposed modelling structure
4. A proper control schema should be designed to track the status all the jobs, faliure and debugging instead fire each time query to Snowflake schema
5. Alerting system should be in place(Slack alert/ any other alerting chanel used by the company)
6. Depends on data volume Spark(pyspark) can be used for in-memory data processing and faster data loading.
