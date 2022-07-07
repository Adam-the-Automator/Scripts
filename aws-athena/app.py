import boto3
import pandas as pd
import io
import re
import time

# region - The region where you created your database.
# database - The name of the database.
# bucket - Your bucket name.
# path - The location where the results of the queries will be stored.
# query - store data in the exact location as the CSV file.  

params = {
    'region': 'us-east-2',
    'database': 'default',
    'bucket': 'athena-112',
    'path': 'temp/athena/results',
    'query': 'SELECT * FROM "default"."athena-112" limit 10;'
}

session = boto3.Session()

def athena_query(client, params):
 
# start_query_execution method - runs the SQL query statements. 
# QueryString - has SQL query statements to be executed.
# QueryExecutionContext - has the database within which the query executes.   
# ResultConfiguration - specifies information about where and 
	# how to save the results of the query execution.
# All the information is dispatched to an executable object response
   
        response = client.start_query_execution(
        QueryString=params["query"],
        QueryExecutionContext={
            'Database': params['database']
        },
        ResultConfiguration={
            'OutputLocation': 's3://' + params['bucket'] + '/' + params['path']
        }
    )
    print(response)
    return response
	

# Information about the query execution is saved with a unique ID.

def athena_to_s3(session, params, max_execution = 5):
    client = session.client('athena', region_name=params["region"])
    execution = athena_query(client, params)
    execution_id = execution['QueryExecutionId']
    state = 'RUNNING'

    # Validates and stores information about the successful execution of a query
    # and store the information to the specified path in an S3 bucket

    while (max_execution > 0 and state in ['RUNNING', 'QUEUED']):
        max_execution = max_execution - 1
        response = client.get_query_execution(QueryExecutionId = execution_id)

        if 'QueryExecution' in response and \
                'Status' in response['QueryExecution'] and \
                'State' in response['QueryExecution']['Status']:
            state = response['QueryExecution']['Status']['State']
            if state == 'FAILED':
                return False
            elif state == 'SUCCEEDED':
                s3_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                filename = re.findall('.*\/(.*)', s3_path)[0]
                return filename
        time.sleep(1)
    
    return False

# Calling above function  
s3_filename = athena_to_s3(session, params)	


# Cleanup method will delete the results of queries from the specified path 

def cleanup(session, params):
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(params['bucket'])
    for item in my_bucket.objects.filter(Prefix=params['path']):
        item.delete()

# Calls the cleanup function to remove all files from the specified S3 folder
cleanup(session, params)